import falcon
import json
import os

class Info(object):

    def on_get(self, req, resp):

        inf = {
            "name": "msbwt-falcon server",
            "desc": "A REST-ful API for delivering genomics queries.",
            "target": get_target()
        }

        resp.body = json.dumps(inf, ensure_ascii=False)

def get_target():
    if not os.path.isdir("/msbwt"):
        return "No BWT Loaded"
    return [f for f in os.listdir("/msbwt") if os.path.isdir(f)][0]

