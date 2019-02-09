from flask import Flask, request, jsonify
import requests
import datetime
import json
from datetime import timedelta
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

import os
from os.path import join, dirname
from dotenv import load_dotenv

app = Flask(__name__)


def lambda_handler(event, context):
    hello_world()


@app.route("/", methods=["GET"])
def hello_world():
    # 祝日リストを取得する
    holiday_list = get_holiday_info()
    print("今年の祝日一覧")
    print(holiday_list)

    # 祝日リストに翌日が含まれるか判定する
    is_holiday = is_tomorrow_holiday(holiday_list)
    print("翌日は祝日か？")
    print(is_holiday)

    push_line_message()

    if is_holiday:
        # このあたりでLine-botの通知機能を記載する
        print("翌日は祝日!")
        return app.response_class(status=200)
    else:
        print("翌日は祝日じゃない")
        return app.response_class(status=200)


# 翌日が祝日か判定する関数
def is_tomorrow_holiday(holiday_list):
    tomorrow = get_tomorrow_str()
    return tomorrow in holiday_list


# 祝日を取得する関数
def get_holiday_info():
    tomorrow = get_tomorrow_str()
    year = tomorrow[0:4]
    url = "https://holidays-jp.github.io/api/v1/" + year + "/date.json"  # 取得先のURL
    holiday_list = requests.get(url)
    return holiday_list.json()


# 翌日の日付をyyyy-mm-ddの形式の文字列で取得する
def get_tomorrow_str():
    today = datetime.datetime.now()
    print("今日の日付")
    print(today)
    tomorrow = today + datetime.timedelta(days=1)
    print("翌日の日付")
    print(tomorrow)
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")
    return tomorrow_str


# LINEメッセージを送る
def push_line_message():
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)
    LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
    SEND_USER_ID = os.environ.get("SEND_USER_ID")

    # url = "https://api.line.me/v2/bot/message/push"
    # headers = {
    #     "Content-Type": "application/json",
    #     "Authorization": "Bearer " + LINE_ACCESS_TOKEN,
    # }
    # data = {"to": SEND_USER_ID, "messages": "text_message"}
    # response = requests.post(url, data=json.dumps(data), headers=headers)
    # print(response.status_code)

    # APIとハンドラーを定義
    line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

    text_message = "テスト用メッセージ"
    try:
        line_bot_api.push_message(SEND_USER_ID, TextSendMessage(text="text_message"))
    except LineBotApiError as e:
        # エラーが起こり送信できなかった場合
        print(e)


@app.route("/get_line_profile", methods=["GET", "POST"])
def get_line_profile():
    LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
    SEND_USER_ID = os.environ.get("SEND_USER_ID")

    line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
    profile = line_bot_api.get_profile(SEND_USER_ID)
    print(profile)
    return app.response_class(status=200)

