import os
import sys
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue
import logging


def consume(q, end_proc, args):
    logging.basicConfig(filename='/local/temp/consumer/example.log',level=logging.INFO)
    logging.info ('starting cons')

    interrupted = False
    while not interrupted:
        try:
            data = q.get()
            status = data.status
            if status == end_proc:
                interrupted = True
                logging.info ('ending analyzer1')
            else:
                if status == 0:
                    index = data.index
                    slice = data.slice
                    logging.info ('index, failed, shape: ' + str(index) + str(data.failed) + str(slice.shape))
                else:
                    logging.info ("missing frame")
        except queue.Empty:
            pass

