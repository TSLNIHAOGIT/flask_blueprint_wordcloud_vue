import sys,os
#将项目根目录加入到运行环境
sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__),'../..')))

from app.project2 import schedule
# from code.project2.origin_schedule import Original_schedule
from code.project2.v0_schedule import schedule_api
from app_logging import logger as logger
import time
from flask import  request, jsonify
import pandas as pd
import math
import traceback
from datetime import  datetime

#服务端获取客户端发来的json数据
@schedule.route('/best_schedule/<uuid>', methods=['GET', 'POST'])
def schedule_func(uuid):
    try:
        logger.info('开始进入模型，服务端获取数据')
        now_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        t1 = time.time()
        content = request.get_json(silent=True, force=True)
        logger.info('from client type content:{},{}'.format(type(content), content))  # Do your processing
        voyage_id = content["voyage"]
        schedule_api(voyage_id)


        logger.info('结果已经返回')
        # fres={'schedule_position':res}
        return jsonify({ 'code': "0", 'message': "success"})
    except Exception as e:
      logger.error('出错：{}\n{}'.format(e,traceback.format_exc()))

      return jsonify({'data': None, 'code': "1", 'message': "{}".format(e)})
    # finally:
    #   res_json_path=os.path.abspath(os.path.join(os.path.dirname(__file__),'../../log'))
    #
    #   with open(os.path.join(res_json_path,'{}_res_path.json'.format(now_time)),'w',encoding='utf8') as f:
    #     data={
    #
    #         "calculateParam": content,
    #         "calculateResult": {'data':fres,'code': "0", 'message': "success"}
    #     }
    #     json.dump(data,f,indent=4,ensure_ascii=False)