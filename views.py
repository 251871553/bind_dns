# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from  dns_api.dns_server import *
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
@csrf_exempt
#head必须Content-Type: application/json
#查询一个区域下所有记录：
#{"env":"test","name_zone":"cloud.bz","action":"list_record"}
#加记录：
#{"env":"test","name_zone":"cloud.bz","action":"add","domain_name":"what","record_type":"A","record":"1.1.1.1"}
#修改记录
#{"env":"test","name_zone":"cloud.bz","action":"edit","domain_name":"what","record_type":"A","record":"6.6.6.6"}
#删除记录
#{"env":"test","name_zone":"cloud.bz","action":"del","domain_name":"what","record_type":"A","record":"6.6.6.6"}


def index(request):
    if request.method == "GET":
        return HttpResponse('success')
    elif request.method == "POST":
        if request.content_type == "application/json":
           req = json.loads(request.body)
           #print(req)
        else:
           return HttpResponse(json.dumps({'code': 1000, 'message': 'bed content_type'}))
        try:
           env=req['env']
        except KeyError:
           return HttpResponse(json.dumps({'code': 1001, 'message': 'loss env parameter'}))
        my_ops = mydns_api(env)
        try:
           zone=req['name_zone']
        except KeyError:
           return HttpResponse(json.dumps({'code': 1002, 'message': 'loss name_zone parameter'}))
        domain_name=req.get('domain_name')
        ttl=req.get('ttl', 300)
        record=req.get('record')
        record_type=req.get('record_type')
        try:
           msg=''
           if req['action'] == 'list_record':
               msg={'code': 0, 'message': my_ops.zone_list(zone)}
           elif req['action'] == 'add':
               msg=my_ops.add_record(zone, domain_name, ttl, record_type, record)
           elif req['action'] == 'del':
               msg=my_ops.del_record(zone, domain_name, record_type)
           elif req['action'] == 'edit':
               msg=my_ops.edit_record(zone, domain_name, ttl, record_type, record)
           elif req['action'] == 'search':
               msg=my_ops.search_record(domain_name+'.'+zone, record_type)
           else:
               msg={'code': 2001, 'message': 'action parameter error'}
           return HttpResponse(json.dumps(msg))
        except KeyError:
            return HttpResponse(json.dumps({'code': 1003, 'message': 'loss action parameter'}))
    else:
        return HttpResponse(json.dumps({'code': 0000, 'message': 'request model error'}))
