from flask import Flask, request, abort, send_file
import os.path
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage,  ButtonsTemplate, MessageTemplateAction,  TemplateSendMessage
import configparser
import re

from fsm import CreateLineBotMachine
from steam_comment import SearchGamebyName, getHistoryPrice, getGameInfo

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
    if text.lower() == "reset":
        machine.go_back()
        response = "輸入想要搜尋的遊戲"
    else:
        if machine.state == "init":
            title_list = SearchGamebyName(text)
            machine.advance(text, title_list)
            if machine.state == "init":
                names = []
                for title in title_list:
                    names.append(title)
                response = "\n\n".join(title_list)
                reply_all.append(TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title = "沒找到輸入的遊戲，你是在指下面哪一款嗎?\n\n(都不是的話請再重新輸入名稱)",
                                text = '選擇名稱',
                                actions=[
                                    MessageTemplateAction(
                                        label = "第一款",
                                        text = names[0]
                                    ),
                                    MessageTemplateAction(
                                        label = "第二款",
                                        text = names[1]
                                    ),
                                    MessageTemplateAction(
                                        label = "第三款",
                                        text = names[2]
                                    ),
                                    MessageTemplateAction(
                                        label = "第四款",
                                        text = names[3]
                                    )
                                ]
                            )
                        )
                    )
            else :
                machine.current_game_id = re.search("https://store.steampowered.com/app/(\d+)" , title_list[text]).group(1)
                response = ""
                reply_all.append(TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title = text,
                                text = '想要知道什麼訊息?',
                                actions=[
                                    MessageTemplateAction(
                                        label='遊戲資訊',
                                        text='遊戲資訊'
                                    ),
                                    MessageTemplateAction(
                                        label='價格資訊',
                                        text='價格資訊'
                                    ),
                                    MessageTemplateAction(
                                        label='唉，不對我打錯了，重來啦',
                                        text='reset'
                                    )
                                ]
                            )
                        )
                )
        elif (machine.state == "game_selected" or machine.state == "price_info" or machine.state == "game_info"):
            machine.info(text)
            response = ""

        else:
            reply_all.append(TextSendMessage(text="好像出錯囉!!!"))
            response = '輸入reset來重新開始'


        if machine.state == "price_info":
            print("start price info")
            priceInfo = getHistoryPrice(machine.current_game_id)
            response = f"原始價格: {priceInfo[0]} 現在價格: {int(priceInfo[0]*(1-priceInfo[1]/100))}\n歷史最低: {int(priceInfo[0]*(1-priceInfo[2]/100))} 在 {priceInfo[3]}"
            reply_all.append(TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title = text,
                                text = '還想要知道其他訊息嗎?',
                                actions=[
                                    MessageTemplateAction(
                                        label='遊戲資訊',
                                        text='遊戲資訊'
                                    ),
                                    MessageTemplateAction(
                                        label='重來啦，換一款',
                                        text='reset'
                                    )
                                ]
                            )
                        )
                    )
        elif machine.state == "game_info":
            print("start game info")
            gameInfo = getGameInfo(machine.current_game_id)
            response = gameInfo
            reply_all.append(TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title = text,
                                text = '還想要知道其他訊息嗎?',
                                actions=[
                                    MessageTemplateAction(
                                        label='價格資訊',
                                        text='價格資訊'
                                    ),
                                    MessageTemplateAction(
                                        label='重來啦，換一款',
                                        text='reset'
                                    )
                                ]
                            )
                        )
                    )

        
    
    if(response):
        reply_all.append(TextSendMessage(text=response))
    line_bot_api.reply_message(event.reply_token, reply_all)

@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")



if __name__ == "__main__":
    app.run(debug=True)