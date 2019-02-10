# Lineボットで通知するアプリケーション
# herokuでのホスティングを前提とする

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

from dateutils import *

app = Flask(__name__)

# Lineへのアクセス情報を取得し、定義する
HEROKU_FLAG = os.environ.get("HEROKU_FLAG", default=False)
if HEROKU_FLAG == False:  # heroku環境以外
    dotenv_path = join(dirname(__file__), ".env")
    load_dotenv(dotenv_path)

LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
SEND_USER_ID = os.environ.get("SEND_USER_ID")

# APIとハンドラーを定義
line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

day_dict = {"today": "今日", "beforeday": "明日"}

# 祝日の前日と当日に対応している。<today_or_beforeday>で以下のように指定する。
# 当日： /notif_holiday/today
# 前日： /notif_holiday/beforeday
@app.route("/notif_holiday/<today_or_beforeday>", methods=["GET"])
def notif_holiday(today_or_beforeday):
    # 日付を取得する。heroku環境ではus時刻なのでus時刻を変換して取得する
    date_str = ""
    if today_or_beforeday == "today":
        date_str = get_today_jp_str()
    elif today_or_beforeday == "beforeday":
        date_str = get_tomorrow_jp_str()
    else:
        raise RuntimeError("ERROR: args is invalid.")

    # 祝日リストを取得する
    holiday_list = get_holiday_info(date_str)
    print("holiday list")
    print(holiday_list)

    # 祝日リストに指定日が含まれるか判定する
    is_holiday_flag = is_holiday(holiday_list, date_str)

    if is_holiday_flag:
        # このあたりでLine-botの通知機能を記載する
        holiday_name = holiday_list[date_str]
        print(day_dict[today_or_beforeday] + "は「" + holiday_name + "」です。")
        push_line_message(holiday_name, today_or_beforeday)
        return app.response_class(status=200)
    else:
        print(day_dict[today_or_beforeday] + " is not holiday")
        return app.response_class(status=200)


# 指定した日付が祝日か判定する
def is_holiday(holiday_list, date_str):
    return date_str in holiday_list


# 指定した日付の年の祝日を取得するメソッド
def get_holiday_info(date_str):
    year = date_str[0:4]
    url = "https://holidays-jp.github.io/api/v1/" + year + "/date.json"  # 取得先のURL
    holiday_list = requests.get(url)
    return holiday_list.json()


# LINEメッセージを送るメソッド
def push_line_message(holiday_name, today_or_beforeday):
    text_message = day_dict[today_or_beforeday] + "は「" + holiday_name + "」です。"
    try:
        line_bot_api.push_message(SEND_USER_ID, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        # エラーが起こり送信できなかった場合
        print(e)


@app.route("/get_line_profile", methods=["GET", "POST"])
def get_line_profile():
    line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
    profile = line_bot_api.get_profile(SEND_USER_ID)
    print(profile)
    return app.response_class(status=200)


# 疎通確認用のテストAPI
@app.route("/test", methods=["GET"])
def test_method():
    return "test ok"
