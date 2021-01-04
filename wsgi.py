# encoding : utf-8
from flask_cors import *
from flask import Flask
from flask import render_template

import sys,os
#将项目根目录加入到运行环境
root_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'.'))
sys.path.insert(0,root_path)

from app_logging import logger_path as logger

from app.wordcloud_example import  wordcloud as predict_score_blueprint


import warnings
warnings.filterwarnings('ignore')


# app = Flask(__name__, static_url_path='')

app = Flask(__name__,
            template_folder="dist",
            static_folder="dist/static")



# load config from config.py
app.config.from_pyfile(os.path.join(root_path,'config.py'))

# url_prefix=app.config.get('URL_PREFIX', '/api/ai/dtf')


CORS(app, supports_credentials=True)
# CORS(app, resources=r'/*')


# @app.route('/')
# def index():
#     return "APIs Server"

# 主页面
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


app.register_blueprint(predict_score_blueprint)#, url_prefix=url_prefix)


if __name__ == '__main__':
    # print('url_prefix',app.config.get('URL_PREFIX'),app.config)

    host = app.config.get('APP_HOST', '0.0.0.0')
    port = app.config.get('APP_PORT', '28095')
    logger.info('host:{},port:{}'.format(host,port))

    # from werkzeug.contrib.fixers import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)

    # app.run(host=host, port=port, threaded=True, debug=True)
    app.run(host=host, debug=False, port=port)
