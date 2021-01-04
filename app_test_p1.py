import requests
import os,sys

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
# from app_logging import logger
import numpy as np

import pandas as pd
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import math
import json
from flask_cors import *
from flask import Flask
app = Flask(__name__, static_url_path='')
# load config from config.py
# app.config.from_pyfile('config.py')
# url_prefix=app.config.get('url_prefix', '/api/cisdi/ml/economic')


CORS(app, supports_credentials=True)
# CORS(app, resources=r'/*')


@app.route('/')
def index():
    return "APIs Server"


import random
num_a = 20
num_b = 15
seed = 2020
random.seed(2020)
largest_delay = 1

waiting_list = [[110, 17], [130, 15], [85, 15], [120, 19], [130, 15]]
data_json=waiting_list
data_json= {"voyage":'12271'}

print('data_json:{}'.format(data_json))

print('客户端发起post请求')


def post_test(post_server=False,server_name=None):
  if post_server:
    # url='http://apis.cisdi.amiintellect.com/api/cisdi/ml/economic/{}/1234'.format(server_name)
    # url='http://apis.develop.ai.dev.amiintellect.com/api/ai/dtf/{}/1234'.format(server_name)
    # url='http://apis.develop.ai.dev.amiintellect.com/api/ai/dtf/{}/1234'.format(server_name)
    pass
  else:
    url = 'http://localhost:18401/api/ai/dtf/{}/1234'.format(server_name)  # 28095


  res = requests.post(url,
                      json=data_json
                      )

  if res.ok:
      # print('res.json()',res)
      print('from server response:{}'.format(res.json()))#response是post请求的返回值

if __name__=='__main__':

  post_test(post_server=False, server_name='best_schedule')
  # print(data_json[0])
  # print(l.head())
  # print(list(l))

  '''
  每次测试结果不一样还需要继续改一下
  '''


  '''
  http://192.168.100.1:28095/api/cisdi/ml/economic/add_message/1234
  '''
