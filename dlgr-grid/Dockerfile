FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

MAINTAINER Vishal Lall <lall@berkeley.edu>
LABEL Description="Docker image for Dallinger with GridUniverse" Version="1.0"

ARG DALLINGER_VERSION=4.0.0

# Click will abort further execution because Python 3 was configured
# to use ASCII as encoding for the environment.  
# Consult http://click.pocoo.org/python3/for mitigation steps.
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

ENV proxy_ip 0.0.0.0
ENV proxy_port 5000

RUN apt-get update && apt-get upgrade -yq
RUN apt-get install -yq apt-utils apt-transport-https tzdata sudo curl python3-pip python3-dev git
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3
RUN apt-get -yq install postgresql-10

#=========================================================================================
# from https://docs.docker.com/engine/examples/postgresql_service/
# ubuntu 18.04 contains postgres 10.3
USER postgres
# Create a PostgreSQL role named ``dallinger`` with ``dallinger`` as the password and
# then create a database `dallinger` and 'dallinger-import' owned by the ``dallinger`` role.
# Note: here we use ``&&\`` to run commands one after the other - the ``\``
#       allows the RUN command to span multiple lines.
RUN    /etc/init.d/postgresql start &&\
    psql --command "CREATE USER dallinger WITH SUPERUSER PASSWORD 'dallinger';" &&\
    createdb -O dallinger dallinger &&\
    createdb -O dallinger dallinger-import

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
USER root
RUN echo "host    all             all              0.0.0.0/0              trust" >> /etc/postgresql/10/main/pg_hba.conf
# And add ``listen_addresses`` to ``/etc/postgresql/10/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/10/main/postgresql.conf
#=========================================================================================
RUN sed /etc/postgresql/10/main/pg_hba.conf -e 's/md5/trust/g' --in-place

# Redis
RUN apt-get -yq install redis-server

#Heroku
RUN curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

RUN sudo pip3 install matplotlib==2.1.0
RUN sudo pip3 install -e git+https://github.com/Dallinger/Dallinger.git@docker-ip-proxy#egg=dallinger[data]
RUN sudo pip3 install -e git+https://github.com/Dallinger/Griduniverse.git@master#egg=dlgr-griduniverse

# Expose web server
EXPOSE 5000
# Expose psql
EXPOSE 5432
# Expose redis
EXPOSE 6379

#CMD [ "sh", "-c", "echo $proxy_ip $proxy_port" ]
ENTRYPOINT sudo service redis-server start && sudo service postgresql start && cd /src/dallinger/demos/dlgr/demos/bartlett1932 && /bin/bash
#ENTRYPOINT /startup.sh ; /bin/bash
#CMD ["bash"]
