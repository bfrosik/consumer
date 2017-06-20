import sys
import realtime.adapter as adapter
import util.utilities as utils
import util.constants as const
from realtime.feed_decorator import FeedDecorator
if sys.version[0] == '2':
    import Queue as queue
else:
    import queue as queue
from multiprocessing import Queue


class Consumer:
    def start_processes(self, config):
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
        dataq = Queue()

        self.feed = FeedDecorator(dataq, decor)
        self.feed.feed_data(no_frames, detector, detector_basic, detector_image, self.logger)

        self.consume(dataq)


    def consume(self, q):
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
        self.logger.info ('starting cons')

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
                    self.logger.info ('type, theta, something, shape: ' + type + str(theta) + str(something) + str(slice.shape))
                elif status == const.DATA_STATUS_END:
                    interrupted = True
                    self.logger.info ('ending analyzer')
                elif status == const.DATA_STATUS_MISSING:
                    self.logger.info ("missing frame")
                else:
                    self.logger.info ("invalid status")
            except queue.Empty:
                pass


if __name__ == "__main__":
    consumer = Consumer()
    consumer.start_processes(sys.argv[1])


