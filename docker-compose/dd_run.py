#!/usr/bin/python

# Windows, MAC (OSX) and Ubuntu/Linux compatible version
# ======================================================================================================
# Script settings:
browser = 'firefox' # Possible options are 'firefox', 'chrome', 'opera' 'safari' for OSX
# Possible options are 'firefox', 'iexplore', 'chrome', 'opera' 'microsoft-edge' for Windows
# Possible options are 'firefox', 'google-chrome', 'opera' for Linux. Note Firefox has been found 
# to be the most robust. Opera and Google Chrome may or may not work.
# modify the script below, if other browser support is needed (line 48)
log_file = 'log_dallinger.txt' # Name of output log file to read from
new_window = True # Open new browser windows (Set to False to reuse existing browser windows)
                  # Note: This might not be possible on all browsers listed above
dallinger_startup_delay = 0 # delay in seconds to allow dallinger to complete its startup processes
                            # set to 0 to bypass
override_port = True # This will override the port of the experiment to port 5000
use_sudo_for_linux = True # This will prepend sudo to all docker commands the script runs in Linux
# ======================================================================================================

import platform
import getopt
import os
import re
import subprocess
import sys
import time

# Parse user defined parameters for browser and docker_machine ip (if present)
docker_machine_ip = ""
argv = sys.argv[1:]
try:
    opts, args = getopt.getopt(argv,"hb:i:",["browser=","machine_ip="])
except getopt.GetoptError:
    print('dd_run.py -b <browser> -i <machine_ip_address>')
    sys.exit(2)
for opt, arg in opts:
    if opt == '-h':
        print('dd_run.py -b <browser> -i <machine_ip_address>')
        sys.exit()
    elif opt in ("-b", "--browser"):
        browser = arg
    elif opt in ("-i", "--machine_ip"):
        docker_machine_ip = arg

# Browser sanity checks
platform = platform.system()
if platform == 'Darwin': # OSX
    if browser not in ['firefox', 'chrome', 'opera', 'safari']:
        browser = 'firefox'
elif platform == 'Windows':
    if browser not in ['firefox', 'iexplore', 'chrome', 'opera', 'microsoft-edge']:
        browser = 'iexplore'
elif platform == 'Linux':
    if browser not in ['firefox', 'google-chrome', 'opera']:
        browser = 'firefox'	

# Python 2 and 3 use different urlparse methods
if sys.version_info[0] == 2:
    from urlparse import urlparse as urlparse
elif sys.version_info[0] == 3:
    from urllib import parse as urlparse

if platform in ['Linux', 'Darwin']:
    # Linux and OSX seem to do fine without docker-machine
    docker_machine_ip = "0.0.0.0" # backup default
else:
    try:
        # the IP to use will be read directly from docker ideally (unless user overriden)
        if docker_machine_ip == "":
            command = "docker-machine ip"
            docker_machine_ip = subprocess.check_output(['bash','-c', command])
            docker_machine_ip = docker_machine_ip.strip('\n')
    except:
        if docker_machine_ip == "":
            docker_machine_ip = "0.0.0.0" # backup default

# Launch Dallinger
command = "docker-compose up -d"
if platform == 'Linux' and use_sudo_for_linux: command = "sudo " + command
output = subprocess.check_output(['bash','-c', command])

# delete old output log if it exists
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
try:
    os.remove(os.path.join(__location__, log_file))
except:
    pass

if dallinger_startup_delay != 0:
    print('')
    print('Waiting ' + str(dallinger_startup_delay) + ' seconds for Dallinger to start.')
    time.sleep(dallinger_startup_delay)

print('')
print('======================')
print(' Dallinger is running ')
print('======================')
print('')
print(' =  If you need to manually stop this script before it has completed:  =')
print(' =  Please run \"docker-compose stop\" before running this script again  =')
print(' =  This is to clean out any unfinished running experiments.           =')
print('')
print(' Use CONTRL-C to stop this script ');
print('')

urls = []
parsed_urls = []
displayed_urls = []

experiment_complete = False

while not experiment_complete:
    try:
        # Grab the latest state of the outout log
        command = "docker-compose logs dallinger >& " + log_file
        if platform == 'Linux' and use_sudo_for_linux: command = "sudo " + command
        output = subprocess.check_output(['bash','-c', command])
        print("Reading Dallinger output log..")
        try:
            f = open(os.path.join(__location__, log_file), 'r');
            lines = f.readlines()
            f.close()
        except IOError:
            print('')
            print("Could not read experiment log file. Exiting.")
            break

    except KeyboardInterrupt:
        print('')
        print('Ctrl-C pressed.')
        break

    try:
        searchtxt = "New participant requested:"
        exit_txt = ["Experiment completed", "Cleaning up local Heroku process"]
        for i, line in enumerate(lines):
            if searchtxt in line and i+1 < len(lines):
                urls.append(re.search("(?P<url>https?://[^\s]+)", line).group("url"))
            for txt in exit_txt:
                if txt in line:
                    if not experiment_complete:
                        print("Experiment complete.")
                        experiment_complete = True
    except KeyboardInterrupt:
        print('')
        print('Ctrl-C pressed.')
        break

    try:
        parsed_hostname = docker_machine_ip
        for x in urls:
            url_parsed = urlparse(x)
            port = url_parsed.netloc.split(':')[1] # keep the same port
            if override_port: port = 5000 # override port if desired
            url = url_parsed._replace(netloc="{}:{}".format(parsed_hostname, port))
            parsed_urls.append(url.geturl())
    except KeyboardInterrupt:
        print('')
        print('Ctrl-C pressed.')
        break

    try:
        # Open dallinger windows in browser specified
        for url in parsed_urls:
            if url not in displayed_urls:

                print("Displaying: " + url)

                if platform == 'Darwin': # OSX
                    if browser == 'safari':
                        if new_window:
                            command = "open -na safari " + ' \"' + url + '\"'
                        else:
                            command = "open -a safari " + ' \"' + url + '\"'
                    elif browser == 'chrome':
                        if new_window:
                            command = "open -na 'Google Chrome' --args --new-window " + ' \"' + url + '\"'
                        else:
                            command = "open -a 'Google Chrome' " + ' \"' + url + '\"'
                    elif browser == 'firefox':
                        if new_window: # 'open -na firefox --args --new-window' fails with
                                       # A copy of Firefox is already open. Only one copy of Firefox can be open at a time.
                                       # Skip open in new window functionality for FF for now
                            command = "open -a firefox " + ' \"' + url + '\"'
                        else:
                            command = "open -a firefox " + ' \"' + url + '\"'
                    elif browser == 'opera':
                        if new_window:
                            command = "open -na opera --args --new-window " + ' \"' + url + '\"'
                        else:
                            command = "open -a opera " + ' \"' + url + '\"'

                elif platform == 'Windows':
                    if browser == 'microsoft-edge': # uses different syntax (does not support new window openings)
                        command = 'start ' + browser + ':\"' + url + '\"'
                    elif browser == 'iexplore':
                        # ie opens up new windows by default (win7) and does not recognize new_window parameter
                        command = 'start ' + browser + ' \"' + url + '\"'
                    # all other browsers:
                    elif new_window:
                        command = 'start ' + browser + ' -new-window \"' + url + '\"'
                    else:
                        command = 'start ' + browser + ' \"' + url + '\"'

                elif platform == 'Linux':
                    if new_window: # '&' makes the browser run in background and not block the terminal. # Does this work?
                        command = browser + ' -new-window \"' + url + '\"' + ' &'
                    else:
                        command = browser + ' \"' + url + '\"' + ' &'

                output = subprocess.check_output(['bash','-c', command])
                displayed_urls.append(url)
    except KeyboardInterrupt:
        print('')
        print('Ctrl-C pressed.')
        break

# SHUTDOWN	
print('')
print('Shutting down Dallinger..')
command = "docker-compose down"
if platform == 'Linux' and use_sudo_for_linux: command = "sudo " + command
output = subprocess.check_output(['bash','-c', command])
