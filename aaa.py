import json
import datetime

start = datetime.datetime.now()
end = start + datetime.timedelta(seconds=20)

import sys
input = sys.argv[2]

f = open(input,"w+")

log = json.loads(f.read()).get("log")
print(log)

d = {
    "result" : "pass",
    "log" : "C:\\Users\\jinchao\\AutoTest\\a.txt",
    "startTime" : '2020-12-10 21:46:38',
    "endTime" : '2020-12-10 21:46:57'
}

with open("result.json") as f:
    f.write(json.dumps(d))
