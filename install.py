import os 
import subprocess
import sys

def main():
    # only built for linux right now
    if sys.platform != 'linux':
        raise SystemError(
"tool is meant for linux-based systems, do not recommend install"
        )
    
    # start from root so all input paths are absolute
    print("Setting up mem tool . . .")
    os.chdir("/")
    while True:
        venv_loc = input(
"Please enter the path to a python venv with psutil installed:\t"
        )

        # check input path for validity and psutil
        if not os.path.isdir(venv_loc):
            print("invalid directory path, try again")
            continue 
        if "python" not in os.listdir(f"{venv_loc}/bin"):
            print(f"{venv_loc} not a valid python venv, try again")
            continue 
        pkg_path = f"{venv_loc}/lib/python{sys.version[:4]}/site-packages"
        try:
            if "psutil" not in os.listdir(pkg_path):
                print("psutil not installed at that venv, try again")
                continue
        except FileNotFoundError:
            print(
"that venv does not store packages under venv_path/lib/python*/site-packages, try again"
            ) 
            continue
        break

    # move back to tool path, replace shbang with new venv loc
    os.chdir(os.path.split(__file__)[0])
    with open("mem.py", "r") as file:
        mem_py = file.readlines()
    mem_py[0] = f"#!{venv_loc}/bin/python\n"
    with open("mem.py", "w") as file:
        file.writelines(mem_py)

    # turn local mem.py to mem tool on the system PATH
    chmod = subprocess.run(["chmod +x mem.py"], shell=True)
    sudo_cp = subprocess.run(["sudo cp mem.py /usr/local/bin/mem.py"], shell=True)
    mv_mem = subprocess.run(
        ["sudo mv /usr/local/bin/mem.py /usr/local/bin/mem"], shell=True
    )

    # all of these need to work, so error and show progress
    if (chmod.returncode, sudo_cp.returncode, mv_mem.returncode) != (0, 0, 0):
        raise SystemError(f"""
Moving executable mem.py to /usr/local/bin failed:
chmod +x command:\t\t{chmod.returncode}
sudo cp to /usr/local/bin\t{sudo_cp.returncode}
sudo mv mem.py to mem:\t\t{mv_mem.returncode}
        """.strip())
    print("install successful, enjoy your new mem tool :D")
    return 

if __name__ == "__main__":
    main()