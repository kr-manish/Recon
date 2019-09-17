import os
import json
import re
import shutil
import subprocess
import argparse
from util import *

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

FAIL = 1
PASS = 0


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
    amass_cmd = 'amass enum -active -src -ip -o {0} -d {1}'.format(out, Target)
    run_amass = subprocess.Popen([amass_cmd],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = run_amass.communicate()
    if(stderr):
        print("{0} AMASS: Something went wrong!!! {1}".format(colors.FAIL, colors.ENDC))
        print(stderr)
        return FAIL, FAIL
    else:
        # Extract the domains from the amass output
        print("extracting domains from the Amass output")
        domFile = os.path.join(path['amass'], 'domains.txt')
        cmd = r"awk -F']' '{{print $2}}' {0} | awk -F' ' '{{print $1}}' > {1}".format(out, domFile)
        runCmd = subprocess.call([cmd], shell=True)
        print("{0} ===========Amass completed============ {1}".format(colors.OKGREEN, colors.ENDC))
        return PASS, domFile


# Content-Discovery
def runGobuster():
    pass


def runMassDns(domainFile, path):
    output = os.path.join(path['massdns'], 'massdns.txt')
    resolve = os.path.join(os.getenv('HOME'), 'Tools', 'massdns', 'lists', 'resolvers.txt')
    print("{}==================Running MASSDNS================{}".format(colors.OKGREEN, colors.ENDC))
    run_massdns = subprocess.Popen(['massdns -r {0} {1} -o S -w {2}'.format(
        resolve, domainFile, output)], shell=True)
    stdout, stderr = run_massdns.communicate()
    if(stderr):
        print("{0} MASSDNS: Something went wrong!!! {1}".format(colors.FAIL, colors.ENDC))
        print(stderr)
        return FAIL
    else:
        print("{0} ===========MASSDNS completed============ {1}".format(colors.OKGREEN, colors.ENDC))
        return PASS


# Port Scanning
def runMassScan(domainFile, path):
    domain_ip_file = os.path.join(path['masscan'], 'domain_ip_dict.json')
    print("{}==================Running MASSCAN================{}".format(colors.OKGREEN, colors.ENDC))
    # ip_cmd = r'dig +short {}'
    scan_cmd = r'masscan -p80 {0}'

    #Get all the unique IPs from the domains
    all_ips, domain_dict = getIPlist(domainFile, path)
    for ip in all_ips:
        ip_output = os.path.join(path['masscan'], ip)
        run_massdns = subprocess.Popen(
            ['masscan -p1-10000 -oG {0} {1}'.format(ip_output, ip)], shell=True)
        stdout, stderr = run_massdns.communicate()

        if stderr:
            print("{0} Something wrong with the port scan!!! {1}".format(colors.FAIL, colors.ENDC))

        # Update the dictionary
        cmd = r"grep 'Ports:' {} | awk -F':' '{{print $4}}'".format(ip_output)
        with open(ip_output, 'r') as f:
            gcmd = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
            ports = gcmd.communicate()[0].split('\n')
            ports.remove('')
            domain_ip_dict = fillPort(ports, ip, domain_dict)

        if(stderr):
            print("{0} MASSCAN: Something went wrong!!! {1}".format(colors.FAIL, colors.ENDC))
            print(stderr)
            return FAIL
        else:
            print("==========={} scan completed============".format(ip))
    print("{0}==================MASSCAN Completed================{1}".
          format(colors.OKGREEN, colors.ENDC))

    with open(domain_ip_file, 'w') as f:
        json.dump(domain_ip_dict, f)

    return PASS


def runEyeWitness():
    pass


def RunRecon(Target, resultDir):
    """
    This is to run all the recon tools on the target
    """
    retcode, domain_File = runAmass(Target, resultDir)
    if not retcode:
        retcode = runMassDns(domain_File, resultDir)
        retcode = runMassScan(domain_File, resultDir)
    else:
        print("{0} Something Went wrong{1}".format(colors.FAIL, colors.ENDC))


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
