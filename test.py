import requests as r
from base64 import b64encode
import json

file = "student_data.xlsx"
with open(file, "rb") as f:
    enc = b64encode(f.read())
enc = b"student_xlsx ," + enc
payload = dict(
    excel_enc_data = enc.decode('utf-8')
)
# payload = {'name':"aniket"}
with r.post(url="http://127.0.0.1:8000/add-ca-marks-from-teacher", headers={'Content-Type':'application/json'}, data=json.dumps(payload)) as resp:
    print (resp.text)