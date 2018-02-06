import json
import requests
import re
import sys
import time
import datetime

with open("starcatalogue.json") as json_catalogue:
    RAW_STARMAP = json.load(json_catalogue)["Stars"][79249:]

NAMES = {}
n = 0
start = time.time()
sleep = 0.05

for s, star in enumerate(RAW_STARMAP):
    hip = star["HIP"]
    simbad = requests.get("http://simbad.u-strasbg.fr/simbad/sim-id?Ident=HIP%20{}&output.format=ASCII".format(hip)).text
    n += 1
    if n == 50:
        now = time.time()
        delta = now - start
        each = delta / s
        eta = (len(RAW_STARMAP) - s) * each
        finish = datetime.datetime.now() + datetime.timedelta(seconds=eta)
        print("{} of {}, {}% done, {}rps/{}s per request, {}s sleep per request, eta {}".format(s, len(RAW_STARMAP), round(s/len(RAW_STARMAP)*100, 2), round(1/each, 2), round(each, 2), round(sleep, 2), finish))
        n = 0
    spec_type = re.findall(r"Spectral type: ([A-Za-z0-9\-]+)", simbad)
    if spec_type:
        names = spec_type[0]
        NAMES[hip] = names
        print(hip, names)
    else:
        print(hip, "FAILED")
    time.sleep(sleep)

with open("spectypes.json", "w") as out:
    json.dump(NAMES, out)

