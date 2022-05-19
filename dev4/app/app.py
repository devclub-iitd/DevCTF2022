from flask import Flask, render_template, request
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random
import string 
import sqlite3
from datetime import datetime
import base64
import os

from io import BytesIO

app = Flask(__name__, template_folder='template')
flag = os.environ.get('RAW_FLAG')

@app.route('/',methods = ['GET'])
def main(msg="", rescode = "200"):
    try:
        conn = sqlite3.connect('captcha.db',detect_types=sqlite3.PARSE_DECLTYPES)
        img = Image.new(mode='RGB',size=(200,75), color=(220,220,220))  
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("CONSOLA.TTF", 16)
        text = gen_str(15,"")
        draw.text((35,30),text,font=font,fill=(0,0,0))
        img_id = gen_str(10,"")
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        data = [img_id, text, datetime.now().replace(microsecond=0)]
        conn.execute('CREATE TABLE IF NOT EXISTS "captcha_details" ("id" integer primary key,"image_id" varchar(20),"time" timestamp,"text" varchar(15));')
        conn.execute('insert into captcha_details (image_id, text, time) values (?,?,?)', (*data,))
        conn.commit()
        return render_template("out.html", img_data=img_str, id = img_id, msg=msg), rescode
    except Exception as e:
        print(str(e)) # Log
        return main("Something Happened. Try again.", 500)

@app.route('/',methods = ['POST'])
def verify():
    try: 
        conn = sqlite3.connect('captcha.db',detect_types=sqlite3.PARSE_DECLTYPES)
        img_text = request.form['captcha']
        if len(img_text) == 15 and img_text.isalnum():
            query = "SELECT * FROM captcha_details WHERE text = ?"
            args = (img_text,)
            conn.row_factory = sqlite3.Row
            cur = conn.execute(query,args).fetchall()
            result = [dict(row) for row in cur]
            if len(result) == 1:
                result = result[0]
                gen_time = result['time']
                cur_time = datetime.now().replace(microsecond=0)
                diff = cur_time-gen_time
                print(diff)
                if diff.seconds <= 3:
                    return flag
                else:
                    return main("Verification Failed", 401)    
            else:
                return main("Verification Failed", 401)
        else:
            return main("Verification Failed", 401)
    except Exception as e:
        print(str(e))  #Log
        return "bad request", 400


def gen_str(len, delimiter):
    return delimiter.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(len))

if __name__ == '__main__':
   app.run(debug=True)
