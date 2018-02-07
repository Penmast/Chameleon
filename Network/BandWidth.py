import psutil
import time

"""

Return the upload and download rate in Kilo Byte per sec for the classic interface

"""

def getBandWidth(nic):
    mesure = True

    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    presc_UL_total = 0
    presc_DL_total = 0
    new_UL_total = 0
    new_DL_total = 0
    presc_UL = {}
    presc_DL = {}
    new_UL = {}
    new_DL = {}

    for item in iostat.items():
        presc_UL[item[0]]=item[1][0]
        presc_DL[item[0]]=item[1][1]

    time.sleep(1)

    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for item in iostat.items():

        new_UL[item[0]]=item[1][0]
        new_DL[item[0]]=item[1][1]

        if new_UL[item[0]] != presc_UL[item[0]]:
            presc_UL_total=presc_UL_total+presc_UL[item[0]]
            new_UL_total=new_UL_total+new_UL[item[0]]

        if new_DL[item[0]] != presc_DL[item[0]]:
            presc_DL_total=presc_DL_total+presc_DL[item[0]]
            new_DL_total=new_DL_total+new_DL[item[0]]

    upload_rate = (new_UL_total - presc_UL_total) / 1000
    download_rate = (new_DL_total - presc_DL_total) / 1000

    #time.sleep(10)
    #print("Download: ",download_rate,"KB/s","   ","Upload: ",upload_rate,"KB/s")
    return [download_rate, upload_rate]
    #time.sleep(1)


"""

Return the upload and download rate in Kilo Byte per sec for the OpenVPN interface

"""

def getBandWidthVPN(nic):
    mesure = True

    if nic is not None:
        OpenVpnCard = nic
    else:
        return "The VPN is Off"

    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for index, item in enumerate(iostat.items()):
        if item[1][0]!= 0 and item[0] == OpenVpnCard:
            card = item[0]
    #print(iostat)

    while(mesure):

        presc_UL=iostat[card][0]
        presc_DL=iostat[card][1]

        iostat = psutil.net_io_counters(pernic=True, nowrap=True)

        for index, item in enumerate(iostat.items()):
            if item[1][0] != 0 and item[0] == OpenVpnCard:
                card = item[0]

        upload_rate = (iostat[card][0] - presc_UL)/1000
        download_rate = (iostat[card][1] - presc_DL)/1000

        #print("Download: ",download_rate,"KB/s","   ","Upload: ",upload_rate,"KB/s")
        return [download_rate, upload_rate]
        #time.sleep(1)

"""

Return the difference in pourcentage between the use of the interface of OpenVPN and the classic interface

"""

def getBandWidthDiff(nic):
    mesure = True

    if nic is not None:
        OpenVpnCard = nic
    else:
        return "The VPN is Off"


    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for item in iostat.items():
        if item[0] == OpenVpnCard:
            VpnCard = item[0]

    while(mesure):

        rate=getBandWidth(nic)

        presc_UL_VPN=iostat[VpnCard][0]
        presc_DL_VPN=iostat[VpnCard][1]

        iostat = psutil.net_io_counters(pernic=True, nowrap=True)

        upload_rate_VPN = (iostat[VpnCard][0] - presc_UL_VPN)/1000
        download_rate_VPN = (iostat[VpnCard][1] - presc_DL_VPN)/1000

        total_VPN = upload_rate_VPN + download_rate_VPN
        total_global = rate[0] + rate[1]

        if total_global == 0:
            diff = 0
        else:
            diff = total_VPN *100 / total_global

        diff = round(diff,2)
        #print("Pourcentage VPN used: ",diff,"%")
        return str(diff)+'%'
        #time.sleep(1


if __name__ =="__main__":
    #getBandWidthDiff("Ethernet")
    while (True):
        getBandWidth("Ethernet 3")
