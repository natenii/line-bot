from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('m92WvYjqgh8+r1V4v6AznR86uJbkOcYGcDWuiXruWqo/mjmqEF7jjifNPQFe7Utc7RIPqmztfRBpD6k6eIMQ9DXRr6NvPviE/DQHneKf/ZGn91DfL0JJNJRb6VPGFhkxTljWy8DBI0X8R8AjUE+6swdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('cb5326c796fbbb288ea32fb9f5a04764')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
