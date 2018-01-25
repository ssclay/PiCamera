from picamera import PiCamera

from nio.block.base import Block
from nio.properties import VersionProperty


class Picamera(Block):

    version = VersionProperty('0.1.0')

    def configure(self, context):
    	super().configure(context)
    	self.camera = PiCamera()

    def process_signals(self, signals):
        for signal in signals:
            self.camera.capture('image.jpg')
        self.notify_signals(signals)
