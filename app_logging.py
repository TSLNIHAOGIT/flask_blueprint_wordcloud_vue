# -*- coding:utf8 -*-
import logging
from logging.handlers import RotatingFileHandler
import os
logging.basicConfig(format='[%(asctime)s.%(msecs)03d][%(process)d][%(levelname)s][%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Schedule model')
##只会显示大于等于改级别以上的日志
logger.setLevel(logging.DEBUG)
#绝对路径
path=os.path.abspath(os.path.join(os.path.dirname(__file__),'log/project2.log'))

""" 输出日志到日志文件 """
rotatingFileHandler = RotatingFileHandler(path, maxBytes=500000, backupCount=2,encoding='utf8')
rotatingFileHandler.setFormatter(logging.Formatter(fmt='{%(asctime)s.%(msecs)03d} [%(thread)d] %(levelname)s - %(message)s',
                                                   datefmt='%Y-%m-%d %H:%M:%S'))
# 设置级别如果低于设置的级别则无效
rotatingFileHandler.setLevel(logging.DEBUG)
logger.addHandler(rotatingFileHandler)



##最短路径日志设置
##只会显示大于等于改级别以上的日志
logger_path = logging.getLogger('Predict Score Mode')
logger_path.setLevel(logging.INFO)
#绝对路径
best_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'log/predictscore_model.log'))

""" 输出日志到日志文件 """
rotatingFileHandler_path = RotatingFileHandler(best_path, maxBytes=10000000, backupCount=5,encoding='utf8')
rotatingFileHandler_path.setFormatter(logging.Formatter(fmt='{%(asctime)s.%(msecs)03d} [%(thread)d] %(levelname)s - %(message)s',
                                                   datefmt='%Y-%m-%d %H:%M:%S'))
# 设置级别如果低于设置的级别则无效
rotatingFileHandler_path.setLevel(logging.DEBUG)
logger_path.addHandler(rotatingFileHandler_path)

# ##最短路径single日志设置
# ##只会显示大于等于改级别以上的日志
# logger_path_single = logging.getLogger('Predict Score Single Mode')
# logger_path_single.setLevel(logging.INFO)
# #绝对路径
# best_path_single=os.path.abspath(os.path.join(os.path.dirname(__file__),'log/predictscore_single_model.log'))
# 
# """ 输出日志到日志文件 """
# rotatingFileHandler_path_single = RotatingFileHandler(best_path_single, maxBytes=500000, backupCount=2,encoding='utf8')
# rotatingFileHandler_path_single.setFormatter(logging.Formatter(fmt='{%(asctime)s.%(msecs)03d} [%(thread)d] %(levelname)s - %(message)s',
#                                                    datefmt='%Y-%m-%d %H:%M:%S'))
# # 设置级别如果低于设置的级别则无效
# rotatingFileHandler_path_single.setLevel(logging.DEBUG)
# logger_path_single.addHandler(rotatingFileHandler_path_single)








#
# #多日志文件，logging.basicConfig将无法完成，需要自定义文件和日志操作对象
#
# # #绝对路径
# path1=os.path.abspath(os.path.join(os.path.dirname(__file__),'log/macroeconomic_model.log'))
#
# path2=os.path.abspath(os.path.join(os.path.dirname(__file__),'log/predictscore_model.log'))
#
#
# # 定义文件
# file1 = logging.FileHandler(filename=path1, mode='a', encoding='utf-8')
# fmt1 = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d][%(process)d][%(levelname)s][%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# file1.setFormatter(fmt1)
#
# file2 = logging.FileHandler(filename=path2, mode='a', encoding='utf-8')
# fmt2 = logging.Formatter(fmt='[%(asctime)s.%(msecs)03d][%(process)d][%(levelname)s][%(name)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
# file2.setFormatter(fmt2)
#
#
# # 定义日志
# logger = logging.Logger(name='Schedule model', level=logging.INFO)
# logger.addHandler(file1)
#
#
# logger_path = logging.Logger(name='Predict Score Model', level=logging.INFO)
# logger_path.addHandler(file2)
# # logger1.removeHandler(file1)
# # logger1.removeHandler(file2)
#
#
#
#
# # # 写日志
# # logger1.error(msg='这里是msg111')
# # logger1.log(msg='这里是msg222', level=50)
# #
# #
# #
# # # 定义文件
# # file3 = logging.FileHandler(filename='l3.log', mode='a', encoding='utf-8')
# # fmt = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
# # file3.setFormatter(fmt)
# #
# # # 定义日志
# # logger_path = logging.Logger(name='这里是name222222', level=logging.INFO)
# # logger_path.addHandler(file3)
# #
# # # 写日志
# # logger_path.info('这里是msg333333')
# #
#
#
#
#
#









