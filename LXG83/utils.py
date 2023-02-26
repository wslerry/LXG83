# -*- coding: utf-8 -*-
import os
import sys
from datetime import timedelta, datetime
import logging
import logging.handlers

sys.path.append(r"C:\Program Files (x86)\ArcGIS\Bin")

import arcgisscripting
#import ConversionUtils

gp = arcgisscripting.create()
gp93 = arcgisscripting.create(9.3)


class LXGLogging(logging.handlers.RotatingFileHandler):
    def emitlog(self, record):
        """
        Write the log message
        """
        try:
            msg = record.msg.format(record.args)
        except:
            msg = record.msg

        if record.levelno >= logging.ERROR:
            gp.AddError(msg)
        elif record.levelno >= logging.WARNING:
            gp.AddWarning(msg)
        elif record.levelno >= logging.INFO:
            gp.AddMessage(msg)

        super(LXGLogging, self).emitlog(record)


class MigrationLog:
    def __init__(self, log_directory):
        self.dir = log_directory

        if os.path.isdir(self.dir):
            pass
        else:
            os.mkdir(self.dir)
        now = datetime.today().strftime("%Y%m%d%H%M%S")

        self.file = os.path.join(self.dir, "sde2gdb_%s.log" % now)

    def __repr__(self):
        logger = logging.getLogger("MIGRATION")
        handler = LXGLogging(
            self.file,
            maxBytes=1024 * 1024 * 2,
            backupCount=10
        )
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        return logger


class ReplicationLog:
    def __init__(self, log_directory):
        self.dir = log_directory

        if os.path.isdir(self.dir):
            pass
        else:
            os.mkdir(self.dir)

        now = datetime.today().strftime("%Y%m%d%H%M%S")

        self.file = os.path.join(self.dir, "gdb2sde_%s.log" % now)

    def __repr__(self):
        logger = logging.getLogger("REPLICATION")
        handler = LXGLogging(
            self.file,
            maxBytes=1024 * 1024 * 2,
            backupCount=10
        )
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        return logger


def progressbar(iterable, prefix='', suffix='', length=100, fill='#'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        if iteration != 0:
            iter_per_total = iteration / float(total)
        else:
            iter_per_total = 0
        decimals = round(100 * iter_per_total, 2)
        percent = str(decimals)
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '.' * (length - filledLength)

        print '\r%s |%s| %s%% %s ' % (prefix, bar, percent, suffix),

    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print


def processtime(seconds):
    conversion = timedelta(seconds=seconds)
    converted_time = str(conversion)

    return converted_time
