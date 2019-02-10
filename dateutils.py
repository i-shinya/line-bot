# 日付関連を扱うユーティリティメソッド集
# クラス変数などが必要になった場合はクラス化する
import datetime
from datetime import timedelta


# 現在の日本日付をyyyy-mm-ddの形式の文字列で取得する
def get_today_jp_str():
    today = datetime.datetime.now()
    today_str = _get_date_str(today)
    return today_str


# 翌日の日本日付をyyyy-mm-ddの形式の文字列で取得する
def get_tomorrow_jp_str():
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    tomorrow_str = _get_date_str(tomorrow)
    return tomorrow_str


# 日付データをyyyy-mm-ddの形式の文字列に変換して返却する
# TODO 日付形式が誤っていた場合の処理を追加する
def _get_date_str(date):
    date_str = ""
    if date != None:
        date_str = date.strftime("%Y-%m-%d")
    return date_str


# US時刻を日本時刻へ変換するメソッド
def _convert_us_to_jp(date):
    date

