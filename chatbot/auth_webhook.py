# auth_webhook_infobip_numbers.py
#
# Configura a INBOUND CONFIGURATION do seu número (WhatsApp) para encaminhar
# mensagens recebidas via HTTP POST em JSON para o seu Django (/webhook/).

import http.client
import json
from urllib.parse import urlencode

API_HOST = "qd5vmq.api.infobip.com"
API_KEY = "App 220ac3453c09fbbb723da15b4ba16506-d1a6ff41-7dc7-4e1c-8a4b-3b676ae232c7"

# Use UM dos dois abaixo:
NUMBER = "447860088970"        # E.164 do seu sender (sem 'whatsapp:')
NUMBER_KEY = None              # Se sua conta usa 'numberKey', coloque aqui e deixe NUMBER=None

WEBHOOK_URL = "https://d4402002365b.ngrok-free.app/webhook/"  # sua URL pública HTTPS

COMMON_HEADERS = {
    "Authorization": API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def set_inbound_configuration():
    """
    Cria/atualiza configuração inbound do número:
      channel: WHATSAPP
      type: HTTP_FORWARD
      httpMethod: POST
      url: WEBHOOK_URL
      contentType: application/json
    """
    conn = http.client.HTTPSConnection(API_HOST)

    body = {
        "channel": "WHATSAPP",
        "number": NUMBER,
        "keyword": "devlife",
        "enabled": True,
        "forwardingAction": {
            "type": "HTTP_FORWARD",
            "httpMethod": "POST",
            "contentType": "application/json",
            "url": WEBHOOK_URL,
        }
    }

    # Em muitos tenants POST faz upsert; se der 409/405/400 específico, tente PUT em /{id}
    conn.request(
        "POST",
        "/resource-management/1/inbound-message-configurations",
        body=json.dumps(body),
        headers=COMMON_HEADERS
    )
    res = conn.getresponse()
    resp_text = res.read().decode("utf-8")
    print("POST inbound config:", res.status, res.reason, resp_text)
    conn.close()

    # Se precisar fazer PUT, você precisará do 'id' retornado no POST bem-sucedido.
    # Ex.: conn.request("PUT", f"/numbers/1/inbound/configurations/{config_id}", body=..., headers=...)
    return res.status, resp_text


def get_inbound_configuration():
    """
    Consulta as configurações existentes filtrando por canal e número/numberKey.
    """
    conn = http.client.HTTPSConnection(API_HOST)
    q = {"channel": "WHATSAPP"}
    if NUMBER:
        q["number"] = NUMBER
    elif NUMBER_KEY:
        q["numberKey"] = NUMBER_KEY

    conn.request(
        "GET",
        f"/resource-management/1/inbound-message-configurations?{urlencode(q)}",
        headers={"Authorization": API_KEY, "Accept": "application/json"}
    )
    res = conn.getresponse()
    resp_text = res.read().decode("utf-8")
    print("GET inbound config:", res.status, res.reason)
    print(resp_text)
    conn.close()
    return res.status, resp_text


if __name__ == "__main__":
    set_inbound_configuration()
    get_inbound_configuration()
