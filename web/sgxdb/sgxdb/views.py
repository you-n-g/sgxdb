#!/usr/bin/env python
#coding:utf8


from sgxdblib import SGXDB
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
import os


@require_POST
def insert(request):	
    key = request.POST.get("key", None)
    value = request.POST.get("value", None)
    code = 0
    if key is None or value is None:
        code = 1
    else:
        try:
            SGXDB.insert(key, value)
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code})


@require_POST
def delete(request):	
    key = request.POST.get("key", None)
    code = 0
    if key is None:
        code = 1
    else:
        try:
            SGXDB.delete(key)
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code})


@require_POST
def query(request):	
    key = request.POST.get("key", None)
    ret = None
    code = 0
    if key is None:
        code = 1
    else:
        try:
            ret = SGXDB.query(key)
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code, "ret": ret})

SEALED_DATA_NAME = "conf.sealed"


@require_POST
def save(request):
    code = 0
    try:
        ret = SGXDB.export_sealed_data()
        with open(os.path.join(settings.BASE_DIR, "conf.sealed"), 'w') as f:
            f.write(ret)
    except RuntimeError:
        code = 1
    return JsonResponse({"code": code})


@require_POST
def load(request):
    code = 0
    dpath = os.path.join(settings.BASE_DIR, "conf.sealed")
    if not os.path.exists(dpath):
        code = 2
    else:
        try:
            with open(dpath, 'r') as f:
                SGXDB.import_sealed_data(f.read())
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code})

