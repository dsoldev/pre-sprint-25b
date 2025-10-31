# import http.client
# import json

# conn = http.client.HTTPSConnection("qd5vmq.api.infobip.com")
# payload = json.dumps({
#     "messages": [
#         {
#             "from": "447860088970",
#             "to": "5511999998938",
#             "messageId": "1828f3e7-7dcf-40bb-afcb-58c2633642a9",
#             "content": {
#                 "templateName": "test_whatsapp_template_en",
#                 "templateData": {
#                     "body": {
#                         "placeholders": ["Diego"]
#                     }
#                 },
#                 "language": "en"
#             }
#         }
#     ]
# })
# headers = {
#     'Authorization': 'App 220ac3453c09fbbb723da15b4ba16506-d1a6ff41-7dc7-4e1c-8a4b-3b676ae232c7',
#     'Content-Type': 'application/json',
#     'Accept': 'application/json'
# }
# conn.request("POST", "/whatsapp/1/message/template", payload, headers)
# res = conn.getresponse()
# data = res.read()
# print(data.decode("utf-8"))

import http.client
import json

conn = http.client.HTTPSConnection("qd5vmq.api.infobip.com")
payload = json.dumps({
    "from": "447860088970",
    "to": "5511999998938",
    "messageId": "a28dd97c-1ffb-4fcf-99f1-0b557ed381da",
    "content": {
        "text": "Some text HUE"
    },
    "callbackData": "Callback data",
    "notifyUrl": "https://www.example.com/whatsapp",
    "urlOptions": {
        "shortenUrl": True,
        "trackClicks": True,
        "trackingUrl": "https://example.com/click-report",
        "removeProtocol": True
    }
})
headers = {
    'Authorization': 'App 220ac3453c09fbbb723da15b4ba16506-d1a6ff41-7dc7-4e1c-8a4b-3b676ae232c7',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
conn.request("POST", "/whatsapp/1/message/text", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))