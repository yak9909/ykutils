import json
import os
import re


# config.json の読み込み
def load_config() -> dict:
    file_path = "config.json"
    # 開発者用configファイルが存在したら
    if os.path.exists("dev_config.json"):
        file_path = "dev_config.json"

    config_file = open(file_path, mode="r+", encoding="utf-8")
    return json.load(config_file)


# is_moderator（語彙力不足）
def is_moderator(user_id):
    moderators_id = load_config()["moderator"]
    if user_id in moderators_id:
        return True
    return False


# cogs/ 内にある .py ファイルを返す
# 先頭に # がつくファイルは無視される
def load_cogs():
    Initial_Cogs = []
    for file in os.listdir("cogs/"):
        if file.startswith("#"):
            continue
        if file.endswith(".py"):
            print(f"cogs.{file.split('.')[0]}")
            Initial_Cogs.append(f"cogs.{file.split('.')[0]}")
    return Initial_Cogs


# dataフォルダの存在確認 無ければ作る
def check_exist(dir, root="./data"):
    if dir:
        d = dir.split("/")
        dx = ""
        for x in d:
            dx += x + "/"
            if not os.path.exists(f"{root}/{dx}"):
                print(f"directory '{x}' is not found.\ncreate '{root}/{dx}'")
                os.mkdir(f"{root}/{dx}")


# dataフォルダの存在確認（デコレータ版）
def data_check(dir, root="./data"):
    def _data_check(func):
        def wrapper(*args, **kwargs):
            check_exist(dir, root)
            return func(*args, **kwargs)
        return wrapper
    return _data_check


# on/off のフォーマットのやつ（？）
def format_toggle(text):
    toggle_map = {
        "enable": ["enable", "on", "true"],
        "disable": ["disable", "off", "false"]
    }
    for k,v in toggle_map.items():
        for x in v:
            if text.lower() == x:
                if k == "enable":
                    return True
                elif k == "disable":
                    return False
    return None


# Code by zkr. thanks!
def update_z(ma, mb):
    ma_keys = ma.keys()
    mb_keys = mb.keys()
    
    for mb_key in mb_keys:
        if mb_key in ma_keys:
            val = mb[mb_key]
            
            if type(val) == type(ma[mb_key]) == dict:
                ma[mb_key] = update_z(ma[mb_key], val)
            else:
                ma[mb_key] = val
        else:
            ma[mb_key] = mb[mb_key]
    
    return ma


# 文字列の中のURLを取得して返す
def find_url(text):
    url = re.findall(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', text)
    return url 


# 文字列の中のTOKENを取得して返す
def find_token(text):
    token = re.findall(r'[M-Z][A-Za-z\d]{23}\.[\w-]{6}\.[\w-]{27}', text)
    return token
