from pathlib import Path
import time
import sys


import subprocess


SOURCE = "./hdrs"


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def execute_command(cmd, **kwargs):

    try:
        start = 0
        end = 0
        if kwargs.get("profile", True):
            start = time.time()

        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

        if kwargs.get("profile", True):
            end = time.time()

        if kwargs.get("verbose", True) or kwargs.get("print_command", False):
            print(
                "\t{} -\r\n {}".format(
                    end - start,
                    bcolors.UNDERLINE + bcolors.WARNING + cmd + bcolors.ENDC,
                )
            )

        if kwargs.get("verbose", True) and output:
            print(output)

        return output

    except subprocess.CalledProcessError as error:
        print("error {} executing {}".format(error.returncode, cmd))
        print(error.output)
        sys.exit(1)
        return None


def run():
    cmd_template = (
        "docker run -v $(pwd):/data -t trigrou/envtools process_environment.py "
    )
    cmd_template += " --encoding rgbe --cubemap-only /data/%s /data/result/%s " ""
    p = Path(SOURCE)
    for hdr in p.glob("*.hdr"):
        cmd = cmd_template % (hdr, hdr)
        print(cmd)
        execute_command(cmd, verbose=True)
        print("")


if __name__ == "__main__":
    run()
