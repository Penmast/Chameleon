# Chameleon VPN and Network Manager

This project is a Windows's python based application that allows a user to monitor and manage it's network, as well as using a vpn only for selected processes

## Getting Started

The project is build using python 3.6.


### Prerequisites

To run the project, you will need 2 third-parties sofware:

- openvpn with the TAP Interface ( https://openvpn.net/index.php/open-source/downloads.html)

- winpcap (https://www.winpcap.org/install/)

**Note**: if you have wireshark installed, you probably already have winpcap on yout computer


### Installing

Libraries required:

```
pip install pyQT5, PyQTchart, psutil, matplotlib, requests, numpy, webbrowser, win32core, scapy-python3
```

There is also a dll that is used in this project (injected into processes to change their IP), but for some reasons it seems that it has to be recompiled on each computer.

So if you have Visual studio, open the project which is in the DLL folder, compile it (DEBUG configuration seems to be more stable), and move the created Dll into the Network Folder. Keep the original name.

To run the programm, launch chameleon.py.

## How to use

First, you have to launch the openvpn server from the app, using the last tab. 
You just have to give it the ovpn file used to connect to the server, and your credentials. The vpn won't be the main Network Adapter, so even if vpn is enabled after this, no application will use it.

Then, you can go to the 2nd tab and select processes that should use the vpn using the lock button (only processes using internet are displayed).
Be careful which process you select, as there is risks of crashing the system if you choose a vital one.

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

* MHook : https://github.com/martona/mhook

## Authors

* **Alazay Quentin** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **David Deray** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **Pierre Haykal** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **Megane Pau** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)
* **AitZaid Ismail** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

## License

This project is licensed under the MIT License

## Acknowledgments

Some inspiration, for the Dll for example:
	* falahati : https://github.com/falahati/NetworkAdapterSelector

