import json
import os

def listserver():
    serverlist = open('serverlist.json',encoding='utf-8')
    serversjson = serverlist.read()
    serverlist.close
    servers = json.loads(serversjson)
    for x in range(servers['number']):
        y = str(x)
        print("编号："+y+" IP："+servers[y]['server_host']+" 描述："+servers[y]['describe'])

def showhelp():
    print("输入 help 查看用法")
    print("输入 list 查看服务器列表")
    print("输入 connect -1 编号 连接服务器并设置全局代理")
    print("输入 connect -2 编号 连接服务器并代理国外IP(出国模式)")
    print("输入 connect -3 编号 连接服务器并代理国内IP(回国模式)")
    print("输入 local 编号 启动socks5代理（暂无）")
    print("输入 stop 清除路由表（关闭连接后请务必执行此命令）")
    print("输入 exit 退出")
 
def startclient(uid):
    print("Connecting to ID："+uid)
    serverlist = open('serverlist.json',encoding='utf-8')
    serversjson = serverlist.read()
    serverlist.close
    servers = json.loads(serversjson)
    server_host = servers[uid]['server_host']
    server_port = str(servers[uid]['server_port'])
    password = servers[uid]['password']
    encrypt_method = servers[uid]['encrypt_method']
    timeout = str(servers[uid]['timeout'])
    syscall = "ss-redir -s "+server_host+" -p "+server_port+" -b 0.0.0.0 -l 7777 -k "+password+" -m "+encrypt_method+" -t "+timeout+" -u"
    os.system(syscall)

def startsslocal(uid):
    print("Connecting to ID："+uid)
    serverlist = open('serverlist.json',encoding='utf-8')
    serversjson = serverlist.read()
    serverlist.close
    servers = json.loads(serversjson)
    server_host = servers[uid]['server_host']
    server_port = str(servers[uid]['server_port'])
    password = servers[uid]['password']
    encrypt_method = servers[uid]['encrypt_method']
    timeout = str(servers[uid]['timeout'])
    syscall = "ss-local -s "+server_host+" -p "+server_port+" -b 127.0.0.1 -l 1080 -k "+password+" -m "+encrypt_method+" -t "+timeout+" -u"
    os.system(syscall)

def setglobal(uid):
    serverlist = open('serverlist.json',encoding='utf-8')
    serversjson = serverlist.read()
    serverlist.close
    servers = json.loads(serversjson)
    server_host = servers[uid]['server_host']
    os.system('sudo iptables -t nat -N SOCKS')
    os.system('sudo iptables -t nat -A SOCKS -d 0.0.0.0/8 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 10.0.0.0/8 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 127.0.0.0/8 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 169.254.0.0/16 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 172.16.0.0/12 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 192.168.0.0/16 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 224.0.0.0/4 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d 240.0.0.0/4 -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -d '+server_host+' -j RETURN')
    os.system('sudo iptables -t nat -A SOCKS -p tcp -j REDIRECT --to-ports 7777')
    os.system('sudo iptables -t nat -A SOCKS -p udp -j REDIRECT --to-ports 7777')
    os.system('sudo iptables -t nat -A OUTPUT -j SOCKS')
    pass

def setoutchn():
    chniptxt = open('chnip.txt',encoding='utf-8')
    for line in chniptxt:
        os.system('sudo iptables -t nat -A SOCKS -d '+line.strip('\n')+' -j RETURN')
    print("尽情使用吧")
#设置出国路由

def setinchn():
    os.system('sudo iptables -t nat -N SOCKS')
    chniptxt = open('chnip.txt',encoding='utf-8')
    for line in chniptxt:
        os.system('sudo iptables -t nat -A SOCKS -p tcp -d '+line.strip('\n')+' -j REDIRECT --to-ports 7777')
        os.system('sudo iptables -t nat -A SOCKS -p udp -d '+line.strip('\n')+' -j REDIRECT --to-ports 7777')
    os.system('sudo iptables -t nat -A OUTPUT -j SOCKS')
    print("尽情使用吧")
#设置回国路由

def setrouter(model,uid):
    if model == "-1":
        print("设置全局代理")
        setglobal(uid)
    elif model == "-2":
        print("设置出国路由")
        setglobal(uid)
        setoutchn()
    elif model == "-3":
        print("设置回国路由")
        setinchn()
    pass
#调整路由表

def connectserver(tasks):
    print(tasks)
    uid = tasks[3:]
    model = tasks[0:2]
    setrouter(model,uid)
    startclient(uid)
    os.system('sudo iptables -t nat -F SOCKS')
    exit()

def showwrong(choose):
    print(choose+"不是有效的命令")
    print("输入help查看用法")

print("ShadowRedir")
print("支持tcp和udp")
print("铭谢https://github.com/17mon/china_ip_list")
print("输入命令")
while True:
    choose = input("")
    print(choose[0:9])
    if choose == "list":
        listserver()
    elif choose == "help":
        showhelp()
    elif choose[0:9] == "connect -":
        connectserver(choose[8:])
    elif choose[0:6] == "local ":
        startsslocal(choose[6:])
    elif choose == "stop":
        os.system('sudo iptables -t nat -F SOCKS')
    elif choose == "exit":
        break
    else:
        showwrong(choose)