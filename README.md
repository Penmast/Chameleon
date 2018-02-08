# Chameleon VPN and Network Manager

This project is a Windows's python based application that allows a user to monitor and manage it's network, as well as using a vpn only for selected processes

![Screenshot](IPChange.png "Screenshot")

## Getting Started

The project is build using python 3.6. It requires admin rights to work well.


The program uses a ovpn file to connect to the openVPN server, but the route are made so the vpn isn't the primary NIC choosen by windows, even if the route is available and works.
Then, a custom built Dll is injected in the desired process to bind the packets, which makes the injected process use the VPN connection, while the others still uses the normal connection.


### Prerequisites

**Note** Due to a compatibility problem in scapy, this software doesn't run on any windows version that is earlier than Windows 8.

To run the project, you will need 2 third-parties sofware:

- openvpn with the TAP Interface ( https://openvpn.net/index.php/open-source/downloads.html)

- winpcap (https://www.winpcap.org/install/)

**Note**: if you have wireshark installed, you probably already have winpcap on yout computer

- Nmap (https://nmap.org/download.html) installed is also used, but only for one function of the project, and can run without it


### Installing

Libraries required:

```
pip install pyQT5, PyQTchart, psutil, matplotlib, requests, numpy, webbrowser, win32core, scapy-python3
```

There is also a dll that is used in this project (injected into processes to change their IP). It works only on some computers, so if for some reasons it doesn't work on your computer, it has to be recompiled.

So if you have Visual studio, open the project which is in the DLL folder, compile it (DEBUG configuration seems to be more stable), and move the created Dll into the Network Folder. Keep the original name.

To run the programm, launch chameleon.py. No arguments needed.

## How to use

First, you have to launch the openvpn server from the app, using the last tab.
You just have to give it the ovpn file used to connect to the server, and your credentials. The vpn won't be the main Network Adapter, so even if vpn is enabled after this, no application will use it.

Then, you can go to the 2nd tab and select processes that should use the vpn using the lock button (only processes using internet are displayed).
Be careful which process you select, as there is risks of crashing the system if you choose a vital one.

If the injection suceeded, the program will display a popup saying "Ip changed". 
You can stop the ip change using the same lock button, or by leaving the program.

## Deployment

If you want to build an exe, it is possible. First, install cx_Freeze:

```
pip install cx_Freeze
```

The setup file is already done, so you just have to run :

```
python setup.py build
```

## Built With

* Python
* MHook : https://github.com/martona/mhook

## Authors

We are a team of French Engineering students, and we built this software for a school project.

* **Alazay Quentin**
* **David Deray**
* **Pierre Haykal**
* **Megane Pau**
* **AitZaid Ismail**

## License

This project is licensed under the MIT License

## Acknowledgments

Some inspiration, for the Dll for example:
	* falahati : https://github.com/falahati/NetworkAdapterSelector
