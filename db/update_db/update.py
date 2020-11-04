from datetime import date, timedelta
import glob
import pandas as pd

sdate = date(2008, 8, 15)   # start date
edate = date(2008, 9, 15)   # end date

delta = edate - sdate       # as timedelta

for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    print(day)


#download link
#https://github.com/thepanacealab/covid19_twitter/tree/master/dailies/2020-10-01
#https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/2020-10-01/2020-10-01_top1000bigrams.csv
#https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/2020-10-01/2020-10-01_top1000terms.csv
#https://github.com/thepanacealab/covid19_twitter/blob/master/dailies/2020-10-01/2020-10-01_top1000trigrams.csv

path = '/Users/maria/PyCharmProjects/covid19_twitter/dailies'
tmp = []
for d in glob.glob(path + "/*/"):
    for f in glob.glob(d + '*_top1000terms.csv'):
        tmp_df = pd.read_csv(f, index_col=None, header=0, names=['term', 'counts'])
        f = f.replace(d, '')
        tmp_df['date'] = f[0:10]
        tmp.append(tmp_df)

df = pd.concat(tmp, axis=0, ignore_index=True)
df['counts'] = pd.to_numeric(df['counts'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], errors='coerce')