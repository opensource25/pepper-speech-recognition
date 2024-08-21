# -*- coding: utf-8 -*-
import socket

###########################################################
# Retrieve robot audio buffer
# Syntaxe:
#    python scriptname --pip <ip> --pport <port>
# 
#    --pip <ip>: specify the ip of your robot (without specification it will use the NAO_IP defined some line below
#
# Author: Alexandre Mazel
###########################################################



import sys
import time

import naoqi
import numpy as np


class SoundReceiverModule(naoqi.ALModule):
    """
    Use this object to get call back from the ALMemory of the naoqi world.
    Your callback needs to be a method with two parameter (variable name, value).
    """

    def __init__( self, strModuleName, strNaoIp ):
        try:
            naoqi.ALModule.__init__(self, strModuleName )
            self.BIND_PYTHON( self.getName(),"callback" )
            self.strNaoIp = strNaoIp
            self.outfile = None
            self.aOutfile = [None]*(4-1) # ASSUME max nbr channels = 4
        except BaseException, err:
            print( "ERR: abcdk.naoqitools.SoundReceiverModule: loading error: %s" % str(err) )

    # __init__ - end
    def __del__( self ):
        print( "INF: abcdk.SoundReceiverModule.__del__: cleaning everything" )
        self.stop()

    def start( self ):

        # Socket Settings
        HOST = ''  # leave empty to accept connections from any IP address or put client IP address here
        PORT = 5001

        # setup socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((HOST, PORT))

        audio = naoqi.ALProxy( "ALAudioDevice", self.strNaoIp, 9559 )
        nNbrChannelFlag = 3 # ALL_Channels: 0,  AL::LEFTCHANNEL: 1, AL::RIGHTCHANNEL: 2 AL::FRONTCHANNEL: 3  or AL::REARCHANNEL: 4.
        nDeinterleave = 0
        nSampleRate = 48000
        audio.setClientPreferences( self.getName(),  nSampleRate, nNbrChannelFlag, nDeinterleave ) # setting same as default generate a bug !?!
        audio.subscribe( self.getName() )
        print( "INF: SoundReceiver: started!" )
        # self.processRemote( 4, 128, [18,0], "A"*128*4*2 ) # for local test

        # on romeo, here's the current order:
        # 0: right;  1: rear;   2: left;   3: front,  

    def stop( self ):
        print( "INF: SoundReceiver: stopping..." )
        audio = naoqi.ALProxy( "ALAudioDevice", self.strNaoIp, 9559 )
        audio.unsubscribe( self.getName() )
        self.s.close()
        print( "INF: SoundReceiver: stopped!" )
        if( self.outfile != None ):
            self.outfile.close()


    def processRemote( self, nbOfChannels, nbrOfSamplesByChannel, aTimeStamp, buffer ):
        """
        This is THE method that receives all the sound buffers from the "ALAudioDevice" module
        """

        data = np.fromstring(str(buffer), dtype=np.int16)

        print(data)
        self.s.send(data)








    # processRemote - end


    def version( self ):
        return "0.6"

# SoundReceiver - end


def main():
    """ Main entry point

    """
    pip   = "192.168.0.140"
    pport = 9559

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = naoqi.ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    # Warning: SoundReceiver must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global SoundReceiver
    SoundReceiver = SoundReceiverModule("SoundReceiver", pip)
    SoundReceiver.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)



if __name__ == "__main__":
    main()