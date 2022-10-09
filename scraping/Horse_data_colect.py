import requests
import urllib
from urllib.parse import urljoin
import bs4
from tqdm import tqdm
import time
import pandas as pd
import csv


CSV_DIR = "Ouma"
URL_BASE = "https://db.netkeiba.com/race/"
 
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36   '
} 

def numStr(num):
    if num >= 10:
        return str(num)
    else:
        return '0' + str(num)


def get_text_from_page(url):

    try:

        # メールアドレスとパスワードの指定
        USER = "****"
        PASS = "****"

        login_info = {
            "login_id":USER,
            "pswd":PASS,
        }
    # セッションを開始
        session = requests.session()

        url_login ="https://regist.netkeiba.com/account/?pid=login&action=auth"

        ses = session.post(url_login, data=login_info)

        res = session.get(url)
        res.encoding = res.apparent_encoding  
        text = res.text

        return text
    except:
        return None

def get_info_from_text(header_flg, text):      
   
    try:      
        # データ
        info = []
         
        soup = bs4.BeautifulSoup(text, features='lxml')
         
        # レース天気場所等表示箇所
        race_info = soup.find(class_="mainrace_data fc")

        # コース・天気情報     
        weather_cols = race_info.find_all("span")
        # 日程・開催場所情報  
        place_cols = race_info.find_all(class_="smalltxt")

        base_elem = soup.find(class_="race_table_01 nk_tb_common")

        elems = base_elem.find_all("tr")
 
        if not weather_cols==None:
                 
            #  文字整形
            for weather_col in weather_cols:
                weather_text = weather_col.text
                weather_text = weather_text.replace("/", "")
                weather_text = weather_text.replace("芝", "", 1)
                weather_text = weather_text.replace("ダ", "", 1)
                weather_text = weather_text.replace("右", "")
                weather_text = weather_text.replace("左", "")
                weather_text = weather_text.replace("m", "")
                weather_text = weather_text.split()
                     
            info.append(weather_text)

        if not place_cols==None:
                 
            #  文字整形
            for place_col in place_cols:
                place_text = place_col.text
                place_text = place_text.replace("回", " ")
                place_text = place_text.replace("日目", " ")
                place_text = place_text.split()
                     
            info.append(place_text)

        for elem in elems:
             
            row_info = []
             
            # ヘッダーを除外するための情報
            r_class = elem.get("class")
             
            r_cols = None
             
            if r_class==None:
                # 列取得
                r_cols = elem.find_all("td")
                 
            else:
                # ヘッダー(先頭行)
                if header_flg:
                    r_cols = elem.find_all("th")
             
            if not r_cols==None:
                 
                for r_col in r_cols:
                    tmp_text = r_col.text
                    tmp_text = tmp_text.replace("\n", "")
                    row_info.append(tmp_text.strip())
                     
                info.append(row_info)

        # if not odds_cols==None: 
        #     for odds_col in odds_cols:
        #         odds_text = odds_col.text
        #         odds_text = odds_text.split()

        #     info.append(odds_text)

            
        return info
    except:
        print("err")
        return None

if __name__ == '__main__':
    for year in tqdm(range(2019, 2022)):
        for place in tqdm(range(1, 11)):
            for times in tqdm(range(1, 13)):
                for days in tqdm(range(1, 13)):
                    for race in range(1, 13):
                    # urlでぶっこ抜く
                        RACE_ID = str(year) + numStr(place) + numStr(times) + numStr(days) + numStr(race)
                        print(RACE_ID)
                        url = URL_BASE + RACE_ID
                        time.sleep(1)
                        text = get_text_from_page(url)
                        info = get_info_from_text(False, text)
                    # csvファイル
                        file_path = CSV_DIR + RACE_ID + ".csv"

                        if info == None:
                            continue
                        else:
                            with open(file_path, "w", newline="") as f:
                                writer = csv.writer(f)
                                writer.writerows(info)