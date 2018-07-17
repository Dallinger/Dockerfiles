FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

MAINTAINER Vishal Lall <lall@berkeley.edu>
LABEL Description="Docker for Dallinger" Version="1.2"

ARG DALLINGER_VERSION=4.0.0

# Expose web server
EXPOSE 5000

# Install some dependencies
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install -yq apt-utils apt-transport-https tzdata sudo curl python-pip python-dev git pandoc

# Install Dallinger
WORKDIR /home
RUN pip install --upgrade pip
RUN git clone --branch v${DALLINGER_VERSION} https://github.com/Dallinger/Dallinger
#RUN pip install -e git+https://github.com/Dallinger/Griduniverse.git@master#egg=dlgr-griduniverse

# add some experiment files
RUN git clone --branch master https://github.com/mongates/mongates_dallinger_demos.git

#Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install Dallinger
WORKDIR /home/Dallinger
# dev-requirements break with `pip install coverage_pth`
RUN pip install -r requirements.txt
RUN python setup.py develop

WORKDIR /home

# Click will abort further execution because Python 3 was configured
# to use ASCII as encoding for the environment.  
# Consult http://click.pocoo.org/python3/for mitigation steps.
# If using Python3 - uncomment next 2 lines
#ENV LC_ALL C.UTF-8
#ENV LANG C.UTF-8

CMD /bin/bash
