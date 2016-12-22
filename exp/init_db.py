#!/usr/bin/env python
import requests
import json

S = requests.Session()



list_data = {
    'all': {
        'hosts': ['localhost'],
        'vars': {
            'ansible_ssh_user': 'root',
            'ansible_ssh_pass': 'yangxiao'
        },
    }
}

host_data = {
    # 'ansible_ssh_user': 'root',
    # 'ansible_ssh_pass': 'yangxiao'
}

r = S.post("http://127.0.0.1:8000/insert/", {'key': "hosts", 'value': "localhost"}, timeout=20)

print r.content


r = S.post("http://127.0.0.1:8000/insert/",
        # {'key': "localhost", 'value': "good{}{}{}{}}{}"}, timeout=20)
        {'key': "hosts", 'value': json.dumps(list_data)}, timeout=20)
print r.content


r = S.post("http://127.0.0.1:8000/insert/",
        # {'key': "localhost", 'value': "good{}{}{}{}}{}"}, timeout=20)
        {'key': "localhost", 'value': json.dumps(host_data)}, timeout=20)
print r.content


r = S.post("http://127.0.0.1:8000/query/",
        {'key': "localhost"}, timeout=20)
print json.loads(r.content)['ret']


r = S.post("http://127.0.0.1:8000/query/",
        {'key': "hosts"}, timeout=20)
print json.loads(r.content)['ret']

