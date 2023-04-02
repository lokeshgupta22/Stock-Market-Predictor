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
    totala = []
    for stk in stcks:
        df = pd.read_csv(path)
        df2 = df.groupby('Ticker')
        nme = stk + ".NS"
        df3 = df2.get_group(nme)
        df = df3

        str = list(df.index)
        nind = [i for i in range(len(str))]
        df['nind'] = nind
        df.set_index(df.iloc[:, -1], inplace=True)
        df.drop(columns=df.columns[-1], axis=1, inplace=True)
        ocn = -1

        col = df.columns
        ar = {}
        arr = {}
        for i in range(0, len(df.iloc[:, ocn])):
            val = df._get_value(i, col[ocn])
            if val not in ar:
                ar[val] = 1
            else:
                ar[val] += 1
        k = sorted(list(ar.keys()))

        df.set_index(df.iloc[:, ocn], inplace=True)
        df.drop(columns=df.columns[ocn], axis=1, inplace=True)

        df = df[["Open", "Close", "Volume"]]

        if type(k[0]) == str:
            for i in range(0, len(df.index)):
                val = df.index[i]
                if val not in ar:
                    arr[val] = 1
                else:
                    arr[val] += 1
            key = list(arr.keys())
            k = key
        avg = []
        se = []
        p = []
        cr = len(df.columns)
        for j in k:
            m = 0
            p.append(len(df.loc[j])/len(df.index))
            for i in range(cr):
                list2 = df.loc[j][df.columns[m]]
                list3 = list(list2)
                avg.append(average(list3))
                se.append(stdev(list3))
                m += 1

        d = {}
        for x in range(0, len(df.index)):
            d["l{0}".format(x)] = list(df.iloc[x])

        avg = list(split(avg, cr))
        se = list(split(se, cr))
        d["avg"] = avg
        d["stdev"] = se
        d["prob"] = p
        v = []
        ans = []
        for j in k:
            for x in range(0, len(df.index)):
                val = 1
                data = d["l{0}".format(x)]
                mean = avg[j]
                dev = se[j]
                pro = p[j]
                for i in range(cr):
                    val = val*norm(data[i], mean[i], dev[i])
                    v.append(val)
                ans.append(val*pro)

        ans = list(split(ans, int(len(df.index))))
        maxval = []
        predict = []
        for i in range(len(df.index)):
            m = []
            for j in k:
                m.append(ans[j][i])
            maxval.append(max(m))
            ke = m.index(max(m))
            predict.append(ke)
        given = list(df.index)
        count = 0
        for i in range(len(df.index)):
            if given[i] == predict[i]:
                count += 1
        accuracy = (count)/(len(df.index))
        totala.append(accuracy)
        print(f"Accuracy of {nme}: {accuracy}")
    # print(totala)
    print(f"Average of all Accuracy: {average(totala)}")


start = time.time()
path = ["nifty50data.csv"]
for i in path:
    accuracy(i)
print(f"Time taken: {time.time() - start}")
