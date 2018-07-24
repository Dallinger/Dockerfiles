FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

LABEL Description="Docker for Dallinger" Version="1.2.1"

# Not in use currently
ARG DALLINGER_VERSION=4.0.0

# Expose web server
EXPOSE 5000

# Install some dependencies
RUN apt-get update && apt-get upgrade -yq
RUN apt-get install -yq apt-utils apt-transport-https tzdata sudo curl python-pip python-dev git pandoc vim

WORKDIR /home

# Clone Dallinger and demos
#RUN git clone --branch v${DALLINGER_VERSION} https://github.com/Dallinger/Dallinger
RUN git clone --branch stories/345-dockerfile-windows https://github.com/Dallinger/Dallinger
RUN git clone --branch master https://github.com/mongates/mongates_dallinger_demos.git
RUN git clone --branch master https://github.com/witekdev/Griduniverse.git

# Install Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Next 2 lines are needed if sourcing Dallinger from context and not cloning directly from github
#RUN mkdir Dallinger
#COPY . /home/Dallinger

# Install Dallinger
WORKDIR /home/Dallinger

RUN apt-get install -yq enchant
#RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install -r dev-requirements.txt
#RUN python setup.py develop
RUN pip install -e .[data]
RUN pip install -e demos

WORKDIR /home
# Do we need these?
#EXPOSE 6379
#EXPOSE 5432

# Add two ENV variables as a fix for when using python3:
# Click will abort further execution because Python 3 was configured
# to use ASCII as encoding for the environment.  
# Consult http://click.pocoo.org/python3/for mitigation steps.
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

CMD /bin/bash
