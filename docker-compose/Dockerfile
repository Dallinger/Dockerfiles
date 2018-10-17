FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

LABEL Description="Docker Compose implementation of Dallinger" Version="1.0"

# This docker compose implementation is not compatible with version 4.0.0 of Dallinger.
# The fix to make this compatible with Dallinger was merged to master on 10 September 2018
# https://github.com/Dallinger/Dallinger/pull/1336

# Not in use currently, can be used once version 5.0.0 is released
#ARG DALLINGER_VERSION=5.0.0

# Expose web server
EXPOSE 5000

# Install some dependencies
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install -yq apt-utils apt-transport-https tzdata sudo curl python-pip python-dev git pandoc vim

WORKDIR /home

# Clone Dallinger and demos
#RUN git clone --branch v${DALLINGER_VERSION} https://github.com/Dallinger/Dallinger
RUN git clone --branch master https://github.com/Dallinger/Dallinger

# Install Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Next 2 lines are needed if sourcing Dallinger from context and not cloning directly from github
#RUN mkdir Dallinger
#COPY . /home/Dallinger

# Install Dallinger
WORKDIR /home/Dallinger

RUN apt-get install -yq enchant
RUN pip install --upgrade pip
RUN pip install -r dev-requirements.txt
RUN pip install -e .[data]
RUN pip install -e demos

WORKDIR /home

# Add two ENV variables as a fix when using python3, to prevent this error:
# Click will abort further execution because Python 3 was configured
# to use ASCII as encoding for the environment.
# Consult http://click.pocoo.org/python3/for mitigation steps.
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD /bin/bash
