from flask import Blueprint
import os,sys
restful_wordcloud = Blueprint('restful_wordcloud_example', __name__,)

#将项目根目录加入到运行环境
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from app.restfulapi_wordcloud_example import views