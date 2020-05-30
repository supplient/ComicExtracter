import zipfile, rarfile, lib7z
import os
import tqdm
from exceptions import BadPasswordError, NotSupportError

def getExtractPath(path, dest_dir):
    basename = os.path.basename(path)
    purename, ext = os.path.splitext(basename)
    extract_path = os.path.join(dest_dir, purename)
    return extract_path

def zip_extract(path, dest_dir, pwd):
    with zipfile.ZipFile(path) as fd:
        try:
            fd.extractall(path=dest_dir, pwd=bytes(pwd, "utf8"))
        except RuntimeError:
            raise BadPasswordError()

def rar_extract(path, dest_dir, pwd):
    with rarfile.RarFile(path) as fd:
        try:
            fd.extractall(path=dest_dir, pwd=pwd)
        except rarfile.RarWrongPassword:
            raise BadPasswordError()
        except rarfile.RarCRCError:
            raise BadPasswordError()

def sevenz_extract(path, dest_dir, pwd):
    if not lib7z.extract(path, dest_dir, pwd):
        raise BadPasswordError

def extract(path, dest_dir, pwds):
    mth = None
    if(zipfile.is_zipfile(path)):
        mth = zip_extract
    elif(rarfile.is_rarfile(path)):
        mth = rar_extract
    else:
        mth = sevenz_extract

    extract_path = getExtractPath(path, dest_dir)
    succeed = False
    for pwd in pwds:
        try:
            mth(path, extract_path, pwd)
            succeed = True
            break
        except BadPasswordError:
            pass
    if not succeed:
        raise BadPasswordError

def extractFilesInFolder(folder_path, dest_dir_path, pwds):
    failed_list = []
    flist = os.listdir(folder_path)

    with tqdm.tqdm(flist, desc="Extract") as ftqdm:
        for f in ftqdm:
            filepath = os.path.join(folder_path, f)
            if os.path.isdir(filepath):
                continue

            ftqdm.set_postfix(extracting=f)
            try:
                extract(filepath, dest_dir_path, pwds)
            except BadPasswordError:
                failed_list.append([f, "Bad Password"])
            except NotSupportError:
                failed_list.append([f, "Not Support"])
            except Exception:
                failed_list.append([f, "Unknown"])
    return failed_list

def moveToFailedFolder(failed_list, folder_path, failed_path):
    with tqdm.tqdm(failed_list, desc="Moving failed") as ftqdm:
        for f in ftqdm:
            ftqdm.set_postfix(moving=f)
            src = os.path.join(folder_path, f[0])
            dst = os.path.join(failed_path, f[0])
            os.rename(src, dst)


if __name__ == "__main__":
    from load_password import getPasswords
    from config import src_folder, dst_folder, failed_folder

    failed_list = extractFilesInFolder(
        src_folder,
        dst_folder,
        getPasswords()
    )

    for filename, cause in failed_list:
        print("[Failed]" + filename + ": " + cause)

    print("Moving failed files to folder '" + failed_folder + "'")

    moveToFailedFolder(
        failed_list,
        src_folder,
        failed_folder
    )

    