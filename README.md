# State of Docker Compose implementation of Dallinger

11 September 2018

## Objectives

  Ideally

  * Users of Windows, Mac OSX and Ubuntu should be able to run Dallinger experiments and specify the experiment that they wish to run, easily.
  * Are able to pick the Dallinger release version they want to run the experiments against, or use their own fork of Dallinger to do so with.

## What works

Bartlett, Memory experiment 2 and Snake have been run successfully (debug mode).

There are currently unsolved issues with running GridUniverse with Docker.

Sandbox mode has not been tested. Running in sandbox mode would rerquire users to supply their credentials to the container to login via Heroku. Unsolved and unattempted.

## Compatibility

This docker compose implementation is currently only compatible with the master branch of Dallinger.
Dallinger v4.0.0 is not supported. It will be supported in Dallinger v4.1.0, once released.
See the Dockerfile for more info.

## Preinstallation notes

Currently the Dockerfile is setup to clone the master branch of Dallinger and uses that for running experiments.

It is also possible to run the Dockerfile in the context of your own existing github clone of Dallinger.
(Note that the version of master should be at least from 11 September 2018 of newer.)
If you wish to do this, comment in the following lines in the Dockerfile:
```
RUN mkdir Dallinger 
COPY . /home/Dallinger
```
and comment out:
```
RUN git clone --branch master https://github.com/Dallinger/Dallinger
```

This can potentially be more convenient as you can make adjustments to your Dallinger code locally.

## Installation

Note that running VPN software may interfere in the setup and running processes of docker-compose and docker-machine.

### Windows 7 or Windows 10 (using Docker-Toolbox)

Make sure that Python is installed on your system.

As a preliminary step, I find that running Kitematic first (until it asks for a Dockerhub account login) seems to smooth out the process of Docker initializing itself on a Windows7 machine. This installs and sets up virtualbox which is needed for the docker-machine to run, which is required by the dd_run.py script.

Open Docker Quickstart Terminal (interactive command line shell)

### Windows 10 (using Docker for Windows)

Make sure that Python is installed on your system.

Run the Powershell app as an administrator

### Mac OSX

Navigate to a new terminal and continue with instructions in "Installation continued (all systems)" section.

### Ubuntu/Linux

Navigate to a terminal.

Start the docker daemon, typically by running ``` sudo dockerd ``` in a terminal.

Open another terminal where you will run docker commands and script.

**Note:** Under Ubuntu/Linux running docker commands might require you to start each of the commands listed in the next few sections, with ``` sudo ```.

**Note:** If you happen to have Postgresql and/or Redis installed in your system, make sure they are not running when you run Dallinger via Docker.

## Installation continued (all systems)


Run ``` docker-compose up -d ``` . This will pull in all the containers necessary and start them in detached mode.

After the process has completed, to see the status of the containers:
``` docker-compose ps ```

To stop your containers:
```docker-compose stop```


## Deciding which experiment to run

The experiment that will be run is set in docker-compose.yml

It can be written as one or multiline:

``` command: /bin/bash -c "cd /home/Dallinger/demos/dlgr/demos/bartlett1932 && dallinger debug --verbose" ```

OR

```
  command: > 
	/bin/bash -c "cd /home/Dallinger/demos/dlgr/demos/bartlett1932 
  	&& dallinger debug --verbose"
```

The Dockerfile is setup to clone all repositories to the home directory of the container. Adjust this if necessary.

## Running the dd_run.py script

The script has been written in Python and contains several configuration parameters (mentioned in the next section).

To run the script:
```
python dd_run.py
```

This starts up the docker containers in detached mode (just like ```docker-compose up -d``` would).
Once the parsing of the setup options is complete, it runs until an exit condition is reached, polling the output log of the dallinger experiment and parsing it for new recruitment requests (to open them in browser windows) and for an indication that the experiment has completed.

The exit condition detection is rather simple at this point. Parsing the log for:
```
exit_txt = ["Experiment completed", "Cleaning up local Heroku process"]
```
or for a ``` KeyboardInterrupt ``` (Ctrl-C) condition.

After an exit condition is reached, the script will shutdown the docker containers and exit. It can take a moment for the script to realize that the experiment has completed.

If the dd_run.py script needed to be preemptively stopped (Ctrl-C), it is necessary to run the ``` docker-compose stop ``` command to stop the containers before running the script again.
Alternatively the dd_stop.sh script can be used by running: ``` ./dd_stop.sh ```, which will stop the containers and display their stopped status after by calling ``` docker-compose ps ```.

**Note:** If the experiment uses another method to indicate that it has completed than the ones specified in the script, it is necessary to manually stop the script using Ctrl-C, and in the case that the script does not shutdown the containers manually, follow with the cleanup mentioned in the previous paragraph.

## dd_run.py configuration options

The dd_run.py script can be configured either in the script itself and/or through command line parameters.
The command line parameters that can be set are:
```
dd_run.py -b <browser> -i <machine_ip_address>'
```

eg: ``` python dd_run.py -b firefox -i 192.168.99.100 ```

Firefox is currently set as the default browser (however no testing takes place to check if the browser has been installed on the system). The possible browser options are: 'firefox', 'iexplore', 'chrome', 'opera' and 'microsoft-edge'. This can be expanded.

Any exposed ports are available on the Docker host’s IP address (known as the "docker-machine ip").
This is determined internally by the script however can be manually overwritten in the command line or in the script settings.

In the script there are other configuration options documented at the beginning of the dd_run.py script itself, namely: 

* ``` browser ``` - which browser to use (command line takes priority)
* ``` log_file  ``` - name of output log file to read from, to poll for experiment output.
* ``` new_window ``` - open new browser windows (Set to False to reuse existing browser windows)
* ``` dallinger_startup_delay ``` - delay in seconds to allow Dallinger to complete its startup processes (tweak this if browsers open up too soon)
* ``` override_port ``` - This will override all the port parts of the experiment's urls to port 5000, otherwise whatever port the experiment desires will be used (however it might be necessary to expose those ports in the Dockerfile first)


## Debugging

Running ``` docker-compose up ``` (normal, non-detached mode) can be used to inspect the current state, by viewing the console output.

The output logs of all three containers can be extracted using the ``` dd_logs.sh ``` script and inspected by running: ``` ./dd_logs.sh ```

One can also manually extract and view the current Dallinger log with: 

``` docker-compose logs dallinger |& tee log_dallinger.txt ```

This saves the log to the ``` log_dallinger.txt ``` file and also displays it in the command line output.


## Known issues

Changing the Postgres version in docker-compose.yml may result in errors later. Postgres may complain and not run stating that the database was previously created with another version of Postgres. Erasing Docker entirely from your machine and reinstalling it fresh worked in solving this. Perhaps other less drastic methods exists but have not been investigated.

If Dallinger runs into an error while executing in the container, it will exit with a non-zero condition. This can be seen with ``` docker-compose ps ``` and it makes it difficult to inspect and debug as one can only bash into a running container. Use the logs in this case to help you.

It should, in theory, be possible to run the experiment from inside the container manually, using: ``` docker-compose exec dallinger bash ``` to enter the container (while the container is running) and then navigating to the experiment directory and running the experiment etc. (The initial command should be set to ``` command: /bin/bash ``` in the docker-compose.yml in this case.)
However, I have found that in such scenarios the output stops more or less after the Dallinger ascii art logo and there is no indication of activity beyond that point. Parsing the logs later after exiting the container has been found to yield no useful information as to whether	the experiment ran or not.


## Making changes

Making small changes to the docker-compose.yml file typically does not require a rebuild. Make sure all the Docker containers are stopped or there may be errors stopping and restarting them later if their configuration is changed (in docker-compose.yml) while they were active/running.

Making changes to the Dockerfile can sometimes be tricky as Docker tries to cache the Dockerfile steps as much as possible. A small change to Dockerfile might not be picked up by Docker as a "change".

I find the following process to be more foolproof (although more time and bandwidth consuming):
* Stop all containers if running: ```	docker-compose stop ```
* Remove all container images: ```	docker-compose down --rmi all ```
* Rebuild and start containers in detached mode: ``` docker-compose up -d ```
* If necessary stop the containers: ```	docker-compose stop ```


## Compatibility and testing notes

Windows 7 currently supports Docker-Toolbox (an older version of Docker).
Docker-Toolbox is the recommended version for Windows 7 and the newer Docker Community Edition/Docker for Windows will not install on Windows 7.

Windows 10 also supports Docker-Toolbox, this script has been tested to be working in Windows 10 using Docker-Toolbox.

Docker for Windows under Windows 10 is also supported, as the script allows one to use Powershell instead of Bash.
If Bash is installed on Windows 10 as part of the "Windows Sybsystem for Linux" option, it will likely be good to force
the script to use Powershell. This is a configurable setting in the script.

Tested on Ubuntu 16.04. Firefox has been found to be the most dependable browser as Google Chrome and Opera both polluted the terminal with their own output, blocking the script from running correctly until the browser window was closed. This may have been due to running Ubuntu in a VM however, more testing has not been done.

Tested on OSX 10.13. Safari has been found to be buggy. Google Chrome is recommended as Firefox has trouble opening more than one instance of Firefox under OSX without additional tweaking. See https://stackoverflow.com/questions/43294774/how-to-open-new-window-in-firefox-with-terminal-on-mac

The dd_run.py script has been tested with Python 2.7.12, however provisions were made in the script to work with Python 3 (not explicitly tested)

No testing was done with versions of Windows 8.


## Docker troubleshooting on Windows 10

These references may prove useful when running Docker in a Windows 10 environment.

**Note:** These are just some potentially helpful leads that may help you in your process of getting Docker working under Windows, not by any means complete or exhaustive.

**Docker machine**

Get ht<span>tps://</span>registry-1.docker.io/v2/: net/http: request canceled while waiting for connection:  
https://github.com/docker/for-win/issues/611

**Docker for Windows**

If you had Docker-toolbox installed before and are now using Docker for Windows:  
https://github.com/docker/for-win/issues/1746

If your experiment is running but you see no output in the browser window(s) when they launch.  
Try running the script with the ``-i 127.0.0.1`` option.

When using Docker for Windows, the default docker-machine might not be configured correctly.  
Check this by running: ``docker-machine ip``.  
If you get an error such as:  
``open C:\Users\admin\.docker\machine\machines\default\config.json: The system cannot find the file specified.``  
Consider removing the default docker-machine by: ``docker-machine rm -f default``, setting up a hyper-v network switch (if you don't have one). Read more on this here: https://docs.docker.com/machine/drivers/hyper-v/  

Then you can create a new default docker-machine.  
For example after setting up a virtual switch called 'ext' run: ``docker-machine create -d hyperv --hyperv-virtual-switch ext default`` to setup a new default docker-machine.

**Other troubleshooting ideas**  

Microsoft edge not seeing the docker-machine IP address:  
https://www.hanselman.com/blog/FixedMicrosoftEdgeCantSeeOrOpenVirtualBoxhostedLocalWebSites.aspx

Common issues and fixes:  
https://github.com/docker/kitematic/wiki/Common-Issues-and-Fixes  


## Reference of useful docker-compose commands

* ``` docker-compose ```
* ``` docker-compose up ```
* ``` docker compose up -d ```
* ``` docker-compose stop ```
* ``` docker-compose exec dallinger bash ```
* ``` docker-compose exec dallinger bash -c "cd /home/Dallinger/ && dallinger debug --verbose" ```
* ``` docker-compose ps ```
* ``` docker-compose build ```
* ``` docker-compose down --rmi all ```

**Note:** Under Ubuntu/Linux running these commands might require you to start each of the commands listed above, with ``` sudo ```.
