import pyupbit
import time
import datetime
import pandas

access = 
secret = 

upbit = pyupbit.Upbit(access, secret)
print("Autotrade start")


def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")  

coinlist = ["KRW-BTC",   "KRW-ETH", "KRW-EOS",  "KRW-SAND", "KRW-XRP",
            "KRW-WAVES", 'KRW-OMG', 'KRW-ETC',  'KRW-HUNT', 'KRW-STRK',
            'KRW-TRX',   'KRW-MBL', 'KRW-CELO', 'KRW-KNC',  'KRW-BORA',
            'KRW-ADA',   'KRW-SRM', 'KRW-SOL',  'KRW-MFT',  'KRW-1INCH']

lower28 = []
higher70 = []

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)

def buy(coin):
    money = upbit.get_balance("KRW")
    if money < 20000 :
        res = upbit.buy_market_order(coin, money)
    elif money < 50000:
        res = upbit.buy_market_order(coin, money*0.4)
    elif money < 100000 :
        res = upbit.buy_market_order(coin, money*0.3)
    else :
        res = upbit.buy_market_order(coin, money*0.2)
    return

def sell(coin):
    amount = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)
    total = amount * cur_price
    if total < 20000 :
        res = upbit.sell_market_order(coin, amount)
    elif total < 50000:
        res = upbit.sell_market_order(coin, amount*0.4)
    elif total < 100000:
        res = upbit.sell_market_order(coin, amount*0.3)        
    else :
        res = upbit.sell_market_order(coin, amount*0.2)
    return

while(True): 
    try:
        for i in range(len(coinlist)):
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute5")
            now_rsi = round(rsi(data, 14).iloc[-1],2)

            if now_rsi <= 28 : 
                lower28[i] = True

            elif now_rsi >= 33 and lower28[i] == True:
                buy(coinlist[i])
                lower28[i] = False
            elif now_rsi >= 70 and higher70[i] == False:
                sell(coinlist[i])
                higher70[i] = True
            elif now_rsi <= 60 :
                higher70[i] = False
            time.sleep(0.2)
    except Exception as e:
        print(e)
