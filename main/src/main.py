from websocket import WebSocketApp, enableTrace
import quantmath
from collections import deque
import json


market_data = {
    "LMT": deque(maxlen=10000),            
    "GE": deque(maxlen=10000),            
    "BA": deque(maxlen=10000), 
    "RTX": deque(maxlen=10000),
    "LLY": deque(maxlen=10000),            
    "JNJ": deque(maxlen=10000),            
    "NVO": deque(maxlen=10000), 
    "ABBV": deque(maxlen=10000)
}

market_returns = {
    "LMT": deque(maxlen=9999),            
    "GE": deque(maxlen=9999),            
    "BA": deque(maxlen=9999), 
    "RTX": deque(maxlen=9999),
    "LLY": deque(maxlen=9999),            
    "JNJ": deque(maxlen=9999),            
    "NVO": deque(maxlen=9999), 
    "ABBV": deque(maxlen=9999)         
}

SECTORS = {
    "Defense": ["LMT","GE","BA","RTX"],
    "Pharma": ["LLY","JNJ","NVO","ABBV"]
}




def on_message(ws, message):
    msg = json.loads(message)
    
    if msg.get("type") == "trade":
        for trade in msg["data"]:
            symbol = trade["s"]
            price = trade["p"]
            
            if symbol in market_data:
                
                market_data[symbol].append(price)
                
                if len(market_data[symbol]) >= 2:
                    prices_list = list(market_data[symbol])
                    latest_return = quantmath.log_returns(prices_list)
                    market_returns[symbol].append(latest_return)
                
        compare_sectors()

def compare_sectors():
    #calculate the math for every individual stock
    individual_results = {}
    for symbol, returns_queue in market_returns.items():
        if len(returns_queue) > 3:
            returns_list = list(returns_queue)
            vol = quantmath.volatility(returns_list)
            sharpe = quantmath.sharpe_ratio(returns_list, 0.0) 
            individual_results[symbol] = {"volatility": vol, "sharpe": sharpe}
    
    #group them by sector and calculate the averages
    sector_results = {}
    for sector_name, symbols in SECTORS.items():
        total_vol = 0
        total_sharpe = 0
        count = 0
        
        for sym in symbols:
            #only include the stock in the average if it actually has data
            if sym in individual_results:
                total_vol += individual_results[sym]["volatility"]
                total_sharpe += individual_results[sym]["sharpe"]
                count += 1
        
        #calculate the mean for the sector
        if count > 0:
            sector_results[sector_name] = {
                "volatility": total_vol / count,
                "sharpe": total_sharpe / count
            }
    
    #print the new, grouped dashboard with individual stocks
    if len(sector_results) >= 2: #both need data
        print("\n" + "="*50)
        print("DEFENSE VS PHARMA LIVE SECTOR MOMENTUM DASHBOARD")
        print("="*50)
        
        for sector, metrics in sector_results.items():
            #prints sector average
            print(f"\n[{sector.upper()} OVERALL] Avg Volatility: {metrics['volatility']:.5f} | Avg Sharpe: {metrics['sharpe']:.5f}")
            print("-" * 35)
            
            #prints individual stocks
            for sym in SECTORS[sector]:
                if sym in individual_results:
                    ind_metrics = individual_results[sym]
                    print(f"  > {sym}: Volatility = {ind_metrics['volatility']:.5f} | Sharpe = {ind_metrics['sharpe']:.5f}")
        
        #overall sector results
        most_volatile = max(sector_results, key=lambda s: sector_results[s]["volatility"])
        best_sharpe = max(sector_results, key=lambda s: sector_results[s]["sharpe"])
        
        print("\n" + "=" * 50)
        print(f"Most Volatile Sector : {most_volatile}")
        print(f"Best Sharpe Sector   : {best_sharpe}")
        print("=" * 50)

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("### Connection Opened. Subscribing... (this will take a bit)###")
    ws.send('{"type":"subscribe","symbol":"LMT"}')
    ws.send('{"type":"subscribe","symbol":"GE"}')
    ws.send('{"type":"subscribe","symbol":"BA"}')
    ws.send('{"type":"subscribe","symbol":"RTX"}')
    ws.send('{"type":"subscribe","symbol":"LLY"}')
    ws.send('{"type":"subscribe","symbol":"JNJ"}')
    ws.send('{"type":"subscribe","symbol":"NVO"}')
    ws.send('{"type":"subscribe","symbol":"ABBV"}')

if __name__ == "__main__":
    enableTrace(False) 
    
    ws = WebSocketApp("wss://ws.finnhub.io?token=d6htio1r01qr5k4d8spgd6htio1r01qr5k4d8sq0",
                      on_message=on_message,
                      on_error=on_error,
                      on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()