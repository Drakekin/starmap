import json
import requests
import re
import sys
import time
import datetime

with open("starcatalogue.json") as json_catalogue:
    RAW_STARMAP = json.load(json_catalogue)["Stars"][20815+1358+14513:]

NAMES = {}
n = 0
start = time.time()
sleep = 0.05

for s, star in enumerate(RAW_STARMAP):
    hip = star["HIP"]
    simbad = requests.get("http://simbad.u-strasbg.fr/simbad/sim-id?Ident=HIP%20{}&output.format=ASCII".format(hip)).text
    print("~", end="")
    n += 1
    if n == 50:
        print()
        now = time.time()
        delta = now - start
        each = delta / s
        eta = (len(RAW_STARMAP) - s) * each
        finish = datetime.datetime.now() + datetime.timedelta(seconds=eta)
        print("{} of {}, {}% done, {}rps/{}s per request, {}s sleep per request, eta {}".format(s, len(RAW_STARMAP), round(s/len(RAW_STARMAP)*100, 2), round(1/each, 2), round(each, 2), round(sleep, 2), finish))
        n = 0
    else:
        sys.stdout.flush()
    name = re.findall(r"NAME\s+((\s?[^\s])+)+\s\s+", simbad)
    if name:
        n = 0
        print()
        names = [n[0] for n in name]
        NAMES[hip] = names
        print(hip, names)
    time.sleep(sleep)

with open("iaunames.json", "w") as out:
    json.dump(NAMES, out)

