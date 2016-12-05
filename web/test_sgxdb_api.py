#!/usr/bin/env python
#coding:utf8

import requests

S = requests.Session()


# print r.status_code, r.content, r.cookies, r.headers

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'data': "good"}, timeout=20)
print r.content


print "inserting..."
r = S.post("http://127.0.0.1:8000/insert/", {'data': "good"}, timeout=20)
print r.content


print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'data': "good"}, timeout=20)
print r.content


print "deleting..."
r = S.post("http://127.0.0.1:8000/delete/", {'data': "good"}, timeout=20)
print r.content


print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'data': "good"}, timeout=20)
print r.content
