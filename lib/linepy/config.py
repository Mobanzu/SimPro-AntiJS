# -*- coding: utf-8 -*-
from akad.ttypes import ApplicationType
import re

class Config(object):
    LINE_HOST_DOMAIN                 = 'https://ga.line.naver.jp'
    LINE_OBS_DOMAIN                    = 'https://obs-sg.line-apps.com'
    LINE_TIMELINE_API                   = 'https://ga.line.naver.jp/mh/api'
    LINE_TIMELINE_MH                   = 'https://ga.line.naver.jp/mh'
    LINE_OBJECT_URL                      = 'https://obs.line-scdn.net/'
    LINE_LOGIN_QUERY_PATH       = '/api/v4p/rs'
    LINE_AUTH_QUERY_PATH        = '/api/v4/TalkService.do'
    LINE_API_QUERY_PATH_FIR     = '/S4'
    LINE_POLL_QUERY_PATH_FIR = '/P4'
    LINE_CALL_QUERY_PATH         = '/V4'
    LINE_CERTIFICATE_PATH         = '/Q'
    LINE_CHAN_QUERY_PATH       = '/CH4'
    LINE_SQUARE_QUERY_PATH   = '/SQS1'
    LINE_SHOP_QUERY_PATH        = '/SHOP4'
    LINE_LIFF_QUERY_PATH           = '/LIFF1'

    CHANNEL_ID = {
        'LINE_TIMELINE': '1341209850',
        'LINE_WEBTOON': '1401600689',
        'LINE_TODAY': '1518712866',
        'LINE_STORE': '1376922440',
        'LINE_MUSIC': '1381425814',
        'LINE_SERVICES': '1459630796'
    }

    APP_VERSION = {
        'IOS': '10.1.1',
        'IOSIPAD': '10.10.0',
        'ANDROID': '10.1.1',
        'ANDROIDLITE': '2.14.0',
        'DESKTOPWIN': '6.0.3',
        'DESKTOPMAC': '6.0.3',
        'CHROMEOS': '2.3.8',
        'DEFAULT': '10.1.1'
    }

    SYSTEM_VERSION = {
        'IOS': '14.2',
        'IOSIPAD': '11.2.5',
        'ANDROID': '14.2',
        'ANDROIDLITE': '5.1.1',
        'DESKTOPWIN': '10',
        'DESKTOPMAC': '10.15',
        'CHROMEOS': '1',
        'DEFAULT': '10.0'
    }

    APP_TYPE            = 'DESKTOPWIN'
    APP_VER              = APP_VERSION[APP_TYPE] if APP_TYPE in APP_VERSION else APP_VERSION['DEFAULT']
    CARRIER               = '51089, 1-0'
    SYSTEM_NAME = 'HELLTERHEAD'
    SYSTEM_VER     = SYSTEM_VERSION[APP_TYPE] if APP_TYPE in SYSTEM_VERSION else SYSTEM_VERSION['DEFAULT']
    IP_ADDR               = '8.8.8.8'
    EMAIL_REGEX    = re.compile(r"[^@]+@[^@]+\.[^@]+")
    URL_REGEX         = re.compile(r'^(?:http|ftp)s?://' r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' r'localhost|' r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' r'(?::\d+)?' r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    MID_REGEX         = re.compile(r'u\w{32}')
    GID_REGEX          = re.compile(r'c\w{32}')
    RID_REGEX           = re.compile(r'r\w{32}')
    ALLIDS_REGEX    = re.compile(r'(?:u\w{32}|c\w{32}|r\w{32})')

    def __init__(self, appType=None):
        if appType:
            self.APP_TYPE = appType
            self.APP_VER = self.APP_VERSION[self.APP_TYPE] if self.APP_TYPE in self.APP_VERSION else self.APP_VERSION['DEFAULT']
        self.APP_NAME = '%s\t%s\t%s\t%s' % (self.APP_TYPE, self.APP_VER, self.SYSTEM_NAME, self.SYSTEM_VER)
        self.USER_AGENT = 'Line/%s' % self.APP_VER