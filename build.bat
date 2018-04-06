cd magicked_admin
python -m pip install cx_freeze requests lxml configparser colorama termcolor re
python setup.py build -b ../bin
cd ..
pause