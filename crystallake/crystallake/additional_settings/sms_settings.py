from os import environ, path
from datetime import timedelta


SMS_CODE_SALT = environ.get('SMS_SALT', 'default_sms_salt')
CODES_FILE = f'{path.abspath(path.dirname(__name__))}/sms_codes.txt'
CODE_ACTIVE_TIME = timedelta(minutes=5)


