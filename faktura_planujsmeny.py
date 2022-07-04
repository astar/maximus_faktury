#!/usr/bin/env python3

import pandas as pd
from dateutil.parser import  parse
import sys

fn = sys.argv[1]
import datetime as dt
import pandas as pd
from dateutil.parser import  parse

fn = 'smeny_2022-06-01_Jaroslav-Vážný.xls'
data = pd.read_html(fn, decimal=",")[0].iloc[:-2]
data.columns = data.columns.get_level_values(1)
data =  data.loc[:, ~data.columns.duplicated()]
data.dropna(subset=['Směna'], inplace=True)
data['date'] = (data['Datum'].str.split(' ').str[1].str[:-1] + f'.{dt.datetime.now().year}').apply(parse, dayfirst=True)
data['Datum objednávky'] = data['date'].apply(lambda row: row.replace(day=1))
data['Datum vystoupení'] = data['date']
data['Typ vystoupení / specifikace'] = '3 ceremoniály'
data['Čas trvání min.'] = (data['Délka'].astype(int)/100*60).astype(int)
data['Jméno klienta'] = 'Wellness resort s.r.o.'

data.iloc[:,6:].to_csv(f"{fn.rsplit('.', 1)[0]}.csv", index=False, header=True)