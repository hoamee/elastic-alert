import asyncio
import traceback
from elasticsearch import AsyncElasticsearch
import sys
import json
from message_helper import generateMessage
from telegram_bot import send_error, send_message, send_file
import time
from datetime import datetime, timedelta
import os
import subprocess

elastic_url = sys.argv[1]  # URL to Elasticsearch
# elastic_usr = sys.argv[2] # Elasticsearch Username
# elastic_pwd = sys.argv[3] # Elasticsearch Password
telegram_token = sys.argv[2]  # Telegram Bot Token

# Initialize Elasticsearch
es = AsyncElasticsearch(
    elastic_url,
    # basic_auth=(elastic_usr, elastic_pwd),
    # ca_certs='./http_ca.crt',
    verify_certs=False,
    request_timeout=1800

)


def format_time(dt: datetime):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'


async def start_alert():
    start = time.time()
    subprocess.call(["curl", "https://raw.githubusercontent.com/hoamee/elastic-alert/main/es-query.json", "--output", "es-query.json"], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
    # Load spec from file
    i = 0
    spec_list = json.load(open('es-query.json', 'r'))
    time_now = datetime.now() - timedelta(minutes=3)
    time_now_str = format_time(time_now)
    config = json.load(open('config.json', 'r'))
    
    # init query range
    last_lte = config['last-lte']
    # if lte is not set, set it to now. And set gte to now + 1 hour
    if last_lte == '':
        gte = format_time(time_now - timedelta(hours=2))
    # if lte is set, set gte to lte. lte + 1 hour
    else:
        gte = last_lte
    
    lte = time_now_str
    
    for spec in spec_list:
        try:
            i += 1
            # put lte and gte to query
            query = spec['query']
            for q in query['query']['bool']['filter']:
                try:
                    q['range']['@timestamp']['gte'] = gte
                    q['range']['@timestamp']['lte'] = lte
                    break
                except:
                    pass
            # send request to Elasticsearch
            resp = await es.search(**query)
            data = resp['hits']['hits']
            if len(data) > 0:
                msg_list = []
                for d in data:
                    fmsg = d['fields']['message'][0]
                    while_list = False
                    if fmsg not in msg_list:
                        msg_list.append(fmsg)
                        
                        # check whitelist
                        for w in spec['white-list']:
                            if w in fmsg:
                                while_list = True
                                break
                        
                        if while_list:
                            continue
                        
                        msg = ''
                        file_name = ''
                        
                        
                        if spec['query-type'] != 'rdp':
                            if len(fmsg) >= 3000:
                                file_name = f"log_{time_now_str}_{str(i)}.txt"
                                d['fields']['message'][0] = f'Please check attachment bellow for full message ({file_name})'
                                with open(file_name, 'w') as f:
                                    f.write(fmsg)
                        
                        msg = generateMessage(d, spec)
                            
                        send_message(msg, telegram_token)
                        if(file_name != ''):
                            time.sleep(1)
                            send_file(file_name, telegram_token)
                            os.remove(file_name)
                        time.sleep(5)            
        except:
            send_error('[So TTTT VP] Error: ' + str(traceback.format_exc()), telegram_token)
    # save lte to config
    config['last-lte'] = lte
    with open('config.json', 'w') as f:
            json.dump(config, f)    
    end = time.time()
    # return elapsed time
    return f'done in {end-start} seconds. {i} requests sent'


async def startup():
    while True:
        elapsed_time = await start_alert()
        print(elapsed_time)
        time.sleep(20)

asyncio.run(startup())
