import os
import shutil
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
def runAmass(Target, path):
    out = os.path.join(path['amass'], 'amass.txt')
    
    if os.path.isfile(out):
        os.remove(out)

    if os.path.isdir(os.path.join(os.getenv('HOME'), 'snap', 'amass')):
        shutil.rmtree(os.path.join(os.getenv('HOME'), 'snap', 'amass'))
    else:
        print("~/snap/amass Directory is not present")

    print("{}==================Running AMASS================={}".format(
        colors.OKGREEN, colors.ENDC))
    run_amass = subprocess.Popen(['amass', 'enum', '-active',
                                 '-src', '-ip', '-o', '{}'.format(out),
                                 '-d', '{}'.format(Target)],
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print run_amass.communicate()


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
            print("{0}{1}{2}: Directory already present".format(
                colors.OKGREEN,toolDir,colors.ENDC))
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

    # RunReconTools
    RunRecon(Target, resultDir)
