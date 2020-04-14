# Development environment for Debian distributions

### Virtual Machine
```
Hypervisor: Dropbox
SSOO: Debian 10.3
```

### Install operating system utilities and develop tools 
```
apt update
apt upgrade
apt install vim terminator python3-pip
apt install git sqlitebrowser
```

### Install Pycharm IDE
```
Download pycharm-*.tar.gz
tar xfz pycharm-*.tar.gz -C /opt/
cd /opt/pycharm-*/bin
sh pycharm.sh
```
For icon desktop, create a new desktop file: /usr/share/applications/pycharm.desktop with the following: 
```
[Desktop Entry]
Name=Pycharm-community
Comment=Pycharm-community
Exec=/opt/pycharm-community-2019.3.4/bin/pycharm.sh
Icon=/opt/pycharm-community-2019.3.4/bin/pycharm.png
Terminal=false
Type=Application
```

### Install LATEX
```
apt install Texlive-full
apt install Texmaker
```

### Install other useful tools
REST: Insomnia
```
echo "deb https://dl.bintray.com/getinsomnia/Insomnia /" \
    | sudo tee -a /etc/apt/sources.list.d/insomnia.list
wget --quiet -O - https://insomnia.rest/keys/debian-public.key.asc \
    | sudo apt-key add -
sudo apt-get update
sudo apt-get install insomnia
```
