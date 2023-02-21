import websocket 
import json

def get_streaming(symbol, interval) :
    closes, highs, lows, volumes, trades = [], [], [], [], []
    candles = {}
    
    def on_message(ws, message):
        nonlocal candles, closes, highs, lows, volumes, trades
        
        json_message = json.loads(message)
        candle = json_message["k"]
        is_candle_closed = candle["x"]
        close =candle["c"]
        high = candle["h"]
        low = candle["l"]
        volume = candle["v"]
        trade = candle["n"]
        symbol = candle["s"]

        if is_candle_closed : 
            closes.append(close)
            highs.append(high)
            lows.append(low)
            volumes.append(volume)
            trades.append(trade)
            candles[symbol]=[closes,highs,lows,volumes,trades]
            print(candles)
            with open("./streaming_data.json", "w") as f:
                json.dump(candles, f)

    def on_close(ws):
        print("Connection closed")

    socket = f'wss://stream.binance.com:9443/ws/{symbol}@kline_{interval}'
    ws = websocket.WebSocketApp(socket, on_message=on_message,on_close=on_close)
    ws.run_forever()
    return candles



intervale = '1s'
symbol = 'ethusdt'

get_streaming(symbol, intervale)