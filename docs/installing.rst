.. _releases page: https://github.com/th3-z/kf2-magicked-admin/releases

==========
Installing
==========

This page covers installing Killing Floor 2 Magicked Admin using the pre-built
binaries or Docker image. If you have already installed or built Killing Floor
2 Magicked Admin you can head to the configuration page next.

The latest pre-built releases are available on the releases page.

Windows
=======

The Windows releases are tested on Windows 10 but should also work on Windows
7, 8, and 8.1.

#. Head over to the `releases page`_ and download the most recent Windows
   version. The file you are looking for is named
   ``kf2-magicked-admin-x.x.x-windows.zip`` where ``x.x.x`` is the version you
   want to download.

#. Extract the zip archive anywhere on your computer.

#. You can now run Killing Floor 2 Magicked Admin by double clicking
   ``magicked_admin.exe`` however it is recommended that you install the
   `web admin patches <#wap-win>`_ before proceeding further.

.. _`wap-win`:

Web Admin Patches
-----------------

test

Linux
=====

The Linux releases are tested on Ubuntu Xenial but should work fine on most
distros.

#. Head over to the `releases page`_ and download the most recent Linux
   version. The file you are looking for is named
   ``kf2-magicked-admin-x.x.x-linux.tar.gz`` where ``x.x.x`` is the version you
   want to download.

    ::

        wget https://github.com/th3-z/kf2-magicked-admin/releases/download/x.x.x/kf2-magicked-admin-x.x.x-linux.tar.gz

#. Extract the tar archive anywhere on your computer.

    ::

        tar -xzf kf2-magicked-admin-x.x.x-linux.tar.gz

#. You can now run Killing Floor 2 Magicked Admin by launching
   ``magicked_admin`` from your command line however it is recommended that you
   install the `web admin patches <#wap-linux>`_ before proceeding further.

    ::

        cd magicked_admin && ./magicked_admin

#. Press ``ctrl+c`` to exit.

.. _`wap-linux`:

Web Admin Patches
-----------------

test

Docker
======

Running with docker is easy. Just issue this command.

::

    docker run -it -p 1880:1880 --name kf2-magicked-admin -v '<host config folder location>':'/magicked_admin/conf' th3z/kf2-magicked-admin

You will need to change ``<host config folder location>`` to wherever you want
to store your config folder. ``/mnt/user/appdata/kf2-magicked-admin`` is a
popular choice for systems running Unraid.

After this command runs the container will exit out and the logs will tell you
to setup the configuration file. Go to your ``conf`` folder and set things up
then run the container again and you are good to go!

Web Admin Patches
-----------------

If you want to use the web admin patches so that Killing Floor 2 Magicked Admin
gets installed into your server directory when the container starts (some
game types wont track stats without it) just mount your game directory into the
container and set the ``PATCHES_TARGET_DIR`` env variable to the directory. You
can mount multiple directories and just separate them with a comma "," in the
env variable if you have many servers. An example follows.

::

    docker run -it -p 1880:1880 --name kf2-magicked-admin -v'<host config folder location>':'/magicked_admin/conf' -v '<host kf folder>':/kf2-server -v '<host kf folder>':/kf2-server-two -e 'PATCHES_TARGET_DIR'='/kf2-server,/kf2-server-two' th3z/kf2-magicked-admin
