#!/usr/bash

set -eux

sudo apt update

echo -n "Install packages via apt? [Y/n]: "
read ANS1

case $ANS1 in
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

echo -n "Rewrite /boot/config.txt ? [Y/n]: "
read ANS2

case $ANS2 in
  "" | [Yy]* )
    echo "Sure."
    sudo sed -i -e 's|\(^dtparam=i2c_vc\).*$|#&\n\1=on|' /boot/config.txt
    ;;
  * )
    echo "Alright, read README.md to rewrite /boot/config.txt."
    ;;
esac

echo -n "Rewrite /etc/modules ? [Y/n]: "
read ANS3

case $ANS3 in
  "" | [Yy]* )
    echo "Sure."
    echo "i2c-dev" >> /etc/modules
    echo "i2c-bcm2708" >> /etc/modules
    ;;
    echo "Alright, read README.md to rewrite /etc/modules."
    ;;
esac

echo -n "Install BCM driver? [Y/n]: "
read ANS4

case $ANS4 in
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

echo "Done."
