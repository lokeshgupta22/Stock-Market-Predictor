import pandas as pd
import time
import statistics
import math
import warnings
warnings.filterwarnings("ignore")


def average(x):
    # return sum(x)/len(x)
    return statistics.mean(x)


def stdev(x):
    return statistics.stdev(x)


def norm(x, mean, stdev):
    ans = (1/(stdev*(math.sqrt(2*math.pi)))) * \
        (math.e**(-0.5*(((x - mean)/stdev)**2)))
    return ans


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]


def accuracy(path):
    df = pd.read_csv(path)
    stcks = ["RELIANCE", "AXISBANK", "HDFC", "ITC", "NESTLEIND", "BAJAJ-AUTO",
             "GRASIM", "HDFCBANK", "POWERGRID", "EICHERMOT", "HINDALCO", "TITAN",
             "ULTRACEMCO", "SBILIFE", "TECHM", "ADANIPORTS", "CIPLA", "ADANIENT",
             "M&M", "HDFCLIFE", "TATASTEEL", "HCLTECH", "WIPRO", "KOTAKBANK", "BPCL",
             "INDUSINDBK", "UPL", "BAJFINANCE", "SUNPHARMA", "DIVISLAB", "TATAMOTORS",
             "HINDUNILVR", "BHARTIARTL", "APOLLOHOSP", "MARUTI", "BRITANNIA", "TCS",
             "BAJAJFINSV", "ASIANPAINT", "HEROMOTOCO", "ONGC", "LT", "NTPC", "DRREDDY",
             "TATACONSUM", "ICICIBANK", "JSWSTEEL", "INFY", "COALINDIA", "SBIN"]
    for stk in stcks:
        df = pd.read_csv(path)
        df2 = df.groupby('Ticker')
        nme = stk + ".NS"
        df3 = df2.get_group(nme)

        dt = list(df3["Date"])
        dtnew = []
        for d in dt:
            date = d.split(" ")[0]
            dtnew.append(date)
        df3["Date"] = dtnew

        for di in range(len(df3.index)):
            a = df3.iloc[di, 0].split("-")
            df3.iloc[di, 0] = f"{a[0]}-{a[1]}"

        str = list(df3.index)
        nind = [i for i in range(len(str))]
        df3['nind'] = nind
        df3.set_index(df3.iloc[:, -1], inplace=True)
        df3.drop(columns=df3.columns[-1], axis=1, inplace=True)

        year1 = int(df3["Date"][0].split("-")[0])
        mth = int(df3["Date"][0].split("-")[1])

        for m in range(1, 13):
            print(f"Month: {m}")
            myroi = []
            mystd = []
            yr = year1
            for y in range(23):
                if yr == 2022 and m > 10:
                    continue
                if yr > 2022:
                    continue
                if mth > m and yr == year1:
                    yr += 1
                if yr > 2022:
                    continue
                if m < 10:
                    df4 = df3[df3["Date"].str.contains(f"{yr}-0{m}")]
                else:
                    df4 = df3[df3["Date"].str.contains(f"{yr}-{m}")]
                str = list(df4.index)
                nind = [i for i in range(len(str))]
                df4['nind'] = nind
                df4.set_index(df4.iloc[:, -1], inplace=True)
                df4.drop(columns=df4.columns[-1], axis=1, inplace=True)
                df = df4
                col = df.columns
                valstd = stdev(df["Close"])
                mystd.append(valstd)
                valroi = (df._get_value(
                    (len(df.index)-1), col[5]) - df._get_value(0, col[2]))/df._get_value(0, col[2])
                myroi.append(valroi)
                yr += 1
            print(f"Average ROI of {nme} of Month {m}: {average(myroi)}")
            print(f"Average STDEV of {nme} of Month {m}: {stdev(myroi)}")


start = time.time()
path = ["nifty50data.csv"]
for i in path:
    accuracy(i)
print(f"Time taken: {time.time() - start}")
