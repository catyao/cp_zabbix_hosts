#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:     xcy7144/Yao
# eMail:      xingzhong.yao@yumchina.com
# datetime:   2018/9/19 17:42
# 自豪的使用 [ PyCharm ] 编写代码 [ zabbix/zabbix_login.py ]
from zabbix_api import zabbix_api_jobs
from customfunction import thefunction as func
import configparser
import sys, re
import config.gettrigger_conf as trigger_conf
APP_HOME = sys.path[0]
actionlist = trigger_conf.actionlist
try:
    huanjing = sys.argv[1]
except:
    huanjing = "yum"

# print(huanjing)
cf = configparser.ConfigParser()

try:
    config_file_ = APP_HOME + "/config.ini." + huanjing
    # print("# 开始使用[ %s ]配置文件" % config_file_)
    cf.read(APP_HOME + "/config.ini." + huanjing)
    zabbix_api_url = cf.get("zabbix_server_conf", "zabbix_api_url").replace('"','')
    username = cf.get("zabbix_server_conf", "username").replace('"','')
    password = cf.get("zabbix_server_conf", "password").replace('"','')
except Exception as e:
    print("# 读取配置文件[ %s ]失败, 请检查脚本所在路径是否有写权限，或者文件是否存在" % config_file_)
    print("# 详细信息：")
    print("# %s" % (e))
    sys.exit(1)


# 读取session id文件
theauthread4file = func.authread4file(huanjing=huanjing)
loginisok = True

print("*"*60)
print("# 开始尝试使用session id登录zabbix server")
try:
    zabbix_server = zabbix_api_jobs(zabbix_api_url, username, password, theauthread4file, huanjing)
    print("# Url__: [ %s ]" % zabbix_api_url)
    print("# 用户名: [ %s ]" % username)
    print("# 环境__: [ %s ]" % config_file_)
    zabbixVersion = zabbix_server.get_apiversion()
    if zabbixVersion == "":
        print("# 登录失败: 未得到zabbix的版本号")
        loginisok = False
    else:
        print("# session id验证通过, 并且api执行正常1, 得到Zabbix API版本为: 【 %s 】" % (zabbixVersion))
except Exception as e:
    print("# 使用session id登录失败，开始尝试使用账密登录")
    try:
        theauthread4file = ""
        zabbix_server = zabbix_api_jobs(zabbix_api_url, username, password,theauthread4file, huanjing)
        zabbixVersion = zabbix_server.get_apiversion()
    except Exception as e:
        print(e)
        zabbixVersion = ""
    if zabbixVersion == "":
        print("# 登录失败: 未得到zabbix的版本号")
        loginisok = False
    else:
        print("# session id验证通过, 并且api执行正常2, 得到Zabbix API版本为: 【 %s 】" % (zabbixVersion))
        print("# 回写session id到文件，下次将使用session id登录")
        theauthwrite2file = func.authwrite2file(zabbix_server.auth, huanjing=huanjing)
        print("_"*60)
        print(theauthwrite2file)
finally:
    if loginisok is False:
        print("# 登录失败，脚本退出%")
        sys.exit(1)
    else:
        print("# 登录成功，开始执行其他步骤")
print("*"*60)
