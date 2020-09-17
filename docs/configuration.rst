=============
Configuration
=============

This page covers the configuration of Killing Floor 2 Magicked Admin. Upon the
initial run you will be prompted to configure the software however there are
many more options available to you that are documented here.

If you are running Killing Floor 2 Magicked Admin for the first time and
already have Killing Floor 2's web admin panel setup you should skip ahead to
the `Interactive Setup`_ section.

Server Configuration
====================

Killing Floor 2 Magicked Admin utilises Killing Floor2's built-in web admin
panel to track statistics, gameplay events, and chat without a mutator. However
the web admin panel is not enabled by default. This section will cover enabling
the web admin panel.

Web Admin Patches
-----------------

Multi-Admin
-----------


Interactive setup
=================

When you first run Killing Floor 2 Magicked Admin you will be presented a
series of prompts that configures a baseline setup. This should be completed
before further configuration.

#. **Language** -- You are presented with an enumerated list of languages that
   are available. Input the number corresponding to the language you wish to
   use or just press Enter to use the default of 'en_GB'. These translations
   are contributed by users, if you wish to contribute translations for your
   language please visit the :doc:`contributing` page.

#. **Address** -- This is the address of your Killing Floor 2 server's web
   admin panel, typically ``localhost:8080``. If you don't have the web admin
   panel enabled you should go back to the `Server Configuration`_ section to
   configure this. If you have more than one server you should just select one
   of them for now, multi-server will be addressed later in this page.

#. **Username** -- The username you use to login to your web admin panel. Just
   press Enter if you want to accept the default of ``Admin``.

    .. note::
        The username you input here will be the username of your chat bot. If
        you want to use a different name for your chat bot visit the
        `Multi-Admin`_ section and use this account here instead.

#. **Password** -- The password for the web admin account you selected above.

    .. note::
        **Windows users** -- Your console session will appear unresponsive
        while you are entering the password. This is normal, input your
        password and press Enter.

#. You should be done now, Killing Floor 2 Magicked Admin will connect to your
   web admin panel and start tracking user statistics and provide commands so
   long as it is running.

Multi-Server
============

