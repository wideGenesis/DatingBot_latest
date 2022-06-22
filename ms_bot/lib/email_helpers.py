import config.conf as conf
import asyncio
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from setup.logger import CustomLogger
from ms_bot.lib.messages import MAILS_MAPPING
from email.mime.base import MIMEBase
from email import encoders
logger = CustomLogger.get_logger('bot')


async def send_mail(message_data: dict, attach=None):
    try:
        message = MIMEMultipart('alternative')
        message['From'] = conf.MAIL_FROM
        message['To'] = message_data['recipients'][0]
        message['Subject'] = message_data['subject']
        plain_text_message = MIMEText(message_data['body'], 'plain', 'utf-8')
        html_message = MIMEText(message_data['html'], 'html', 'utf-8')
        message.attach(plain_text_message)
        message.attach(html_message)
        if attach:
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open("current_statuses.xls", "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="current_statuses.xls"')
            message.attach(part)

        asyncio.create_task(aiosmtplib.send(
            message,
            recipients=message_data['recipients'],
            hostname=conf.MAIL_SERVER,
            port=conf.MAIL_PORT,
            username=conf.MAIL_USER,
            password=conf.MAIL_PASSWORD,
            # start_tls=True,
            timeout=10,
        ))

    except Exception:
        logger.exception('Mail message sent to %s has been failed', message_data['recipients'])
        raise

    logger.info('Email message has been sent to %s ', message_data['recipients'])


def build_email_message(
        recipients: list,
        message=None,
        message_type=None
) -> dict:
    mail_data = MAILS_MAPPING[message_type]

    return dict(
        email_from=configuration.MAIL_FROM,
        recipients=recipients,
        subject=mail_data['subject'],
        body=mail_data['text'].format(message),
        html=mail_data['text'].format(message),
    )


