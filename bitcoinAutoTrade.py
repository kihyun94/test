import pyupbit
import pandas

upbit = pyupbit.Upbit("ZSXz6AcY9FlMhnrR6bM8K47NQhuJQgDRCMi9BOEQ","LOmkniz4QpEZMNj6QYlNL1XzuYGAtIpbotGtvtwo") 

coinlist = ['KRW-ZIL', 'KRW-WAVES', 'KRW-VET', 'KRW-ETC', 'KRW-AAVE', 'KRW-CHZ', 'KRW-BTC', 'KRW-SRM', 'KRW-XRP', 'KRW-AERGO', 'KRW-ETH', 'KRW-BORA', 'KRW-QTUM', 'KRW-KAVA', 'KRW-SAND']

lower = []

avg123 =[[] for _ in range(100)]
madocut =[[] for _ in range(100)]

for i in range(len(coinlist)):
    lower.append(False) 
    for j in range(len(madocut)):
        madocut[j].append(False) 
    for j in range(len(avg123)):
        avg123[j].append(0) 



#RSI
def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")  


def buy1(coin):
    money = 30000  
    res = upbit.buy_market_order(coin, money)
    return


def buy2(coin):
    money = 30000  
    res = upbit.buy_market_order(coin, money)
    return


def sell(coin):
    amount = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)

    if amount > 0.00001:
        res = upbit.sell_market_order(coin, amount)
    return


def get_avg(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['avg_buy_price'] is not None:
                return float(b['avg_buy_price'])
            else:
                return 0
        return 0


def get_balance(ticker):
    
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

############MAIN############
while(True): 
    try:
        for i in range(len(coinlist)):
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute5")         
            now_rsi = round(rsi(data, 14).iloc[-1],2)                                
            krw = get_balance("KRW")
            avg_buy_price = upbit.get_avg_buy_price(coinlist[i])
            amount = upbit.get_balance(coinlist[i])
            cur_price = pyupbit.get_current_price(coinlist[i])                       

            if avg_buy_price == 0 :
                avg_buy_price = 1 
                                            
            if krw >= 9000: 
                if now_rsi <= 28 and amount == 0 and lower[i] == False :            
                    lower[i] = True                                                 
                if now_rsi >= 30 and lower[i] == True:                              
                    lower[i] = False                                                
                    buy1(coinlist[i])                                               
                    avg_buy_price = upbit.get_avg_buy_price(coinlist[i])            
                    amount = upbit.get_balance(coinlist[i])                         
                  
                if avg_buy_price * 0.95 > cur_price :                                 
                    if amount * avg_buy_price < 29500 * 5 :                            
                        buy2(coinlist[i])                                               
                        avg_buy_price = upbit.get_avg_buy_price(coinlist[i])            
                        amount = upbit.get_balance(coinlist[i])                         
                  

            
            madoma = upbit.get_balance(coinlist[i])                                                
            if amount != 0 and avg_buy_price != 1 :                                                
                for k in range(len(madocut)):                                                      
                    if avg_buy_price * (1.010 + 0.005*k) < cur_price and madocut[k][i] == False:   
                        avg123[k][i] = avg_buy_price*(1.006+0.005*k)                                
                        madocut[k][i] = True                                                       

                    if madocut[k][i] == True:                                                      
                        if avg123[k][i] >= cur_price:                                              
                            sell(coinlist[i])                                                      

            if amount == 0 :                                                                       
                for k in range(len(madocut)):                                                      
                    madocut[k][i] = False

    except Exception as e:
        print(e)
