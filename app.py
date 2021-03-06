import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image_message

load_dotenv()

machine = TocMachine(
    states=[
        "user", 
        "choose_area",
        "choose_region", 
        "choose_restaurant",
        "recommand_restaurant",
        "recommand_menu"
    ],
    transitions=[
        {"trigger": "advance","source": "user","dest": "choose_area","conditions": "is_going_to_choose_area"},
        {"trigger": "advance","source": "choose_area","dest": "choose_region","conditions": "is_going_to_choose_region"},
        {"trigger": "advance","source": "choose_region","dest": "choose_restaurant","conditions": "is_going_to_choose_restaurant"},
        {"trigger": "advance","source": "choose_region","dest": "choose_area","conditions": "is_going_to_choose_area"},
        {"trigger": "advance","source": "choose_restaurant","dest": "recommand_restaurant","conditions": "is_going_to_recommand_restaurant"},
        {"trigger": "advance","source": "choose_restaurant","dest": "choose_region","conditions": "is_going_to_choose_region"},
        {"trigger": "advance","source": "recommand_restaurant","dest": "recommand_menu","conditions": "is_going_to_recommand_menu"},
        {"trigger": "advance","source": "recommand_restaurant","dest": "recommand_restaurant","conditions": "is_going_to_recommand_restaurant"},
        {"trigger": "advance","source": "recommand_menu","dest": "recommand_restaurant","conditions": "is_going_to_recommand_restaurant"},
        {
            "trigger": "go_back",
            "source": [
                "choose_area",
                "choose_region", 
                "choose_restaurant",
                "recommand_restaurant",
                "recommand_menu"
            ], 
            "dest": "user"
        },
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://i.ibb.co/YdjDk6w/fsm.png?')
            elif machine.state != 'user' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, '?????????aneater????????????????????????\n???????????????restart????????????????????????\n???????????????fsm????????????????????????????????????')
                machine.go_back()
            elif machine.state == "user":
                send_text_message(event.reply_token, '?????????aneater????????????????????????\n???????????????restart????????????????????????\n???????????????fsm????????????????????????????????????')
            elif machine.state == "choose_area":
                text = '????????????????????????\n\n?????????????????????????????????????????????????????????????????????\n'
                text += '????????????????????????????????????????????????????????????????????????\n'
                text += '????????????????????????????????????????????????????????????????????????\n'
                text += '??????????????????????????????????????????????????????????????????????????????\n'
                text += '????????????????????????????????????????????????????????????\n'        
                send_text_message(event.reply_token, text)
            elif machine.state == "choose_region":
                send_text_message(event.reply_token, '??????????????????????????????????????????????????????')
            elif machine.state == "choose_restaurant":
                send_text_message(event.reply_token, '?????????????????????????????????????????????????????????')
            elif machine.state == "recommand_restaurant":
                send_text_message(event.reply_token, '????????????????????????????????????????????????????????????????????????????????????')
            elif machine.state == "recommand_menu":
                send_text_message(event.reply_token, "?????????????????????????????????????????????restart???????????????")
            
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
    
