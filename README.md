# cp_zabbix_hosts
python环境3.x

文件说明：
cp_zabbix_hosts.py  拷贝zabbix主机的脚本<br>
customfunction.py   自定义function<br>
zabbix_api.py       zabbix api封装<br>
zabbix_login.py     zabbix登录封装<br>
config.ini.default  配置文件，实际使用时候请把文件名改成config.ini.yum<br>



# 用法:
# cp_zabbix_hosts.py '源主机（zabbix中的主机名：第一行）' '目标主机名1|目标主机ip1|FORCE（表示强制删除，留空为不删除）,目标主机名2|目标主机ip2,目标主机名3|目标主机ip3...'
# 例如:
# python cp_zabbix_hosts.py 'SGH01VVAT05' '02-S-V-C-00994|172.17.216.21|FORCE,02-S-V-C-00995|172.17.216.22'

注意：
脚本不会检查目标机器的有效性
