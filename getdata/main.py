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
    
    msg = json.loads(message)
    
    
    if msg.get("type") == "trade":
        for trade in msg["data"]:
            symbol = trade["s"]
            price = trade["p"]
            
            
            if symbol in market_data:
                market_data[symbol].append(price)
                
       
        compare_sectors()

def compare_sectors():
    results = {}
    
    for symbol, prices in market_data.items():
        
        if len(prices) > 3:
            prices_list = list(prices)
            
           
            returns_list = quantmath.log_returnshistorical(prices_list)
            
            vol = quantmath.volatility(returns_list)
            sharpe = quantmath.sharpe_ratio(returns_list, 0.0) 
            
            results[symbol] = {"volatility": vol, "sharpe": sharpe}
    
    
    if len(results) >= 2:
        print("\n" + "="*30)
        print("LIVE SECTOR COMPARISON")
        print("="*30)
        
        for sym, metrics in results.items():
            print(f"{sym}: Vol = {metrics['volatility']:.5f} | Sharpe = {metrics['sharpe']:.5f}")
        
        
        most_volatile = max(results, key=lambda s: results[s]["volatility"])
        best_sharpe = max(results, key=lambda s: results[s]["sharpe"])
        
        print("-" * 30)
        print(f"Most Volatile : {most_volatile}")
        print(f"Best Sharpe   : {best_sharpe}")
        print("=" * 30)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("### Connection Opened. Subscribing to sectors... ###")
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')

if __name__ == "__main__":
    enableTrace(True) 
    
    ws = WebSocketApp("wss://ws.finnhub.io?token=d6htio1r01qr5k4d8spgd6htio1r01qr5k4d8sq0",
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()