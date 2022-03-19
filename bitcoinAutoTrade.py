secret


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
lower23 = []
lower18 = []
sblower23 = []
sblower18 = []
higher65 = []

# initiate
for i in range(len(coinlist)):
    lower28.append(False)
    lower23.append(False)
    lower18.append(False)    
    sblower23.append(False)
    sblower18.append(False)
    higher65.append(False)

def buy1(coin):
    money = 20000
    res = upbit.buy_market_order(coin, money)
    return

def buy2(coin):
    money = 20000
    res = upbit.buy_market_order(coin, money)
    return

def buy3(coin):
    money = 20000
    res = upbit.buy_market_order(coin, money)
    return

# 시장가 매도 함수
def sell(coin):
    amount = upbit.get_balance(coin)
    cur_price = pyupbit.get_current_price(coin)
    total = amount * cur_price

    if amount > 0.00001:
        res = upbit.sell_market_order(coin, amount)
    return

while(True): 
    try:
        for i in range(len(coinlist)):
            data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute5")
            now_rsi = round(rsi(data, 14).iloc[-1],2)
            

            if now_rsi <= 28 and sblower23[i] == False and sblower18[i] == False : 
                lower28[i] = True
                sblower23[i] = True

            elif now_rsi >= 32 and lower28[i] == True:
                lower28[i] = False
                buy1(coinlist[i])


            elif now_rsi <= 23 and sblower23[i] == True and sblower18[i] == False :
                lower23[i] = True
                sblower18[i] = True

            elif now_rsi >= 28 and lower23[i] == True :
                lower23[i] = False
                buy2(coinlist[i])

            elif now_rsi <= 18 and sblower18[i] == True :
                lower18[i] = True

            elif now_rsi >= 23 and lower18[i] == True :
                lower18[i] = False
                buy3(coinlist[i])

            elif now_rsi >= 65 and higher65[i] == False:           
                sell(coinlist[i])
                higher65[i] = True
                sblower23[i] = False
            elif now_rsi <= 55 :
                higher65[i] = False


            time.sleep(0.5)
    except Exception as e:
        print(e)
