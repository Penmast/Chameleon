import os
import time
import winreg as reg
import subprocess
from pathlib import Path
import sys
from threading import Thread, currentThread
import psutil
import socket


ADAPTER_KEY = r'SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}'

OpenVpnPath = "C:\\Program Files\\OpenVPN\\bin\\openvpn.exe"
ConfigPath = os.environ['USERPROFILE'] + "\\OpenVPN\\config"

ConnectionKey = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}"

### kill a process and it's children (Mouhahaha !!)
def kill(proc_pid):
    process = psutil.Process(proc_pid)
    try:
        for proc in process.children(recursive=True):
            proc.kill()
    except:
        pass
    process.kill()

### Get the gateway address of an interface
def getIpAddressGateway(family,interfaceName):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family and interface == interfaceName:
                host = snic.address.split(".")
                host[-1] = "1"
                return ".".join(host)


### Execute the Openvpn command (use in a thread)
def VPNConnect(OpenVpnPath,componentId,TcpConf,UdpConf=None):


    if UdpConf is None:
        cmd = [OpenVpnPath,"--dev-node", componentId, "--config", TcpConf,"--route-nopull"]
    else:
        cmd = [OpenVpnPath,"--dev-node", componentId, "--config", TcpConf,"--config",UdpConf,"--route-nopull"]

    prog = subprocess.Popen(cmd,stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    try:
        # Get the credentials
        fh = open("data/openVPNid.data", "r").read().splitlines()
        login = fh[0]
        password = fh[1]
    except:
        return
    time.sleep(0.1)
    prog.stdin.write(login.encode("utf-8"))
    prog.stdin.flush()
    time.sleep(0.1)
    prog.stdin.write(password.encode("utf-8"))
    prog.stdin.close()

    t = currentThread()
    while True:
        line = prog.stdout.readline()
        print(line)

        if b'Initialization' in line:
            print("Makeroute called")
            makeRoute(componentId)
            break
        if line is b'':
            break
        if b'Restart' in line:
            t.do_run = False
            break
        time.sleep(0.2)

    while getattr(t, "do_run", True):
        prog.poll()
        time.sleep(0.5)
    print("stopped")
    kill(prog.pid)

#def setAddress(componentId):
#    cmd = ["netsh.exe","interface","ip","set","address","name="+componentId,"static",ip, mask, gateway]
#    prog = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

### Add the route to connect to the vpn
def makeRoute(componentId):
    gateway = getIpAddressGateway(socket.AF_INET,componentId)
    cmd = ["route", "add", "0.0.0.0", "mask", "0.0.0.0", gateway, "metric", "1000"]
    prog = subprocess.Popen(cmd)

### Add a vpn connection using the conf file. Returns a thread that runs the VPN
def mainVPN(ConfTcp,ConfUdp = None):

    if not Path(OpenVpnPath).is_file():
        raise ValueError("Openvpn not installed")

    with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ADAPTER_KEY) as adapters:
        try:
            for i in range(10000):
                key_name = reg.EnumKey(adapters, i)
                with reg.OpenKey(adapters, key_name) as adapter:
                    try:
                        component_id = reg.QueryValueEx(adapter, 'ComponentId')[0]
                        if component_id == 'tap0901':
                            key = reg.QueryValueEx(adapter, 'NetCfgInstanceId')[0]
                    except :
                        pass
        except:
            pass

    if key is None:
        raise ValueError("TAP Windows not installed")

    for proc in psutil.process_iter():
        try:
            process = psutil.Process(proc.pid)
            pname = process.name()
            if pname == "openvpn.exe" and process.parent().parent() == "python.exe":
                kill(proc.pid)
        except:
            pass


    regConnection = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ConnectionKey+"\\"+key+"\\Connection")
    componentId = reg.QueryValueEx(regConnection, "name")[0]
    print("RESULT: "+componentId)

    if Path(ConfTcp).is_file():
        if (ConfUdp is not None) and (Path(ConfUdp).is_file()):
            thVPN = Thread(target=VPNConnect, args=(OpenVpnPath, componentId, ConfTcp, ConfUdp))
            thVPN.start()
        else:
            thVPN = Thread(target=VPNConnect, args=(OpenVpnPath, componentId, ConfTcp,))
            thVPN.start()

    return (thVPN,componentId)