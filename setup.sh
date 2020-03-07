#!/usr/bash

set -eux

sudo apt update

echo -n "Install packages via apt? [Y/n]: "
read ANS_APT

case $ANS_APT in
  "" | [Yy]* )
    echo "Sure."
    sudo apt install -y python3-opencv
    sudo apt install -y python3-pygame
    sudo apt install -y wiringpi
    sudo apt install -y python3-bluez
    sudo apt install -y libatlas-base-dev
    sudo apt install -y libjasper-dev
    sudo apt install -y libqtgui4
    sudo apt install -y libqt4-test
    sudo apt install -y python3-pyqt5
    sudo apt install -y python3-skimage
    ;;
  * )
    echo "Alright, read README.md to install each packages."
    ;;
esac

echo -n "Rewrite /etc/modules ? [Y/n]: "
read ANS_MODULES

case $ANS_MODULES in
  "" | [Yy]* )
    echo "Sure."
    echo "i2c-dev" >> /etc/modules
    echo "i2c-bcm2708" >> /etc/modules
    ;;
    echo "Alright, read README.md to rewrite /etc/modules."
    ;;
esac

echo -n "Install BCM driver? [Y/n]: "
read ANS_BCM

case $ANS_BCM in
  "" | [Yy]* )
    echo "Sure."
    wget -O - http://www.airspayce.com/mikem/bcm2835/bcm2835-1.62.tar.gz | tar zxvf -
    cd bcm2835-1.62
    ./configure
    make
    sudo make check
    sudo make install
    ;;
  * )
    echo "Alright, read README.md to install BCM driver."
    ;;
esac

echo -n "Run setup_LiPoSHIM.sh? [Y/n]: "
read ANS_LIPOSHIM

case $ANS_LIPOSHIM in
  "" | [Yy]* )
    echo "Sure."
    chmod +x setup_LiPoSHIM.sh
    ./setup_LiPoSHIM.sh
    ;;
  * )
    echo "Alright, read README.md to run setup_LiPoSHIM.sh."
    ;;
esac

echo "Done."
