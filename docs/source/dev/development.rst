.. _development:

===============
Developer Guide
===============

Project Structure
-----------------

Issue Tracking
--------------

The bug tracker for the Working Waterfronts API is at `code.osuosl.org`_, and all bugs and feature
requests for the Working Waterfronts API should be tracked there. Please create an issue for any
code, documentation or translation you wish to contribute.

.. _`code.osuosl.org`: https://code.osuosl.org/projects/sea-grant-working-waterfronts/

Repository Layout
-----------------

We loosely follow `Git-flow <http://github.com/nvie/gitflow>`_ for managing
repository. Read about the `branching model <http://nvie.com/posts/a-successful-git-branching-model/>`_
and why `you may wish to use it too <http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/>`_.


**master**
    Releases only, this is the main public branch.
**release/<version>**
    A release branch, the current release branch is tagged and merged into master.
**develop**
    Mostly stable development branch. Small changes only. It is acceptable that this branch have bugs, but should remain mostly stable.
**feature/<issue number>**
    New features, these will be merged into develop when complete.

When working on new code, be sure to create a new branch from the appropriate place:

-  **develop** - if this is a new feature
-  **release/<version>** - if this is a bug fix on an existing release

Code Standards
--------------

We follow `PEP 8 <http://www.python.org/dev/peps/pep-0008/>`_, "the guide for python style".

Developing with Docker
======================

Platform dependent specifics
----------------------------
If you are using Linux you will need to prefix all of the
following commands with sudo. If you are using OS X you will need to use
the boot2docker tool.

Postgis image
-------------
The Working Waterfronts Docker workflow relies on the kartoza/postgis image available
on the docker hub. To pull this image run:

::

    $ docker pull kartoza/postgis

The image can take two optional environment variables to specify a user and
password to the database. These will be specified with the -e option. A port
should be provided with the -p followed by the port to communicate with the
host machine, a colon, and the port to communicate with the container.
Make sure the environment variables passed to this container match those which
are passed to the Working Waterfronts Docker image. Reasonable defaults can be
found in the Dockerfile. Postgres typically runs on port 5432.
To run the image:

::

    $ docker run -d --name postgis -p $HOSTPORT:$CONTAINERPORT -e  USERNAME=$USERNAME -e PASS=$PASSWORD kartoza/postgis

Make sure that the What's Fresh project container connects to the database over
the host port.

Building the What's Fresh docker image
--------------------------------------

::

    $ docker build -t="osuosl/working_waterfronts:dev" .

Running the What's Fresh docker image
-------------------------------------

The Dockerfile included in the root of the repository will load the code from
the current directory. This means that any changes you made to your copy of the
repository will be run. Environment variables can be passed with the -e option.
The Dockerfile specifies a reasonable default set of environment variables,
which can be overridden with the -e option.

Before the app is ready, create the database and run migrations.

::

    $ docker exec -it postgis bash
    # createdb -U $USERNAME -h localhost $DBNAME
    # psql -U $USERNAME -h localhost
    DBNAME=# create extension postgis;
    CREATE EXTENSION
    DBNAME=# ^D
    # ^D
    $ docker run --link postgis:postgis osuosl/working_waterfronts:dev python manage.py migrate

Next, connect to the database with psql and create the relevant user.

::

    $ psql -h localhost -U docker -p $HOSTPORT

Running the server is similar:

::

    $ docker run --link postgis:postgis -p 8000:8000 osuosl/working_waterfronts:dev

If you are running linux, connect to http://localhost:8000 in your browser.
If you are running OS X, get the IP address of your boot2docker vm

::

    $ boot2docker ip
    192.168.59.103

Next connect to http://192.168.59.103:8000 in your browser.

On occasion it may be necessary to obtain a shell in the container:

::

    $ docker run -it osuosl/working_waterfronts:dev bash

Some developers may prefer to mount their copy of the application as a volume
when they run the app:

::

    $ docker run -v /path/to/code/:/opt/working_waterfronts --link postgis:postgis osuosl/working_waterfronts:dev

Developing
==========

Requirements
------------

This project uses a Vagrant virtual machine to create a homogeneous development
environment and allow developers to destroy and recreate their environment in
the case that something goes horribly, horribly wrong.

To set up this environment on your own machine, you'll need a few things:

**Vagrant**

To install Vagrant, just use your package manager::

    sudo yum install vagrant # Debian or Ubuntu
    sudo apt-get install vagrant # Centos

**vagrant-berkshelf and vagrant-omnibus**

These plugins are used to configure the Vagrant machine. To install these
plugins, you'll need to use Vagrant's plugin manager::

    vagrant plugin install vagrant-berkshelf
    vagrant plugin install vagrant-omnibus

Running the Django project
--------------------------

Testing
-------
