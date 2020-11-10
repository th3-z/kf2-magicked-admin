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

.. _`official wiki`: https://wiki.killingfloor2.com/index.php?title=Dedicated_Server_(Killing_Floor_2)

Killing Floor 2 Magicked Admin utilises Killing Floor2's built-in web admin
panel to track statistics, gameplay events, and chat without a mutator. However
the web admin panel is not enabled by default. This section will cover enabling
the web admin panel.

These instructions are based on the guidance available at the `official wiki`_.

Enabling the Web Admin Panel
----------------------------

Your Killing Floor 2 server's configuration files are located in
``KFGame/Config/`` relative to the server install location, navigate to this
path. The configuration files contain a series of ``[sections]`` followed by
several ``SomeOption=SomeValue``.

#. Open ``KFWeb.ini`` in your favourite text editor.

    - Add ``bEnabled=true`` to the end of the ``[IpDrv.WebServer]`` section.

    - By default the web admin panel will listen on port ``8080`` this can be
      changed here by modifying ``ListenPort=8080`` option in the
      ``[IpDrv.WebServer]`` section.

    - Save and close this file.

#. Open ``PCServer-KFGame.ini`` in your favourite text editor.

    - Modify the ``AdminPassword`` option in the ``[Engine.AccessControl]``,
      this is the password for the web admin panel. Make this something secure,
      for example ``AdminPassword=hunter2``.

    - Save and close this file.

    .. note::
        **Linux users** -- This file is called ``LinuxServer-KFGame.ini`` on
        Linux systems.

#. Restart your Killing Floor 2 server.

#. You should now be able to access the web admin panel in your web browser at
   ``localhost:8080``, or ``127.0.0.1:8080``.

Multi-Admin
-----------

If you want Killing Floor 2 Magicked Admin's in-game chat bot to be named
something other than ``Admin`` you need to create an account for it. Multi
admin has to be manually enabled before you can create more accounts.

#. Open ``KFWebAdmin.ini`` in your favourite text editor.

    - Add ``AuthenticationClass=WebAdmin.MultiWebAdminAuth`` to the end of the
      ``[WebAdmin.WebAdmin]`` section.

    - Save and close this file.

#. Restart your Killing Floor 2 server.

#. Open the web admin panel in your web browser, this is will be at
   ``localhost:8080`` if you are using the default port.

#. Login using the ``Admin`` account and the password configured earlier. The
   web admin panel should now have a new page on the left side titled
   'Administrators', use this area to create new accounts.

    - Click 'Create Administrator', input a username, and click 'OK'.

    - Set the display name to match the username.

    - Set 'Account enabled' to 'Enabled'.

    - Set and password and confirm it.

    - Click 'Save'

#. You can now use this new account with Killing Floor 2 Magicked Admin. Head
   to the `configuration file <#conf-file>`_ section if you want to change
   Killing Floor 2 Magicked Admin's account credentials.

.. note::
    When creating an account for Killing Floor 2 Magicked Admin please don't
    change the access permissions or access order.


Web Admin Patches
-----------------

When your Killing Floor 2 is running the Survival game mode a wave counter is
visible at the top-right of the web admin panel. Killing Floor 2 Magicked Admin
requires this for several features to work however it isn't available in other
game modes by default. Head over to the `installing <installing.html#wap>`__
page to enable this in all game modes, it is important that this is completed
if you plan to use Killing Floor 2 Magicked Admin outside of the Survival game
mode, otherwise this can be skipped.

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
        `Multi-Admin`_ section and use a different account here instead.

#. **Password** -- The password for the web admin account you selected above.

    .. note::
        **Windows users** -- Your console session will appear unresponsive
        while you are entering the password. This is normal, input your
        password and press Enter.

#. You should be done now, Killing Floor 2 Magicked Admin will connect to your
   web admin panel and start tracking user statistics and provide commands so
   long as it is running.

#. If you want to run the interactive setup again delete
   ``conf/magicked_admin.conf``.

.. _`conf-file`:

The Configuration Files
=======================

After the first time setup is completed a folder name ``conf/`` will have been
created. This folder contains all of your configuration and server specific
files.

**magicked_admin.conf** -- This is the main configuration file, it is covered
in more detail in the `magicked_admin.conf` section.

**magicked_admin.log** -- This is a text file containing a log of all activity,
Killing Floor 2 Magicked Admin appends activity to this file as it runs.

**scripts/** -- This folder contains scripts that can be run either on server
initialisation or from the in-game chat. These files are covered in more detail
on the :docs:`scripts` page. Files ending in ``.init`` are ran when the
relevant server is connected to Killing Floor 2 Magicked Admin. Files with no
extension can be ran from the in-game chat with the
``run <commands.html#run>`` command.

**server_one.motd** -- This is a text file containing the message of the day
for ``server_one`` as defined in ``magicked_admin.conf``. This file is covered
in more detail on the :docs:`welcome screen` page.

**storage.sqlite** -- Killing Floor 2 Magicked Admin records all gameplay stats
in this file as they are received. It's a SQLite database. This file might be a
point of interest if you wish to use Killing Floor 2 Magicked Admin's data in
external software.

magicked_admin.conf
-------------------

After the initial setup this file will contain two ``[sections]``. Global
options are under the ``[magicked_admin]`` section. The section for your server
will be named ``[server_one]`` by default. The name of the server is arbitrary
however the files ``conf/scripts/server_one.init`` and ``conf/server_one.motd``
must match the name of the section, and it cannot be ``magicked_admin``. The
server name will appear in the log file and program output.

The **global** section has the following options.

    ``language`` -- Locale code for the selected language. The default is
    ``en_GB``. If you wish to contribute translations for your language head
    over to the :doc:`contributing` page.

The **server** section(s) has the following options.

    ``username`` -- The username Killing Floor 2 Magicked Admin uses to log in
    to the server's web admin panel. This will also be the name shown when
    Killing Floor 2 Magicked Admin interacts with the in-game chat.

    ``password`` -- The login password of the specified account.

    ``address`` -- The URL of the server's web admin panel.

    ``refresh_rate`` -- This is the rate at which Killing Floor 2 Magicked
    Admin polls the server's server info page to retrieve stats, measured in
    seconds. Decimal or integer values are acceptable. The default value is
    ``1``.

    ``game_password`` -- Optional pre-configured game password for use with the
    `password <commands.html#password>`_ command. For example ``TODO``.

    .. note::
        This doesn't add a password to your server, it allows you to set a
        pre-defined game password without having to type the password into
        chat.

    ``url_extras`` -- Optional extra url parameters to be used when switching
    maps. This might be needed if you are using a custom game mode.

Multi-Server
~~~~~~~~~~~~

Killing Floor 2 Magicked Admin can manage multiple servers at once. This
section covers how to add more servers.

#. Open ``conf/magicked_admin.conf`` in your favourite editor.

#. Copy the entire ``[server_one]`` section, including the options below it,
   and paste it at the end of the file.

    .. note::
        If you've renamed the section copy your renamed section instead.

#. Rename the section heading to something unique, for example
   ``[server_two]``.

#. Change the ``username``, ``password``, and ``address`` options to match your
   new server.

#. Restart Killing Floor 2 Magicked Admin.

Linux Background Service
========================

Linux user's have the option of running Killing Floor 2 Magicked Admin as a
background process. The examples are for systemd.

Two example unit files follow, these files need go in ``/etc/systemd/system/``.
If you already have a unit file for Killing Floor 2 you can skip the first
file.

These example services run as the user ``kf2``. Make sure you create this user
and update any relevant file permissions as required
(``sudo chown -R kf2 /srv/killing-floor-2``). The ``ExecStart`` and
``WorkingDirectory`` options will also need to be adjusted to match your
system.

Once installed you will be able to manage your Killing Floor 2 server and
Killing Floor 2 Magicked Admin with ``systemctl``.

Example unit file for Killing Floor 2 (``killing-floor-2.service``).

    ::

        [Unit]
        Description=Killing Floor 2 Server

        [Service]
        ExecStart=/srv/killing-floor-2/kf2-server-start
        WorkingDirectory=/srv/killing-floor-2
        Restart=on-failure
        RestartSec=60s
        Type=simple
        User=kf2
        Group=kf2
        KillSignal=SIGINT

        [Install]
        WantedBy=multi-user.target

Example unit file for Killing Floor 2 Magicked Admin
(``killing-floor-2-magicked-admin.service``).

    ::

        [Unit]
        Description=Killing Floor 2 Magicked Admin

        [Service]
        ExecStart=/srv/killing-floor-2/magicked_admin/magicked_admin -s
        WorkingDirectory=/srv/killing-floor-2/magicked_admin
        Restart=on-failure
        RestartSec=60s
        Type=simple
        User=kf2
        Group=kf2
        KillSignal=SIGINT

        [Install]
        WantedBy=multi-user.target

.. note::
    The ``-s`` flag in the ``ExecStart`` line disables interactive setup. When
    this is set a template config file will be created on initial run. You will
    then need to configure your server(s) with a text editor and restart the
    service.