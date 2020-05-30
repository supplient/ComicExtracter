import subprocess

def extract(path, dest_dir, pwd):
    args = ["7z.exe", "x", path, "-p"+pwd, "-o"+dest_dir]
    p = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    stdout, stderr = p.communicate("S".encode("utf8"))
    stdout = stdout.decode("gbk")
    stderr = stderr.decode("gbk")

    if "ERROR" in stderr:
        return False
    return True


if __name__ == "__main__":
    p = subprocess.Popen(
            ["7z.exe", "x", "test/c.7z", "-pgmgard.com", "-otest/oo"],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    stdout, stderr = p.communicate("S".encode("utf8"))
    stdout = stdout.decode("gbk")
    stderr = stderr.decode("gbk")

    print(stdout)
    print(stderr)

    if "ERRORS" in stderr:
        print("Failed")
    elif "Ok" in stdout:
        print("Succeed")