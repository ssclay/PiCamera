import sys
from unittest.mock import patch, MagicMock, Mock

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase


class TestPicamera(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        sys.modules['picamera'] = MagicMock()
        sys.modules['PiCamera'] = MagicMock()
        from ..PiCamera_block import Picamera
        global Picamera

    def test_capture(self):
        blk = Picamera()
        self.configure_block(blk, {'name': 'pic',
                                   'file_type': 'PNG',
                                   'preview': False})
        blk.start()
        blk.process_signals([Signal({"hi": "there"})])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hi": "there"})
        blk.camera.capture.assert_called_with('pic_0.png', format='png')
        blk.camera.close.assert_called()
        
    def test_preview(self):
        blk = Picamera()
        self.configure_block(blk, {'name': 'namen',
                                   'file_type': 'JPEG',
                                   'preview': True})
        blk.start()
        blk.process_signals([Signal({"hi": "there"})])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hi": "there"})
        blk.camera.capture.assert_called_with('namen_0.jpeg', format='jpeg')
        blk.camera.start_preview.assert_called()
        blk.camera.stop_preview.assert_called()
