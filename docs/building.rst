========
Building
========

This page covers the process of building Killing Floor 2 Magicked Admin from
source.

    .. note::
        Pre-built executables are available for Windows and Linux on the
        :doc:`installing` page. The downloads already contain the built
        executable so you can skip to the :doc:`configuration` page.

The build instructions assume a unix-like environment. If you are compiling on
a Windows platform you will need to set up Cygwin or WSL before continuing.

Windows
=======

1. download source code zip: https://github.com/th3-z/kf2-magicked-admin/archive/master.zip

1.1. extract source code to desktop

2. download python >=3.6: https://www.python.org/

3. Run the Python installer

3.1. tick "Add Python 3.8 to PATH" and "Install for all users (recommended)"

3.2. click "Install Now"

4. Shift + Right Click in kf2-ma source folder

4.1. click "Open PowerShell window here"

4.2. enter command: "pip install -r .\requirements.txt" and press enter


4.3. enter command: "pybabel compile -d locale -D "magicked_admin" and press enter

4.4. enter command: "pybabel compile -d locale -D "admin_patches" and press enter


4.5. enter command "python .\magicked_admin\setup.py build -b bin/magicked_admin" and press enter

4.6. enter command "python .\admin_patches\setup.py build -b bin/admin_patches" and press enter


Linux
=====

Documentation
=============

sudo apt install python3-pip git

git clone https://github.com/th3-z/kf2-magicked-admin.git

cd kf2-magicked-admin/docs

pip3 install -r requirements.txt

echo "export PATH=\$PATH:\$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc

make

