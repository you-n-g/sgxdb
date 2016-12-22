#!/usr/bin/env python
# coding:utf8

import sys
import os
import re
from optparse import OptionParser
import json
import copy
import yaml
import requests
import json

S = requests.Session()

DIRNAME = os.path.abspath(os.path.dirname(__file__))


def query(key):
    r = S.post("http://127.0.0.1:8000/query/",
	    {'key': key}, timeout=20)
    res = json.loads(r.content)
    if int(res['code']) != 0:
        raise RuntimeError("Error when querying")
    return res["ret"]



def get_hosts():
    hosts = query("hosts")
    if hosts is None:
        raise KeyError("No such query")
    return json.loads(hosts)


def pick_host(name):
    host_config = query(name)
    if host_config is None:
        raise KeyError("No such query")
    return json.loads(host_config)


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option(
        "--list",
        action="store_true",
        dest="list_host",
        default=None,
        help="list hosts"
    )
    parser.add_option(
        "--host",
        dest="host_name",
        help="get info about a HOST",
        metavar="HOST"
    )

    (options, args) = parser.parse_args()

    if options.host_name:
        print(pick_host(options.host_name))
        sys.exit(0)

    if options.list_host:
        print(json.dumps(get_hosts()))
        sys.exit(0)
