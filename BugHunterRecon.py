import os

OUTPUT_DIR = os.path.join(os.getenv('HOME'), 'BugB')

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print colors.FAIL+ "Warning: ...." + colors.ENDC

# Sub-domain finder
def runAmass():
    pass


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


if __name__ == "__main__":
    if os.path.isdir(OUTPUT_DIR):
        print True
    else:
        os.makedirs(OUTPUT_DIR)

