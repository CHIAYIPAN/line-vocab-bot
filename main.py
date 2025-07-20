import pandas as pd
import datetime
import random
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
import pytz

def main():
    # 從環境變數取得設定
    line_bot_token = os.getenv('LINE_BOT_TOKEN')
    user_id = os.getenv('LINE_USER_ID')
    
    if not line_bot_token or not user_id:
        print("❌ 錯誤：請設定環境變數 LINE_BOT_TOKEN 和 LINE_USER_ID")
        return
    
    # 初始化 LINE Bot
    line_bot_api = LineBotApi(line_bot_token)
    
    # 檢查時間範圍
    taipei_tz = pytz.timezone('Asia/Taipei')
    now = datetime.datetime.now(taipei_tz)
    current_hour = now.hour
    
    print(f"🕐 台灣時間現在是：{now.strftime('%Y-%m-%d %H:%M:%S')} ({current_hour}點)")
    
    # 檢查是否在發送時間內（8:00-17:00）
    if not (8 <= current_hour < 17):
        print(f"⏰ 不在發送時間範圍內（8:00-17:00），當前時間：{current_hour}點")
        return
    
    try:
        # 讀取單字檔案
        print("📖 正在讀取單字檔案...")
        df = pd.read_excel("vocab.xlsx")
        
        if df.empty:
            print("❌ Excel 檔案是空的")
            return
        
        # 隨機選擇一個單字
        random_row = df.sample(1).iloc[0]
        english_word = random_row['英文單字']
        chinese_meaning = random_row['中文解釋']
        
        # 建立訊息
        message = f"📚 今日單字\n{english_word} : {chinese_meaning}"
        
        # 發送訊息
        line_bot_api.push_message(user_id, TextSendMessage(text=message))
        print(f"✅ 發送成功: {message}")
        
    except FileNotFoundError:
        print("❌ 找不到 vocab.xlsx 檔案")
    except Exception as e:
        print(f"❌ 發送失敗：{e}")

if __name__ == '__main__':
    main()
