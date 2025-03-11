from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import json


app = Flask(__name__)

#輸入第一個機器人
line_bot_api = LineBotApi('')
handler = WebhookHandler("")

#輸入第二個機器人
line_bot_api2 = LineBotApi('')
handler2 = WebhookHandler("")

#輸入第三個機器人
line_bot_api3 = LineBotApi('')
handler3 = WebhookHandler("")

#輸入第4個機器人
line_bot_api4 = LineBotApi('')
handler4 = WebhookHandler("")

#輸入第5個機器人
line_bot_api5 = LineBotApi('')
handler5 = WebhookHandler("")


#輸入第6個機器人
line_bot_api6 = LineBotApi('')
handler6 = WebhookHandler("")

#輸入第7個機器人
line_bot_api7 = LineBotApi('')
handler7 = WebhookHandler("")

#輸入第8個機器人
line_bot_api8 = LineBotApi('')
handler8 = WebhookHandler("")


#輸入第9個機器人
line_bot_api9 = LineBotApi('')
handler9 = WebhookHandler("")




linebots = {1: line_bot_api, 2: line_bot_api2, 3: line_bot_api3, 4: line_bot_api4, 5: line_bot_api5, 6: line_bot_api6, 7: line_bot_api7, 8: line_bot_api8, 9: line_bot_api9}


@app.route("/")
def hello():
    return "Hello, World!"



@app.route("/api/dirupdate", methods=["POST"])
def recive():
    name = request.data
    print(name.decode('utf-8'))
    return name


@app.route("/api/stocklinebot" , methods=['POST'])
def stocklinebot():
  try:
    msg = request.data   # 取得網址的 msg 參數
    if msg:
      msg_data = json.loads(msg.decode("utf-8"))
      linrbot_index = msg_data.get("linebot", None)
      linebot_quota = msg_data.get("quotas", None)
      stock_infor = msg_data.get("message", None)
      msg_data = stock_infor + f"\n data send from linebot{linrbot_index} \n quota_usage: {linebot_quota}"
      # 如果有 msg 參數，觸發 LINE Message API 的 push_message 方法
      linebots[linrbot_index].push_message('', TextSendMessage(text=msg_data)) #''填入自己的UID
      print(msg_data)
      return "OK"
    else:
      return 'somthing wrong'
  except:
    print('error')

    



if __name__ == "__main__":
    port = 5000
    app.run(host='0.0.0.0', port=port)