import ctypes
from ctypes import wintypes
import psutil
import win32pipe, win32file, win32con
import socket
from threading import Thread, currentThread
import os
import time

kernel32 = ctypes.WinDLL('kernel32.dll', use_last_error=True)

MEM_COMMIT = 0x1000
MEM_RELEASE = 0x8000
PAGE_READWRITE = 0x0004
INFINITE = -1

SIZE_T = ctypes.c_size_t
LPSIZE_T = ctypes.POINTER(SIZE_T)
WCHAR_SIZE = ctypes.sizeof(wintypes.WCHAR)
LPSECURITY_ATTRIBUTES = wintypes.LPVOID
LPTHREAD_START_ROUTINE = wintypes.LPVOID

class BOOL_CHECKED(ctypes._SimpleCData):
    _type_ = "l"
    def _check_retval_(retval):
        if retval == 0:
            raise ctypes.WinError(ctypes.get_last_error())
        return retval

class LPVOID_CHECKED(ctypes._SimpleCData):
    _type_ = "P"
    def _check_retval_(retval):
        if retval is None:
            raise ctypes.WinError(ctypes.get_last_error())
        return retval

HANDLE_CHECKED = LPVOID_CHECKED  # not file handles

kernel32.OpenProcess.restype = HANDLE_CHECKED
kernel32.OpenProcess.argtypes = (
    wintypes.DWORD, # dwDesiredAccess
    wintypes.BOOL,  # bInheritHandle
    wintypes.DWORD) # dwProcessId

kernel32.VirtualAllocEx.restype = LPVOID_CHECKED
kernel32.VirtualAllocEx.argtypes = (
    wintypes.HANDLE, # hProcess
    wintypes.LPVOID, # lpAddress
    SIZE_T,          # dwSize
    wintypes.DWORD,  # flAllocationType
    wintypes.DWORD)  # flProtect

kernel32.VirtualFreeEx.argtypes = (
    wintypes.HANDLE, # hProcess
    wintypes.LPVOID, # lpAddress
    SIZE_T,          # dwSize
    wintypes.DWORD)  # dwFreeType

kernel32.WriteProcessMemory.restype = BOOL_CHECKED
kernel32.WriteProcessMemory.argtypes = (
    wintypes.HANDLE,  # hProcess
    wintypes.LPVOID,  # lpBaseAddress
    wintypes.LPCVOID, # lpBuffer
    SIZE_T,           # nSize
    LPSIZE_T)         # lpNumberOfBytesWritten _Out_

kernel32.CreateRemoteThread.restype = HANDLE_CHECKED
kernel32.CreateRemoteThread.argtypes = (
    wintypes.HANDLE,        # hProcess
    LPSECURITY_ATTRIBUTES,  # lpThreadAttributes
    SIZE_T,                 # dwStackSize
    LPTHREAD_START_ROUTINE, # lpStartAddress
    wintypes.LPVOID,        # lpParameter
    wintypes.DWORD,         # dwCreationFlags
    wintypes.LPDWORD)       # lpThreadId _Out_

kernel32.WaitForSingleObject.argtypes = (
    wintypes.HANDLE, # hHandle
    wintypes.DWORD)  # dwMilliseconds

kernel32.CloseHandle.argtypes = (
    wintypes.HANDLE,) # hObject

def injectdll(pid, dllpath):
    size = (len(dllpath) + 1) * WCHAR_SIZE
    hproc = hthrd = addr = None
    try:
        hproc = kernel32.OpenProcess(
            win32con.PROCESS_ALL_ACCESS, False, pid)
        addr = kernel32.VirtualAllocEx(
            hproc, None, size, MEM_COMMIT, PAGE_READWRITE)
        kernel32.WriteProcessMemory(
            hproc, addr, dllpath, size, None)
        hthrd = kernel32.CreateRemoteThread(
            hproc, None, 0, kernel32.LoadLibraryW, addr, 0, None)
        kernel32.WaitForSingleObject(hthrd, 1000)
    finally:
        if addr is not None:
            kernel32.VirtualFreeEx(hproc, addr, 0, MEM_RELEASE)
        if hthrd is not None:
            kernel32.CloseHandle(hthrd)
        if hproc is not None:
            kernel32.CloseHandle(hproc)

def NPServer(id, ip):

    hNP = win32pipe.CreateNamedPipe("\\\\.\\pipe\\"+str(id),
                                      win32pipe.PIPE_ACCESS_DUPLEX,
                                      win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_NOWAIT,
                                      1, len(ip), len(ip), 300, None)
    time.sleep(5)
    try:
        # Start connection
        win32pipe.ConnectNamedPipe(hNP, None)
        print("connected")
        win32file.WriteFile(hNP, ip.encode("utf-8"))

        t = currentThread()
        # while not closed
        while getattr(t, "do_run", True):
            time.sleep(0.2)

        # close connection
        win32pipe.DisconnectNamedPipe(hNP)
    except:
        pass

def getIpAddress(family,name):
    for interface, snics in psutil.net_if_addrs().items():
        for snic in snics:
            if snic.family == family and interface == name:
                return snic.address


def ChangeProcessIp(pidlist,processName,card):

    d = {}
    # get ip of the card
    ip = getIpAddress(socket.AF_INET,card)
    print(ip)

    print(pidlist)
    for pid in pidlist:
        try:
            process = psutil.Process(pid)
            pname = process.name()
            print(pname)
            ### Only if the pid hasn't changed
            if pname == processName:
                injectdll(process.pid,os.path.abspath(os.getcwd()+'\\Network\\netHook.dll'))
                d[process.pid] = Thread(target=NPServer, args=(process.pid, ip))
                d[process.pid].start()
        except:
            pass
    return d
