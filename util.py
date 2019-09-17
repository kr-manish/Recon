import subprocess
from BugHunterRecon import colors
import os
import re
import json

def getIPlist(domainFile, path):
    ip_list_file = os.path.join(path['masscan'], 'ip_list')
    all_ip = []
    domain_dict = {}
    with open(domainFile, 'r') as f:
        domain = f.readline().rstrip()
        while domain:
            # Get IPs
            ip_cmd = r'dig +short {}'.format(domain)
            runcmd = subprocess.Popen([ip_cmd], shell=True, stdout=subprocess.PIPE)
            ip_list = runcmd.communicate()[0].split('\n')

            # Get IPs related to a domain in a dictionary
            # Convert to dictionary of empty list in which ports will go
            ip_dict = {ip:[] for ip in ip_list}
            # removing '' key from dictionary
            ip_dict = {k:v for k, v in ip_dict.items() if k is not ''}
            domain_dict[domain] = ip_dict
            for ip in ip_list:
                valid = re.search(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip)
                if valid:
                    all_ip.append(ip)
            domain = f.readline().rstrip()
    
    all_ip = list(dict.fromkeys(all_ip))

    # Write all the IPs to file
    with open(ip_list_file, 'w') as f:
        for ip in all_ip:
            f.write('%s\n' % ip)

    return all_ip, domain_dict


def fillPort(ports, ip, domain_dict):
    print(ip)
    for domain,_ip in domain_dict.iteritems():
        if ip in _ip:
            domain_dict[domain][ip] = ports

    return domain_dict


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

