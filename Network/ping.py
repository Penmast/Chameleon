# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 17:16:01 2018

@author: aitza

"""
"""""""""""""""""""""""""""
" Ping Module, plugN'safe "
"   """"""""""""""""""    "
"""""""""""""""""""""""""""

#import subrocess to spawn porcess
import subprocess
import re #re to do regex expression to extract infos

def getPing():
    hostname= "8.8.8.8" # determine the Ip to ping, like google.com

#try to call subprocess
    try:
        response = subprocess.check_output(
                ['ping', '-n', '1', hostname],
                shell=True,
                stderr=subprocess.STDOUT,  # get error output
                universal_newlines=True  # return string not bytes
                )

        ping_stats = re.findall(r'=(.*)$', response) # retrieve last line of the stats after the '='

        ping_timestr= re.sub(r'ms.*','',ping_stats[0]) #keep only numbers
        try:
            ping_time= int(ping_timestr) #get the ping time as an int
            return ping_time

        except :
            ping_time= "lost"

#handle subprocess error
    except subprocess.CalledProcessError:
        return "error" #return an error message

if __name__ == "__main__":
    getPing()
