from config import password_filepath

def getPasswords():
    pws = ""
    with open(password_filepath, "r", encoding="utf8") as fd:
        pws = fd.readlines()
    pws = [pw.strip() for pw in pws]
    return pws

if __name__ == "__main__":
    print(getPasswords())