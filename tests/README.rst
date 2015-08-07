flask-todoapp tests
===================

Set up on Ubuntu/Debian
-----------------------

Run the following::

    $ sudo apt-get install python3 python-setuptools python3-dev python-virtualenv python-pip automake libtool libreadline6 libreadline6-dev zlib1g-dev libxml2 libxml2-dev make build-essential libssl-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libpq-dev iceweasel

    $ sudo pip install hitch


Set up on Red Hat/CentOS/Fedora
-------------------------------

Make sure python 3 is installed, e.g.::

    $ sudo yum install https://dl.iuscommunity.org/pub/ius/stable/CentOS/6/x86_64/ius-release-1.0-14.ius.centos6.noarch.rpm

    $ sudo yum install python34u

And then::

    $ sudo yum install python-setuptools python-devel python-pip python-virtualenv firefox automake libtool readline-devel zlib-devel libxml2 libxml2-devel gcc gcc-c++ make openssl-devel bzip2-libs zlib-devel sqlite-devel wget curl llvm postgresql-libs postgresql-devel xorg-x11-xauth

    $ sudo pip install hitch


Set up on Arch
--------------

Run the following::

    $ sudo pacman -S python3 python-setuptools python-pip python-virtualenv m4 base-devel git firefox xorg-xauth xorg-xhost firefox automake readline zlib libxml2 gcc make openssl bzip2 zlib sqlite3 wget curl llvm postgresql-libs

    $ sudo pip install hitch

Set up on Mac OS X
------------------

On Mac OS X, ensure that you have firefox installed, and then run::

    $ brew install python python3 git libtool automake readline

    $ brew link readline

    $ pip install -U setuptools pip virtualenv hitch


Run tests
=========

Once in the tests folder, just run::

  $ hitch init

There is currently one test which creates a TODO to clean the house and the finishes it::

  $ hitch clean-the-house.test

There is also one stub test which just loads the website and pauses::

  $ hitch test stub.test

Note that the first run of either test may take up to 20 minutes to run as it must download and build Python and Postgres. Subsequent test runs will take seconds.

Note that you can pause tests by putting a "- Pause" step in them.


Caveats
-------

* The tests will only run on *nix systems. Windows is not supported.
