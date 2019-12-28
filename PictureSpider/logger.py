import logging

fmt = "%(asctime)s %(levelname)s %(filename)s:%(lineno)d" \
          " pid-%(process)d %(message)s"
date_fmt = "%Y-%m-%d %H:%M:%S"

def set_logger(logger_name,level):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    log_fh = logging.StreamHandler()
    log_fh.setFormatter(fmt)
    logger.handlers = [log_fh]
