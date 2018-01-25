from datetime import datetime
from picamera import PiCamera

from nio.block.base import Block
from nio.properties import VersionProperty, FileProperty 


class Picamera(Block):

    version = VersionProperty('0.1.0')
    image = FileProperty(title='Image', default='image')
    count = 0

    def configure(self, context):
    	super().configure(context)
    	self.camera = PiCamera()

    def process_signals(self, signals):
        for signal in signals:
            image_name = '{}_{}'.format(self.image, self.count)
            self.camera.capture('{}.jpg'.format(image_name))
            self.count += 1
        self.notify_signals(signals)
