# nuricame-pi

Turtle makes a contour by pictures, Raspberry Pi version.

- [How to Setup](#how-to-setup)
  - [LiPo SHIM](#lipo-shim)
  - [Camera](#camera)
  - [I2C Display](#i2c-display)
  - [Thermal Printer](#thermal-printer)
  - [Enclosure](#enclosure)
- [Misc](#misc)
  - [LICENSE](#license)

## How to Setup

### LiPo SHIM

![RPi+LiPoSHIM](https://user-images.githubusercontent.com/32637762/75518641-c190f500-5a44-11ea-8736-6ecb60e01e31.jpg)

To use LiPo battery, implement [Pimoroni LiPo SHIM](https://shop.pimoroni.com/products/lipo-shim) to Raspberry Pi.

`VBAT+` and `GND` are used for charging.
`EN` can be pulled to ground to cut the power output from LiPo SHIM.

```sh
chmod +x setup_LiPoSHIM.sh
./setup_LiPoSHIM.sh
```

Config: `/etc/cleanshutd.conf`

### Camera

![IMG_2124](https://user-images.githubusercontent.com/32637762/75620129-114bf980-5bc8-11ea-9ea2-bf4a6d332509.jpg)

[Arducam 5MP OV5647](https://www.arducam.com/product/5mp-ov5647-motorized-focus-camera-sensor-raspberry-pi/) is Motorized Focus Camera Sensor for Raspberry Pi.

Append the following line to `/boot/config.txt`.

```txt
dtparam=i2c_vc=on
```

```sh
sudo apt install python3-opencv
pip3 install pygame
sudo reboot
```

### I2C Display

![IMG_2123](https://user-images.githubusercontent.com/32637762/75620123-fc6f6600-5bc7-11ea-8c64-a6be5f6e3077.jpg)

[Waveshare 1.3inch LCD HAT](https://www.waveshare.com/1.3inch-lcd-hat.htm) is 240x240 diagonal display with 1 joystick and 3 buttons via SPI interface.

```sh
sudo apt install wiringpi
```

```sh
wget -O - http://www.airspayce.com/mikem/bcm2835/bcm2835-1.62.tar.gz | tar zxvf -
cd bcm2835-1.62
./configure
make
sudo make check
sudo make install
```

Add the following 2 lines to `/etc/modules`.

```txt
i2c-bcm2708
i2c-dev
```

`sudo raspi-config` to enable `I2C` and `SPI`.

### Thermal Printer

We use [Paperang](https://www.paperang.com/).

```sh
sudo apt install python3-bluez
```

```python
import bluetooth

nearby = bluetooth.discover_devices(lookup_names=True)
for addr, name in nearby:
    print(f"{addr} -> {name}")
```

Find `Paperang`'s Bluetooth MAC address, like `00-15-82-90-1E-10`.

Thanks, [BroncoTc/python-paperang](https://github.com/BroncoTc/python-paperang).

### Enclosure

![case](https://user-images.githubusercontent.com/32637762/75654865-f9e23e80-5ca3-11ea-9939-00b3bb930a9f.jpg)

## Misc

### LICENSE

See [LICENSE.md](LICENSE.md).
