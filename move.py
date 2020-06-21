import os

EMPTY = "=!=!=Empty=!=!="

def hasOnlyOneSubdir(path):
    flist = os.listdir(path)
    if len(flist) > 1:
        return False
    if len(flist) == 0:
        return EMPTY
    filepath = os.path.join(path, flist[0])
    return filepath

def isDirEmpty(path):
    flist = os.listdir(path)
    return len(flist) == 0

def moveToSepearteFolder(folder_path, tmp_folder_name="this_is_a_tmp_folder"):
    count = 0

    flist = os.listdir(folder_path)
    tmp_path = os.path.join(folder_path, tmp_folder_name)
    for f in flist:
        filepath = os.path.join(folder_path, f)
        if os.path.isfile(filepath):
            continue

        subfile = hasOnlyOneSubdir(filepath)
        if subfile == False:
            continue
        elif subfile == EMPTY:
            if isDirEmpty(filepath):
                os.rmdir(filepath)
            continue

        subbase = os.path.basename(subfile)
        subbase = subbase.strip()
        sub_newpath = os.path.join(folder_path, subbase).strip()

        try:
            os.rename(subfile, tmp_path)
        except FileExistsError:
            raise Exception("Please assign a tmp_folder_name which not exists.")
        if isDirEmpty(filepath):
            os.rmdir(filepath)
        else:
            raise Exception("Something error with " + filepath + ", which should be empty now.")
        try:
            os.rename(tmp_path, sub_newpath)
        except FileExistsError:
            raise Exception("Something wrong with " + subfile + ", which is now " + tmp_path)

        count += 1
    return count


if __name__ == "__main__":
    from config import dst_folder
    count = 1
    while count > 0:
        count = moveToSepearteFolder(dst_folder)
        print("Moved " + str(count))
    print("Finished.")