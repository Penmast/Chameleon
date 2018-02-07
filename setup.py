from cx_Freeze import setup, Executable

import sys
base = 'Win32GUI' if sys.platform=='win32' else None
base = None

executables = [Executable("chameleon.py", base=base,icon="favicon.ico")]
additional_mods = ['numpy.core._methods', 'numpy.lib.format','pyqtgraph.debug','pyqtgraph.ThreadsafeTimer','win32pipe', 'win32file', 'win32con','speedtest','requests',
                   "nmap","scapy","scapy.all","scapy.layers","ctypes",'scapy.layers.all', 'scapy.layers.bluetooth', 'scapy.layers.can', 'scapy.layers.dhcp', 'scapy.layers.dhcp6',
                   'scapy.layers.dns', 'scapy.layers.dot11', 'scapy.layers.gprs', 'scapy.layers.hsrp', 'scapy.layers.inet', 'scapy.layers.inet6', 'scapy.layers.ipsec',
                   'scapy.layers.ir', 'scapy.layers.isakmp', 'scapy.layers.isotp', 'scapy.layers.l2', 'scapy.layers.l2tp', 'scapy.layers.llmnr', 'scapy.layers.mgcp',
                   'scapy.layers.mobileip', 'scapy.layers.netbios', 'scapy.layers.netflow', 'scapy.layers.ntp', 'scapy.layers.pflog', 'scapy.layers.ppp', 'scapy.layers.radius',
                   'scapy.layers.rip', 'scapy.layers.rtp', 'scapy.layers.sctp', 'scapy.layers.sebek', 'scapy.layers.skinny', 'scapy.layers.smb', 'scapy.layers.snmp',
                   'scapy.layers.tftp', 'scapy.layers.uds', 'scapy.layers.vrrp', 'scapy.layers.x509']

include_file = ["Network/","ui/","data/","images/"]
packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
        'includes': additional_mods,
        'include_files': include_file
    },

}

setup(
    name = "Chameleon",
    options = options,
    version = "0.1",
    description = 'VPN Management App',
    executables = executables
)