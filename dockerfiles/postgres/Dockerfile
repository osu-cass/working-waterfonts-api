FROM ubuntu:vivid

MAINTAINER OSU Open Source Lab <support@osuosl.org>


RUN apt-get -y update

RUN apt-get install -y postgresql-9.4 postgresql-client-9.4 postgresql-server-dev-9.4 postgresql-9.4-postgis-2.1

ENV DATADIR /var/lib/postgresql/9.4/main
ENV INITDB /usr/lib/postgresql/9.4/bin/initdb 
ENV USER docker
ENV PASSWORD docker
ENV DATABASE geodb
ENV POSTGRES /usr/lib/postgresql/9.4/bin/postgres

EXPOSE 5432

RUN $POSTGRES createdb $DATABASE
RUN $POSTGRES createuser --superuser $USER
RUN psql -U $USERNAME -c 'create extension postgis'
