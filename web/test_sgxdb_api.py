#!/usr/bin/env python
#coding:utf8

import requests

S = requests.Session()


# print r.status_code, r.content, r.cookies, r.headers

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "good"}, timeout=20)
print r.content


print "inserting..."
r = S.post("http://127.0.0.1:8000/insert/", {'key': "good", 'value': "good_value"}, timeout=20)
print r.content


print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "good"}, timeout=20)
print r.content


print "deleting..."
r = S.post("http://127.0.0.1:8000/delete/", {'key': "good"}, timeout=20)
print r.content


print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "good"}, timeout=20)
print r.content

print "Testing saving and loading" + '-' * 30

print "inserting..."
r = S.post("http://127.0.0.1:8000/insert/", {'key': "bad", 'value': "bad_value"}, timeout=20)
print r.content

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "good"}, timeout=20)
print r.content

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "bad"}, timeout=20)
print r.content

print "saving..."
r = S.post("http://127.0.0.1:8000/save/", {}, timeout=20)
print r.content

print "deleting..."
r = S.post("http://127.0.0.1:8000/delete/", {'key': "bad"}, timeout=20)
print r.content

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "good"}, timeout=20)
print r.content

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "bad"}, timeout=20)
print r.content

print "loading..."
r = S.post("http://127.0.0.1:8000/load/", {}, timeout=20)
print r.content

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "good"}, timeout=20)
print r.content

print "querying..."
r = S.post("http://127.0.0.1:8000/query/", {'key': "bad"}, timeout=20)
print r.content
