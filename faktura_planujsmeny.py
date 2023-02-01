#!/usr/bin/env python3

import pandas as pd
from dateutil.parser import  parse
import sys

fn = sys.argv[1]
import datetime as dt
import pandas as pd
from dateutil.parser import  parse

data = pd.read_html(fn, decimal=",")[0].iloc[:-2]
data.columns = data.columns.get_level_values(1)
data = data.loc[:, ~data.columns.duplicated()]
data.dropna(subset=['Směna'], inplace=True)
data['date'] = (data['Datum'].str.split(' ').str[1].str[:-1] + f'.{dt.datetime.now().year}').apply(parse, dayfirst=True)
data['Datum objednávky'] = data['date'].apply(lambda row: row.replace(day=1))
data['Datum vystoupení'] = data['date']
data['Typ vystoupení / specifikace'] = '3 ceremoniály'
data['Čas trvání min.'] = (data['Délka'].str.replace(",", "").str.split().apply(lambda row: sum(map(float, row))).astype(float)/100*60)
data['Jméno klienta'] = 'Wellness resort s.r.o.'
data.iloc[:,4:].to_csv(f"{fn.rsplit('.', 1)[0]}.csv", index=False, header=True)