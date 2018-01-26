from time import sleep
from enum import Enum
from picamera import PiCamera

from nio.block.base import Block
from nio.properties import VersionProperty, StringProperty, BoolProperty, SelectProperty


class Filetypes(Enum):
    JPEG = 'jpeg'
    PNG = 'png'
    GIF = 'gif'
    BMP = 'bmp'
    YUV = 'yuv'
    RGB = 'rgb'
    RGBA = 'rgba'
    BGR = 'bgr'
    BGRA = 'bgra'
    RAW = 'raw'

class Picamera(Block):

    version = VersionProperty('0.1.0')
    name = StringProperty(title='Image Name')
    file_type = SelectProperty(Filetypes, title='file_type',
                               default=Filetypes.JPEG)
    preview = BoolProperty(title='Open Preview Window', default=False)
    count = 0

    def configure(self, context):
        super().configure(context)
        self.camera = PiCamera()
        if self.preview:
            self.camera.start_preview()
        sleep(2)

    def process_signals(self, signals):
        for signal in signals:
            image_name = '{}_{}.{}'.format(self.name(), self.count, self.file_type().value)
            self.camera.capture('{}'.format(image_name), format=self.file_type().value)
            self.count += 1
        self.notify_signals(signals)

    def stop(self):
        if self.preview:
            self.camera.stop_preview()
        self.camera.close()
        super().stop()
