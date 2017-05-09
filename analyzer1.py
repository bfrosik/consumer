import os
import sys
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue
import logging


def consume(q, status_def, args):
    # status_def = [DATA_STATUS_DATA, DATA_STATUS_MISSING, DATA_STATUS_END]
    DATA_STATUS_DATA = status_def[0]
    DATA_STATUS_MISSING = status_def[1]
    DATA_STATUS_END = status_def[2]

    logging.basicConfig(filename='/local/temp/consumer/example.log',level=logging.INFO)
    logging.info ('starting cons')

    interrupted = False
    while not interrupted:
        try:
            data = q.get()
            status = data.status
            if status == DATA_STATUS_DATA:
                index = data.index
                slice = data.slice
                logging.info ('index, failed, shape: ' + str(index) + str(data.failed) + str(slice.shape))
            elif status == DATA_STATUS_END:                
                interrupted = True
                logging.info ('ending analyzer1') 
            elif status == DATA_STATUS_MISSING:
                logging.info ("missing frame")
            else:
                logging.info ("invalid status")
        except queue.Empty:
            pass

