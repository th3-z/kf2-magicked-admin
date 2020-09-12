========
Building
========

sudo apt install python3-pip git

git clone https://github.com/th3-z/kf2-magicked-admin.git

cd kf2-magicked-admin/docs

pip3 install -r requirements.txt

echo "export PATH=\$PATH:\$HOME/.local/bin" >> ~/.bashrc && source ~/.bashrc

make

