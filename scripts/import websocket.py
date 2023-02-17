import websocket
import json
import datetime

def on_message(ws, message):
   data = json.loads(message)
   if data['e'] == 'error':
     print(f"Error: {data['m']}")
   else:
        btc_real_price = float(data['c'])
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('btc_real_price.json', 'a') as f:
            json.dump({'timestamp': timestamp, 'BTC/USDT': btc_real_price}, f)
            f.write('\n')

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")
    ws.send(json.dumps({
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@ticker"
        ],
        "id": 1
    }))

websocket.enableTrace(True)
ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws",
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close)
ws.on_open = on_open
ws.run_forever()