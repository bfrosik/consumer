"""
This module starts consumer.
"""

import sys
import util.constants as const
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue

__author__ = "Barbara Frosik"
__copyright__ = "Copyright (c), UChicago Argonne, LLC."
__docformat__ = 'restructuredtext en'
__all__ = ['consume']

def consume(q, logger):
    """
    This function consumes the data.

    Parameters
    ----------
    q : Queue
        an Queue object on which data is delivered

    Returns
    -------
    none

    """
    logger.info ('starting cons')

    interrupted = False
    while not interrupted:
        try:
            data = q.get()
            status = data.status
            if status == const.DATA_STATUS_DATA:
                type = data.type
                slice = data.slice
                theta = data.theta
                something = data.something
                logger.info ('type, theta, something, shape: ' + type + str(theta) + str(something) + str(slice.shape))
            elif status == const.DATA_STATUS_END:
                interrupted = True
                logger.info ('ending analyzer')
            elif status == const.DATA_STATUS_MISSING:
                logger.info ("missing frame")
            else:
                logger.info ("invalid status")
        except queue.Empty:
            pass



