FROM ubuntu:16.04

MAINTAINER OSU Open Source Lab, support@osuosl.org

ENV PASSWORD working_waterfronts
ENV HOST postgis
ENV USER working_waterfronts
ENV NAME  working_waterfronts
ENV ENVIRONMENTCONFIG True
ENV ENGINE django.contrib.gis.db.backends.postgis

EXPOSE 8000

# Add add UbuntuGIS repository to install GDAL
RUN apt-get -y update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable
RUN apt-get -y update

RUN apt-get install -y --no-install-recommends \
    python-dev \
    python-setuptools \
    python-pip \
    build-essential \
    postgresql-server-dev-9.5 \
    gdal-bin \
    gcc \
    curl

WORKDIR /opt/working_waterfronts

COPY . /opt/working_waterfronts
RUN pip install wheel
RUN pip install .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
