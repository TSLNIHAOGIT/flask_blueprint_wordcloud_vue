
from flask import Blueprint
import os,sys
schedule = Blueprint('project2', __name__,)

#将项目根目录加入到运行环境
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from app.project2 import views

