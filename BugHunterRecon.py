import os
import subprocess
import argparse

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


OUTPUT_DIR = os.path.join(os.getenv('HOME'), 'BugBounty')
if os.path.isdir(OUTPUT_DIR):
    print("Bug Bounty folder -> {0}{1}{2}{3}".format(colors.BOLD, colors.YELLOW, OUTPUT_DIR,
                                                  colors.ENDC))
else:
    os.makedirs(OUTPUT_DIR)
    print("Bug Bounty folder -> {0}{1}{2}".format(colors.YELLOW, OUTPUT_DIR,
                                                  colors.ENDC))

# print colors.FAIL+ "Warning: ...." + colors.ENDC

def argsParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required='True', help="The domain to target")
    return parser.parse_args()

# Sub-domain finder
def runAmass():
    print("{}==================Running AMASS================={}".format(
        colors.OKGREEN, colors.ENDC))


def runSubfinder():
    pass

# Content-Discovery
def runGobuster():
    pass


def runMassDns():
    pass


# Port Scanning
def runMassScan():
    pass


def runEyeWitness():
    pass


def create_dir(tools, output_dir):
    dirs = {}
    for tool in tools:
        toolDir = os.path.join(output_dir, tool)
        if os.path.isdir(toolDir):
            print("{}: Directory already present".format(toolDir))
        else:
            os.makedirs(toolDir)
        
        dirs[tool] = toolDir
    return dirs


def RunRecon(Target, resultDir):
    """
    This is to run all the recon tools on the target
    """
    runAmass(Target, resultDir)


if __name__ == "__main__":
    args = argsParser()
    Target = args.target

    recon = ['amass', 'subfinder', 'gobuster', 'massdns', 'masscan',
             'eyewitness']

    # Target directory
    target_dir = os.path.join(OUTPUT_DIR, Target)
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    resultDir = create_dir(recon, target_dir)
    print(resultDir)

    # RunReconTools
    RunRecon(Target, resultDir)
