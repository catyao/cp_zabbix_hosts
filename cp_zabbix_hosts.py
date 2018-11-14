#-*-coding:utf-8-*-
from zabbix_api import zabbix_api_jobs
from customfunction import thefunction as func
import configparser
import sys

APP_HOME = sys.path[0]

useargv = True
# useargv = False
source_host_name1 = 'st-phdido2.0-online-dmz-3.novalocal'
tragetIps_Temp1 = "123|172.31.123.123|FORCE"

#使用变量还是传参

argvtemp = '''-----------------------
# 用法:
# cp_zabbix_hosts.py '源主机（zabbix中的主机名：第一行）' '目标主机名1|目标主机ip1|FORCE（表示强制删除，留空为不删除）,目标主机名2|目标主机ip2,目标主机名3|目标主机ip3...'
# 例如:
# cp_zabbix_hosts.py 'SGH01VVAT05' '02-S-V-C-00994|172.17.216.21|FORCE,02-S-V-C-00995|172.17.216.22'
-----------------------
'''

print("*"*60)
if useargv is False:
    print("开始使用脚本内部变量source_host_name1和tragetIps_Temp1执行添加步骤")
    source_host_name = source_host_name1
    tragetIps_Temp = tragetIps_Temp1
else:
    print("开始使用外部传参执行添加步骤")
    if len(sys.argv)==1:
        print("参数错误")
        print(argvtemp)
        sys.exit()
    else:
        # source_host_name='SGH01VVAT05'
        source_host_name=sys.argv[2]
        #复制的目标机
        # tragetIps_Temp = "02-S-V-C-00994|172.17.216.21,02-S-V-C-00995|172.17.216.22"
        tragetIps_Temp = sys.argv[3]
        huanjing = sys.argv[1]
        if source_host_name == "" or tragetIps_Temp == "":
            print("# 参数错误")
            print(argvtemp)
            # sys.exit(1)


print("# 源机器:【 %s 】" % (source_host_name))
print("# 目标机器:【 %s 】" % (tragetIps_Temp))
print("*"*60)


from zabbix_login import *

# sys.exit()


# tragetIps_Temp = "02-S-V-C-00994|172.17.216.21,02-S-V-C-00995|172.17.216.22"
targetIPs = tragetIps_Temp.strip(',').split(',')
# print(targetIPs)


# source_host_name = "st-phdido2.0-online-dmz-3.novalocal"
source_host_id = zabbix_server.get_host_id_by_host_name(source_host_name)[0]["hostid"]
print(source_host_id)
# sys.exit()
temp1s = zabbix_server.get_template_id_name_by_host_id(source_host_id)      #template id
temp2s = zabbix_server.get_host_all_by_host_id(source_host_id)              #得到host所有信息
temp3s = zabbix_server.get_group_id_name_by_host_id(source_host_id)         #group id
temp4s = zabbix_server.get_not_template_item_by_hostid(source_host_id)      #所有没有模板的item（包含没有trigger的项目）
temp5s = zabbix_server.get_usermacro_by_host_id(source_host_id)             #宏
temp6s = zabbix_server.get_triggersid_by_host_id(source_host_id)            #所有 trigger id
temp7s = zabbix_server.get_no_template_triggersid_by_triggerid(temp6s)      #没有模板的 trigger id

#得到自定义的web test
httptest = zabbix_server.get_httptest_id_by_host_id(source_host_id)
httptest_lists = httptest[0]["httpTests"]
# print(httptest_lists)
httptest_list_all = []
for httptest_list in range(len(httptest_lists)):
    httptest_id = httptest_lists[httptest_list]["httptestid"]
    # print(httptest_id)
    get_httptest = zabbix_server.get_httptest_by_httptest_id(httptest_id)
    del get_httptest[0]["httptestid"]
    del get_httptest[0]["applicationid"]
    # del get_httptest[0]["hostid"]

    # print(get_httptest)
    httptest_list_all.append(get_httptest[0])
# print(httptest_list_all)

# print(temp7s)
# sys.exit()
# temp8s = zabbix_server.get_hostid_by_triggerid(temp7s)                      #没有模板但是有trigger 的 item id
# temp9s = zabbix_server.get_trigger_triggersid_by_triggerid(temp7s)          #trigger all
# temp10s = zabbix_server.get_no_template_itemid_by_hostid(source_host_id)    #没有模板的 item id
# temp12s = zabbix_server.check_no_template_by_itemid(temp8s)                 #判断这个itemid有没有模板
# temp14s = zabbix_server.check_no_template_by_itemid(temp7s)                 #判断这个itemid有没有模板
# temp11s = [ i for i in temp10s if i not in temp12s ]                         #item id 去重
# temp13s = zabbix_server.get_not_template_item_by_hostid_1(source_host_id,temp12s)      #所有没有模板的item（包含没有trigger的项目）
# temp14s = zabbix_server.get_not_template_item_by_hostid_2(source_host_id,temp12s)      #所有没有模板的item（包含没有trigger的项目）
# temp15s = zabbix_server.get_itemid_by_triggerid(temp7s)      #所有没有模板的item（包含没有trigger的项目）
# temp16s = zabbix_server.get_trigger_by_triggerid('257939')      #所有没有模板的item（包含没有trigger的项目）

# print(temp16s)
# sys.exit()
# for i in range(len(temp7s)):
#     a=zabbix_server.get_trigger_by_triggerid(temp7s[i])
#     a[0]["expression"]=a[0]["expression"].replace("SGH01VVAT05","aaa")
#     del a[0]["triggerid"]
#     print(a)
# sys.exit()


groupids = []
for temp2 in range(0, len(temp3s)):
    groupids.append(temp3s[temp2]["groupid"])

available = temp2s[0]["available"]
proxy_hostid = temp2s[0]["proxy_hostid"]
cpTempLates = []
cpGroupID = []
new_host_ids = []
dict={}
dict1={}
for temp1 in range(0, len(temp1s[0]["parentTemplates"])):
    dict['templateid'] = int(temp1s[0]["parentTemplates"][temp1]["templateid"])
    cpTempLates.append(dict)
    dict = {}
for temp3 in range(0, len(temp3s)):
    dict1['groupid'] = int(temp3s[temp3]["groupid"])
    cpGroupID.append(dict1)
    dict1 = {}


sourceInterfaces = []
sourceInterfaces = zabbix_server.get_host_interfaces_by_host_id(source_host_id)

# 批量添加del_host_by_hostid
for targetIP in targetIPs:
    hostname = targetIP.split("|")[0]
    if len(hostname) == 0 or hostname == "":
        print("*" * 60)
        print("hostname参数不对，请确认传入的参数是否正确！！！")
        print("*" * 60)
        sys.exit()
    interface = targetIP.split("|")[1]
    #如果主机存在，强制删除主机
    try:
        forcedelhost = targetIP.split("|")[2]
    except:
        forcedelhost = ""
    name = interface + '_' + hostname
    sourceInterfaces[0]["interfaces"][0]["ip"] = interface
    data = {
        "host":            hostname,
        "name":            name,
        "interfaces":      sourceInterfaces[0]["interfaces"][0],
        "groupid":         cpGroupID,
        "templateid":      cpTempLates,
        "available":       available,
        "proxy_hostid":    proxy_hostid,

    }


    checkhost   = zabbix_server.get_host_id_by_host_name(hostname)
    #如果查找主机长度是0，则表示在zabbix里面找不到数据，可以新增主机
    if forcedelhost == "":
        pass
    else:
        if len(checkhost) == 0:
            pass
        else:
            checkhostid = checkhost[0]["hostid"]
            print("# 主机[%s]需要强制删除，开始强制删除主机，主机id为【 %s 】" % (hostname,checkhostid))
            Ret2 = zabbix_server.del_host_by_hostid([checkhostid])
            if len(Ret2["hostids"]) == 0:
                print("# 删除主机【 %s]失败" % (checkhostid))
            else:
                print("# 删除主机【 %s 】成功" % (Ret2["hostids"]))
                checkhost=[]
    # print(checkhostid)
    # sys.exit()
    if len(checkhost) == 0:
        # try:
        print("*"*60)
        print("# 开始尝试增加机器: %s" % (name))
        # print("*" * 60)
        try:
            new_host = zabbix_server.create_host(data)
            new_host_id = new_host["hostids"]
            print("# 添加机器【  %s  】成功" % (name))

            # new_host_id = ['18198']
            print("# 新机器创建成功,host id :"+new_host_id[0])
            # print(new_host_id)
            # new_host_ids.append(new_host_id)
            # del temp4s["templateid"]
            # 增加webtest
            print("# 自定义http test: 【  " + str(len(httptest_list_all)) + "  】 个")
            for httptest_list_1 in range(len(httptest_list_all)):
                httptest_list_all[httptest_list_1]["hostid"] = new_host_id[0]
                Ret = zabbix_server.add_httptest(httptest_list_all[httptest_list_1])


            # 增加自定义监控项目
            # print("开始添加的自定义监控项")
            a = temp4s
            # print(a)
            item2item=[]
            print("# 自定义监控项总计: 【  " + str(len(a)) + "  】 个")

            ret1_msg_ok = []
            ret1_msg_er = []
            i_ok = 0
            i_er = 0
            for i in range(len(a)):
                try:
                    del a[i]["templateid"]
                    del a[i]["state"]
                except:
                    # print("警告：删除某些元素失败1")
                    pass
                a[i]["interfaceid"] = zabbix_server.get_host_interfaceid_by_host_id(new_host_id[0])
                a[i]["hostid"] = new_host_id
                ret1 = zabbix_server.add_item_by_hostid(new_host_id[0], [a[i]])
                # print(ret1)
                if len(ret1) == 0:
                    i_er+=1
                    # print("添加项目失败: %s" % (a[i]))
                    ret1_msg_er.append(ret1["itemids"])
                else:
                    i_ok+=1
                    # print("添加项目成功:%s" % (ret1["itemids"]))
                    ret1_msg_ok.append(ret1["itemids"])
            print("# 自定义【 监控项 】总计成功【 %s 】个,失败【 %s 】" % (i_ok,i_er))
            if i_ok > 0:
                print("# 成功的【 监控项 】ID列表:【 %s 】" % (ret1_msg_ok))
            if i_er > 0:
                print("# 失败的【 监控项 】ID列表:【 %s 】" % (ret1_msg_er))

            ret1_msg_ok = []
            ret1_msg_er = []
            i_ok = 0
            i_er = 0
            
            print("# 自定义触发器项总计: 【  " + str(len(temp7s)) + "  】 个")
            for i in range(len(temp7s)):
                a=zabbix_server.get_trigger_by_triggerid(temp7s[i])
                # print(source_host_id,hostname)
                a[0]["expression"]=a[0]["expression"].replace("{"+source_host_name+":","{"+hostname+":")
                try:
                    del a[0]["triggerid"]
                    del a[0]["templateid"]
                    del a[0]["state"]
                    del a[0]["value"]
                except:
                    # print("警告：删除某些元素失败2")
                    pass
                print(a)
                Ret1 = zabbix_server.create_trigger(a)
                if len(Ret1) == 0:
                    # print("添加触发器失败: %s" % (a))
                    i_er += 1
                    ret1_msg_er.append(Ret1["triggerids"])
                else:
                    # print("添加触发器成功:%s" % (Ret1["triggerids"]))
                    i_ok += 1
                    ret1_msg_ok.append(Ret1["triggerids"])
            print("# 自定义【 触发器 】总计成功【 %s 】个,失败【 %s 】" % (i_ok,i_er))
            if i_ok > 0:
                print("# 成功的【 触发器 】ID列表:【 %s 】" % (ret1_msg_ok))
            if i_er > 0:
                print("# 失败的【 触发器 】ID列表:【 %s 】" % (ret1_msg_er))
            #
            #
            #  增加自定义监控项目
            # print("开始添加【 没有 】tigger的自定义监控项")
            # a = temp13s
            # for i in range(len(a)):
            #     del a[i]["templateid"]
            #     del a[i]["state"]
            #     a[i]["interfaceid"] = zabbix_server.get_host_interfaceid_by_host_id(new_host_id[0])
            #     a[i]["hostid"] = new_host_id
            #     ret1 = zabbix_server.add_item_by_hostid(new_host_id[0], [a[i]])

            # print("开始添加【 有 】tigger的自定义监控项")
            # for i in range(len(temp14s)):
            #     del temp14s[i]["templateid"]
            #     del temp14s[i]["state"]
            #     temp14s[i]["interfaceid"] = zabbix_server.get_host_interfaceid_by_host_id(new_host_id[0])
            #     temp14s[i]["hostid"] = new_host_id
            #     ret1 = zabbix_server.add_item_by_hostid(new_host_id[0],[temp14s[i]])

            #循环增加宏

            # print("开始添加【 有 】tigger的自定义监控项")

            # print("开始增加宏")
            ret1_msg_ok = []
            ret1_msg_er = []
            i_ok = 0
            i_er = 0

            print("# 自定义宏项总计: 【  " + str(len(temp5s)) + "  】 个")
            for i in range(len(temp5s)):
                # print(temp5s[i])
                hongRet = zabbix_server.add_usermacro_by_host_id(new_host_id[0],temp5s[i])
                if len(hongRet) == 0:
                    i_er += 1
                    ret1_msg_er.append(hongRet["hostmacroids"])
                    # print("添加宏失败: %s" % (a))
                else:
                    # print("添加宏成功: %s" % (hongRet["hostmacroids"]))
                    # print("自定义触发器总计成功【 %s 】个,失败[%s]" % (i_ok,i_er))
                    i_ok += 1
                    ret1_msg_ok.append(hongRet["hostmacroids"])
            print("# 自定义【 宏 】总计成功【 %s 】个,失败【 %s 】" % (i_ok, i_er))
            if i_ok > 0:
                print("# 成功的【 宏 】ID列表:【 %s 】" % (ret1_msg_ok))
            if i_er > 0:
                print("# 失败的【 宏 】ID列表:【 %s 】" % (ret1_msg_er))
            # except Exception as e:
            #     print(e)
        except Exception as e:
            print("# 添加某些项目失败【  %s  】失败" % (name))
            print(e)
            print("*"*60)
    else:
        print("*"*60)
        print("# 主机【  %s  】已经存在，并且未配置该主机需要强制删除，请查看url: %s/hosts.php?form=update&hostid=%s" % (name,zabbix_api_url.replace("/api_jsonrpc.php",""),checkhost[0]["hostid"]))
        # print("*" * 60)



