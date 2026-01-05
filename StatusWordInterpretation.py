# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision N, 12/26/2025

Verified working on: Python 3.11/12/13 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################
import os
import sys
import platform

from pprint import pprint
from pprint import pformat
##########################################

##########################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

#########################################################
#########################################################
# https://drives.novantamotion.com/summit/0x6041-status-word
global StatusWordFlagNames_DictBitNumberAsKey
StatusWordFlagNames_DictBitNumberAsKey = dict([(0, "ReadyToSwitchOn"),  # Ready to switch on
                                                    (1, "SwitchedOn"),  # Switched on
                                                    (2, "OperationEnabled"),  # Operation enabled
                                                    (3, "Fault"),  # Fault
                                                    (4, "VoltageEnabled"),  # Voltage enabled
                                                    (5, "QuickStop"),  # Quick stop
                                                    (6, "SwitchOnDisabled"),  # Switch on disabled
                                                    (7, "Warning"),  # Warning
                                                    (10, "TargetReached"),  # Target reached
                                                    (11, "InternalLimitActive"),  # Internal limit active
                                                    (14, "InitialAngleDetProcFinished")])  # Initial angle determination process finished

global StatusWordFlagStates_DictEnglishNameAsKey
StatusWordFlagStates_DictEnglishNameAsKey = dict([("ReadyToSwitchOn", -1),
                                                       ("SwitchedOn", -1),
                                                       ("OperationEnabled", -1),
                                                       ("Fault", -1),
                                                       ("VoltageEnabled", -1),
                                                       ("QuickStop", -1),
                                                       ("SwitchOnDisabled", -1),
                                                       ("Warning", -1),
                                                       ("TargetReached", -1),
                                                       ("InternalLimitActive", -1),
                                                       ("InitialAngleDetProcFinished", -1)])
#########################################################
#########################################################

##########################################################################################################
##########################################################################################################
def StatusWordInterpretation(StatusWordToIntrepret):
    
    global StatusWordFlagNames_DictBitNumberAsKey
    global StatusWordFlagStates_DictEnglishNameAsKey
    
    '''
    https://drives.novantamotion.com/summit/0x6041-status-word
    Each bit in the device status word represents a device state or event.
    15: Reserved
    14: Initial angle determination process finished
    13: Operation mode specific
    12: Operation mode specific
    11: Internal limit active
    10: Target reached
    9: Remote
    8: Reserved
    7: Warning
    6: Switch on disabled
    5: Quick stop
    4: Voltage enabled
    3: Fault
    2: Operation enabled
    1: Switched on
    0: Ready to switch on
    '''

    try:
        StatusWordFlagStates_DictEnglishNameAsKey_TEMP = StatusWordFlagStates_DictEnglishNameAsKey.copy()

        ##########################################################################################################
        for BitNumber in StatusWordFlagNames_DictBitNumberAsKey:
            EnglishName = StatusWordFlagNames_DictBitNumberAsKey[BitNumber]
            State = StatusWordToIntrepret & (1 << BitNumber)

            StatusWordFlagStates_DictEnglishNameAsKey_TEMP[EnglishName] = bool(State)
        ##########################################################################################################

        return StatusWordFlagStates_DictEnglishNameAsKey_TEMP

    except:
        exceptions = sys.exc_info()[0]
        print("StatusWordInterpretation, exceptions: %s" % exceptions)
        return StatusWordFlagStates_DictEnglishNameAsKey.copy()
        traceback.print_exc()

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    StatusWord = 563 #0x4637
    #StatusWord = 1587 #0x4633

    print("StatusWord: " + str(StatusWord) + "\n" + pformat(StatusWordInterpretation(StatusWord)))

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################