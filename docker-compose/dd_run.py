#!/usr/bin/python

# ======================================================================================================
# Script settings:
browser = 'firefox' # Possible options are 'firefox', 'iexplore', 'chrome', 'opera'
					# modify the script on your own below, if other browser support is needed (line 67)
log_file = 'log_dallinger.txt' # Name of output log file to read from
new_window = True # Open new browser windows (Set to False to reuse existing browser windows)
docker_machine_ip = "192.168.99.100" # docker-machine address
dallinger_startup_delay = 2 # delay in seconds to allow dallinger to complete its startup processes
override_port = True # This will override the port of the experiment to port 5000
# ======================================================================================================

import os
import re
import subprocess
import sys
import time

# TODO?
# add parameters machine-ip
# add browser parameter via cmd

if sys.version_info[0] == 2:
	from urlparse import urlparse as urlparse
elif sys.version_info[0] == 3:
	from urllib import parse as urlparse

try:
	# the IP to use will be read directly from docker ideally
	command = "docker-machine ip"
	docker_machine_ip = subprocess.check_output(['bash','-c', command])
	docker_machine_ip = docker_machine_ip.strip('\n')
except:
	if docker_machine_ip == "":
		docker_machine_ip = "0.0.0.0" # backup default

# Launch Dallinger

command = "docker-compose up -d"
output = subprocess.check_output(['bash','-c', command])

# delete old output log if it exists
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
try:
	os.remove(os.path.join(__location__, log_file))
except:
	pass

print('')
print('Waiting ' + str(dallinger_startup_delay) + ' seconds for Dallinger to start.')

time.sleep(dallinger_startup_delay) 

print('')
print('======================')
print(' Dallinger is running ')
print('======================')
print('')
print(' =  If you need to manually stop this script before it has completed:  =')
print(' =  Please run \"docker-compose down\" before running this script again  =')
print(' =  This is to clean out any unfinished running experiments.           =')
print('')
print(' Use CONTRL-C to stop this script ');
print('')

if browser not in ['firefox', 'iexplore', 'chrome', 'opera']:
	browser = 'iexplore' # XXX check for edge in win10?
	
urls = []
parsed_urls = []
displayed_urls = []

experiment_complete = False

while not experiment_complete:
    try:
		# Grab the latest logs
		command = "docker-compose logs dallinger |& tee " + log_file
		output = subprocess.check_output(['bash','-c', command])
		print("Reading Dallinger output log..")
#		time.sleep(1)

		f = open(os.path.join(__location__, log_file), 'r');
		lines = f.readlines()
		f.close()

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

		parsed_hostname = docker_machine_ip
		for x in urls:
			url_parsed = urlparse(x)
			port = url_parsed.netloc.split(':')[1] # keep the same port
			if override_port: port = 5000
			url = url_parsed._replace(netloc="{}:{}".format(parsed_hostname, port))
			parsed_urls.append(url.geturl())
			
		# Open dallinger windows in browser specified 	
		for url in parsed_urls:
			if url not in displayed_urls:
				print("Displaying: " + url)
				if new_window:
					command = 'start ' + browser + ' -new-window \"' + url + '\"'
				else:
					command = 'start ' + browser + ' \"' + url + '\"'
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
output = subprocess.check_output(['bash','-c', command])