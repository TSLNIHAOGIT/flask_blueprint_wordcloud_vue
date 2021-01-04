# configuration file
# -*- coding:utf8 -*-

#url_prefix
URL_PREFIX = '/api/ai/dtf'
# url_prefix = 'api/ai/dtf'


# db config
MYSQL_IP = 'mysql.dev.amiintellect.com'
MYSQL_USER = 'amidba'
MYSQL_PASS = 'ami#42aa3B11'
MYSQL_DB = 'chinaport_chongqing'
SQLALCHEMY_DATABASE_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASS + '@' \
                          + MYSQL_IP + '/' + MYSQL_DB

# host IP port
# APP_HOST = 'localhost'
APP_PORT = 18401


