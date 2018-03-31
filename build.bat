cd magicked_admin
python -m pip install cx_freeze requests lxml configparser colorama termcolor
python setup.py build -b ../bin
cd ..
pause