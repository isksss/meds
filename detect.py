import cv2
import datetime
import time
import torch
import math
import requests, json
import sqlite3

##########
# test 
##########
# 検出間隔(秒)
wait = 5
# 通知設定
# 1: 毎回
# 100: 1時間ごと
timer_dur = 1

#######################################################
#######################################################
#######################################################
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

pt_path = "best.pt"
model = torch.hub.load("./yolov5", "custom", path=pt_path, source="local")
model.conf = 0.75

old_amount = 0

webhook_url  = 'https://discord.com/api/webhooks/1054942193573449728/Ywe5aSujPgHSGU3xK3iWdm5XhP1Lsb0bGcumC0yK7EWr8tkQQ33l2cwFvwsJIXYdGDL8'

dbname = 'meds.db'

check_flag = 0

old = 0

headers      = {'Content-Type': 'application/json'}
#######################################################
#######################################################
#######################################################

# 検出
def detect(frame, d):
    result = model(frame)

    cnt = 0
    for idx, row in enumerate(result.pandas().xyxyn[0].itertuples()):
        cnt += 1
        height, width = frame.shape[:2]
        xmin = math.floor(width * row.xmin)
        xmax = math.floor(width * row.xmax)
        ymin = math.floor(height * row.ymin)
        ymax = math.floor(height * row.ymax)
        cripped_img = frame[ymin:ymax, xmin:xmax]
        cv2.imwrite(f"clip/crip_{d}_{idx}.jpg", cripped_img)
    
    objects = result.pandas().xyxy[0]
    
    amount = len(objects)
    print(f'検出数:{amount}')
    old_amount = amount
    
    now = datetime.datetime.now(JST)
    hm = now.strftime('%H%M')
    hm = int(hm)
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    sql = f'insert into record(amount, time) values ({amount},{hm})'
    cur.execute(sql)
    conn.commit()
    
    cur.execute(f'SELECT * FROM time')
    rec = cur.fetchall()
    
    cur.execute(f'SELECT * FROM record')
    old_r = cur.fetchall()
    
    
    last = old_r[len(old_r)-1]
    last2 = old_r[len(old_r)-2]
    
    
    cur.close()
    conn.close()
    
    ## timer
    if hm%timer_dur == 0:
        print('@ 通知を送ります。')
        for i in rec:
            # t   a
            a = i[1]
            t = i[2]
            if hm < t:
                print(f'@ {t}時の通知を送りました。')
                main_content = {'content': f'{t}に{a}個のみましょう！'}
                esponse     = requests.post(webhook_url, json.dumps(main_content), headers=headers)
            
    if last2[2] == 999:
        print('初回検出なので増減メッセージをスキップします。')
        return
    
    if last[1] > last2[1]:
        # ふえたとき
        print('+ 増量メッセージを送りました。')
        main_content = {'content': f'薬が増えたよ, {last[1]-last2[1]}個増えて現在{last[1]}個置いてあります。'}
        esponse     = requests.post(webhook_url, json.dumps(main_content), headers=headers)
        
    elif last[1] < last2[1]:
        # 減った時
        print('- 減少メッセージを送りました。')
        main_content = {'content': f'薬が減ったよ, {last2[1]-last[1]}個減って現在{last[1]}個置いてあります。'}
        esponse     = requests.post(webhook_url, json.dumps(main_content), headers=headers)
    
#######################################################
#######################################################
#######################################################
while (True):
    print('##### 待機中 ##### ##### ##### ##### #####')
    time.sleep(wait) # 5sec
    cap = cv2.VideoCapture(-1)
    print('----- 撮影します。 ----- ----- -----')
    ret, frame = cap.read()
    if not ret:
        print("not capture")
        break

    print(frame.shape)
    frame = cv2.resize(frame, (640, 480))
    # sleep(1)
    now = datetime.datetime.now(JST)
    d = now.strftime('%Y%m%d%H%M%S')
    save_path = 'img/'+ d +'.png'
    print('----- 保存します。 ----- ----- -----')
    cv2.imwrite(save_path, frame)
    print(save_path)
    print('----- 検出します。 ----- ----- -----')
    detect(frame, d)
    cap.release()
    

cv2.destroyAllWindows()
    