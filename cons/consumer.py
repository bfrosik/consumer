import sys
import realtime.adapter as adapter
import util.utilities as utils
from realtime.feed_decorator import FeedDecorator

"""
This module is a suite of utility functions.
"""

import tifffile as tf
import numpy as np
import os
import logging
import stat
from functools import reduce

__author__ = "Barbara Frosik"
__copyright__ = "Copyright (c), UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['Consumer']

class Consumer:
    def start_consumer(self, config):
        """
        This function starts analyzer process and feed.

        Parameters
        ----------
        conf : str
            configuration file name, including path

        Returns
        -------
        none

        """
        conf = utils.get_config(config)
        if conf is None:
            print ('configuration file is missing')
            exit(-1)

        self.logger = utils.get_logger(__name__, conf)

        no_frames, detector, detector_basic, detector_image = adapter.parse_config(config)
        theta = 'BBF1:cam1:AcquirePeriod'
        something = 'BBF1:cam1:AcquireTime'

        decor = {'theta':theta, 'something':something}

        self.feed = FeedDecorator(decor)
        self.feed.feed_data(no_frames, detector, detector_basic, detector_image, self.logger)


if __name__ == "__main__":
    consumer = Consumer()
    consumer.start_consumer(sys.argv[1])


