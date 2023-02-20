import websocket
import json
import datetime

def on_message(ws, message):
   data = json.loads(message)
   if data['e'] == 'error':
     print(f"Error: {data['m']}")
   else:
        symbol = data['s']   # Trading symbol
        price = float(data['c'])   # Last price
        bid_price = float(data['b'])   # Current best bid price
        ask_price = float(data['a'])   # Current best ask price
        trade_volume = float(data['v'])   # 24h trading volume
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # Current timestamp
        with open('btc_real_price.json', 'a') as f:
            json.dump({
                'timestamp': timestamp,
                'symbol': symbol,
                'last_price': price,
                'best_bid_price': bid_price,
                'best_ask_price': ask_price,
                '24h_volume': trade_volume
            }, f)
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