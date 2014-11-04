#!/opt/anaconda/bin/python

import os
import datetime
import time
import schedule
from nest_thermostat import Nest
from pymongo import MongoClient

def getDataStructure (nc):
    
    result = {}
    
    timestamp = datetime.datetime.utcnow()
    result['date'] = timestamp
    
    for structure in nc.structures:
        weather = structure.weather.current
        wind = weather.wind
        structres = {}
        
        structres['postal_code'] = structure.postal_code

        for i, dev in enumerate(structure.devices):
            structres['dev{}'.format(i)] = {
                'temperature':  dev.temperature,
                'humidity':     dev.humidity,
                'fan':          dev.fan,
                'mode':         dev.mode,
                'target':       dev.target,
            }
        
        
        structres['outdoor'] = {
            'condition':    weather.condition,
            'humidity':     weather.humidity,
            'temperature':  weather.temperature,
            'wind': {
                #'azimuth':      wind.azimuth,
                'direction':    wind.direction,
                'kph':          wind.kph,
            },
        }
        
        result[structure.name] = structres

    return result

def dumpReadings ():
    nestlogin = os.environ.get('NESTLOGIN')
    mongologin = os.environ.get('MONGOURI')

    if (nestlogin is not None) and (mongologin is not None):
        nest = Nest(*nestlogin.split(':'))
        client = MongoClient(mongologin)
    else:
        raise EnvironmentError

    record = getDataStructure(nest)
    col = client.nest.records
    col.insert(record)
    
    print(record['date'].isoformat())

if __name__ == '__main__':

    interval = os.environ.get('INTERVAL')
    if interval is not None:
        interval = int(interval)
    else:
        interval = 60
    
    schedule.every(interval).minutes.do(dumpReadings)
    
    while True:
        schedule.run_pending()
        time.sleep(30)