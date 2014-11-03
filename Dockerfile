FROM continuumio/miniconda:py27_latest

MAINTAINER Brendan Smithyman

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install git
RUN /opt/anaconda/bin/conda update --prefix /opt/anaconda conda
RUN /opt/anaconda/bin/conda install pip pymongo
RUN /opt/anaconda/bin/pip install git+https://github.com/bsmithyman/nest_thermostat.git

RUN mkdir -p /etc/cron.hourly
ADD /nestlog.py /etc/cron.hourly/

exec /usr/sbin/cron -f