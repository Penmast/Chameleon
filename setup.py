from cx_Freeze import setup, Executable

import sys
base = 'Win32GUI' if sys.platform=='win32' else None
base = None

executables = [Executable("chameleon.py", base=base)]
additional_mods = ['numpy.core._methods', 'numpy.lib.format','pyqtgraph.debug','pyqtgraph.ThreadsafeTimer','win32pipe', 'win32file', 'win32con','speedtest','requests',
                   "nmap","scapy","scapy.all","ctypes"]

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
    name = "AppVpn",
    options = options,
    version = "0.1",
    description = 'VPN Management App',
    executables = executables
)