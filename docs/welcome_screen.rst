.. role:: underline
    :class: underline

==============
Welcome Screen
==============

This page cover's Killing Floor 2 Magicked Admin's dynamic welcome screen
features.

The MOTD File
=============

The welcome screen is configured in the ``conf/<server_name>.motd`` file. Upon
the initial run the contents of this file will default to your existing MOTD.

.. note::
    The welcome screen has a maximum length of 10 lines.

Text Formatting Options
-----------------------

Killing Floor 2's message of the day has some support for adding tags to your
message of the day that allow you to change the appearance of sections of text.

These tags are of the form ``<tag attribute="value">formatted text</tag>``. The
available tags are as follows.

.. _`this`: https://duckduckgo.com/?q=color+picker&ia=answer

**<font>** -- This can be used to change the size and color of text. This tag has
two attributes: ``size``, and ``color``. The size attribute is measured in
points and the color is in hexadecimal. You may use `this`_ link to generate
hexadecimal color codes.

    ::

        <font size="24">This sentence is in size 24pt.</font>
        <font color="#00ff00">This sentence is green.</font>
        <font size="32" color="#0000ff">This sentence is blue and in size 32pt.</font>

**<b>** -- Makes text **bold**.

    ::

        <b>This sentence will be bold.</b>

**<i>** -- Makes text *italic*.

    ::

        <i>This sentence will be italic.</i>

**<u>** -- Makes text :underline:`underlined`.

    ::

        <u>This sentence will be underlined.</u>


Updating the MOTD
=================

The welcome screen is updated by the ``update_motd`` command. After the initial
configuration you will have a command that regularly updates your welcome
screen automatically added to your server's ``.init`` file. It looks like as
follows.

    ::
        ; Update the motd every 1 minute
        on_time add -n 60 -r update_motd





.. note::
    While the welcome screen can be updated as often as you'd like it will not
    be presented in-game until the next match.
