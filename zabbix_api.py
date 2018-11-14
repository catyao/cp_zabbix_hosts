#-*-coding:utf-8-*-

# import requests
import json
import urllib.request
import customfunction

def requestJson(url, values):
    data = json.dumps(values)
    # print(data)
    data = bytes(data, 'utf8')
    #req = requests.post(url, data, {'Content-Type': 'application/json'})
    header = {"Content-Type":"application/json"}
    request = urllib.request.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    result = urllib.request.urlopen(request)
    res = result.read().decode('utf-8')
    output = json.loads(res)
    #print(output)
    #print(response.content)
    #    print output
    try:
        message = output['result']
    except:
        message = output['error']['data']
        # print(message)

    return message

class zabbix_api_jobs(object):
    def __init__(self, url, name, password,auth,huanjing="yum"):
        self.url = url
        self.name = name
        self.huanjin = huanjing
        if auth == "":
            values = {'jsonrpc': '2.0',
                      'method': 'user.login',
                      'params': {
                          'user': name,
                          'password': password
                      },
                      'id': '1',
                      }
            idvalue = requestJson(url, values)
            customfunction.thefunction.authwrite2file(idvalue, huanjing)
            self.auth = idvalue
        else:
            self.auth = auth

    # 得到所有hostgroup信息
    def get_hostgroups(self):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'hostgroup.get',
                  'params': {
                      "output": "extend",
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output[0]

    # 得到所有hostgroup信息
    def get_apiversion(self):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "apiinfo.version",
            "params": [],
            "id": 2
        }
        output = requestJson(self.url, values)
        return output

    # 传入group_name,得到host_id,host_name
    def get_host_id_name_by_group_name(self, group_name):
        auth = self.auth

        values = {'jsonrpc': '2.0',
                  'method': 'hostgroup.get',
                  'params': {
                      "output": "extend",
                      "filter": {
                          "name": group_name
                      },
                      "selectHosts": ['host'],
                      # "selectHosts": ['hostid', 'host'],
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output[0]

    # 删除主机
    def del_host_by_hostid(self, host_id):
        auth = self.auth

        values = {
                    "jsonrpc": "2.0",
                    "method": "host.delete",
                    "params": host_id,
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output
    #得到非模板的item
    def get_not_template_item_by_hostid(self, hostid):
        auth = self.auth

        values = {"jsonrpc": "2.0",
                  "method": "item.get",
                  "params": {
                      "output": "extend",
                      "hostids": hostid,
                      # "search": {
                          # "key_": "system"
                      # },
                      "sortfield": "name"
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output=[]
        output1 = requestJson(self.url, values)
        for i in range(len(output1)):
            if output1[i]["templateid"] == "0" and output1[i]["flags"] == "0":
                # del output1[i]["itemid"]
                output.append(output1[i])
        # output = output1
        return output

    #通过传入的itemid删除字典


    def get_not_template_item_by_hostid_1(self, hostid,itemid):
        auth = self.auth

        values = {"jsonrpc": "2.0",
                  "method": "item.get",
                  "params": {
                      "output": "extend",
                      "hostids": hostid,
                      # "search": {
                          # "key_": "system"
                      # },
                      "sortfield": "name"
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output=[]
        output1 = requestJson(self.url, values)
        for i in range(len(output1)):
            if output1[i]["templateid"] == "0" and output1[i]["flags"] == "0":
                if output1[i]["itemid"] in itemid:
                    pass
                else:
                    output.append(output1[i])
        # output = output1
        return output

    def get_not_template_item_by_hostid_2(self, hostid,itemid):
        auth = self.auth

        values = {"jsonrpc": "2.0",
                  "method": "item.get",
                  "params": {
                      "output": "extend",
                      "hostids": hostid,
                      # "search": {
                          # "key_": "system"
                      # },
                      "sortfield": "name"
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output=[]
        output1 = requestJson(self.url, values)
        for i in range(len(output1)):
            if output1[i]["templateid"] == "0" and output1[i]["flags"] == "0":
                if output1[i]["itemid"] in itemid:
                    output.append(output1[i])

        # output = output1
        return output

    #创建自定义的item项目
    def add_not_template_item_by_hostid(self, hostid, data):
        auth = self.auth
        for i in range(len(data)):
            data[i]["hostid"] = hostid
        print("1111111111111111111111111")
        print(data)
        values = {"jsonrpc": "2.0",
                  "method": "item.create",
                  "params": data,
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    #一个一个增加item
    def add_item_by_hostid(self, hostid, data):
        auth = self.auth
        for i in range(len(data)):
            data[i]["hostid"] = hostid
        values = {"jsonrpc": "2.0",
                  "method": "item.create",
                  "params": data,
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

        # 从host_name得到host_id
    def get_host_id_by_host_name(self, host_names):
        auth = self.auth

        values = {'jsonrpc': '2.0',
                  "method": "host.get",
                  'params': {
                      "output": "extend",
                      "filter": {
                          "host":  host_names
                      },
                      "selectHosts": ['hostids'],
                      # "selectHosts": ['hostid', 'host'],
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output


    def get_ip_by_triggerid(self, triggerid):
        auth = self.auth

        values = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["host","hostid"],
                    "selectInterfaces": ["ip"],
                    "triggerids": triggerid
                },
                'auth': auth,
                'id': '2'
            }
        output = requestJson(self.url, values)
        return output

    def get_hostid_by_host_names(self, host_names):
        auth = self.auth

        values = {'jsonrpc': '2.0',
                  "method": "host.get",
                  'params': {
                      "output": "extend",
                      "filter": {
                          "host":  host_names
                      },
                      "selectHosts": ['hostids'],
                      # "selectHosts": ['hostid', 'host'],
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    def get_itemid_by_triggerid(self, triggerid):
        auth = self.auth

        values = {
                "jsonrpc": "2.0",
                "method": "trigger.get",
                "params": {
                    "triggerids": triggerid,
                    "output": "extend",
                    "selectItems": "extend"
                },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    #  得到宏
    def get_usermacro_by_host_id(self, host_id):
        auth = self.auth

        values = {  "jsonrpc": "2.0",
                    "method": "usermacro.get",
                    "params": {
                    "output": "extend",
                    "hostids": host_id
                    },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output    
    #写入宏
    def add_usermacro_by_host_id(self, host_id, data):
        auth = self.auth

        values = {      
                "jsonrpc": "2.0",
                    "method": "usermacro.create",
                    "params": {
                    "hostid": host_id,
                    "macro":  data["macro"],
                    "value":  data["value"],
                    },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output 
        
    # 从主机名得到模板名字
    def get_template_id_name_by_host_id(self, host_id):
        auth = self.auth

        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid"],
                "selectParentTemplates": [
                    "templateid",
                    "name"
                ],
                "hostids": host_id
            },
                      # "selectHosts": ['hostid', 'host'],
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    # 从host_name 得到 host_id
    def get_host_id_name_by_host_name(self, host_name):
        auth = self.auth

        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid"],
                "selectGroups": "extend",
                "filter": {
                    "host": host_name
                }
            },
                      # "selectHosts": ['hostid', 'host'],
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    # 从host_id得template_id

    def test(self, host_id):
        auth = self.auth
        values = {
                  "jsonrpc": "2.0",
                  "method": "host.get",
                  "params": {
                      "output": "extend",
                      "filter": {
                          "hostid": host_id
                      }
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    # 从名字得到主机
    def get_host_by_name(self,name):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'host.get',
                  'params': {
                      "output": "extend",
                      "filter": {
                          "host": [
                              name
                          ]
                      }
                  },
                  'auth': auth,
                  'id': '3'
                  }
        output = requestJson(self.url, values)
        return output

    # 创建主机
    # def create_host(self,data):
    #     auth = self.auth
    #     values = {'jsonrpc': '2.0',
    #               'method': 'host.create',
    #               'params': {
    #                   "host": data["host"],
    #                   "groups": data["group"],
    #                   "templates": data["templates"],
    #                   "interfaces": data["interface"]
    #               },
    #               'auth': auth,
    #               'id': '4'
    #               }
    #     output = requestJson(self.url, values)
    #     return output

    # 得到主机所在的组
    def get_group_id_name_by_host_id(self,hostid):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'hostgroup.get',
                  'params': {
                      "output": "extend",
                      "hostids": hostid
                  },
                  'auth': auth,
                  'id': '5'
                  }
        output = requestJson(self.url, values)
        return output

    # 从名字得到主机组
    def get_hostgroup_by_name(self,name):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'hostgroup.get',
                  'params': {
                      "output": "extend",
                      "filter": {
                          "name": name
                      }
                  },
                  'auth': auth,
                  'id': '6'
                  }
        output = requestJson(self.url, values)
        return output

    # 创建组机组
    def create_hostgroup(self,name):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'hostgroup.create',
                  'params': {
                      "name": name
                  },
                  'auth': auth,
                  'id': '7'
                  }
        output = requestJson(self.url, values)
        return output

    # 得到主机的triggers
    def get_triggersid_by_host_id(self, host_id):
        auth = self.auth

        values = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["triggersid"],
                    "selectTriggers": [
                        "triggersid",
                    ],
                    "hostids": host_id
                },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        output1 = []
        for i in range(len(output[0]["triggers"])):
            output1.append(output[0]["triggers"][i]["triggerid"])
        return output1

    #得到triggers为自定的
    def get_no_template_triggersid_by_triggerid(self, trigger_id):
        auth = self.auth

        values = {
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                        "triggerids": trigger_id,
                        "output": "extend",
                        "selectFunctions": "extend",
                        # "filter": {
                        #     "flags": 0,
                        #     "templateid": ""
                        # },
                    },
                  'auth': auth,
                  'id': '2'
                  }
        output1 = []
        output = requestJson(self.url, values)
        for i in range(len(output)):
            if output[i]["flags"] == "0" and output[i]["templateid"] == "0":
                output1.append(output[i]["triggerid"])
        return output1

    def get_trigger_by_triggerid(self, trigger_id):
        auth = self.auth

        values = {
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                        "triggerids": trigger_id,
                        "output": "extend",
                        "expandExpression": "extend"
                    },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    def create_trigger(self, data):
        auth = self.auth

        values = {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": data,
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output


    #通过trigger得到trigger详细信息
    def get_trigger_triggersid_by_triggerid(self, trigger_id):
        auth = self.auth

        values = {
                    "jsonrpc": "2.0",
                    "method": "trigger.get",
                    "params": {
                        "triggerids": trigger_id,
                        "output": "extend",
                        "selectFunctions": "extend",
                        # "filter": {
                        #     "flags": 0,
                        #     "templateid": ""
                        # },
                    },
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output




    #通过hostname得到没有模板的itemid
    def get_no_template_itemid_by_hostid(self, host_id):
        auth = self.auth

        values = {"jsonrpc": "2.0",
                  "method": "item.get",
                  "params": {
                      "output": "extend",
                      "hostids": host_id,
                      # "search": {
                      # "key_": "system"
                      # },
                      "sortfield": "name"
                  },
                  'auth': auth,
                  'id': '2'
                  }
        output = []
        output1 = requestJson(self.url, values)
        for i in range(len(output1)):
            if output1[i]["templateid"] == "0" and output1[i]["flags"] == "0":
                # del output1[i]["itemid"]
                output.append(output1[i]["itemid"])
        # output = output1
        return output


    def check_no_template_by_itemid(self, item_id):
        auth = self.auth

        values = {
                    "jsonrpc": "2.0",
                    "method": "item.get",
                    "params": {
                        "output": "extend",
                        "itemids": item_id,
                        "sortfield": "name"
                    },
                  'auth': auth,
                  'id': '2'
                  }

        output1 = requestJson(self.url, values)
        output = []
        for i in range(len(output1)):
            if output1[i]["templateid"] == "0" and output1[i]["flags"] == "0":
                # del output1[i]["itemid"]
                output.append(output1[i]["itemid"])
        # output = output1
        return output

    def get_host_all_by_host_id(self, host_id):
        auth = self.auth

        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": "extend",
                "filter": {
                    "hostid": host_id
                }
            },
                      # "selectHosts": ['hostid', 'host'],
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output


    def get_host_interfaces_by_host_id(self, host_id):
        auth = self.auth

        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    # "interfaceid",
                    "type",
                    "main",
                    "userip",
                    "dns",
                    "port",
                    "ip"
                ],
                "filter": {
                    "hostid": host_id
                }
            },
                      # "selectHosts": ['hostid', 'host'],
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output

    def get_host_interfaceid_by_host_id(self, host_id):
        auth = self.auth

        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": [
                    "hostid",
                    "host"
                ],
                "selectInterfaces": [
                    "interfaceid",
                    "type",
                    "main",
                    "userip",
                    "dns",
                    "port",
                    "ip"
                ],
                "filter": {
                    "hostid": host_id
                }
            },
                      # "selectHosts": ['hostid', 'host'],
                  'auth': auth,
                  'id': '2'
                  }
        output = requestJson(self.url, values)
        return output[0]["interfaces"][0]["interfaceid"]

    def create_host(self, data):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": data["host"],
                "name": data["name"],
                "interfaces": [
                    {
                        "type":     data["interfaces"]["type"],
                        "main":     data["interfaces"]["main"],
                        "useip":    1,
                        "ip":       data["interfaces"]["ip"],
                        "dns":      "",
                        "port":     data["interfaces"]["port"],
                    }
                ],
                "proxy_hostid":     data["proxy_hostid"],
                "groups":           data["groupid"],
                "templates":        data["templateid"],
                "inventory_mode":   0,
            },
            "auth": auth,
            "id": 4
        }
        # print(data)
        output = requestJson(self.url, values)
        return output


    # 得到所有模板
    def get_all_templates(self):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'template.get',
                  'params': {
                      "output": "extend",
                  },
                  'auth': auth,
                  'id': '8'
                  }
        output = requestJson(self.url, values)
        return output

    def get_all_trigger(self):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "filter": {
                    "value": 1
                },
                "sortfield": "priority",
                "sortorder": "DESC",
                "active": 1,
                "expandDescription": 1,
                "expandComment": 1,
                "expandExpression": 1,
                "only_true": 1

            },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def get_all_monitored_trigger(self, \
                                  active=0,\
                                  expandDescription=1, \
                                  expandComment=1, \
                                  expandExpression=1, \
                                  monitored=1, \
                                  only_true=1\
                                  ):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "filter": {
                    "value": 1
                },
                "sortfield": "priority",
                "sortorder": "DESC",
                "active": active,
                "expandDescription": expandDescription,
                "expandComment": expandComment,
                "expandExpression": expandExpression,
                "monitored": monitored,
                "only_true": only_true

            },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def get_host_id_by_trigger_id(self, trigger_id):
        auth = self.auth
        values = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": host_id,
            "filter": {
                "itemid" : item_id
            },
            "sortfield": "name"
        },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def get_item_value_by_host_id_item_id(self, host_id, item_id):
        auth = self.auth
        values = {
        "jsonrpc": "2.0",
        "method": "item.get",
        "params": {
            "output": "extend",
            "hostids": host_id,
            "filter": {
                "itemid" : item_id
            },
            "sortfield": "name"
        },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def get_all_trigger(self):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": "extend",
                "filter": {
                    "value": 1
                },
                "sortfield": "priority",
                "sortorder": "DESC",
                "active": 1,
                "expandDescription": 1,
                "expandComment": 1,
                "expandExpression": 1,
                "only_true": 1

            },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def disable_action_by_action_id(self, action_id):
        auth = self.auth
        values = {
                "jsonrpc": "2.0",
                "method": "action.update",
                "params": {
                    "actionid": action_id,
                    "status": "1"
                },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def enable_action_by_action_id(self, action_id):
        auth = self.auth
        values = {
                "jsonrpc": "2.0",
                "method": "action.update",
                "params": {
                    "actionid": action_id,
                    "status": "0"
                },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def get_httptest_by_httptest_id(self, httptest_id):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "httptest.get",
            "params": {
                "output": "extend",
                "selectSteps": "extend",
                "httptestids": httptest_id
            },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def add_httptest(self, data):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "httptest.create",
            "params": data,
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output


    def get_httptest_id_by_host_id(self, host_id):
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["hostid"],
                "selectHttpTests": [
                    "httptestid"
                ],
                "hostids": host_id
            },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output

    def get_all_action_id(self, status="enable2disable"):
        if status == "disable2enable":
            thestatus = 1
        else:
            thestatus = 0
        auth = self.auth
        values = {
            "jsonrpc": "2.0",
            "method": "action.get",
            "params": {
                "output": "actionid",
                "filter": {
                    "eventsource": 0,
                    "status": thestatus
                }
            },
                  'auth': auth,
                  'id': 2
                  }
        output = requestJson(self.url, values)
        return output
    # 增加主机模板
    def add_templates_by_host(self,hostid,template_ids):
        auth = self.auth
        values = {'jsonrpc': '2.0',
                  'method': 'host.update',
                  'params': {
                      "output": "extend",
                      "hostid": hostid,
                      "templates": []
                  },
                  'auth': auth,
                  'id': '9'
                  }
        origin_templates = self.get_template_by_host(hostid)
        origin_ids = []
        if len(origin_templates) > 0:
            for item in origin_templates:
                origin_ids.append(item["templateid"])
        for id in template_ids:
            if id in origin_ids:
                origin_ids.remove(id)
            values["params"]["templates"].append({"templateid": id})
        for id in origin_ids:
            values["params"]["templates"].append({"templateid": id})
        output = requestJson(self.url, values)
        return output


