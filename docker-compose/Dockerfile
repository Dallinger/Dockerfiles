FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

MAINTAINER Vishal Lall <lall@berkeley.edu>
LABEL Description="Docker for Dallinger" Version="1.2"

ARG DALLINGER_VERSION=4.0.0

# Expose web server
EXPOSE 5000

# Install some dependencies
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install -yq apt-utils apt-transport-https tzdata sudo curl python-pip python-dev git


# Install Dallinger
WORKDIR /home
RUN pip install --upgrade pip
#RUN pip --no-cache-dir install git+git://github.com/Dallinger/Dallinger.git@v${DALLINGER_VERSION}
RUN git clone --branch v${DALLINGER_VERSION} https://github.com/Dallinger/Dallinger
#RUN git clone --branch v3.4.1 https://github.com/Dallinger/Dallinger
#RUN pip install -e git+https://github.com/Dallinger/Griduniverse.git@master#egg=dlgr-griduniverse

# add some experiment files
#RUN git clone --branch master https://github.com/mongates/mongates_dallinger_demos.git

#RUN mkdir Dallinger
#COPY . /home/Dallinger

#Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Install Dallinger
#RUN dallinger setup
WORKDIR /home/Dallinger
# dev-requirements break with `pip install coverage_pth`
RUN pip install -r requirements.txt
RUN python setup.py develop

# Click will abort further execution because Python 3 was configured
# to use ASCII as encoding for the environment.  
# Consult http://click.pocoo.org/python3/for mitigation steps.
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

#RUN apt-get update && apt-get install -y firefox

# Grab supervisord script
#CMD /usr/bin/firefox
#RUN echo "Docker-Dallinger is running... attach to container by running: docker run -p 5000:5000 -p 5432:5432 -p 6379:6379 --name dallinger-test1 <YOUR_IMAGE_NAME>"
