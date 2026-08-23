from websocket import WebSocketApp, enableTrace
import quantmath
from collection import deque
import json

#setup rolling windows for max 100 latest prices
market_data = {
    "AAPL": deque(maxlen=100),            
    "AMZN": deque(maxlen=100),            
    "BINANCE:BTCUSDT": deque(maxlen=100), 
    "IC MARKETS:1": deque(maxlen=100)
}



def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    enableTrace(True)  # Correct usage
    ws = WebSocketApp("wss://ws.finnhub.io?token=d6htio1r01qr5k4d8spgd6htio1r01qr5k4d8sq0",
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()