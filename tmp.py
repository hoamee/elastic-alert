from dateutil import parser
from datetime import datetime, timedelta

datestring = '2022-01-31 00:01:02'
yourdate = parser.parse(datestring) + timedelta(milliseconds=10)
printdate = yourdate.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z'
print(datestring)
print(yourdate)

# yourdate = datetime.now()
# mydate =  datetime.now() - timedelta(hours=48)
# diff = yourdate - mydate
# seconds_in_day = 24 * 60 * 60
# print(diff.total_seconds()/3600)
