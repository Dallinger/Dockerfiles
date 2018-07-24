# State of Docker Windows support experiment

07/24/2018

## Objectives

  Ideally
  
  * Windows users should be able to run Dallinger experiments and specify the experiment that they wish to run, easily.
  * Are able to pick the Dallinger release version they want to run the experiments against, or use their own fork of Dallinger to do so with.


## What works

Bartlett, Memory experiment 2 and Snake have been run successfully (debug mode).

As of 07/24/2018 there are yet unsolved issues with running GridUniverse under Docker.

Sandbox mode has not been tested. Running in sandbox mode would rerquire users to supply their credentials to the container to login via Heroku. Unsolved and unattempted.


## Installation

 As a preliminary step, I find that running Kinematic first (until it asks for a Dockerhub account login) seems to smooth out the process of Docker initializing itself on a Windows7 machine.

Open Docker Quickstart Terminal (interactive command line shell)

Run ``` docker-compose up -d ``` . This will pull in all the containers necessary and start them in detached mode.   
This pulling of containers may take a few minutes (depending on your internet connection speed).

After the process has completed, to see the status of the containers:
``` docker-compose ps ```

To stop your containers:
```docker-compose stop```


## Deciding which experiment to run

The experiment that will be run is set in docker-compose.yml

It can be written as one or multiline:

``` command: /bin/bash -c "cd /home/Dallinger/demos/dlgr/demos/snake && dallinger debug --verbose" ```

OR

```
  command: > 
	/bin/bash -c "cd /home/mongates_dallinger_demos/memoryexpt2 
  	&& dallinger debug --verbose"
```

The Dockerfile is setup to clone all repositories to the home directory of the container. Adjust if necessary.


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
Alternatively the dd_stop.sh script can be used, which will stop the containers and display their stopped status after by calling ``` docker-compose ps ```.

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

The output logs of all three containers can be extracted using the ``` dd_logs.sh ``` script and inspected.

One can also manually extract and view the current Dallinger log with: 

``` docker-compose logs dallinger |& tee log_dallinger.txt ```

This saves the log to the ``` log_dallinger.txt ``` file and also displays it in the command line output.


## Known issues

Changing the Postgres version in docker-compose.yml may result in errors later. Postgres may complain and not run saying that the database was created with another version of Postgres. I have gotten past this by wiping Docker entirely on my machine and reinstalling it fresh.

If Dallinger runs into an error while executing in the container, it will exit with a non-zero condition. This can be seen with ``` docker-compose ps ``` and it makes it difficult to inspect and debug as one can only bash into a running container. Use the logs in this case to help you.

It should, in theory, be possible to run the experiment from inside the container manually, using: ``` docker-compose exec dallinger bash ``` to enter the container (while the container is running) and then navigating to the experiment directory and running the experiment etc. (The initial command should be set to ``` command: /bin/bash ``` in the docker-compose.yml in this case.)   
However, I have found that in such scenarios the output stops more or less after the Dallinger ascii art and there is no indication of activity. Parsing the logs later after exiting the container has been found to yield no useful information as to whether	the experiment ran or not.


## Making changes

Making small changes to the docker-compose.yml file typically does not require a rebuild. Make sure all the Docker containers are stopped or there may be errors stopping and restarting them later if their configuration is changed (in docker-compose.yml) while they were active/running.

Making changes to the Dockerfile can sometimes be tricky as Docker tries to cache the Dockerfile steps as much as possible. A small change to Dockerfile might not be picked up by Docker as a "change".

I find the following process to be more foolproof (though more time consuming):
* Stop all containers if running: ```	docker-compose stop ```
* Remove all container images: ```	docker-compose down --rmi all ```
* Rebuild and start containers in detached mode: ``` docker-compose up -d ```
* If necessary stop the containers: ```	docker-compose stop ```


## Compatibility and testing notes

Windows 7 currently supports Docker-Toolbox (an older version).

Docker-Toolbox is the recommended version for Windows 7 and the newer Docker Community Edition/Docker for Windows will not install on Windows 7.

The dd_run.py script setup has not been tested on Windows 10. (With the exception of integrating microsoft-edge command line syntax into the script, syntax tested in a Windows 10 VM)

The dd_run.py script has been tested with Python 2.7.12, however provisions were made in the script to work with Python 3 (not explicitly tested)


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