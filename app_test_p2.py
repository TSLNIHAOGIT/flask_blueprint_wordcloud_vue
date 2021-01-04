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

#
# @app.route('/')
# def index():
#     return "APIs Server"






# data_json={
#  'economyName':'重庆',
#  'dB_tab_exportTimeDocs': 9.0,
#  'dB_tab_importTimeDocs': 10.37217071506418,
#  'dB_tab_exportTimeCompliance': 20.9999999,
#  'dB_tab_importTimeCompliance': 33.22248402285782,
#  'dB_tab_exportCostDocs': 74.0,
#  'dB_tab_importCostDocs': 77.0,
#  'dB_tab_exportCostCompliance': 244.6687250410281,
#  'dB_tab_importCostCompliance': 216.0596746375363}

# data_json={
#     "economyName": "重庆",
#     "dB_tab_exportTimeDocs": '109.67',
#     "dB_tab_importTimeDocs": '598.53',
#     "dB_tab_exportTimeCompliance": '47.07',
#     "dB_tab_importTimeCompliance": '86.47',
#     "dB_tab_exportCostDocs": '116.0',
#     "dB_tab_importCostDocs": '135.83',
#     "dB_tab_exportCostCompliance": '588.83',
#     "dB_tab_importCostCompliance": '1177.83'
# }



# data_json={
#     "economyName": "重庆",
#     "dB_tab_exportTimeDocs": ,
#     "dB_tab_importTimeDocs": 109.67,
#     "dB_tab_exportTimeCompliance": 47.07,
#     "dB_tab_importTimeCompliance": ,
#     "dB_tab_exportCostDocs":450 ,
#     "dB_tab_importCostDocs": ,
#     "dB_tab_exportCostCompliance": ,
#     "dB_tab_importCostCompliance":
# }

data_json={
    "economyName": "重庆",
    "dB_tab_importTimeDocs": 172.2,
    "dB_tab_exportTimeCompliance": 32.8,
    "dB_tab_exportCostDocs": 450.00,
    "dB_tab_importTimeCompliance": 78.8,
    "dB_tab_importCostDocs": 450.00,
    "dB_tab_exportTimeDocs": 440.6,
    "dB_tab_exportCostCompliance": 1027.17,
    "dB_tab_exportTimeTotal": 77.4,
    "dB_tab_importCostCompliance": 1560.17,
    "dB_tab_importTimeTotal": 142.4
}

# with open(r'E:\tsl_file\python_project\water_env\log\2020-11-30-19-37-16_res_path.json',encoding='utf8') as f:
#     data=json.load(f)
#     data_json=data["calculateParam"]

print('data_json:{}'.format(data_json))

print('客户端发起post请求')

def post_test(post_server=False,server_name=None):
  if post_server:
    pass
    # url='http://apis.cisdi.amiintellect.com/api/cisdi/ml/economic/{}/1234'.format(server_name)
    ##   http://apis.develop.ai.dev.amiintellect.com/api/ai/dtf
    # url='http://apis.develop.ai.dev.amiintellect.com/api/ai/dtf/{}/1234'.format(server_name)
    # url='http://119.3.205.60:18401/{}/1234'.format(server_name)
    # url = 'http://apis.develop.ai.dev.amiintellect.com/api/water_env/ml/index/{}/1234'.format(server_name)

  else:
    url = 'http://localhost:18401/api/ai/dtf/{}/1234'.format(server_name)  # 28095
  print('url={}'.format(url))
  try:
      res = requests.post(url,
                          json=data_json
                          )
      print('res status',res.ok,res)
  except Exception as e:
      print('error',e)

  if res.ok:
      # print('res.json()',res)
      print('from server response:{}'.format(res.json()))#response是post请求的返回值

if __name__=='__main__':

  post_test(post_server=False, server_name='get_score')
  pass
  # print(data_json[0])
  # print(l.head())
  # print(list(l))




  '''
  http://192.168.100.1:28095/api/cisdi/ml/economic/add_message/1234
  '''
