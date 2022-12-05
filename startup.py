import asyncio
import traceback
from elasticsearch import AsyncElasticsearch
import sys
import json
from message_helper import generateMessage
from telegram_bot import send_error, send_message
import time
from datetime import datetime, timedelta
from dateutil import parser

elastic_url = sys.argv[1]  # URL to Elasticsearch
# elastic_usr = sys.argv[2] # Elasticsearch Username
# elastic_pwd = sys.argv[3] # Elasticsearch Password

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
    # Load spec from file
    i = 0
    spec_list = json.load(open('es-query.json', 'r'))
    for spec in spec_list:
        try:
            i += 1
            # init query range
            time_now = datetime.now()
            lte = spec['last-lte']
            # if lte is not set, set it to now. And set gte to now + 1 hour
            if lte == '':
                gte = format_time(time_now - timedelta(hours=1))
                lte = format_time(time_now)
            # if lte is set, set gte to lte. lte + 1 hour
            else:
                gte = lte
                lte = format_time(time_now)

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
            with open('query.json', 'w') as f:
                f.write(json.dumps(query))
            resp = await es.search(**query)
            data = resp['hits']['hits']
            if len(data) > 0:
                msg_list = []
                for d in data:
                    fmsg = d['fields']['message'][0]
                    fmsg = fmsg.replace('<script>', '<scr*pt>')
                    fmsg = fmsg.replace('</script>', '</scr*pt>')
                    if fmsg not in msg_list:
                        msg_list.append(fmsg)
                        msg = generateMessage(d, spec['query-name'], spec['query-type'])
                        send_message(msg)
                        time.sleep(5)

            # update last-lte
            spec['last-lte'] = lte

            # update spec file
            with open('es-query.json', 'w') as f:
                json.dump(spec_list, f)
        except Exception as e:
            send_error('[So TTTT VP] Error: ' + str(traceback.format_exc()))
    end = time.time()
    # return elapsed time
    return f'done in {end-start} seconds. {i} requests sent'


async def startup():
    while True:
        elapsed_time = await start_alert()
        print(elapsed_time)
        time.sleep(20)

asyncio.run(startup())
