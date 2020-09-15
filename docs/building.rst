========
Building
========

This page covers the process of building Killing Floor 2 Magicked Admin from
source for Windows and Linux platforms.

    .. note::
        Pre-built executables are available for Windows and Linux on the
        :doc:`installing` page. The downloads already contain the built
        executable, you can skip to the :doc:`configuration` page if you're
        using these.

Windows
=======

.. _Python: https://www.python.org/

.. _`source code`: https://github.com/th3-z/kf2-magicked-admin/archive/master.zip

#. Download Killing Floor 2 Magicked Admin's `source code`_.

#. Extract the source code zip anywhere on your computer.

#. Download a Python_ installer for Windows of version ``3.8`` or higher.

#. Run the Python installer and when prompted check the following options
   before clicking "Install Now".

    - "Add Python 3.8 to PATH"

    - "Install for all users (recommended)"

#. Shift + Right-Click in the source code folder from step two and click
   "Open PowerShell window here".

#. Use the following command to install the Python requirements from PowerShell.

    ::

        pip install -r .\requirements.txt

#. The following command builds Killing Floor 2 Magicked Admin for Windows.

    ::

        python .\magicked_admin\setup.py build -b bin/magicked_admin

#. The following command builds the web admin patcher for Windows.

    ::

        python .\admin_patches\setup.py build -b bin/admin_patches

#. All done, the output binaries can be found to the ``bin/`` folder.


Linux
=====

The build instructions for Linux are tested on Ubuntu Focal but should work for
most distros with minor changes.

#. Install the required system packages.

    ::

        sudo apt install make git python3-pip python3-tk

#. Download the source code with git

    ::

        git clone https://github.com/th3-z/kf2-magicked-admin.git

#. Cd into the source folder

    ::

        cd kf2-magicked-admin

#. Install the Python requirements

    ::

        pip3 install -r requirements.txt

#. Add ``~/.local/bin`` to your ``PATH`` if it isn't already.

    ::

        echo "export PATH=\$PATH:\$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc

#. Run make to build both Killing Floor 2 Magicked Admin and the web admin
   patcher

    ::

        make

#. The build is complete, the Linux binaries are output in the ``bin/`` folder.

Documentation
=============

The documentation can only be built on unix-like systems. These instructions
are for Ubuntu Focal but should be similar for most other distros.

#. Install pip and git if you haven't got them already installed.

    ::

        sudo apt install python3-pip git

#. Download Killing Floor 2 Magicked Admin's source code.

    ::

        git clone https://github.com/th3-z/kf2-magicked-admin.git

#. Cd into the ``docs`` folder.

    ::

        cd kf2-magicked-admin/docs

#. Install the documentation's Python requirements

    ::

        pip3 install -r requirements.txt

#. Add ``~/.local/bin`` to your ``PATH`` if it isn't already.

    ::

        echo "export PATH=\$PATH:\$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc

#. Build the HTML documentation with make.

    ::

        make

#. The HTML pages will be output in the ``_build`` folder.

PDF Documentation
-----------------

Further to the above if you want to build the PDF documentation there are some
additional requirements.

#. Install the system requirements.

    ::

        sudo apt install texlive-latex-recommended texlive-fonts-recommended texlive-latex-extra latexmk

#. Build the PDF documentation.

    ::

        make pdf

#. All done, a PDF file will be output in the ``_build`` folder.