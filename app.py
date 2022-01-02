from flask import Flask, request, abort
import os.path
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,  ButtonsTemplate, MessageTemplateAction
import configparser
import re
import requests

from fsm import CreateLineBotMachine
from steam_comment import SearchGamebyName,getHistoryPrice

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel-access-token'))
handler = WebhookHandler(config.get('line-bot', 'channel-secret'))

machine = CreateLineBotMachine()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    reply_all = []
    game_id = 0
    if text == "reset":
        machine.go_back()
        response = "輸入想要搜尋的遊戲"
    else:
        if machine.state == "init":
            title_list = SearchGamebyName(text)
            machine.advance(text, title_list)
            if machine.state == "init":
                response = "\n\n".join(title_list)
                # for title in title_list:
                #     print(title)
                #     # reply_all.append(TextSendMessage(text = title))
                # response = "搜尋結果"
            else :
                game_id = re.search("https://store.steampowered.com/app/(\d+)" , title_list[text]).group(1)
                print(game_id) 
                response = "find game: " + text
        elif machine.state == "game_selected":
            machine.info(text)
            if machine.state == "price_info":
                print("start price info")
                #priceInfo = getHistoryPrice(game_id)
                API_key = "eb1a57f191778cf4dc5d621422ffd49ec56b8317"
                Identifier = requests.get("https://api.isthereanydeal.com/v02/game/plain/?key=" + API_key + "&shop=steam&game_id=app/" + str(game_id)).json()
                plain = Identifier["data"]["plain"]
                print(plain)
                response = "price_info"
            else:
                response = "格式錯誤!!"

        else:
            reply_all.append(TextSendMessage(text="格式錯誤!!!"))
            response = '<<詢問問題>>\n"Q:XXX"'

    #if machine.state == "init":
        
    
    reply_all.append(TextSendMessage(text=response))
    line_bot_api.reply_message(event.reply_token, reply_all)



if __name__ == "__main__":
    app.run(debug=True)