#!/usr/bin/env python
#coding:utf8


from sgxdblib import SGXDB
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@require_POST
def insert(request):	
    data = request.POST.get("data", None)
    code = 0
    if data == None:
        code = 1
    else:
        try:
            SGXDB.insert(data)
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code})



@require_POST
def delete(request):	
    data = request.POST.get("data", None)
    code = 0
    if data == None:
        code = 1
    else:
        try:
            SGXDB.delete(data)
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code})

@require_POST
def query(request):	
    data = request.POST.get("data", None)
    ret = None
    code = 0
    if data == None:
        code = 1
    else:
        try:
            ret = SGXDB.query(data)
        except RuntimeError:
            code = 1
    return JsonResponse({"code": code, "ret": ret})
