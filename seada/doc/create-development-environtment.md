### Virtual Machine
```
Hypervisor: Dropbox
SSOO: Debian 10.3
```

### Install SSOO utilities
```
apt install Terminator/stable
apt install Python3-pip
apt install vim
```

### Install develop tools
```
apt install Git
apt install sqlitebrowser
apt install Pycharm-community-2019.3.2
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
