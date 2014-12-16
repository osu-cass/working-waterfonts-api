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
