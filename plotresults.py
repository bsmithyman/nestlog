#!/opt/anaconda/bin/python

import os
from datetime import datetime
import plotly.plotly as py
from plotly.graph_objs import *
from pymongo import MongoClient

plotlylogin = os.environ.get('PLOTLYLOGIN')
mongologin = os.environ.get('MONGOURI')

if (plotlylogin is not None) and (mongologin is not None):
    py.sign_in(*plotlylogin.split(':'))
    client = MongoClient(mongologin)
    col = client.nest.records
else:
    raise EnvironmentError

records = [item for item in col.find()]
structures = records[0].keys()
structures.remove('_id')
structures.remove('date')

# Nest config
structure = structures[0]
thermostat = 'dev0'

# Plotting configuration
baseline = {
    'width': 5,
    'smoothing': 10,
}
iline = baseline.copy()
oline = baseline.copy()
tline = baseline.copy()
iline['color'] = 'orange'
oline['color'] = 'blue'
tline['color'] = 'gray'

# Put together data 'arrays'
dates = [item['date'] for item in records]
itemp = [item[structure][thermostat]['temperature'] for item in records]
otemp = [item[structure]['outdoor']['temperature']  for item in records]
ttemp = [item[structure][thermostat]['target']      for item in records]

# Create plot
data = Data([
    Scatter(x=dates, y=otemp, name='Outdoor Temp.', line=oline),
    Scatter(x=dates, y=ttemp, name='Target Temp.',  line=tline),
    Scatter(x=dates, y=itemp, name='Indoor Temp.',  line=iline),
    ])
plot_url = py.plot(data, filename='nest-logs', auto_open=False)

# Output URL
print(plot_url)

