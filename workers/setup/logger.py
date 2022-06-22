import logging
import os
import email.utils
import smtplib

from logging.handlers import RotatingFileHandler, SMTPHandler
from configuration import LOG_TO, LOGGER_LEVEL, IS_LOCAL_ENV
from email.message import EmailMessage


DEBUG_LOG_FILE = None


class BColors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    BLUE = '\033[34m'
    CYAN = '\033[36m'
    LIGHT_GREEN = '\033[92m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREY = '\033[37m'

    def disable(self):
        self.RED = ''
        self.GREEN = ''
        self.YELLOW = ''
        self.BLUE = ''
        self.CYAN = ''
        self.LIGHT_GREEN = ''
        self.LIGHT_RED = ''
        self.LIGHT_GREY = ''


class ColorHandler(logging.StreamHandler):
    COLORS = {
        logging.DEBUG: BColors.CYAN,
        logging.INFO: BColors.LIGHT_GREY,
        logging.WARNING: BColors.YELLOW,
        logging.ERROR: BColors.LIGHT_RED,
        logging.CRITICAL: BColors.RED
    }

    def emit(self, record: logging.LogRecord) -> None:
        color = self.COLORS.get(record.levelno, '')
        self.stream.write(color + self.format(record) + '\n')


class SSLSMTPHandler(SMTPHandler):

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP_SSL(self.mailhost, port)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                smtp.login(self.username, self.password)
            smtp.send_message(msg, self.fromaddr, self.toaddrs)
            smtp.quit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class CustomLogger:
    if IS_LOCAL_ENV == 1:
        LOG_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(__name__)), 'logs', 'debug_logs.log')
    else:
        LOG_FILE_PATH = os.path.join('/home/site/wwwroot/logs/', 'debug_logs.log')
    logger = None

    @classmethod
    def get_logger(cls, service_name='django'):
        if cls.logger is not None:
            return cls.logger

        stdout_handler = ColorHandler()
        formatter = logging.Formatter(
            '%(asctime)s - [%(levelname)-3s] - FILE: %(module)-3s - FUNC: %('
            'funcName)-3s - [LINE: %(lineno)-3s] >>> %(message)s '
        )

        cls.logger = logging.getLogger(service_name)
        if not cls.logger.hasHandlers():
            if LOG_TO == 1:
                file_handler = RotatingFileHandler(cls.LOG_FILE_PATH, maxBytes=50000, backupCount=20)
                cls.logger.addHandler(file_handler)
                file_handler.setFormatter(formatter)
                cls.logger.addHandler(stdout_handler)
                stdout_handler.setFormatter(formatter)
            elif LOG_TO == 2:
                # smtpHandler = SSLSMTPHandler(
                #     mailhost=('smtp.gmail.com', 465),
                #     fromaddr=os.environ.get("MAIL_USER"),
                #     toaddrs=[os.environ.get("MAIL_USER")],
                #     subject='Alert! Logger Exception has been registered!',
                #     credentials=(f'{os.environ.get("MAIL_USER")}', f'{os.environ.get("MAIL_PASSWORD")}')
                # )
                smtpHandler = logging.handlers.SMTPHandler(
                    mailhost=('smtp.gmail.com', 587),
                    fromaddr=os.environ.get("MAIL_USER"),
                    toaddrs=[os.environ.get("MAIL_USER")],
                    subject='Alert! Logger Exception has been registered!',
                    credentials=(f'{os.environ.get("MAIL_USER")}', f'{os.environ.get("MAIL_PASSWORD")}'),
                    secure=()
                )

                cls.logger.addHandler(smtpHandler)
                smtpHandler.setFormatter(formatter)
                smtpHandler.setLevel(logging.ERROR)

                cls.logger.addHandler(stdout_handler)
                stdout_handler.setFormatter(formatter)
            else:
                cls.logger.addHandler(stdout_handler)
                stdout_handler.setFormatter(formatter)
            cls.logger.setLevel(LOGGER_LEVEL)
            return cls.logger
        else:
            cls.logger.removeHandler(stdout_handler)
