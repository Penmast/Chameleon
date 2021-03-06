// dllmain.cpp : Définit le point d'entrée pour l'application DLL.
#include "stdafx.h"
#define _WINSOCK_DEPRECATED_NO_WARNINGS
#pragma warning(disable:4996)
#include <windows.h>
#include <stdio.h>
#include <winsock2.h>
#include <stdlib.h>
#include <string>
#include <thread>
#include "mhook-lib/mhook.h"
#include <regex>

// Need to link with Ws2_32.lib
#pragma comment(lib, "ws2_32.lib")

FARPROC fpBind;
BYTE bSavedByteBind;
char* ip;
bool end = false;
HANDLE th;
EXTERN_C IMAGE_DOS_HEADER __ImageBase;

typedef int (WSAAPI* _connect)(
	SOCKET s,
	const struct sockaddr *name,
	int namelen
	);
_connect PConnect = (_connect)GetProcAddress(GetModuleHandle(L"ws2_32"), "connect");

typedef int (WSAAPI* _bind)(
	SOCKET s,
	const struct sockaddr *name,
	int namelen
	);
_bind PBind = (_bind)GetProcAddress(GetModuleHandle(L"ws2_32"), "bind");

typedef int (WSAAPI* _WSAconnect)(
	SOCKET s,
	const struct sockaddr *name,
	int namelen,
	LPWSABUF lpcallerData,
	LPWSABUF lpCalleeData,
	LPQOS lpSQOS,
	LPQOS lpGQOS
	);
_WSAconnect PWSAConnect = (_WSAconnect)GetProcAddress(GetModuleHandle(L"ws2_32"), "WSAConnect");


int WSAAPI Hookconnect(SOCKET s, sockaddr *addr, int namelen)
{
	// bind to local ip
	sockaddr_in localaddr = { 0 };
	localaddr.sin_family = AF_INET;
	localaddr.sin_addr.s_addr = inet_addr(ip);

	if (bind(s, (sockaddr*)&localaddr, sizeof(localaddr)) == SOCKET_ERROR) {
		/*int wError = WSAGetLastError();
		MessageBoxA(NULL, std::to_string(wError).c_str(), "DLL Injected",
		MB_OK);*/
	}
	return PConnect(s, addr, namelen);
}

int WSAAPI Hookbind(SOCKET s, sockaddr *addr, int namelen)
{
	// bind to local ip
	sockaddr_in localaddr = { 0 };
	localaddr.sin_family = AF_INET;
	localaddr.sin_port = 0;
	localaddr.sin_addr.s_addr = inet_addr(ip);

	return PBind(s, addr, namelen);
}

int WSAAPI HookWSAconnect(SOCKET s, sockaddr *addr, int namelen, LPWSABUF lpcallerData, LPWSABUF lpCalleeData, LPQOS lpSQOS, LPQOS lpGQOS)
{
	// bind to local ip
	sockaddr_in localaddr = { 0 };
	localaddr.sin_family = AF_INET;
	localaddr.sin_addr.s_addr = inet_addr(ip);

	if (bind(s, (sockaddr*)&localaddr, sizeof(localaddr)) == SOCKET_ERROR) {
		/*int wError = WSAGetLastError();
		MessageBoxA(NULL, std::to_string(wError).c_str(), "DLL Injected",
		MB_OK);*/
	}
	return PWSAConnect(s, addr, namelen, lpcallerData, lpCalleeData, lpSQOS, lpGQOS);
}


void checkInjectEnd(bool* endBool) {

	HANDLE hPipe;
	char szTest[256];

	sprintf_s(szTest, "\\\\.\\pipe\\%d", GetCurrentProcessId());

	while (*endBool == false)
	{
		hPipe = CreateFileA(
			szTest,   // pipe name 
			GENERIC_READ,
			0,              // no sharing 
			NULL,           // default security attributes
			OPEN_EXISTING,  // opens existing pipe 
			0,              // default attributes 
			NULL);          // no template file 
		if (hPipe == INVALID_HANDLE_VALUE) {
			if (GetLastError() != ERROR_PIPE_BUSY)
			{
				*endBool = true;
			}
		}
		else {
			CloseHandle(hPipe);
		}
		Sleep(1000);
	}

	CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)FreeLibrary, &__ImageBase, 0, NULL);
}

//TO DO: Extract IP from erronous incoming message
void cleanIp() {
	std::regex expr("(\\d{1,3}(\\.\\d{1,3}){3})");
	std::string target = ip;
	std::smatch matches;

	if (std::regex_search(target, matches, expr)) {
		strcpy(ip, matches.str(1).c_str());
	}
}

void getIp() {

	HANDLE hPipe;
	DWORD dwRead;

	char szTest[256];
	sprintf_s(szTest, "\\\\.\\pipe\\%d", GetCurrentProcessId());

	hPipe = CreateFileA(
		szTest,   // pipe name 
		GENERIC_READ,
		0,              // no sharing 
		NULL,           // default security attributes
		OPEN_EXISTING,  // opens existing pipe 
		0,              // default attributes 
		NULL);          // no template file 

	DWORD numBytesRead = 0;
	BOOL result = false;
	int count = 0;

	DWORD bytesAvail = 0;
	while ((bytesAvail == 0) && (count < 100))
	{
		count += 1;
		PeekNamedPipe(hPipe, NULL, 0, NULL, &bytesAvail, NULL);
		Sleep(100);
	}
	if ((bytesAvail > 19) || (bytesAvail < 10)) {
		bytesAvail = 19;
	}

	char* buffer = (char*)malloc(bytesAvail - 4);

	result = ReadFile(
		hPipe,    // pipe handle 
		buffer,    // buffer to receive reply 
		bytesAvail,  // size of buffer 
		&numBytesRead,  // number of bytes read 
		NULL);    // not overlapped 
	/*
	buffer = strdup("10.7.7.48");
	result = true;
	MessageBoxA(NULL, buffer, "DLL Injected",
		MB_OK);*/

	if (result) {
		ip = buffer;
		cleanIp();
		CloseHandle(hPipe);
	}
	/*else {
		CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)FreeLibrary, &__ImageBase, 0, NULL);
	}*/
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD trigger, LPVOID lpReserved)
{
	switch (trigger)
	{
	case DLL_PROCESS_ATTACH:



		//Wait for the pipe to be created
		Sleep(2000);
		// get the ip to bind to using namedpipe
		getIp();


		// if ip is valid (###TO DO: Improve check)
		if ((strlen(ip) != 0) && (strlen(ip) < 17)) {
			th = CreateThread(0, 0, (LPTHREAD_START_ROUTINE)checkInjectEnd, &end, 0, NULL);

			Mhook_SetHook((PVOID*)&PConnect, Hookconnect);
			Mhook_SetHook((PVOID*)&PWSAConnect, HookWSAconnect);
			Mhook_SetHook((PVOID*)&PBind, Hookbind);
			MessageBox(NULL, L"IP changed", L"DLL Injected",
				MB_OK);
		}
		else
		{
			MessageBox(NULL, L"Error while injecting new ip", L"DLL Injected",
				MB_OK);
		}
		break;
	case DLL_THREAD_ATTACH:

		break;
	case DLL_THREAD_DETACH:
		break;
	case DLL_PROCESS_DETACH:
		MessageBox(NULL, L"End of the ip change", L"DLL Injected",
			MB_OK);
		Mhook_Unhook((PVOID*)&PConnect);
		Mhook_Unhook((PVOID*)&PBind);
		Mhook_Unhook((PVOID*)&PWSAConnect);
		break;
	}
	return TRUE;
}