import hardware
import image_data
import skimage as ski
import skimage.io


class Paperang_Printer:
    def __init__(self):
        self.printer_hardware = hardware.Paperang('00:15:83:55:5C:48')

    def print_image_file(self, path):
        if self.printer_hardware.connected:
            # self.printer_hardware.sendSelfTestToBt()
            self.printer_hardware.sendImageToBt(image_data.binimage2bitstream(
                image_data.im2binimage(ski.io.imread(path), conversion="threshold")))

    def print_dithered_image(self, path):
        if self.printer_hardware.connected:
            self.printer_hardware.sendImageToBt(image_data.im2binimage2(path))


if __name__ == "__main__":
    mmj = Paperang_Printer()
    mmj.print_dithered_image("../original.jpg")
