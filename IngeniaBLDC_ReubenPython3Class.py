# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision O, 1/22/2026

Python 3.11/12 but NOT 3.13 (ingenialink requires scipy==1.12.0 compatible, which is NOT compatible with Python 3.13)
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

##########################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
##########################################

##########################################
from EntryListWithBlinking_ReubenPython2and3Class import *
from GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3 import *
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import math
import queue as Queue
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import signal #for CTRLc_HandlerFunction
import threading
import traceback
import subprocess
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
from functools import partial
from ingeniamotion import MotionController #Installation folder: C:\Anaconda3\Lib\site-packages\ingeniamotion
from ingeniamotion.enums import OperationMode
from ingenialink.pdo import RPDOMapItem, TPDOMapItem
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

##########################################################################################################
##########################################################################################################

class IngeniaBLDC_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### IngeniaBLDC_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.PrintAllReceivedSerialMessageForDebuggingFlag = 0

        self.UsePDOflag = 1

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        
        self.DedicatedPDOthread_StillRunningFlag = 0
        self.DedicatedTxThread_StillRunningFlag = 0
        self.DedicatedRxThread_StillRunningFlag = 0

        self.DedicatedTxThread_TxMessageToSend_Queue = Queue.Queue()

        self.DetectedSlaveID_List = []

        self.STO_EstopPRESSEDValue = 0x4
        self.STO_EstopNOTpressedValue = 0x17

        #########################################################
        self.SDOcommands_Rx_EnabledFlag = 1 #unicorn
        self.SDOcommands_Rx_PrintDebuggingStatementsFlag = 0
        #########################################################

        self.Position_AcceptableUnitsList = ["EncoderTicks", "Deg", "Rad", "Rev"]

        self.MostRecentDataDict = dict()

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #https://drives.novantamotion.com/cap-xcr/error-management#ErrorManagementcomoco-Faultreactionanderrormasking
        self.ErrorCodes_DictHexNumberAsKey_FromWebsite = dict([(0x00000000, "NoError"),
                                                           (0x00001001, "Communications watchdog error"),
                                                           (0x00002280, "Over-current detected (internal drive limit)"),
                                                           (0x00002281, "Faulty gate driver"),
                                                           (0x00002282, "Current A sensing reached upper saturation limit"),
                                                           (0x00002283, "Current A sensing reached lower saturation limit"),
                                                           (0x00002284, "Current B sensing reached upper saturation limit"),
                                                           (0x00002285, "Current B sensing reached lower saturation limit"),
                                                           (0x00002286, "Current C sensing reached upper saturation limit"),
                                                           (0x00002287, "Current C sensing reached lower saturation limit"),
                                                           (0x00002288, "User I2T limit detected without current control"),
                                                           (0x00002289, "Over-current detected (user limit) without current control"),
                                                           (0x0000228A, "System I2T detected"),
                                                           (0x0000228B, "Derating without current control"),
                                                           (0x0000228C, "Current sensor calibration error"),
                                                           (0x00002301, "Brake over-current"),
                                                           (0x00002302, "Brake tracking error"),
                                                           (0x00003210, "Over-voltage detected (internal drive limit)"),
                                                           (0x00003211, "Over-voltage detected (redundant internal drive limit)"),
                                                           (0x00003221, "Under-voltage detected (internal drive limit)"),
                                                           (0x00003231, "Over-voltage detected (user limit)"),
                                                           (0x00003241, "Under-voltage detected (user limit)"),
                                                           (0x00003280, "STO is enabled"),
                                                           (0x00003281, "STO supply fault"),
                                                           (0x00003282, "STO abnormal fault"),
                                                           (0x00003283, "STO active in operation enabled"),
                                                           (0x00003290, "Input stage problem"),
                                                           (0x00004300, "Over-Temperature detected (internal drive limit)"),
                                                           (0x00004301, "Under-Temperature detected (internal drive limit)"),
                                                           (0x00004303, "Over-temperature detected (user limit)"),
                                                           (0x00004304, "Under-temperature detected (user limit)"),
                                                           (0x00004305, "Wrong ADC measurements detection"),
                                                           (0x00004400, "Motor Over Temperature detected"),
                                                           (0x00004500, "External fault"),
                                                           (0x00007370, "Halls sequence error"),
                                                           (0x00007371, "Halls combination error"),
                                                           (0x00007372, "Feedback runaway error"),
                                                           (0x0000737E, "Absolute encoder 1 disconnection or frame overlap"),
                                                           (0x0000737F, "Absolute encoder 2 disconnection or frame overlap"),
                                                           (0x00007380, "Too many incorrect invalid position flags detected in SSI / BiSS - C readings"),
                                                           (0x00007381, "BiSS-C warning bit active"),
                                                           (0x00007382, "Too many incorrect CRC checks in SSI / BiSS-C readings"),
                                                           (0x00007384, "Absolute encoder error bit active without exceeding error tolerance"),
                                                           (0x00007385, "Position out of limits out of position modes"),
                                                           (0x00007386, "Velocity out of limits out of velocity or position modes"),
                                                           (0x00007387, "In a position mode, following error overcomes the position following error window"),
                                                           (0x00007388, "In a velocity mode, following error overcomes the velocity following error window"),
                                                           (0x0000738C, "Position out of limits in position mode"),
                                                           (0x00007390, "Interpolation time is too small when PVT is enabled."),
                                                           (0x00007391, "Profiler parameters not valid. They should all have positive values."),
                                                           (0x0000739A, "The electrical velocity limit has been exceeded"),
                                                           (0x0000739B, "Over-temperature warning detected (user limit)"),
                                                           (0x0000739C, "Under-temperature warning detected (user limit)"),
                                                           (0x0000F011, "Cyclic mode mapping error"),
                                                           (0x0000FF42, "EtherCAT cable disconnected"),
                                                           (0x0000FF43, "Cyclic timeout EtherCAT PDO lifeguard"),
                                                           (0x0000738B, "Trapezoidal commutation without digital halls not allowed"),
                                                           (0x00007400, "Unsupported synchronization method"),
                                                           (0x00007500, "Number of active feedbacks is higher than allowed"),
                                                           (0x00007503, "Access unsupported in the current state."),
                                                           (0x00007504, "Access unsupported because of local control"),
                                                           (0x05040000, "COMKIT Timeout. CORE device is not properly connected"),
                                                           (0x06010000, "Incorrect access type"),
                                                           (0x06020000, "Object does not exist"),
                                                           (0x06040041, "Object isn't cyclic mappable as requested"),
                                                           (0x06040042, "Cyclic mapping is too large"),
                                                           (0x06070010, "Mapped cyclic register size is wrong"),
                                                           (0x06090011, "Sub-Index does not exist"),
                                                           (0x060A0000, "Unsupported value introduced in register"),
                                                           (0x08000000, "Read / Write operation not executed"),
                                                           (0x08010000, "Cyclic mapping key is wrong"),
                                                           (0x08010010, "Communication state is unreachable"),
                                                           (0x08010020, "Communication setting is not modifiable in the current state"),
                                                           (0x08010030, "Invalid command"),
                                                           (0x08010040, "CRC error")])

        self.ErrorCodes_DictHexNumberAsKey_FromXDFfile = dict([(0x00003280, "STO is active and could have disabled the power stage disabled"),
                                                        (0x00002280, "HW over current"),
                                                        (0x00002288, "User I2T limit detected without current control"),
                                                        (0x00003290, "Input stage problem"),
                                                        (0x00003210, "HW Over-voltage detected"),
                                                        (0x00003211, "FW Over-voltage detected"),
                                                        (0x00003221, "FW Under-voltage detected"),
                                                        (0x00004300, "Over-Temperature detected (internal drive limit)."),
                                                        (0x00004301, "Under-Temperature detected (internal drive limit)"),
                                                        (0x00004400, "Motor Over Temperature error"),
                                                        (0x00007380, "Too many error bits or invalid position flags detected in absolute encoder"),
                                                        (0x00007382, "Too many incorrect CRC checks in absolute encoder readings"),
                                                        (0x00007385, "Position out of limits out of position modes"),
                                                        (0x00007386, "Velocity out of limits out of velocity or position modes"),
                                                        (0x00007387, "Position following error"),
                                                        (0x06010000, "Incorrect access type"),
                                                        (0x06020000, "Object doesn't exist"),
                                                        (0x06040041, "Object isn't PDO mappable as requested"),
                                                        (0x06070010, "Incorrect specified object size"),
                                                        (0x06090011, "Sub-Index does not exist"),
                                                        (0x060A0000, "Unsupported value introduced in register"),
                                                        (0x08000000, "Read / Write operation not executed"),
                                                        (0x00003231, "User Over-voltage detected"),
                                                        (0x00003241, "User Under-voltage detected"),
                                                        (0x00004303, "Over-temperature detected (user limit)"),
                                                        (0x00004304, "Under-temperature detected (user limit)"),
                                                        (0x00004500, "External error"),
                                                        (0x00007390, "Interpolation time is to small when PVT is enabled"),
                                                        (0x00003281, "Abnormal STO Supply. Unit could be damaged"),
                                                        (0x00003282, "Abnormal STO. STO1 and STO2 inputs differed more than latching time"),
                                                        (0x00007370, "Halls sequence error"),
                                                        (0x00007371, "Halls combination error"),
                                                        (0x00007372, "Feedback runaway error"),
                                                        (0x00002289, "Over current without current control"),
                                                        (0x00007391, "Profiler parameters not valid. They should all have positive values."),
                                                        (0x00000000, "NoError"),
                                                        (0x00007381, "BiSS-C warning bit active"),
                                                        (0x00001001, "Communications watchdog error"),
                                                        (0x00007388, "Velocity following error"),
                                                        (0x00007389, "Angle integrity check 1 error"),
                                                        (0x0000738A, "Angle integrity check 2 error"),
                                                        (0x0000738B, "Trapezoidal commutation without digital halls not allowed. Review commutation sensor configuration and phasing"),
                                                        (0x0000228A, "System I2T detected"),
                                                        (0x00007383, "Maximum absolute velocity exceeded"),
                                                        (0x0000738D, "Incremental encoder 1 index pulse integrity check fail"),
                                                        (0x0000738E, "Incremental encoder 2 index pulse integrity check fail"),
                                                        (0x00002281, "Fault detected in the power stage gate driver"),
                                                        (0x00002291, "Open phase detected"),
                                                        (0x00002290, "Non-zero total phase current"),
                                                        (0x00002282, "Current A sensing reached upper saturation limit"),
                                                        (0x00002283, "Current A sensing reached lower saturation limit"),
                                                        (0x00002284, "Current B sensing reached upper saturation limit"),
                                                        (0x00002285, "Current B sensing reached lower saturation limit"),
                                                        (0x00002286, "Current C sensing reached upper saturation limit"),
                                                        (0x00002287, "Current C sensing reached lower saturation limit"),
                                                        (0x0000738F, "Digital encoder index pulse integrity check calibration error"),
                                                        (0x00002302, "Brake current tracking error"),
                                                        (0x0000228B, "Current derating without current control"),
                                                        (0x00004305, "Wrong ADC measurements detection"),
                                                        (0x00004306, "User over temperature warning threshold exceeded."),
                                                        (0x00004307, "User under temperature warning threshold exceeded."),
                                                        (0x00003212, "Gate voltage out of limits"),
                                                        (0x00004501, "Load cell health signal error detected."),
                                                        (0x00004502, "Load cell analog input out of range"),
                                                        (0x00007393, "Current direct following error detected"),
                                                        (0x00007392, "Current quadrature following error detected"),
                                                        (0x00007384, "Absolute encoder error bit active without exceeding error tolerance"),
                                                        (0x05040000, "COM-KIT Timeout. CORE device is not properly connected"),
                                                        (0x0000FF42, "EtherCAT cable is disconnected during operation"),
                                                        (0x00008130, "Lifeguard error or heartbeat error in CANOpen communication"),
                                                        (0x0000FF43, "Cyclic timeout Ethercat PDO lifeguard"),
                                                        (0x00007394, "Emergency position set-point not configured."),
                                                        (0x0000F011, "Cyclic mode mapping error"),
                                                        (0x0000228C, "Current calibration error"),
                                                        (0x0000737E, "Absolute encoder 1 disconnection or frame overlap"),
                                                        (0x0000737F, "Absolute encoder 2 disconnection or frame overlap"),
                                                        (0x00008210, "PDO not processed due to length error"),
                                                        (0x0000738C, "Position out of limits in position mode"),
                                                        (0x00003283, "STO is active in operation enabled and has disabled the power stage"),
                                                        (0x00002301, "Brake over-current")])

        self.ErrorCodes_DictHexNumberAsKey = self.ErrorCodes_DictHexNumberAsKey_FromXDFfile #unicorn
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CommutationMode_DictIntNumberAsKey = dict([(0, "Brushless_3phase_SVM_Sinusoidal"),
                                                         (1, "Brushless_3phase_SVM_Trapezoidal"),
                                                         (2, "BrushedDC_2phase")])

        self.CommutationMode_DictEnglishNameAsKey = dict([("Brushless_3phase_SVM_Sinusoidal", 0),
                                                         ("Brushless_3phase_SVM_Trapezoidal", 1),
                                                         ("BrushedDC_2phase", 2)])
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OperationMode_ListOfAcceptableValuesStrings = ["CyclicPosition",
                                                            "CyclicCurrent",
                                                            "CyclicVoltage"]

        self.OperationMode_DictIntNumberAsKey = dict([(0, "Voltage"),
                                                     (1, "CurrentAmplifier"),
                                                     (2, "Current"),
                                                     (34, "CyclicCurrent"),
                                                     (3, "Velocity"),
                                                     (35, "CyclicVelocity"),
                                                     (19, "ProfileVelocity"),
                                                     (4, "Position"),
                                                     (36, "CyclicPosition"),
                                                     (20, "ProfilePosition"),
                                                     (68, "ProfilePositionScurve"),
                                                     (180, "PVT"),
                                                     (275, "Homing")])
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #https://drives.novantamotion.com/summit/0x6041-status-word
        self.StatusWordFlagNames_DictBitNumberAsKey = dict([(0, "ReadyToSwitchOn"),                #Ready to switch on
                                                            (1, "SwitchedOn"),                      #Switched on
                                                            (2, "OperationEnabled"),                #Operation enabled
                                                            (3, "Fault"),                           #Fault
                                                            (4, "VoltageEnabled"),                  #Voltage enabled
                                                            (5, "QuickStop"),                       #Quick stop
                                                            (6, "SwitchOnDisabled"),                #Switch on disabled
                                                            (7, "Warning"),                         #Warning
                                                            (10, "TargetReached"),                  #Target reached
                                                            (11, "InternalLimitActive"),            #Internal limit active
                                                            (14, "InitialAngleDetProcFinished")])   #Initial angle determination process finished

        self.StatusWordFlagStates_DictEnglishNameAsKey = dict([("ReadyToSwitchOn", -1),
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

        #########################################################
        #########################################################
        #https://drives.novantamotion.com/summit/0x251a-sto-status

        self.STOstatusFlagNames_DictBitNumberAsKey = dict([(0, "STO1state"),                #0: STO1 State
                                                            (1, "STO2state"),               #1: STO2 State
                                                            (2, "STOSupplyFault"),          #2: /STO Supply Fault
                                                            (3, "STOabnormalFault"),        #3: STO Abnormal Fault
                                                            (4, "STOreport")])              #4: STO Report
        
        self.STOstatusFlagStates_DictEnglishNameAsKey = dict([("STO1state", -1),
                                                            ("STO2state", -1),
                                                            ("OperationEnabled", -1),
                                                            ("STOSupplyFault", -1),
                                                            ("STOabnormalFault", -1),
                                                            ("STOreport", -1)])
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromGUIthread = -11111.0
        self.LastTime_CalculatedFromGUIthread = -11111.0
        self.StartingTime_CalculatedFromGUIthread = -11111.0
        self.DataStreamingFrequency_CalculatedFromGUIthread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromGUIthread = -11111.0
        
        self.CurrentTime_CalculatedFromDedicatedTxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedTxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = -11111.0

        self.LastTimeHeartbeatWasSent_CalculatedFromDedicatedTxThread = -11111.0

        self.CurrentTime_CalculatedFromDedicatedRxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedRxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = -11111.0
        
        self.CurrentTime_CalculatedFromDedicatedPDOThread = -11111.0
        self.LastTime_CalculatedFromDedicatedPDOThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedPDOThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedPDOThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedPDOThread = -11111.0
        
        self.CurrentTime_CalculatedFromRPDOcallback = -11111.0
        self.LastTime_CalculatedFromRPDOcallback = -11111.0
        self.StartingTime_CalculatedFromRPDOcallback = -11111.0
        self.DataStreamingFrequency_CalculatedFromRPDOcallback = -11111.0
        self.DataStreamingDeltaT_CalculatedFromRPDOcallback = -11111.0
        
        self.CurrentTime_CalculatedFromTPDOcallback = -11111.0
        self.LastTime_CalculatedFromTPDOcallback = -11111.0
        self.StartingTime_CalculatedFromTPDOcallback = -11111.0
        self.DataStreamingFrequency_CalculatedFromTPDOcallback = -11111.0
        self.DataStreamingDeltaT_CalculatedFromTPDOcallback = -11111.0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.ListOfAcceptableVariableNameStringsForReading = ["Position_Actual_EncoderTicks",
                                                                "Velocity_Actual_EncoderTicks",
                                                                "Current_Direct_Actual",
                                                                "Current_Quadrature_Actual",
                                                                "EnabledState_Actual"] #unicorn
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("IngeniaBLDC_ReubenPython3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in setup_dict:
            self.GUIparametersDict = setup_dict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("IngeniaBLDC_ReubenPython3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("IngeniaBLDC_ReubenPython3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            ##########################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("IngeniaBLDC_ReubenPython3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("IngeniaBLDC_ReubenPython3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("IngeniaBLDC_ReubenPython3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in setup_dict:
            self.NameToDisplay_UserSet = str(setup_dict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("IngeniaBLDC_ReubenPython3Class __init__: NameToDisplay_UserSet" + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredInterfaceName" in setup_dict:
            self.DesiredInterfaceName = setup_dict["DesiredInterfaceName"]

        else:
            print("IngeniaBLDC_ReubenPython3Class __init__: ERROR, must initialize object with 'DesiredInterfaceName' argument.")
            return

        print("IngeniaBLDC_ReubenPython3Class __init__: DesiredInterfaceName: " + str(self.DesiredInterfaceName))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredInterfaceName_MustItBeExactMatchFlag" in setup_dict:
            self.DesiredInterfaceName_MustItBeExactMatchFlag = self.PassThrough0and1values_ExitProgramOtherwise("DesiredInterfaceName_MustItBeExactMatchFlag", setup_dict["DesiredInterfaceName_MustItBeExactMatchFlag"])

        else:
            self.DesiredInterfaceName_MustItBeExactMatchFlag = 1

        print("IngeniaBLDC_ReubenPython3Class __init__: DesiredInterfaceName_MustItBeExactMatchFlag: " + str(self.DesiredInterfaceName_MustItBeExactMatchFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSlaves_DictOfDicts" in setup_dict:
            DesiredSlaves_DictOfDicts_TEMP = setup_dict["DesiredSlaves_DictOfDicts"]

            self.DesiredSlaves_DictOfDicts = dict()
            self.DesiredSlaveID_List = []
            for SlaveID_Int in DesiredSlaves_DictOfDicts_TEMP:
                if SlaveID_Int in range(1, 255):
                    self.DesiredSlaveID_List.append(int(SlaveID_Int))
                    self.DesiredSlaves_DictOfDicts[SlaveID_Int] = DesiredSlaves_DictOfDicts_TEMP[SlaveID_Int]
                else:
                    print("IngeniaBLDC_ReubenPython3Class __init__: Error, each element in 'DesiredSlaveID_List' but be an integer in the range [1, 255]")

        else:
            self.DesiredSlaves_DictOfDicts = [1]

        print("IngeniaBLDC_ReubenPython3Class __init__: DesiredSlaves_DictOfDicts: " + str(self.DesiredSlaves_DictOfDicts))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict = dict()
        for SlaveID_Int in self.DesiredSlaveID_List:
            self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int] = dict([("PDO_ListOfTPDOvariableNames",[]),("PDO_ListOfRPDOvariableNames", [])]) #Does not include all keys
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.IngeniaMotionController_GUIobjectsOnlyDict = dict()
        for SlaveID_Int in self.DesiredSlaveID_List:
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int] = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #########################################################
        #########################################################
        self.IngeniaMotionController_MainDict = dict()
        for SlaveID_Int in self.DesiredSlaveID_List:

            ######################################################### unicorn
            #########################################################
            #########################################################
            self.IngeniaMotionController_MainDict[SlaveID_Int] = dict([("SlaveID_Int", SlaveID_Int),
                                                                        ("AliasOrServoName_String", str(SlaveID_Int)),
                                                                        ("JointEnglishName", ""),
                                                                        ("MotorConnectedFlag", 0),

                                                                        ("SerialNumber_Actual", -1),
                                                                        ("VendorID_Actual", -1),
                                                                        ("ProductCode_Actual", -1),
                                                                        ("FWversion_Actual", -1),

                                                                        ("BusVoltage", 24.0),

                                                                        ("OperationMode", "CyclicPosition"),
                                                                        ("OperationMode_Actual_Int", -11111),
                                                                        ("OperationMode_Actual_EnglishName", "default"),

                                                                        ("Status_Word", -1),
                                                                        ("StatusWordFlagStates_DictEnglishNameAsKey", dict()),

                                                                        ("STO_Status", -1),
                                                                        ("STO_Status_last", -1),
                                                                        ("STOstatusFlagStates_DictEnglishNameAsKey", dict()),

                                                                        ("Error_Last_HexCode", -1),
                                                                        ("Error_Last_EnglishName", ""),

                                                                        ("FaultReset_EventNeedsToBeFiredFlag", 0),
                                                                        ("ResetFaults_EventNeedsToBeFiredFlag", 0),

                                                                        ("EnabledState_ToBeSet", 0),
                                                                        ("EnabledState_NeedsToBeSetFlag", 0),
                                                                        ("EnabledState_Actual", -1),

                                                                        ("DynamicBrakingEnabledState_ToBeSet", -1),
                                                                        ("DynamicBrakingEnabledState_NeedsToBeSetFlag", 0),
                                                                        ("DynamicBrakingEnabledState_Actual", -1),

                                                                        ("EncoderTicksPerRevolution_ToBeSet", 1),
                                                                        ("EncoderTicksPerRevolution_Actual", -11111),
                                                                        ("EncoderOffset_NeedsToBeSetFlag", 0),
                                                                        ("ZeroEncoder_EventNeedsToBeFiredFlag", 0),
                                                                        ("ZeroEncoder_FireEventOnStartupFlag", 0),
                                                                        ("AllowEncoderToBeZeroedFlag", 1),

                                                                        ("Position_ToBeSet_EncoderTicks", 0.0),
                                                                        ("Position_NeedsToBeSetFlag", 0), #Not needed when using TPDO
                                                                        ("Position_ToBeSet_AllUnitsDict", dict([("EncoderTicks", 0.0), ("Deg", 0.0), ("Rad", 0.0), ("Rev", 0.0)])),

                                                                        ("Position_Actual_EncoderTicks", -11111.0),
                                                                        ("Position_Actual_AllUnitsDict", dict([("EncoderTicks", -1.11111), ("Deg", -1.11111), ("Rad", -1.11111), ("Rev", -1.11111)])),

                                                                        ("HallEffectValue_Actual_Int", -1),

                                                                        ("PositionSetPoint_Actual_EncoderTicks", -11111.0),
                                                                        ("PositionSetPoint_Actual_AllUnitsDict", dict([("EncoderTicks", -1.11111), ("Deg", -1.11111), ("Rad", -1.11111), ("Rev", -1.11111)])),

                                                                        ("PositionMinRange_EncoderTicks_Actual", -11111),
                                                                        ("PositionMaxRange_EncoderTicks_Actual", -11111),
                                                                        ("PositionMin_EncoderTicks_Actual", -11111),
                                                                        ("PositionMax_EncoderTicks_Actual", -11111),
                                                                        ("PositionMinAndMaxInEncoderTicks_NeedsToBeSetFlag", 0),

                                                                        ("PositionFollowingErrorWindow_ToBeSet", -11111.0),
                                                                        ("PositionFollowingErrorTimeoutMilliseconds_ToBeSet", -11111.0),
                                                                        ("PositionFollowingErrorFaultModeInt_ToBeSet", 0),
                                                                        ("PositionFollowingErrorWindow_Actual", -11111.0),
                                                                        ("PositionFollowingErrorTimeoutMilliseconds_Actual", -11111.0),
                                                                        ("PositionFollowingErrorFaultModeInt_Actual", -11111),
                                                                        ("PositionFollowingErrorWindowTimeoutAndFaultParameters_NeedsToBeSetFlag", -11111.0),

                                                                        ("PositionPIDgains_Kp_Actual", -11111.0),
                                                                        ("PositionPIDgains_Ki_Actual", -11111.0),
                                                                        ("PositionPIDgains_Kd_Actual", -11111.0),
                                                                        ("PositionPIDgains_Kp_ToBeSet", -11111.0),
                                                                        ("PositionPIDgains_Ki_ToBeSet", -11111.0),
                                                                        ("PositionPIDgains_Kd_ToBeSet", -11111.0),
                                                                        ("PositionPIDgains_NeedsToBeSetFlag", 0),

                                                                        ("MaxVelocity_ToBeSet", -11111.0),
                                                                        ("MaxVelocity_NeedsToBeSetFlag", 0),
                                                                        ("MaxVelocity_Actual", -11111.0),

                                                                        ("MaxProfileVelocity_ToBeSet", -11111.0),
                                                                        ("MaxProfileVelocity_NeedsToBeSetFlag", 0),
                                                                        ("MaxProfileVelocity_Actual", -11111.0),

                                                                        ("Velocity_Actual_EncoderTicks", -11111.0),
                                                                        ("Velocity_Actual_AllUnitsDict", dict([("EncoderTicks", -1.11111), ("Deg", -1.11111), ("Rad", -1.11111), ("Rev", -1.11111)])),

                                                                        ("VelocityPIDgains_Kp_Actual", -11111.0),
                                                                        ("VelocityPIDgains_Ki_Actual", -11111.0),
                                                                        ("VelocityPIDgains_Kd_Actual", -11111.0),
                                                                        ("VelocityPIDgains_Kp_ToBeSet", -11111.0),
                                                                        ("VelocityPIDgains_Ki_ToBeSet", -11111.0),
                                                                        ("VelocityPIDgains_Kd_ToBeSet", -11111.0),
                                                                        ("VelocityPIDgains_NeedsToBeSetFlag", 0),

                                                                        ("MaxProfileAcceleration_ToBeSet", -11111.0),
                                                                        ("MaxProfileAcceleration_NeedsToBeSetFlag", 0),
                                                                        ("MaxProfileAcceleration_Actual", -11111.0),

                                                                        ("Current_FOCcombinedDQ_Actual", 0.0),

                                                                        ("Current_Direct_ToBeSet", 0.0),
                                                                        ("Current_Direct_NeedsToBeSetFlag", 0),
                                                                        ("Current_Direct_Actual", 0.0),

                                                                        ("Current_Quadrature_ToBeSet", 0.0),
                                                                        ("Current_Quadrature_NeedsToBeSetFlag", 0),
                                                                        ("Current_Quadrature_Actual", 0.0),

                                                                        ("MaxCurrentHardLimit_ToBeSet", -11111.0),
                                                                        ("MaxCurrentHardLimit_NeedsToBeSetFlag", 0),
                                                                        ("MaxCurrentHardLimit_Actual", -11111.0),

                                                                        ("MaxContinuousCurrent_ToBeSet", -11111.0),
                                                                        ("MaxContinuousCurrent_NeedsToBeSetFlag", 0),
                                                                        ("MaxContinuousCurrent_Actual", -11111.0),

                                                                        ("PeakCurrentValue_ToBeSet", -11111.0),
                                                                        ("PeakCurrentTimeMilliseconds_ToBeSet", -11111.0),
                                                                        ("PeakCurrentFaultModeInt_ToBeSet", 0),
                                                                        ("PeakCurrentValueTimeAndFaultParameters_NeedsToBeSetFlag", -11111.0),
                                                                        ("PeakCurrentValue_Actual", -11111.0),
                                                                        ("PeakCurrentTimeMilliseconds_Actual", -11111.0),
                                                                        ("PeakCurrentTime_Actual", -11111.0),
                                                                        ("PeakCurrentFaultModeInt_Actual", -11111),

                                                                        ("CurrentDirectPIgains_Kp_ToBeSet", -11111.0),
                                                                        ("CurrentDirectPIgains_Ki_ToBeSet", -11111.0),
                                                                        ("CurrentDirectPIgains_NeedsToBeSetFlag", 0),
                                                                        ("CurrentDirectPIgains_Kp_Actual", -11111.0),
                                                                        ("CurrentDirectPIgains_Ki_Actual", -11111.0),
                                                                        ("CurrentDirect_CL_CUR_D_MAX_OUT_Actual", -11111.0),
                                                                        ("CurrentDirect_CL_CUR_D_MIN_OUT_Actual", -11111.0),
                                                                       
                                                                        ("CurrentQuadraturePIgains_Kp_ToBeSet", -11111.0),
                                                                        ("CurrentQuadraturePIgains_Ki_ToBeSet", -11111.0),
                                                                        ("CurrentQuadraturePIgains_NeedsToBeSetFlag", 0),
                                                                        ("CurrentQuadraturePIgains_Kp_Actual", -11111.0),
                                                                        ("CurrentQuadraturePIgains_Ki_Actual", -11111.0),
                                                                        ("CurrentQuadrature_CL_CUR_Q_MAX_OUT_Actual", -11111.0),
                                                                        ("CurrentQuadrature_CL_CUR_Q_MIN_OUT_Actual", -11111.0),

                                                                        ("Voltage_Quadrature_ToBeSet", 0.0),
                                                                        ("Voltage_Quadrature_NeedsToBeSetFlag", 0),

                                                                        ("CommutationMode_ToBeSet_EnglishName", "Brushless_3phase_SVM_Sinusoidal"),
                                                                        ("CommutationMode_Actual_Int", -1),
                                                                        ("CommutationMode_Actual_EnglishName", "default"),

                                                                        ("ListOfVariableNameStringsToGetViaSDO", []),
                                                                        ("GetSDOvariablesEveryNloopsCycles", 0),
                                                                        ("AskForInfrequentDataReadLoopCounter", 0)])
            #########################################################
            #########################################################
            #########################################################

            ######################################################### Copy all info from DesiredSlaves_DictOfDicts into IngeniaMotionController_MainDict
            #########################################################
            #########################################################
            for Key in self.DesiredSlaves_DictOfDicts[SlaveID_Int]:
                self.IngeniaMotionController_MainDict[SlaveID_Int][Key] = self.DesiredSlaves_DictOfDicts[SlaveID_Int][Key]
                #print(Key + ", " + str(self.DesiredSlaves_DictOfDicts[SlaveID_Int][Key]))

            #########################################################
            #########################################################
            #########################################################

            ######################################################### Perform a special search for Position_Min and Position_Max and convert to all units
            #########################################################
            #########################################################
            for Key in self.DesiredSlaves_DictOfDicts[SlaveID_Int]:

                #########################################################
                #########################################################
                if Key.find("Position_Min") != -1:

                    #########################################################
                    UnitType_TEMP = "unknown"
                    for UnitType in self.Position_AcceptableUnitsList:
                        if Key.find(UnitType) != -1:
                            UnitType_TEMP = UnitType
                    #########################################################

                    #########################################################
                    if UnitType_TEMP != "unknown": #Meaning that we located an acceptable unit type:
                        PositionMin_TEMP = self.DesiredSlaves_DictOfDicts[SlaveID_Int][Key]
                        PositionMin_TEMP_ConvertedToAllUnits = self.ConvertPositionToAllUnits(SlaveID_Int, PositionMin_TEMP, UnitType_TEMP)
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"] = PositionMin_TEMP_ConvertedToAllUnits

                    else:
                        pass
                    #########################################################

                #########################################################
                #########################################################

                #########################################################
                #########################################################
                if Key.find("Position_Max") != -1:

                    #########################################################
                    UnitType_TEMP = "unknown"
                    for UnitType in self.Position_AcceptableUnitsList:
                        if Key.find(UnitType) != -1:
                            UnitType_TEMP = UnitType
                    #########################################################

                    #########################################################
                    if UnitType_TEMP != "unknown": #Meaning that we located an acceptable unit type:
                        PositionMax_TEMP = self.DesiredSlaves_DictOfDicts[SlaveID_Int][Key]
                        PositionMax_TEMP_ConvertedToAllUnits = self.ConvertPositionToAllUnits(SlaveID_Int, PositionMax_TEMP, UnitType_TEMP)
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"] = PositionMax_TEMP_ConvertedToAllUnits

                    else:
                        pass
                    #########################################################

                #########################################################
                #########################################################

            #########################################################
            #########################################################
            #########################################################

            ######################################################### If the min and max weren't passed in, then set them to 0. DON'T put them in the original initialization "self.IngeniaMotionController_MainDict[SlaveID_Int] = dict(["
            #########################################################
            #########################################################
            for Key in self.DesiredSlaves_DictOfDicts[SlaveID_Int]:
                if "PositionMin_AllUnitsDict" not in self.IngeniaMotionController_MainDict[SlaveID_Int]:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, 0.0, "EncoderTicks")

                if "PositionMax_AllUnitsDict" not in self.IngeniaMotionController_MainDict[SlaveID_Int]:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, 0.0, "EncoderTicks")
            #########################################################
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            #########################################################
            if self.DesiredSlaves_DictOfDicts[SlaveID_Int]["OperationMode"] in ["CyclicCurrent", "CyclicVoltage"]:
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, 0.0, "EncoderTicks") #Must disable position limits for current and voltage modes.
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, 0.0, "EncoderTicks") #Must disable position limits for current and voltage modes.
            #########################################################
            #########################################################
            #########################################################

        #########################################################
        #########################################################
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedRxThread_TimeToSleepEachLoop" in setup_dict:
            self.DedicatedRxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedRxThread_TimeToSleepEachLoop", setup_dict["DedicatedRxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedRxThread_TimeToSleepEachLoop = 0.001

        print("IngeniaBLDC_ReubenPython3Class __init__: DedicatedRxThread_TimeToSleepEachLoop: " + str(self.DedicatedRxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DedicatedTxThread_TimeToSleepEachLoop" in setup_dict:
            self.DedicatedTxThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DedicatedTxThread_TimeToSleepEachLoop", setup_dict["DedicatedTxThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.DedicatedTxThread_TimeToSleepEachLoop = 0.001

        print("IngeniaBLDC_ReubenPython3Class __init__: DedicatedTxThread_TimeToSleepEachLoop: " + str(self.DedicatedTxThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "PDO_UpdateDeltaTinSeconds" in setup_dict:
            self.PDO_UpdateDeltaTinSeconds = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("PDO_UpdateDeltaTinSeconds", setup_dict["PDO_UpdateDeltaTinSeconds"], 0.001, 100000)

        else:
            self.PDO_UpdateDeltaTinSeconds = 0.010

        print("IngeniaBLDC_ReubenPython3Class __init__: PDO_UpdateDeltaTinSeconds: " + str(self.PDO_UpdateDeltaTinSeconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EnableMotorAutomaticallyAfterEstopRestorationFlag" in setup_dict:
            self.EnableMotorAutomaticallyAfterEstopRestorationFlag = self.PassThrough0and1values_ExitProgramOtherwise("EnableMotorAutomaticallyAfterEstopRestorationFlag", setup_dict["EnableMotorAutomaticallyAfterEstopRestorationFlag"])

        else:
            self.EnableMotorAutomaticallyAfterEstopRestorationFlag = 1

        print("IngeniaBLDC_ReubenPython3Class __init__: EnableMotorAutomaticallyAfterEstopRestorationFlag: " + str(self.EnableMotorAutomaticallyAfterEstopRestorationFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "EnableMotorAtStartOfProgramFlag" in setup_dict:
            self.EnableMotorAtStartOfProgramFlag = self.PassThrough0and1values_ExitProgramOtherwise("EnableMotorAtStartOfProgramFlag", setup_dict["EnableMotorAtStartOfProgramFlag"])

        else:
            self.EnableMotorAtStartOfProgramFlag = 0

        print("IngeniaBLDC_ReubenPython3Class __init__: EnableMotorAtStartOfProgramFlag: " + str(self.EnableMotorAtStartOfProgramFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CheckDetectedVsDesiredSlaveListFlag" in setup_dict:
            self.CheckDetectedVsDesiredSlaveListFlag = self.PassThrough0and1values_ExitProgramOtherwise("CheckDetectedVsDesiredSlaveListFlag", setup_dict["CheckDetectedVsDesiredSlaveListFlag"])

        else:
            self.CheckDetectedVsDesiredSlaveListFlag = 0

        print("IngeniaBLDC_ReubenPython3Class __init__: CheckDetectedVsDesiredSlaveListFlag: " + str(self.CheckDetectedVsDesiredSlaveListFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromDedicatedPDOThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                             ("DataStreamingFrequency_CalculatedFromDedicatedTxThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                             ("DataStreamingFrequency_CalculatedFromDedicatedRxThread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromGUIthread", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1), ("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromTPDOcallback", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                            ("DataStreamingFrequency_CalculatedFromRPDOcallback", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)]))])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict = dict([("DictOfVariableFilterSettings", self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings)])

        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject = LowPassFilterForDictsOfLists_ReubenPython2and3Class(self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_setup_dict)
        self.LOWPASSFILTER_OPEN_FLAG = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG
        #########################################################

        #########################################################
        if self.LOWPASSFILTER_OPEN_FLAG != 1:
            print("IngeniaBLDC_ReubenPython3Class __init__: Failed to open LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.")
            return
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            SuccessFlag = self.InitializeMotors()

            if SuccessFlag != 1:
                print("IngeniaBLDC_ReubenPython3Class __init__: self.InitializeMotors() failed.")
                return

        except:
            exceptions = sys.exc_info()[0]
            print("IngeniaBLDC_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        '''
        THIS MUST BE CALLED FROM PARENT PROGRAM:
        if IngeniaBLDC_OPEN_FLAG == 1:
            if IngeniaBLDC_Object.IsDedicatedPDOthreadStillRunning() == 0:
                IngeniaBLDC_Object.StartPDOdedicatedThread()
        '''
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedRxThread_ThreadingObject = threading.Thread(target=self.DedicatedRxThread, args=())
        self.DedicatedRxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.DedicatedTxThread_ThreadingObject = threading.Thread(target=self.DedicatedTxThread, args=())
        self.DedicatedTxThread_ThreadingObject.start()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CTRLc_RegisterHandlerFunction()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

        print("#################### IngeniaBLDC_ReubenPython3Class __init__ ending. ####################")

    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_RegisterHandlerFunction(self):

        CurrentHandlerRegisteredForSIGINT = signal.getsignal(signal.SIGINT)
        defaultish = (signal.SIG_DFL, signal.SIG_IGN, None, getattr(signal, "default_int_handler", None)) #Treat Python's built-in default handler as "unregistered"

        if CurrentHandlerRegisteredForSIGINT in defaultish:  # Only install if it's default/ignored (i.e., nobody set it yet)
            signal.signal(signal.SIGINT, self.CTRLc_HandlerFunction)
            print("IngeniaBLDC_ReubenPython3Class, CTRLc_RegisterHandlerFunction event fired!")

        else:
            print("IngeniaBLDC_ReubenPython3Class, could not register CTRLc_RegisterHandlerFunction (already registered previously)")
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## MUST ISSUE CTRLc_RegisterHandlerFunction() AT START OF PROGRAM
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def CTRLc_HandlerFunction(self, signum, frame):

        print("IngeniaBLDC_ReubenPython3Class, CTRLc_HandlerFunction event firing!")

        self.ExitProgram_Callback()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(self, CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction):

        self.TimerObject = threading.Timer(CallbackAfterDeltaTseconds, FunctionToCall_NoParenthesesAfterFunctionName, ArgumentListToFunction) #Must pass arguments to callback-function via list as the third argument to Timer call
        self.TimerObject.daemon = True #Without the daemon=True, this recursive function won't terminate when the main program does.
        self.TimerObject.start()

        print("TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName event fired to call function: '" + str(FunctionToCall_NoParenthesesAfterFunctionName.__name__) + "' at time " + str(self.getPreciseSecondsTimeStampString()))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
                              str(InputNameString) +
                              "' must be 0 or 1 (value was " +
                              str(InputNumber_ConvertedToFloat) +
                              "). Press any key (and enter) to exit.")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print(self.TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict()  # So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedPDOThread_Filtered(self):

        try:

            self.DataStreamingDeltaT_CalculatedFromDedicatedPDOThread = self.CurrentTime_CalculatedFromDedicatedPDOThread - self.LastTime_CalculatedFromDedicatedPDOThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedPDOThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedPDOThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedPDOThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedPDOThread", DataStreamingFrequency_CalculatedFromDedicatedPDOThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedPDOThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedPDOThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedPDOThread = self.CurrentTime_CalculatedFromDedicatedPDOThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedPDOThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedTxThread_Filtered(self):

        try:

            self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread - self.LastTime_CalculatedFromDedicatedTxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedTxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedTxThread", DataStreamingFrequency_CalculatedFromDedicatedTxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedTxThread = self.CurrentTime_CalculatedFromDedicatedTxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedTxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_DedicatedRxThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread - self.LastTime_CalculatedFromDedicatedRxThread

            if self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread != 0.0:
                DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromDedicatedRxThread", DataStreamingFrequency_CalculatedFromDedicatedRxThread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = ResultsDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromDedicatedRxThread = self.CurrentTime_CalculatedFromDedicatedRxThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_DedicatedRxThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_GUIthread_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromGUIthread = self.getPreciseSecondsTimeStampString()

            self.DataStreamingDeltaT_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread - self.LastTime_CalculatedFromGUIthread

            if self.DataStreamingDeltaT_CalculatedFromGUIthread != 0.0:
                DataStreamingFrequency_CalculatedFromGUIthread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromGUIthread

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromGUIthread", DataStreamingFrequency_CalculatedFromGUIthread_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromGUIthread = ResultsDict["DataStreamingFrequency_CalculatedFromGUIthread"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromGUIthread = self.CurrentTime_CalculatedFromGUIthread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_GUIthread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromTPDOcallback_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromTPDOcallback = self.getPreciseSecondsTimeStampString()
            
            self.DataStreamingDeltaT_CalculatedFromTPDOcallback = self.CurrentTime_CalculatedFromTPDOcallback - self.LastTime_CalculatedFromTPDOcallback

            if self.DataStreamingDeltaT_CalculatedFromTPDOcallback != 0.0:
                DataStreamingFrequency_CalculatedFromTPDOcallback_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromTPDOcallback

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromTPDOcallback", DataStreamingFrequency_CalculatedFromTPDOcallback_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromTPDOcallback = ResultsDict["DataStreamingFrequency_CalculatedFromTPDOcallback"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromTPDOcallback = self.CurrentTime_CalculatedFromTPDOcallback
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_CalculatedFromTPDOcallback_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_CalculatedFromRPDOcallback_Filtered(self):

        try:
            self.CurrentTime_CalculatedFromRPDOcallback = self.getPreciseSecondsTimeStampString()
            
            self.DataStreamingDeltaT_CalculatedFromRPDOcallback = self.CurrentTime_CalculatedFromRPDOcallback - self.LastTime_CalculatedFromRPDOcallback

            if self.DataStreamingDeltaT_CalculatedFromRPDOcallback != 0.0:
                DataStreamingFrequency_CalculatedFromRPDOcallback_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromRPDOcallback

                ResultsDict = self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject.AddDataDictFromExternalProgram(dict([("DataStreamingFrequency_CalculatedFromRPDOcallback", DataStreamingFrequency_CalculatedFromRPDOcallback_TEMP)]))
                self.DataStreamingFrequency_CalculatedFromRPDOcallback = ResultsDict["DataStreamingFrequency_CalculatedFromRPDOcallback"]["Filtered_MostRecentValuesList"][0]

            self.LastTime_CalculatedFromRPDOcallback = self.CurrentTime_CalculatedFromRPDOcallback
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_CalculatedFromRPDOcallback_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def InitializeMotors(self):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            print("IngeniaBLDC_ReubenPython3Class, Entering 'InitializeMotors'.")

            ##########################################################################################################
            ##########################################################################################################
            self.IngeniaMotionControllerObject = MotionController()

            InterfaceList = self.IngeniaMotionControllerObject.communication.get_interface_name_list()
            print("InterfaceList:")

            CorrectInterfaceIndex = -1
            for Index, Interface in enumerate(InterfaceList):
                print("Index: " + str(Index) + ", InterfaceName: " + str(Interface))

                if self.DesiredInterfaceName_MustItBeExactMatchFlag == 1:
                    if Interface == self.DesiredInterfaceName:
                        CorrectInterfaceIndex = Index
                        break
                else:
                    if Interface.find(self.DesiredInterfaceName) != -1:
                        CorrectInterfaceIndex = Index
                        break
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            if CorrectInterfaceIndex == -1:
                print("InitializeMotors: Could not locate CorrectInterfaceIndex = " + str(CorrectInterfaceIndex))
                return 0

            InterfaceSelected = self.IngeniaMotionControllerObject.communication.get_ifname_by_index(CorrectInterfaceIndex)
            print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': InterfaceSelected:")
            print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': Interface index: " + str(CorrectInterfaceIndex))
            print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': Interface identifier: " + str(InterfaceSelected))
            print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': Interface name: " + str(InterfaceList[CorrectInterfaceIndex]))
            ##########################################################################################################

            ##########################################################################################################
            DetectedSlaveID_List_ORIGINAL = self.IngeniaMotionControllerObject.communication.scan_servos_ethercat(InterfaceSelected)
            print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': DetectedSlaveID_List_ORIGINAL: " + str(DetectedSlaveID_List_ORIGINAL))

            self.DetectedSlaveID_List = []

            DetectedVsDesiredMismatchFlag = 0
            for SlaveID_Int in DetectedSlaveID_List_ORIGINAL:
                if SlaveID_Int not in self.DesiredSlaveID_List:
                    print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': error, DetectedSlaveID = " + str(SlaveID_Int)  + " is not in self.DesiredSlaveID_List.")
                    DetectedVsDesiredMismatchFlag = 1
                else:
                    self.DetectedSlaveID_List.append(SlaveID_Int)

            for SlaveID_Int in self.DesiredSlaveID_List:
                if SlaveID_Int not in DetectedSlaveID_List_ORIGINAL:
                    print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': error, DesiredlaveID = " + str(SlaveID_Int)  + " is not in self.DetectedSlaveID_List.")
                    DetectedVsDesiredMismatchFlag = 1

            print("IngeniaBLDC_ReubenPython3Class, 'InitializeMotors': self.DetectedSlaveID_List: " + str(self.DetectedSlaveID_List))
            ##########################################################################################################

            ##########################################################################################################
            if self.CheckDetectedVsDesiredSlaveListFlag == 1:
                if DetectedVsDesiredMismatchFlag == 1:
                    print("InitializeMotors, error: DesiredSlaveID_List does NOT match DetectedSlaveID_List Exiting program.")
                    return 0
            ##########################################################################################################

            ##########################################################################################################
            if len(self.DetectedSlaveID_List) == 0:
                print("InitializeMotors, error: no slaves found. Exiting program.")
                return 0
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("InitializeMotors, finding adapter and scanning slaves section, exceptions: %s" % exceptions)
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] = 0
            #traceback.print_exc()
            return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        SlaveID_Int_List = []
        for SlaveID_Int in self.DetectedSlaveID_List:
            SlaveID_Int_List.append(SlaveID_Int)

        #print("SlaveID_Int_List: " + str(SlaveID_Int_List))
        self.SlaveID_Int_Min = min(SlaveID_Int_List)
        print("IngeniaBLDC_ReubenPython3Class InitializeMotors: self.SlaveID_Int_Min = " + str(self.SlaveID_Int_Min))

        self.IngeniaMotionController_MainDict[self.SlaveID_Int_Min]["AliasOrServoName_String"] = "default" #This is a requirement of the "ingeniamotion" module. Can use any alias after "default" has been set for one controller.
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            for SlaveID_Int in self.DetectedSlaveID_List:

                ##########################################################################################################
                ##########################################################################################################
                self.IngeniaMotionControllerObject.communication.connect_servo_ethercat(InterfaceSelected,
                                                                                        SlaveID_Int,
                                                                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["XDFfileDictionaryPath"],
                                                                                        alias=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                print("InitializeMotors: SlaveID_Int = " + str(SlaveID_Int) + " connected!")
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] = 1
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.__ResetFaults(SlaveID_Int, PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.__SetCommutationMode(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_ToBeSet_EnglishName"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.__SetOperationMode(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.IngeniaMotionController_MainDict[SlaveID_Int]["SerialNumber_Actual"] = self.IngeniaMotionControllerObject.configuration.get_serial_number()
                self.IngeniaMotionController_MainDict[SlaveID_Int]["VendorID_Actual"] = self.IngeniaMotionControllerObject.configuration.get_vendor_id()
                self.IngeniaMotionController_MainDict[SlaveID_Int]["ProductCode_Actual"] = self.IngeniaMotionControllerObject.configuration.get_product_code()
                self.IngeniaMotionController_MainDict[SlaveID_Int]["FWversion_Actual"] = self.IngeniaMotionControllerObject.configuration.get_fw_version()

                print("For SlaveID_Int = " + str(SlaveID_Int) + ", SerialNumber_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["SerialNumber_Actual"]))
                print("For SlaveID_Int = " + str(SlaveID_Int) + ", VendorID_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["VendorID_Actual"]))
                print("For SlaveID_Int = " + str(SlaveID_Int) + ", ProductCode_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["ProductCode_Actual"]))
                print("For SlaveID_Int = " + str(SlaveID_Int) + ", FWversion_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["FWversion_Actual"]))
                ##########################################################################################################
                ##########################################################################################################

                ########################################################################################################## THESE SET'S HAVE TO TAKE PLACE AFTER THE MOTOR IS CONNECTED
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"] != -11111.0 and self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"] != 1:
                    self.__SetEncoderTicksPerRevolution(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ########################################################################################################## THESE SET'S HAVE TO TAKE PLACE AFTER THE MOTOR IS CONNECTED
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_ToBeSet"] != -1:
                    self.__SetDynamicBrakingEnabledState(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"] != -11111.0:
                    self.__SetMaxCurrentHardLimit(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################
                
                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_ToBeSet"] != -11111.0:
                    self.__SetMaxContinuousCurrent(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_ToBeSet"] != -11111.0 and self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTimeMilliseconds_ToBeSet"] != -11111.0 and self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_ToBeSet"] != -11111:

                    Value = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_ToBeSet"]
                    Time = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTimeMilliseconds_ToBeSet"]
                    FaultModeInt = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_ToBeSet"]

                    self.__SetPeakCurrentValueTimeAndFaultParameters(SlaveID_Int, Value, Time, FaultModeInt, FaultReactionTimeoutMilliseconds_ToBeSet=1, PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_ToBeSet"] != -11111.0 and self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_ToBeSet"] != -11111.0 and self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_ToBeSet"] != -11111:

                    Window = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_ToBeSet"]
                    Timeout = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_ToBeSet"]
                    FaultModeInt = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_ToBeSet"]

                    self.__SetPositionFollowingErrorWindowTimeoutAndFaultParameters(SlaveID_Int, Window, Timeout, FaultModeInt, PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["ZeroEncoder_FireEventOnStartupFlag"] == 1:
                    self.__SetEncoderOffset(SlaveID_Int, 0.0, PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ########################################################################################################## We ensured that this value will always be valid.
                ##########################################################################################################
                self.__SetPositionMinAndMaxInEncoderTicks(SlaveID_Int,
                                                          self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"]["EncoderTicks"],
                                                          self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"]["EncoderTicks"],
                                                          PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_ToBeSet"] != -11111.0:
                    self.__SetMaxProfileVelocity(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_ToBeSet"] != -11111.0:
                    self.__SetMaxVelocity(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_ToBeSet"] != -11111.0:
                    self.__SetMaxProfileAcceleration(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_ToBeSet"], PrintDebugFlag=1)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":

                    ##########################################################################################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"] != -11111.0 and\
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"] != -11111.0 and\
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"] != -11111.0:
                            self.__SetPositionPIDgains(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"],
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"],
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"],
                                                       PrintDebugFlag=1)
                    ##########################################################################################################

                    ########################################################################################################## Need to set target to zero
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["ZeroEncoder_FireEventOnStartupFlag"] == 1:
                        self.SetPosition_ExternalProgram(SlaveID_Int, 0.0)
                        self.__SetPosition(SlaveID_Int, 0.0)
                        #self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_NeedsToBeSetFlag"] = 1 #Not needed when using TPDO
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if 1:#self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":

                    ##########################################################################################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_ToBeSet"] != -11111.0 and\
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_ToBeSet"] != -11111.0:
                            self.__SetCurrentDirectPIgains(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_ToBeSet"],
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_ToBeSet"],
                                                       PrintDebugFlag=1)
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"] != -11111.0 and\
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"] != -11111.0:
                            self.__SetCurrentQuadraturePIgains(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"],
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"],
                                                       PrintDebugFlag=1)
                    ##########################################################################################################
                    
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                    pass
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                #'''
                self.__SetEnabledState(SlaveID_Int, 0, PrintDebugFlag=1) #Disable by default
                #self.TimerCallbackFunctionWithFunctionAsArgument_SingleShot_NoParenthesesAfterFunctionName(CallbackAfterDeltaTseconds=10.0,
                #                                                                                           FunctionToCall_NoParenthesesAfterFunctionName=self.SetEnabledState_ExternalProgram,
                #                                                                                           ArgumentListToFunction=[SlaveID_Int, self.EnableMotorAtStartOfProgramFlag])
                #'''

                ''' #Not sure why we get unexpected motion if we call this from InitializeMotors immediately. The temporary fix is to put this callback on a timer.
                self.SetEnabledState_ExternalProgram(SlaveID_Int, self.EnableMotorAtStartOfProgramFlag) #unicorn
                self.__SetEnabledState(SlaveID_Int,
                                       self.EnableMotorAtStartOfProgramFlag,
                                       PrintDebugFlag=1)
                self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_NeedsToBeSetFlag"] = 0  #Have to issue this here because it takes a while to enter the main loop and look at the flags.
                '''

                ##########################################################################################################
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            return 1
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("InitializeMotors, connecting to slaves and sending initial settings section, SlaveID_Int = " + str(SlaveID_Int) + ", exceptions: %s" % exceptions)
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] = 0
            traceback.print_exc()
            return 0
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertPositionToAllUnits(self, SlaveID_Int, InputValue, InputUnits, VelocityInsteadOfPositionFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            InputValue = float(InputValue)
            InputUnits = str(InputUnits)

            ConvertedValue_EncoderTicks = -11111.0
            ConvertedValue_Deg = -11111.0
            ConvertedValue_Rad = -11111.0
            ConvertedValue_Rev = -11111.0
            ##########################################################################################################

            ##########################################################################################################
            if VelocityInsteadOfPositionFlag == 0:
                ConvertedValuesDict =  dict([("EncoderTicks", ConvertedValue_EncoderTicks),
                                            ("Deg", ConvertedValue_Deg),
                                            ("Rad", ConvertedValue_Rad),
                                            ("Rev", ConvertedValue_Rev)])
            else:
                ConvertedValuesDict =  dict([("EncoderTicksPerSec", ConvertedValue_EncoderTicks),
                                            ("DegPerSec", ConvertedValue_Deg),
                                            ("RadPerSec", ConvertedValue_Rad),
                                            ("RevPerSec", ConvertedValue_Rev)])
            ##########################################################################################################

            ##########################################################################################################
            if "EncoderTicksPerRevolution_ToBeSet" not in self.IngeniaMotionController_MainDict[SlaveID_Int]: #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.
                return ConvertedValuesDict
            ##########################################################################################################

            ##########################################################################################################
            if InputUnits.upper() == "ENCODERTICKS":
                ConvertedValue_EncoderTicks = InputValue*(1.0)
            ##########################################################################################################

            ##########################################################################################################
            elif InputUnits.upper() == "DEG":
                ConvertedValue_EncoderTicks = InputValue*(self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"]/360.0) #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.
            ##########################################################################################################

            ##########################################################################################################
            elif InputUnits.upper() == "RAD":
                ConvertedValue_EncoderTicks = InputValue*(self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"]/(2*math.pi)) #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.
            ##########################################################################################################

            ##########################################################################################################
            elif InputUnits.upper() == "REV":
                ConvertedValue_EncoderTicks = InputValue*(self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"]/1.0) #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.
            ##########################################################################################################

            ##########################################################################################################
            else:
                print("ConvertPositionToAllUnits: InputUnits not recognized. Input value: " + str(InputValue) + ", InputUnits: " + str(InputUnits))
                return ConvertedValuesDict
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            if InputUnits in self.Position_AcceptableUnitsList:
                ConvertedValue_EncoderTicks = ConvertedValue_EncoderTicks/1.0
                ConvertedValue_Deg = ConvertedValue_EncoderTicks/(self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"]/360.0) #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.
                ConvertedValue_Rad = ConvertedValue_EncoderTicks/(self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"]/(2*math.pi)) #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.
                ConvertedValue_Rev = ConvertedValue_EncoderTicks/(self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"]/1.0) #Don't use EncoderTicksPerRevolution_Actual as some times we don't want to read it.

            else:
                print("ConvertPositionToAllUnits: InputUnits not recognized. Input value: " + str(InputValue) + ", InputUnits: " + str(InputUnits))
                return ConvertedValuesDict
            ##########################################################################################################

            ##########################################################################################################
            if VelocityInsteadOfPositionFlag == 0:
                ConvertedValuesDict = dict([("EncoderTicks", round(ConvertedValue_EncoderTicks)),
                                            ("Deg", ConvertedValue_Deg),
                                            ("Rad", ConvertedValue_Rad),
                                            ("Rev", ConvertedValue_Rev)])
            else:
                ConvertedValuesDict = dict([("EncoderTicksPerSec", round(ConvertedValue_EncoderTicks)),
                                            ("DegPerSec", ConvertedValue_Deg),
                                            ("RadPerSec", ConvertedValue_Rad),
                                            ("RevPerSec", ConvertedValue_Rev)])
            ##########################################################################################################'

            ##########################################################################################################
            return ConvertedValuesDict
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("ConvertPositionToAllUnits InputValue: " + str(InputValue) + ", InputUnits: " + str(InputUnits) + ", exceptions: %s" % exceptions)
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS AN SDO CALL
    ##########################################################################################################
    def __SetPosition(self, SlaveID_Int, PositionTarget_EncoderTicks, PrintDebugFlag = 0):
        try:

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"]  == 1:

                #MUST PASS IN AN INT FOR COMMAND
                self.IngeniaMotionControllerObject.motion.move_to_position(int(PositionTarget_EncoderTicks), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])  # , blocking=False, timeout=2.0

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__SetPosition event fired for SlaveID_Int = " + str(SlaveID_Int) + ", PositionTarget_EncoderTicks_Limited = " + str(PositionTarget_EncoderTicks_Limited))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPosition, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitValue_ConvertUnits_And_SetVariable___PositionToBeSet(self, SlaveID_Int, PositionTarget, Units="EncoderTicks", PrintDebugFlag = 0):
        try:

            PositionTarget_ConvertedToAllUnitsDict = self.ConvertPositionToAllUnits(SlaveID_Int, PositionTarget, Units, VelocityInsteadOfPositionFlag=0)
            PositionTarget_EncoderTicks = PositionTarget_ConvertedToAllUnitsDict["EncoderTicks"]

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"]["EncoderTicks"] == 0.0 and self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"]["EncoderTicks"] == 0:
                PositionTarget_EncoderTicks_Limited = PositionTarget_EncoderTicks  # We set min and max both to 0 to tell teh Ingenia controller to disable the position limits.

            else:
                PositionTarget_EncoderTicks_Limited = self.LimitNumber_FloatOutputOnly(self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"]["EncoderTicks"],
                                                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"]["EncoderTicks"],
                                                                                       PositionTarget_EncoderTicks)

            self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_EncoderTicks"] = PositionTarget_EncoderTicks_Limited
            #self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_NeedsToBeSetFlag"] = 1 #Not needed when using TPDO

            self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, PositionTarget_EncoderTicks_Limited, "EncoderTicks", VelocityInsteadOfPositionFlag=0)

            ##########################################################################################################
            if PrintDebugFlag == 1:
                print("LimitValue_ConvertUnits_And_SetVariable___PositionToBeSet event fired for SlaveID_Int = " + str(SlaveID_Int) + ", PositionTarget = " + str(PositionTarget))
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("LimitValue_ConvertUnits_And_SetVariable___PositionToBeSet, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPosition_ExternalProgram(self, SlaveID_Int, PositionTarget, Units="EncoderTicks", PrintDebugFlag = 0):
        try:

            self.LimitValue_ConvertUnits_And_SetVariable___PositionToBeSet(SlaveID_Int, PositionTarget, Units, PrintDebugFlag=PrintDebugFlag)

            #self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_NeedsToBeSetFlag"] = 1 #Not needed when using TPDO

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] = 1

            ##########################################################################################################
            if PrintDebugFlag == 1:
                print("SetPosition_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int) + ", PositionTarget = " + str(PositionTarget))
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("SetPosition_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetCurrentQuadrature(self, SlaveID_Int, CurrentQuadratureTarget, PrintDebugFlag = 0):
        try:

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                CurrentQuadratureTarget_Limited = self.LimitNumber_FloatOutputOnly(-1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"],
                                                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"],
                                                                                       CurrentQuadratureTarget)

                # MUST PASS IN A FLOAT FOR COMMAND
                self.IngeniaMotionControllerObject.motion.set_current_quadrature(float(CurrentQuadratureTarget_Limited), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__SetCurrentQuadrature event fired for SlaveID_Int = " + str(SlaveID_Int) + ", CurrentQuadratureTarget_Limited = " + str(CurrentQuadratureTarget_Limited))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetCurrentQuadrature, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetCurrent_Quadrature_ExternalProgram(self, SlaveID_Int, CurrentQuadratureTarget, PrintDebugFlag = 0):
        try:

            CurrentQuadratureTarget = float(CurrentQuadratureTarget)

            #CurrentQuadratureTarget_Limited = self.LimitNumber_FloatOutputOnly(-1.0 * self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"],
            #                                                                   self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"],
            #                                                                   CurrentQuadratureTarget)

            CurrentQuadratureTarget_Limited = CurrentQuadratureTarget

            self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_ToBeSet"] = CurrentQuadratureTarget_Limited
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_NeedsToBeSetFlag"] = 1

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] = 1

            ##########################################################################################################
            if PrintDebugFlag == 1:
                print("SetCurrent_Quadrature_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int) + ", CurrentQuadratureTarget_Limited = " + str(CurrentQuadratureTarget_Limited))
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("SetCurrent_Quadrature_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ###########################################################################################################
    ##########################################################################################################
    def __SetVoltageQuadrature(self, SlaveID_Int, VoltageQuadratureTarget, PrintDebugFlag = 0):
        try:

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                #VoltageQuadratureTarget_Limited = self.LimitNumber_FloatOutputOnly(-1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVoltage_ToBeSet"], #WHAT SHOULD THESE VALUES BE?
                #                                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVoltage_ToBeSet"], #WHAT SHOULD THESE VALUES BE?
                #                                                                       VoltageQuadratureTarget)

                VoltageQuadratureTarget_Limited = VoltageQuadratureTarget

                # MUST PASS IN A FLOAT FOR COMMAND
                self.IngeniaMotionControllerObject.motion.set_voltage_quadrature(float(VoltageQuadratureTarget_Limited), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #0x2018 - Voltage quadrature set-point

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__SetVoltageQuadrature event fired for SlaveID_Int = " + str(SlaveID_Int) + ", VoltageQuadratureTarget_Limited = " + str(VoltageQuadratureTarget_Limited))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetVoltageQuadrature, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetVoltage_Quadrature_ExternalProgram(self, SlaveID_Int, VoltageQuadratureTarget, PrintDebugFlag = 0):
        try:

            VoltageQuadratureTarget = float(VoltageQuadratureTarget)

            #VoltageQuadratureTarget_Limited = self.LimitNumber_FloatOutputOnly(-1.0 * self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVoltage_ToBeSet"], #WHAT SHOULD THESE VALUES BE?
            #                                                                   self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVoltage_ToBeSet"],
            #                                                                   VoltageQuadratureTarget)

            VoltageQuadratureTarget_Limited = VoltageQuadratureTarget

            self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_ToBeSet"] = VoltageQuadratureTarget_Limited
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_NeedsToBeSetFlag"] = 1

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] = 1

            ##########################################################################################################
            if PrintDebugFlag == 1:
                print("SetVoltage_Quadrature_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int) + ", VoltageQuadratureTarget_Limited = " + str(VoltageQuadratureTarget_Limited))
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("SetVoltage_Quadrature_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetEnabledState(self, SlaveID_Int, EnabledState, PrintDebugFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                ##########################################################################################################
                if EnabledState in [0, 1]:
                    N = 1

                    ##########################################################################################################
                    if EnabledState == 0:
                        for Counter in range(0, N):
                            self.IngeniaMotionControllerObject.motion.motor_disable(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                            time.sleep(0.001)
                    ##########################################################################################################

                    ##########################################################################################################
                    if EnabledState == 1:
                        for Counter in range(0, N):
                            self.IngeniaMotionControllerObject.motion.motor_enable(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                            time.sleep(0.001)
                    ##########################################################################################################

                    ##########################################################################################################
                    #self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState"] = EnabledState
                    ##########################################################################################################

                    ##########################################################################################################
                    if PrintDebugFlag == 1:
                        print("__SetEnabledState event fired for SlaveID_Int = " + str(SlaveID_Int) + ", EnabledState = " + str(EnabledState))
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                else:
                    print("__SetEnabledState: Error, EnabledState must be 0 or 1 for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################
                ##########################################################################################################

            else:
                print("__SetEnabledState error: MotorConnectedFlag != 0 for SlaveID_Int = " + str(SlaveID_Int))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("__SetEnabledState, exceptions: %s" % exceptions)
            #traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEnabledState_ExternalProgram(self, SlaveID_Int, EnabledStateTarget, PrintDebugFlag = 0):
        try:

            EnabledStateTarget = int(EnabledStateTarget)
            if EnabledStateTarget not in [0, 1]:
                print("SetEnabledState_ExternalProgram error for SlaveID_Int = " + str(SlaveID_Int) + ", EnabledStateTarget must be in [0, 1].")
                return

            self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_ToBeSet"] = EnabledStateTarget
            self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetEnabledState_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int) + ", EnabledStateTarget = " + str(EnabledStateTarget))

        except:
            exceptions = sys.exc_info()[0]
            print("SetEnabledState_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ResetFaults_ExternalProgram(self, SlaveID_Int, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["ResetFaults_EventNeedsToBeFiredFlag"] = 1

            if PrintDebugFlag == 1:
                print("ResetFaults_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("ResetFaults_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __ResetFaults(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:
                self.IngeniaMotionControllerObject.motion.fault_reset()

                if PrintDebugFlag == 1:
                    print("__ResetFaults event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__ResetFaults, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetDynamicBrakingEnabledState(self, SlaveID_Int, PrintDebugFlag = 0):

        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("PS_DISABLE_OPTION", #"0x262E"
                                                                                                                                                               servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__GetDynamicBrakingEnabledState event fired for SlaveID_Int = " + str(SlaveID_Int) + ", DynamicBrakingEnabledState_Actual: "  + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_Actual"]))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__GetDynamicBrakingEnabledState, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def __SetDynamicBrakingEnabledState(self, SlaveID_Int, DynamicBrakingEnabledState, PrintDebugFlag = 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                ##########################################################################################################
                if DynamicBrakingEnabledState in [0, 1]:
                    N = 1

                    ##########################################################################################################
                    for Counter in range(0, N):
                        self.IngeniaMotionControllerObject.communication.set_register("PS_DISABLE_OPTION", DynamicBrakingEnabledState, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x262E"
                        time.sleep(0.001)
                    ##########################################################################################################

                    ##########################################################################################################
                    self.__GetDynamicBrakingEnabledState(SlaveID_Int, PrintDebugFlag)
                    ##########################################################################################################

                    ##########################################################################################################
                    if PrintDebugFlag == 1:
                        print("__SetDynamicBrakingEnabledState event fired for SlaveID_Int = " + str(SlaveID_Int) + ", DynamicBrakingEnabledState = " + str(DynamicBrakingEnabledState))
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                else:
                    print("__SetDynamicBrakingEnabledState: Error, DynamicBrakingEnabledState must be 0 or 1 for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################
                ##########################################################################################################

            else:
                print("__SetDynamicBrakingEnabledState error: MotorConnectedFlag != 0 for SlaveID_Int = " + str(SlaveID_Int))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("__SetDynamicBrakingEnabledState, exceptions: %s" % exceptions)
            #traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetDynamicBrakingEnabledState_ExternalProgram(self, SlaveID_Int, DynamicBrakingEnabledStateTarget, PrintDebugFlag = 0):
        try:

            DynamicBrakingEnabledStateTarget = int(DynamicBrakingEnabledStateTarget)
            if DynamicBrakingEnabledStateTarget not in [0, 1]:
                print("SetDynamicBrakingEnabledState_ExternalProgram error for SlaveID_Int = " + str(SlaveID_Int) + ", DynamicBrakingEnabledStateTarget must be in [0, 1].")
                return

            self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_ToBeSet"] = DynamicBrakingEnabledStateTarget
            self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetDynamicBrakingEnabledState_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int) + ", DynamicBrakingEnabledStateTarget = " + str(DynamicBrakingEnabledStateTarget))

        except:
            exceptions = sys.exc_info()[0]
            print("SetDynamicBrakingEnabledState_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetHallEffectValue(self, SlaveID_Int, PrintDebugFlag = 0):

        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["HallEffectValue_Actual_Int"] = self.IngeniaMotionControllerObject.communication.get_register("FBK_DIGHALL_VALUE", #Contains digital input values of digital hall sensors A, B and C, where A is the least significant bit.
                                                                                                                                                               servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__GetHallEffectValue event fired for SlaveID_Int = " + str(SlaveID_Int) + ", HallEffectValue_Actual_Int: "  + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["HallEffectValue_Actual_Int"]))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__GetHallEffectValue, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetOperationMode(self, SlaveID_Int, OperationMode_ToBeSet, PrintDebugFlag = 0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if OperationMode_ToBeSet not in self.OperationMode_ListOfAcceptableValuesStrings:
                    print("__SetOperationMode, error: " + OperationMode_ToBeSet + " is not in self.OperationMode_ListOfAcceptableValuesStrings = " + str(self.OperationMode_ListOfAcceptableValuesStrings))
                    return
                ##########################################################################################################

                ##########################################################################################################
                if OperationMode_ToBeSet == "CyclicPosition":
                    self.IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_POSITION, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                elif OperationMode_ToBeSet == "CyclicCurrent":
                    self.IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_CURRENT, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                elif OperationMode_ToBeSet == "CyclicVoltage":
                    self.IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.VOLTAGE, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                else:
                    pass
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__SetOperationMode event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

                ##########################################################################################################
                time.sleep(0.001)
                self.__GetOperationMode(SlaveID_Int, PrintDebugFlag)
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetOperationMode, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetOperationMode(self, SlaveID_Int, PrintDebugFlag = 0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_Int"] = self.IngeniaMotionControllerObject.communication.get_register("DRV_OP_VALUE", #Indicates the mode of operation applied in the drive VS DRV_OP_CMD, which is the User-requested mode of operation
                                                                                                                                                               servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_Int"] in self.OperationMode_DictIntNumberAsKey:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_EnglishName"] = self.OperationMode_DictIntNumberAsKey[self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_Int"]]
                else:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_EnglishName"] = "default"
                    print("__GetOperationMode, error: OperationMode_Actual_Int = " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_Int"]) + " not in OperationMode_DictIntNumberAsKey!")
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__GetOperationMode event fired for SlaveID_Int = " + str(SlaveID_Int) + ", OperationMode_Actual_EnglishName: "  + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_Int"]))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__GetOperationMode, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetCommutationMode(self, SlaveID_Int, CommutationMode_ToBeSet_EnglishName, PrintDebugFlag = 0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if CommutationMode_ToBeSet_EnglishName not in self.CommutationMode_DictEnglishNameAsKey:
                    print("__SetCommutationMode, error: " + CommutationMode_ToBeSet_EnglishName + " is not in self.CommutationMode_DictEnglishNameAsKey = " + str(self.CommutationMode_DictEnglishNameAsKey))
                    return
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionControllerObject.communication.set_register("MOT_COMMU_MOD", self.CommutationMode_DictEnglishNameAsKey[CommutationMode_ToBeSet_EnglishName], servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__SetCommutationMode event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

                ##########################################################################################################
                time.sleep(0.001)
                self.__GetCommutationMode(SlaveID_Int, PrintDebugFlag)
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetCommutationMode, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetCommutationMode(self, SlaveID_Int, PrintDebugFlag = 0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_Int"] = self.IngeniaMotionControllerObject.communication.get_register("MOT_COMMU_MOD",
                                                                                                                                                               servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_Int"] in self.CommutationMode_DictIntNumberAsKey:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_EnglishName"] = self.CommutationMode_DictIntNumberAsKey[self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_Int"]]
                else:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_EnglishName"] = "default"
                    print("__GetCommutationMode, error: CommutationMode_Actual_Int = " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_Int"]) + " not in CommutationMode_DictIntNumberAsKey!")
                ##########################################################################################################

                ##########################################################################################################
                if PrintDebugFlag == 1:
                    print("__GetCommutationMode event fired for SlaveID_Int = " + str(SlaveID_Int) + ", CommutationMode_Actual_EnglishName: "  + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_Int"]))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__GetCommutationMode, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetPositionPIDgains(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KP", Kp_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KI", Ki_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KD", Kd_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    PIDcontrollerMaxOutputUmax_ToBeSet = 100000
                    PIDcontrollerMinOutputUmin_ToBeSet = -1.0*PIDcontrollerMaxOutputUmax_ToBeSet

                    ###
                    #self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KD_FILTER", KdFilter_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_MAX_OUT", PIDcontrollerMaxOutputUmax_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_MIN_OUT", PIDcontrollerMinOutputUmin_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    ###

                    ### Not sure why these registers (which are supposed to be in CL Torque mode) are limiting in position control, but they are.

                    '''
                    <Register access="rw" address_type="NVM" address="0x0527"  dtype="float" id="CL_TOR_PID_MAX_OUT" units="A" subnode="1" cyclic="CYCLIC_RX" desc="Maximum output of the torque PID controller" cat_id="CONTROL">
                    <Register access="rw" address_type="NVM" address="0x0528"  dtype="float" id="CL_TOR_PID_MIN_OUT" units="A" subnode="1" cyclic="CYCLIC_RX" desc="Minimum output of the torque PID controller" cat_id="CONTROL">
                    '''

                    self.IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_MAX_OUT", 10.0, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_MIN_OUT", -10.0, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    #self.IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_MAX_OUT", self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"], servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    #self.IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_MIN_OUT", -1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"], servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    ###

                    time.sleep(0.001)

                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetPositionPIDgains for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetPositionPIDgains(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_Actual"]
                #############################################

                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedFromExternalSourceFlag"] = 1

                if PrintDebugFlag == 1:
                    print("__SetPositionPIDgains event fired for SlaveID_Int = " + str(SlaveID_Int) +
                          ", Kp = " + str(Kp_ToBeSet) +
                          ", Ki = " + str(Ki_ToBeSet) +
                          ", Kd = " + str(Kd_ToBeSet))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPositionPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPositionPIDgains_ExternalProgram(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"] = Kp_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"] = Ki_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"] = Kd_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetPositionPIDgains_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetPositionPIDgains_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetPositionPIDgains(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KP", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KI", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KD", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_KdFilter_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KD_FILTER", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_PIDcontrollerMaxOutputUmax_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_MAX_OUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_PIDcontrollerMinOutputUmin_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_MIN_OUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetPositionPIDgains event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetPositionPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def __SetVelocityPIDgains(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_VEL_KP", Kp_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_VEL_KI", Ki_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_VEL_KD", Kd_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetVelocityPIDgains for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetVelocityPIDgains(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kp_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kp_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Ki_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Ki_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kd_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kd_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetVelocityPIDgains event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetVelocityPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    
    ###########################################################################################################
    ##########################################################################################################
    def SetVelocityPIDgains_ExternalProgram(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kp_ToBeSet"]= Kp_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Ki_ToBeSet"] = Ki_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kd_ToBeSet"] = Kd_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetVelocityPIDgains_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetVelocityPIDgains_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetVelocityPIDgains(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kp_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_PID_KP", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Ki_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_PID_KI", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kd_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_PID_KD", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetVelocityPIDgains event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetVelocityPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetEncoderTicksPerRevolution(self, SlaveID_Int, EncoderTicksPerRevolution_ToBeSet, PrintDebugFlag=0):
        try:

            '''
            <Register access="rw" dtype="u32" id="FBK_DIGENC1_RESOLUTION" storage="8192" subnode="1"/>
            '''

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:
                    self.IngeniaMotionControllerObject.communication.set_register("FBK_DIGENC1_RESOLUTION", int(EncoderTicksPerRevolution_ToBeSet), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetEncoderTicksPerRevolution for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetEncoderTicksPerRevolution(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetEncoderTicksPerRevolution event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetEncoderTicksPerRevolution, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEncoderTicksPerRevolution_ExternalProgram(self, SlaveID_Int, EncoderTicksPerRevolution_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_ToBeSet"] = EncoderTicksPerRevolution_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetEncoderTicksPerRevolution_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetEncoderTicksPerRevolution_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetEncoderTicksPerRevolution(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("FBK_DIGENC1_RESOLUTION", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetEncoderTicksPerRevolution event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetEncoderTicksPerRevolution, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetCurrentDirectPIgains(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, PrintDebugFlag = 0):

        '''

        '''

        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                CL_CUR_D_MAX_OUT = self.IngeniaMotionController_MainDict[SlaveID_Int]["BusVoltage"]
                CL_CUR_D_MIN_OUT = -1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["BusVoltage"]

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_KP", Kp_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_KI", Ki_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_MAX_OUT", CL_CUR_D_MAX_OUT, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_MIN_OUT", CL_CUR_D_MIN_OUT, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) 

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetCurrentDirectPIgains for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetCurrentDirectPIgains(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_Actual"]
                #############################################

                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedFromExternalSourceFlag"] = 1

                if PrintDebugFlag == 1:
                    print("__SetCurrentDirectPIgains event fired for SlaveID_Int = " + str(SlaveID_Int) +
                          ", Kp = " + str(Kp_ToBeSet) +
                          ", Ki = " + str(Ki_ToBeSet) +
                          ", CL_CUR_D_MAX_OUT = " + str(CL_CUR_D_MAX_OUT) +
                          ", CL_CUR_D_MIN_OUT = " + str(CL_CUR_D_MIN_OUT))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetCurrentDirectPIgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetCurrentDirectPIgains_ExternalProgram(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_ToBeSet"] = Kp_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_ToBeSet"] = Ki_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetCurrentDirectPIgains_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetCurrentDirectPIgains_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetCurrentDirectPIgains(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_D_KP", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_D_KI", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirect_CL_CUR_D_MAX_OUT_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_D_MAX_OUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirect_CL_CUR_D_MIN_OUT_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_D_MIN_OUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetCurrentDirectPIgains event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetCurrentDirectPIgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetCurrentQuadraturePIgains(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, PrintDebugFlag = 0):

        '''
        https://drives.novantamotion.com/summit/0x2502-current-quadrature-loop-max-out
        <Register access="rw" address_type="NVM" address="0x0502"  dtype="float" id="CL_CUR_Q_MAX_OUT" units="V" subnode="1" cyclic="CONFIG" desc="Maximum output of the quadrature current PI controller." cat_id="CONTROL">
        This parameter allows configuring the Umax of the PI controller used for current Q regulation.

        https://drives.novantamotion.com/summit/0x2503-current-quadrature-loop-min-out
        <Register access="rw" address_type="NVM" address="0x0503"  dtype="float" id="CL_CUR_Q_MIN_OUT" units="V" subnode="1" cyclic="CONFIG" desc="Minimum output of the quadrature current PI controller." cat_id="CONTROL">
        This parameter allows configuring the Umin of the PI controller used for current Q regulation.
        '''

        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                CL_CUR_Q_MAX_OUT = self.IngeniaMotionController_MainDict[SlaveID_Int]["BusVoltage"]
                CL_CUR_Q_MIN_OUT = -1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["BusVoltage"]

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_KP", Kp_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_KI", Ki_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_MAX_OUT", CL_CUR_Q_MAX_OUT, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) 
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_MIN_OUT", CL_CUR_Q_MIN_OUT, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) 

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetCurrentQuadraturePIgains for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetCurrentQuadraturePIgains(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_Actual"]
                #############################################

                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedFromExternalSourceFlag"] = 1

                if PrintDebugFlag == 1:
                    print("__SetCurrentQuadraturePIgains event fired for SlaveID_Int = " + str(SlaveID_Int) +
                          ", Kp = " + str(Kp_ToBeSet) +
                          ", Ki = " + str(Ki_ToBeSet) +
                          ", CL_CUR_Q_MAX_OUT = " + str(CL_CUR_Q_MAX_OUT) +
                          ", CL_CUR_Q_MIN_OUT = " + str(CL_CUR_Q_MIN_OUT))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetCurrentQuadraturePIgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetCurrentQuadraturePIgains_ExternalProgram(self, SlaveID_Int, Kp_ToBeSet, Ki_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"] = Kp_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"] = Ki_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetCurrentQuadraturePIgains_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetCurrentQuadraturePIgains_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetCurrentQuadraturePIgains(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_Q_KP", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_Q_KI", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadrature_CL_CUR_Q_MAX_OUT_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_Q_MAX_OUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadrature_CL_CUR_Q_MIN_OUT_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_CUR_Q_MIN_OUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])


                if PrintDebugFlag == 1:
                    print("__GetCurrentQuadraturePIgains event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetCurrentQuadraturePIgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetMaxCurrentHardLimit(self, SlaveID_Int, MaxCurrentHardLimit_ToBeSet, PrintDebugFlag=0):
        try:

            '''
            <Register access="rw" address_type="NVM" address="0x01E0"  dtype="float" id="CL_CUR_REF_MAX" units="A" subnode="1" cyclic="CYCLIC_RX" desc="User allowed maximum current" cat_id="LIMITS">
            '''

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:
                    self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_REF_MAX", MaxCurrentHardLimit_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetMaxCurrentHardLimit for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetMaxCurrentHardLimit(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetMaxCurrentHardLimit event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetMaxCurrentHardLimit, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetMaxCurrentHardLimit_ExternalProgram(self, SlaveID_Int, MaxCurrentHardLimit_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"] = MaxCurrentHardLimit_ToBeSet
            
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetMaxCurrentHardLimit_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetMaxCurrentHardLimit_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetMaxCurrentHardLimit(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_Actual"] = self.IngeniaMotionControllerObject.configuration.get_max_current(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetMaxCurrentHardLimit event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetMaxCurrentHardLimit, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetMaxContinuousCurrent(self, SlaveID_Int, MaxContinuousCurrent_ToBeSet, PrintDebugFlag=0):
        try:

            '''
            <Register access="rw" address_type="NVM" address="0x0100"  dtype="float" id="MOT_RATED_CURRENT" units="A" subnode="1" cyclic="CYCLIC_RX" desc="Indicates the continuous current of the actuator / system" cat_id="PROTECTIONS">
            '''

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:
                    self.IngeniaMotionControllerObject.communication.set_register("MOT_RATED_CURRENT", MaxContinuousCurrent_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetMaxContinuousCurrent for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetMaxContinuousCurrent(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetMaxContinuousCurrent event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetMaxContinuousCurrent, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetMaxContinuousCurrent_ExternalProgram(self, SlaveID_Int, MaxContinuousCurrent_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_ToBeSet"] = MaxContinuousCurrent_ToBeSet
            
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetMaxContinuousCurrent_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetMaxContinuousCurrent_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetMaxContinuousCurrent(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("MOT_RATED_CURRENT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetMaxContinuousCurrent event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetMaxContinuousCurrent, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetPeakCurrentValueTimeAndFaultParameters(self, SlaveID_Int, PeakCurrentValue_ToBeSet, PeakCurrentTimeMilliseconds_ToBeSet, PeakCurrentFaultModeInt_ToBeSet, FaultReactionTimeoutMilliseconds_ToBeSet=1, PrintDebugFlag=0):

        '''
        ###
        https://drives.novantamotion.com/summit/0x2101-peak-current

        <Register access="rw" address_type="NVM" address="0x0101"  dtype="float" id="DRV_PROT_I2T_PEAK_VALUE" units="A" subnode="1" cyclic="CONFIG" desc="User peak current" cat_id="PROTECTIONS">

        This register defines the maximum allowed instant current during the defined peak current time.
        These registers allows to configure the I2T parameters to protect the drive and/or motor in front of exceeding their thermal limit. It is a complementary protection that works together with temperature limits and current derating.

        This protection is always active. For modes of operation where current loop is not enabled, instead of limiting the current a fault is generated.

        There is a maximum configurable I2T. If a user sets an I2T less restrictive than the allowed, the drive overwrites the user configuration with its own. The applied nominal current is the smaller between both configurations.

        If maximum configurable I2T is detected before the user I2T levels, a fault is generated independently if the current loop is enabled or not.
        ###

        ###
        https://drives.novantamotion.com/summit/0x2102-peak-current-time

        <Register access="rw" address_type="NVM" address="0x0102"  dtype="u32" id="DRV_PROT_I2T_PEAK_TIME" units="ms" subnode="1" cyclic="CONFIG" desc="User allowed peak current time" cat_id="PROTECTIONS">

        This register defines the maximum time the drive is able to source the peak current.

        This register allows to configure the I2T parameters to protect the drive and/or motor in front of exceeding their thermal limit. It is a complementary protection that works together with temperature limits and current derating.

        The main functionality of the I2T is to detect an instantaneous exceed of thermal energy on the drive. It covers the case where the temperature sensors are too slow to detect a dangerous situation.

        This protection is always active. For modes of operation where current loop is not enabled, instead of limiting the current a fault is generated.

        There is a maximum configurable I2T. If a user sets an I2T less restrictive than the allowed, the drive overwrites the user configuration with its own. The applied nominal current is the smaller between both configurations.

        If maximum configurable I2T is detected before the user I2T levels, a fault is generated independently if the current loop is enabled or not.
        ###

        ###
        https://drives.novantamotion.com/summit/0x260f-user-i2t-error-option-code

        <Register access="rw" address_type="NVM" address="0x060F"  dtype="u16" id="ERROR_PROT_I2T_OPTION" units="-" subnode="1" cyclic="CONFIG" desc="Reaction option code for the &quot;I2T without current control&quot; error" cat_id="PROTECTIONS">

        This register set the drive fault reaction for an I2T detection without active current control.
        The value of this register determines the reaction of the drive when a fault is triggered:

        0	Fault	Disable power stage
        1	Warning	Do nothing
        2	Fault	Slow down ramp
        3	Fault	Quick stop ramp

        Further information in Error management.
        When using slow down ramp or quick stop ramp option codes, it is important to have the velocity loop operative and properly configured.
        In the option codes that also disable the power stage after detecting that the motor has stopped, velocity threshold and velocity threshold time have to be also configured.
        ###

        ###
        https://drives.novantamotion.com/summit/0x262b-fault-reaction-timeout

        <Register access="rw" address_type="NVM" address="0x062B"  dtype="u32" id="FAULT_REACTION_TIMEOUT" units="ms" subnode="1" cyclic="CONFIG" desc="Timeout in milliseconds after which fault reaction state will be exited into fault state." cat_id="PROTECTIONS">

        This register configures a timeout after which fault reaction active state will have to exit into fault state.
        ###

        ###
        https://drives.novantamotion.com/summit/0x21d6-velocity-threshold
        <Register access="rw" address_type="NVM" address="0x01D6"  dtype="float" id="PROF_VEL_THRESHOLD" units="rev/s" subnode="1" cyclic="CYCLIC_RX" desc="Threshold (in absolute value) below which, the velocity is considered to be zero." cat_id="THRESHOLDS">
        This register sets the threshold (in absolute value) below which actual velocity can be considered to be zero
        In profile velocity mode, the speed bit in the status word register will be set whenever the actual velocity (in absolute value)
        stays below the Velocity threshold for longer than the amount of time defined in Velocity threshold time.

        https://drives.novantamotion.com/summit/0x21d7-velocity-threshold-time
        <Register access="rw" address_type="NVM" address="0x01D7"  dtype="u32" id="PROF_VEL_THRESHOLD_TIME" units="ms" subnode="1" cyclic="CYCLIC_RX" desc="Time that the velocity (in absolute value) has to remain below velocity threshold in order to detect zero velocity" cat_id="THRESHOLDS">
        This register sets the time that the Actual velocity (in absolute value) has to stay below the Velocity threshold to consider it zero speed

        In Profile velocity mode, the speed bit in the status word register will be set whenever the actual velocity (in absolute value)
        stays below the Velocity threshold for longer than the amount of time defined in Velocity threshold time.

        UNICORN IMPORTANT:
        From https://drives.novantamotion.com/summit/0x260f-user-i2t-error-option-code:
        When using slow down ramp or quick stop ramp option codes, it is important to have the velocity loop operative and properly configured.
        In the option codes that also disable the power stage after detecting that the motor has stopped, ***velocity threshold and velocity threshold time have to be also configured***.
        ###

        ###
        https://drives.novantamotion.com/summit/0x261b-over-current-without-current-control-error-
        <Register access="rw" address_type="NVM" address="0x061B"  dtype="u16" id="ERROR_PROT_OVER_CUR_OPTION" units="-" subnode="1" cyclic="CONFIG" desc="Reaction option code for the &quot;Over current without current control&quot; error" cat_id="PROTECTIONS">

        ###

        '''

        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    PeakCurrentTimeMilliseconds_ToBeSet = self.LimitNumber_IntOutputOnly(0.0, 1.0*60.0*60.0*1000.0, PeakCurrentTimeMilliseconds_ToBeSet) #1hr worth of milliseconds

                    FaultReactionTimeoutMilliseconds_ToBeSet = self.LimitNumber_IntOutputOnly(0.0, 1.0*60.0*60.0*1000.0, FaultReactionTimeoutMilliseconds_ToBeSet) #1hr worth of milliseconds

                    PeakCurrentFaultModeInt_ToBeSet = int(PeakCurrentFaultModeInt_ToBeSet)

                    if PeakCurrentFaultModeInt_ToBeSet not in [0, 1, 2, 3]:
                        PeakCurrentFaultModeInt_ToBeSet = 0

                    self.IngeniaMotionControllerObject.communication.set_register("DRV_PROT_I2T_PEAK_VALUE", PeakCurrentValue_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x0101"
                    self.IngeniaMotionControllerObject.communication.set_register("DRV_PROT_I2T_PEAK_TIME", PeakCurrentTimeMilliseconds_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x0102"
                    self.IngeniaMotionControllerObject.communication.set_register("ERROR_PROT_I2T_OPTION", PeakCurrentFaultModeInt_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x060F"
                    self.IngeniaMotionControllerObject.communication.set_register("ERROR_PROT_OVER_CUR_OPTION", 0, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])  #"0x061B"
                    self.IngeniaMotionControllerObject.communication.set_register("FAULT_REACTION_TIMEOUT", 1, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x062B"

                    ### I DON'T EVEN SEE THE "0x060F" REGISTER FROM XDF FILE

                    #https://drives.novantamotion.com/summit/0x260f-user-i2t-error-option-code
                    #https://drives.novantamotion.com/summit/0x261b-over-current-without-current-control-error-

                    self.IngeniaMotionControllerObject.communication.set_register("PROF_VEL_THRESHOLD", 1.0, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x01D6"
                    self.IngeniaMotionControllerObject.communication.set_register("PROF_VEL_THRESHOLD_TIME", 10, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #"0x01D7"


                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetPeakCurrentValueTimeAndFaultParameters for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetPeakCurrentValueTimeAndFaultParameters(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTimeMilliseconds_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTimeMilliseconds_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetPeakCurrentValueTimeAndFaultParameters event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPeakCurrentValueTimeAndFaultParameters, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPeakCurrentValueTimeAndFaultParameters_ExternalProgram(self, SlaveID_Int, PeakCurrentValue_ToBeSet, PeakCurrentTimeMilliseconds_ToBeSet, PeakCurrentFaultModeInt_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_ToBeSet"] = PeakCurrentValue_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTimeMilliseconds_ToBeSet"] = PeakCurrentTimeMilliseconds_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_ToBeSet"] = PeakCurrentFaultModeInt_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValueTimeAndFaultParameters_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetPeakCurrentValueTimeAndFaultParameters_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetPeakCurrentValueTimeAndFaultParameters_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetPeakCurrentValueTimeAndFaultParameters(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("DRV_PROT_I2T_PEAK_VALUE", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTime_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("DRV_PROT_I2T_PEAK_TIME", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("ERROR_PROT_I2T_OPTION", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetPeakCurrentValueTimeAndFaultParameters event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetPeakCurrentValueTimeAndFaultParameters, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetPositionFollowingErrorWindowTimeoutAndFaultParameters(self, SlaveID_Int, PositionFollowingErrorWindow_ToBeSet, PositionFollowingErrorTimeoutMilliseconds_ToBeSet, PositionFollowingErrorFaultModeInt_ToBeSet, PrintDebugFlag=0):

        '''
        ###
        https://drives.novantamotion.com/summit/0x21ec-position-following-error-window
        <Register access="rw" address_type="NVM" address="0x01EC"  dtype="float" id="CL_POS_ERROR_WINDOW" units="cnt" subnode="1" cyclic="CYCLIC_RX" desc="Indicates the maximum allowed difference between demand and actual position before generating a fault." cat_id="THRESHOLDS">
        This object indicates the configured range of tolerated position values symmetrically to the position demand value.
        If the position actual value is out of the position following error window for a position following error timeout time, a position following error occurs.
        When the error condition is detected, the Following error bit (bit number 13) of the status word will be set. A following error may occur when a drive is blocked, when an unreachable profile velocity occurs, or when using wrong closed-loop coefficients.

        https://drives.novantamotion.com/summit/0x21ed-position-following-error-timeout
        <Register access="rw" address_type="NVM" address="0x01ED"  dtype="u32" id="CL_POS_ERROR_TIMEOUT" units="ms" subnode="1" cyclic="CYCLIC_RX" desc="Indicates the maximum time in which the difference between demand and actual position is allowed to be outside the position window." cat_id="THRESHOLDS">
        This object indicates the minimum time that actual position must be out of position following error window in order to generate an error.
        When the error condition is detected, the Following error bit (bit number 13) of the statusword will be set.

        https://drives.novantamotion.com/summit/0x21ee-following-error
        <Register access="r" address_type="NVM_NONE" address="0x01EE"  dtype="float" id="CL_ERROR_FOLLOWING_1" units="-" subnode="1" cyclic="CYCLIC_TX" desc="Difference between demand and actual value of active operation mode variables." cat_id="REPORTING">
        This register contains the difference between demand and actual value of active operation mode variables.
        Note *Following error parameter contains the following error of the active operation mode. If a velocity mode is selected, the units will be rev/s, if a position mode is selected, it will represent counts.

        https://drives.novantamotion.com/summit/0x2612-position-following-error-option-code
        <Register access="rw" address_type="NVM" address="0x0612"  dtype="u16" id="ERROR_POS_FOLLOWING_OPTION" units="-" subnode="1" cyclic="CONFIG" desc="Reaction option code for the &quot;Position following error&quot; error" cat_id="PROTECTIONS">
        This register set the drive fault reaction for a position following error detection.
        The value of this register determines the reaction of the drive when a fault is triggered:

        0	Fault	Disable power stage
        1	Warning	Do nothing
        2	Fault	Slow down ramp
        3	Fault	Quick stop ramp

        Further information in Error management.

        When using slow down ramp or quick stop ramp option codes, it is important to have the velocity loop operative and properly configured.
        In the option codes that also disable the power stage after detecting that the motor has stopped, velocity threshold and velocity threshold time have to be also configured.
        ###
        '''

        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    PositionFollowingErrorWindow_ToBeSet = self.LimitNumber_IntOutputOnly(0.0, 1000000, PositionFollowingErrorWindow_ToBeSet)

                    PositionFollowingErrorTimeoutMilliseconds_ToBeSet = self.LimitNumber_IntOutputOnly(0.0, 1.0*60.0*60.0*1000.0, PositionFollowingErrorTimeoutMilliseconds_ToBeSet) #1hr worth of milliseconds

                    PositionFollowingErrorFaultModeInt_ToBeSet = int(PositionFollowingErrorFaultModeInt_ToBeSet)

                    if PositionFollowingErrorFaultModeInt_ToBeSet not in [0, 1, 2, 3]:
                        PositionFollowingErrorFaultModeInt_ToBeSet = 0

                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_ERROR_WINDOW", PositionFollowingErrorWindow_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("CL_POS_ERROR_TIMEOUT", PositionFollowingErrorTimeoutMilliseconds_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.communication.set_register("ERROR_POS_FOLLOWING_OPTION", PositionFollowingErrorFaultModeInt_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetPositionFollowingErrorWindowTimeoutAndFaultParameters for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetPositionFollowingErrorWindowTimeoutAndFaultParameters(SlaveID_Int, PrintDebugFlag=0)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_Actual"]
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetPositionFollowingErrorWindowTimeoutAndFaultParameters event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPositionFollowingErrorWindowTimeoutAndFaultParameters, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPositionFollowingErrorWindowTimeoutAndFaultParameters_ExternalProgram(self, SlaveID_Int, PositionFollowingErrorWindow_ToBeSet, PositionFollowingErrorTimeoutMilliseconds_ToBeSet, PositionFollowingErrorFaultModeInt_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_ToBeSet"] = PositionFollowingErrorWindow_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_ToBeSet"] = PositionFollowingErrorTimeoutMilliseconds_ToBeSet
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_ToBeSet"] = PositionFollowingErrorFaultModeInt_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindowTimeoutAndFaultParameters_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetPositionFollowingErrorWindowTimeoutAndFaultParameters_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetPositionFollowingErrorWindowTimeoutAndFaultParameters_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetPositionFollowingErrorWindowTimeoutAndFaultParameters(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_ERROR_WINDOW", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_ERROR_TIMEOUT", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("ERROR_POS_FOLLOWING_OPTION", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetPositionFollowingErrorWindowTimeoutAndFaultParameters event fired for SlaveID_Int = " + str(SlaveID_Int) + \
                        ", PositionFollowingErrorWindow_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_Actual"])+\
                        ", PositionFollowingErrorTimeoutMilliseconds_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_Actual"])+\
                        ", PositionFollowingErrorFaultModeInt_Actual: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_Actual"]))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetPositionFollowingErrorWindowTimeoutAndFaultParameters, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetMaxVelocity(self, SlaveID_Int, MaxVelocity_ToBeSet, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    self.IngeniaMotionControllerObject.communication.set_register("CL_VEL_REF_MAX", MaxVelocity_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #address="0x01E8"
                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetMaxVelocity for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetMaxVelocity(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetMaxVelocity event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetMaxVelocity, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetMaxVelocity_ExternalProgram(self, SlaveID_Int, MaxVelocity_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_ToBeSet"] = MaxVelocity_ToBeSet
            
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetMaxVelocity_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetMaxVelocity_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetMaxVelocity(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_REF_MAX", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #address="0x01E8" 

                if PrintDebugFlag == 1:
                    print("__GetMaxVelocity event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetMaxVelocity, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetMaxProfileVelocity(self, SlaveID_Int, MaxProfileVelocity_ToBeSet, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:
                    self.IngeniaMotionControllerObject.communication.set_register("PROF_MAX_VEL", MaxProfileVelocity_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetMaxProfileVelocity for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetMaxProfileVelocity(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetMaxProfileVelocity event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetMaxProfileVelocity, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetMaxProfileVelocity_ExternalProgram(self, SlaveID_Int, MaxProfileVelocity_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_ToBeSet"] = MaxProfileVelocity_ToBeSet
            
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetMaxProfileVelocity_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetMaxProfileVelocity_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetMaxProfileVelocity(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("PROF_MAX_VEL", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetMaxProfileVelocity event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetMaxProfileVelocity, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetMaxProfileAcceleration(self, SlaveID_Int, MaxProfileAcceleration_ToBeSet, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                    #self.IngeniaMotionControllerObject.configuration.set_max_acceleration(max_acceleration_deceleration, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #deprecated
                    self.IngeniaMotionControllerObject.configuration.set_max_profile_acceleration(MaxProfileAcceleration_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    self.IngeniaMotionControllerObject.configuration.set_max_profile_deceleration(MaxProfileAcceleration_ToBeSet, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    time.sleep(0.001)
                ##########################################################################################################

                ##########################################################################################################
                else:
                    if PrintDebugFlag == 1:
                        print("__SetMaxProfileAcceleration for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                ##########################################################################################################

                ##########################################################################################################
                self.__GetMaxProfileAcceleration(SlaveID_Int)

                #############################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_Actual"]
                #############################################

                if PrintDebugFlag == 1:
                    print("__SetMaxProfileAcceleration event fired for SlaveID_Int = " + str(SlaveID_Int))
                ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("__SetMaxProfileAcceleration, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetMaxProfileAcceleration_ExternalProgram(self, SlaveID_Int, MaxProfileAcceleration_ToBeSet, PrintDebugFlag = 0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_ToBeSet"] = MaxProfileAcceleration_ToBeSet
            
            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetMaxProfileAcceleration_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetMaxProfileAcceleration_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetMaxProfileAcceleration(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("PROF_MAX_ACC", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                #self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileDeceleration_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("PROF_MAX_DEC", servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetMaxProfileAcceleration event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetMaxProfileAcceleration, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEncoderOffset_ExternalProgram(self, SlaveID_Int, EncoderOffset_ToBeSet, PrintDebugFlag=0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_ToBeSet"] = EncoderOffset_ToBeSet

            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetEncoderOffset_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetEncoderOffset_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetEncoderOffset(self, SlaveID_Int, EncoderOffset_ToBeSet, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowEncoderToBeZeroedFlag"] == 1:

                    ##########################################################################################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:
                        self.IngeniaMotionControllerObject.configuration.homing_on_current_position(int(EncoderOffset_ToBeSet), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                        time.sleep(0.001)
                    ##########################################################################################################

                    ##########################################################################################################
                    else:
                        if PrintDebugFlag == 1:
                            print("__SetEncoderOffset for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                    ##########################################################################################################

                    ##########################################################################################################
                    #self.__GetEncoderOffset(SlaveID_Int)

                    #############################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                        pass
                        #self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_Actual"] #Currently, EncoderOffset_Actual doesn't exist
                    #############################################

                    if PrintDebugFlag == 1:
                        print("__SetEncoderOffset event fired for SlaveID_Int = " + str(SlaveID_Int))
                    ##########################################################################################################

                else:
                    print("__SetEncoderOffset event CANNOT be fired for SlaveID_Int = " + str(SlaveID_Int) + " because AllowEncoderToBeZeroedFlag = 0.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetEncoderOffset, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPositionMinAndMax_ExternalProgram(self, SlaveID_Int, PositionMin_ToBeSet, PositionMax_ToBeSet, Units, PrintDebugFlag=0):
        try:

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, PositionMin_ToBeSet, Units, VelocityInsteadOfPositionFlag=0)
            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, PositionMax_ToBeSet, Units, VelocityInsteadOfPositionFlag=0)

            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinAndMaxInEncoderTicks_NeedsToBeSetFlag"] = 1

            if PrintDebugFlag == 1:
                print("SetPositionMinAndMax_ExternalProgram event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("SetPositionMinAndMax_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetPositionMinAndMaxInEncoderTicks(self, SlaveID_Int, PositionMin_EncoderTicks, PositionMax_EncoderTicks, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                if PositionMin_EncoderTicks <= PositionMax_EncoderTicks:

                    ##########################################################################################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 1:

                        self.IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MIN_RANGE", -2147483648, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Signed 32-bit int. Minimum position value range. On reaching or exceeding this limit, the position set-point and position actual are wrapped automatically to the other end of the range.
                        self.IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MAX_RANGE", 2147483647, servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Signed 32-bit int. Maximum position value range. On reaching or exceeding this limit, the position set-point and position actual are wrapped automatically to the other end of the range.\

                        self.IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MIN", int(PositionMin_EncoderTicks), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #User minimum allowed position.
                        self.IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MAX", int(PositionMax_EncoderTicks), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #User maximum allowed position.

                        time.sleep(0.001)
                    ##########################################################################################################

                    ##########################################################################################################
                    else:
                        if PrintDebugFlag == 1:
                            print("__SetPositionMinAndMaxInEncoderTicks for SlaveID_Int = " + str(SlaveID_Int) + ", not allowed to write.")
                    ##########################################################################################################

                    ##########################################################################################################
                    self.__GetPositionMinAndMaxInEncoderTicks(SlaveID_Int)

                    #############################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"] == 0:
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinRange_EncoderTicks_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinRange_EncoderTicks_Actual"]
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMaxRange_EncoderTicks_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMaxRange_EncoderTicks_Actual"]
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_EncoderTicks_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_EncoderTicks_Actual"]
                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_EncoderTicks_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_EncoderTicks_Actual"]
                    #############################################

                    if PrintDebugFlag == 1:
                        print("__SetPositionMinAndMaxInEncoderTicks event fired for SlaveID_Int = " + str(SlaveID_Int))
                    ##########################################################################################################

                else:
                    print("__SetPositionMinAndMaxInEncoderTicks: Error, PositionMin_EncoderTicks must be <= PositionMax_EncoderTicks.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPositionMinAndMaxInEncoderTicks, exceptions: %s" % exceptions)
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetPositionMinAndMaxInEncoderTicks(self, SlaveID_Int, PrintDebugFlag=0):
        try:
            if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinRange_EncoderTicks_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MIN_RANGE",
                                                                                                                                                                      servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMaxRange_EncoderTicks_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MAX_RANGE",
                                                                                                                                                                      servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_EncoderTicks_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MIN",
                                                                                                                                                                      servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_EncoderTicks_Actual"] = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MAX",
                                                                                                                                                                      servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                if PrintDebugFlag == 1:
                    print("__GetPositionMinAndMaxInEncoderTicks event fired for SlaveID_Int = " + str(SlaveID_Int))

        except:
            exceptions = sys.exc_info()[0]
            print("__GetPositionMinAndMaxInEncoderTicks, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TPDOcallbackFunction_UpdateAllTPDOvariables_General(self, SlaveID_Int, ActualAllTPDOvariables_ListOfTPDOitems):
        #Callback to set new values to registers for each cycle.

        #print("TPDOcallbackFunction_UpdateAllTPDOvariables_General: SlaveID_Int = " + str(SlaveID_Int))

        try:
            for Index, Element in enumerate(ActualAllTPDOvariables_ListOfTPDOitems):

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"][Index] == "Position_Setpoint":
                    Element.value = int(self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_EncoderTicks"]) #MUST BE INT
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"][Index] == "Current_Quadrature_Setpoint":
                    Element.value = float(self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_ToBeSet"]) #MUST BE FLOAT
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"][Index] == "Voltage_Quadrature_Setpoint":
                    Element.value = float(self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_ToBeSet"]) #MUST BE FLOAT
                ##########################################################################################################

                '''
                ##########################################################################################################
                print("TPDOcallbackFunction_UpdateAllTPDOvariables_General: SlaveID_Int = " + str(SlaveID_Int) +
                      ", Time = " + str(self.getPreciseSecondsTimeStampString()) +
                      ", Variable = " + self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"][Index] +
                      ", Value = " + str(Element.value))
                ##########################################################################################################
                '''
        except:
            exceptions = sys.exc_info()[0]
            print("TPDOcallbackFunction_UpdateAllTPDOvariables, exceptions %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_1(self, ActualAllTPDOvariables_ListOfTPDOitems):

        SlaveID_Int = 1
        self.TPDOcallbackFunction_UpdateAllTPDOvariables_General(SlaveID_Int, ActualAllTPDOvariables_ListOfTPDOitems)

        self.UpdateFrequencyCalculation_CalculatedFromTPDOcallback_Filtered()  # We're guaranteed to always have slave 1, so we'll just measure here!
        
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_2(self, ActualAllTPDOvariables_ListOfTPDOitems):

        SlaveID_Int = 2
        self.TPDOcallbackFunction_UpdateAllTPDOvariables_General(SlaveID_Int, ActualAllTPDOvariables_ListOfTPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_3(self, ActualAllTPDOvariables_ListOfTPDOitems):

        SlaveID_Int = 3
        self.TPDOcallbackFunction_UpdateAllTPDOvariables_General(SlaveID_Int, ActualAllTPDOvariables_ListOfTPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_4(self, ActualAllTPDOvariables_ListOfTPDOitems):

        SlaveID_Int = 4
        self.TPDOcallbackFunction_UpdateAllTPDOvariables_General(SlaveID_Int, ActualAllTPDOvariables_ListOfTPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_5(self, ActualAllTPDOvariables_ListOfTPDOitems):

        SlaveID_Int = 5
        self.TPDOcallbackFunction_UpdateAllTPDOvariables_General(SlaveID_Int, ActualAllTPDOvariables_ListOfTPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General(self, SlaveID_Int, ActualAllRPDOvariables_ListOfRPDOitems):
        #Callback that is subscribed to get the actual variables for each cycle. Args: actual_AllPDOvariables:

        #print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General: SlaveID_Int = " + str(SlaveID_Int))

        try:
            for Index, Element in enumerate(ActualAllRPDOvariables_ListOfRPDOitems):

                ########################################################################################################## UNICORN. This is the line where RPDO data gets written to the main dictionary.
                #!@#!@#!@#!@#!@#!@#
                #!@#!@#!@#!@#!@#!@#
                #!@#!@#!@#!@#!@#!@#
                self.IngeniaMotionController_MainDict[SlaveID_Int][self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index]] = Element.value
                #!@#!@#!@#!@#!@#!@#
                #!@#!@#!@#!@#!@#!@#
                #!@#!@#!@#!@#!@#!@#
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "Position_Actual_EncoderTicks":
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_Actual_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, Element.value, "EncoderTicks", VelocityInsteadOfPositionFlag=0)
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "PositionSetPoint_Actual_EncoderTicks":
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionSetPoint_Actual_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, Element.value, "EncoderTicks", VelocityInsteadOfPositionFlag=0)
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "Velocity_Actual_EncoderTicks":
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["Velocity_Actual_AllUnitsDict"] = self.ConvertPositionToAllUnits(SlaveID_Int, Element.value, "EncoderTicks", VelocityInsteadOfPositionFlag=1)
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "Current_Direct_Actual":
                    pass
                    #print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General, Time = " + str(self.getPreciseSecondsTimeStampString()) + ", SlaveID_Int = " + str(SlaveID_Int) + ", PDOitem_Current_Direct_Actual received with a value of: " + str(Element.value))
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "Current_Quadrature_Actual":
                    pass
                    #print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General, Time = " + str(self.getPreciseSecondsTimeStampString()) + ", SlaveID_Int = " + str(SlaveID_Int) + ", PDOitem_Current_Quadrature_Actual received with a value of: " + str(Element.value))
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "Status_Word":
                    pass
                    #print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General, Time = " + str(self.getPreciseSecondsTimeStampString()) + ", SlaveID_Int = " + str(SlaveID_Int) + ", PDOitem_Status_Word received with a value of: " + str(Element.value))
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "STO_Status":
                    pass
                    #print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General, Time = " + str(self.getPreciseSecondsTimeStampString()) + ", SlaveID_Int = " + str(SlaveID_Int) + ", PDOitem_STO_Status received with a value of: " + str(Element.value))
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] == "Error_Last_HexCode":
                    pass
                    #print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General, Time = " + str(self.getPreciseSecondsTimeStampString()) + ", SlaveID_Int = " + str(SlaveID_Int) + ", Error_Last_HexCode received with a value of: " + str(Element.value))
                ##########################################################################################################


                '''
                ##########################################################################################################
                print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General: SlaveID_Int = " + str(SlaveID_Int) +
                      ", Time = " + str(self.getPreciseSecondsTimeStampString()) +
                      ", Variable = " + self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"][Index] +
                      ", Value = " + str(Element.value))
                ##########################################################################################################
                '''

        except:
            exceptions = sys.exc_info()[0]
            print("RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General, exceptions %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_1(self, ActualAllRPDOvariables_ListOfRPDOitems):

        SlaveID_Int = 1
        self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General(SlaveID_Int, ActualAllRPDOvariables_ListOfRPDOitems)

        self.UpdateFrequencyCalculation_CalculatedFromRPDOcallback_Filtered() #We're guaranteed to always have slave 1, so we'll just measure here!

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_2(self, ActualAllRPDOvariables_ListOfRPDOitems):

        SlaveID_Int = 2
        self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General(SlaveID_Int, ActualAllRPDOvariables_ListOfRPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_3(self, ActualAllRPDOvariables_ListOfRPDOitems):

        SlaveID_Int = 3
        self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General(SlaveID_Int, ActualAllRPDOvariables_ListOfRPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_4(self, ActualAllRPDOvariables_ListOfRPDOitems):

        SlaveID_Int = 4
        self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General(SlaveID_Int, ActualAllRPDOvariables_ListOfRPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_5(self, ActualAllRPDOvariables_ListOfRPDOitems):

        SlaveID_Int = 5
        self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_General(SlaveID_Int, ActualAllRPDOvariables_ListOfRPDOitems)

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def InitializeAndStartPDOdataExchange(self):

        #PDO mapping: https://drives.novantamotion.com/summit/ethercat-canopen-registers

        self.IngeniaMotionControllerObject.capture.pdo.clear_pdo_mapping()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.FunctionList_UpdateAllTPDOvariables = [self.TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_1,
                                                    self.TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_2,
                                                    self.TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_3,
                                                    self.TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_4,
                                                    self.TPDOcallbackFunction_UpdateAllTPDOvariables_SlaveID_5]

        self.FunctionList_NotifyAllRPDOvariablesActualValue = [self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_1,
                                                               self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_2,
                                                               self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_3,
                                                               self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_4,
                                                               self.RPDOcallbackFunction_NotifyAllRPDOvariablesActualValue_SlaveID_5]
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            for SlaveID_Int in self.DetectedSlaveID_List:

                print("InitializeAndStartPDOdataExchange: SlaveID_Int = " + str(SlaveID_Int))

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":

                    ####################################################
                    InitialValue_PositionSetpoint_TEMP = self.IngeniaMotionControllerObject.motion.get_actual_position(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])

                    print("InitializeAndStartPDOdataExchange: SlaveID_Int = " + str(SlaveID_Int) + ", InitialValue_PositionSetpoint_TEMP = " + str(InitialValue_PositionSetpoint_TEMP))

                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Position_Setpoint"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_POS_SET_POINT_VALUE",
                                                                                                                                                           value=int(InitialValue_PositionSetpoint_TEMP),
                                                                                                                                                           servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    ####################################################

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"] = []
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Position_Setpoint"])
                    ####################################################

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"].append("Position_Setpoint")
                    ####################################################

                ##########################################################################################################

                ##########################################################################################################
                elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Current_Quadrature_Setpoint"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_CUR_Q_SET_POINT",
                                                                                                                                                           value=int(0),
                                                                                                                                                           servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    ####################################################

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"] = []
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Current_Quadrature_Setpoint"])
                    ####################################################

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"].append("Current_Quadrature_Setpoint")
                    ####################################################

                ##########################################################################################################

                ##########################################################################################################
                elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":

                    ####################################################
                    #The units controlled are volts, so you would use the limit of your design (24VDC, then CAN command to +/- 24VDC?) not duty cycle.
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Voltage_Quadrature_Setpoint"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_VOL_Q_SET_POINT",
                                                                                                                                                           value=int(0),
                                                                                                                                                           servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                    ####################################################

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"] = []
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Voltage_Quadrature_Setpoint"])
                    ####################################################

                    ####################################################
                    self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfTPDOvariableNames"].append("Voltage_Quadrature_Setpoint")
                    ####################################################

                ##########################################################################################################

                ##########################################################################################################
                else:
                    print("InitializeAndStartPDOdataExchange: Error, OperationMode not supported!")
                    return
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Position_Actual"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_POS_FBK_VALUE",
                                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ########################################################################################################## ValueError: Cannot add a RPDOItem to a TPDOMap
                #self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_PositionSetPoint_Actual"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_POS_SET_POINT_VALUE",
                #                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"], value=0) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Velocity_Actual"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_VEL_FBK_VALUE",
                                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Current_Direct_Actual"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_CUR_D_VALUE",
                                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Current_Quadrature_Actual"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("CL_CUR_Q_VALUE",
                                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Status_Word"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("DRV_STATE_STATUS",
                                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_STO_Status"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("DRV_PROT_STO_STATUS",
                                                                                                                                                    servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                #https://drives.novantamotion.com/summit/0x200f-last-error
                #https://drives.novantamotion.com/summit/0x580f-last-error
                #https://drives.novantamotion.com/summit/0x5e49-system-last-error
                #DRV_DIAG_ERROR_LAST #works
                #DRV_DIAG_ERROR_LIST_CODE #Works
                #DRV_DIAG_ERROR_LAST_COM #KeyError: 'DRV_DIAG_ERROR_LAST_COM'
                #DRV_DIAG_SYS_ERROR_LAST #KeyError: 'DRV_DIAG_SYS_ERROR_LAST'
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Error_Last_HexCode"] = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_item("DRV_DIAG_ERROR_LAST",
                                                                                                                     servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #Create a RPDO map item
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"] = []
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Position_Actual"])
                #self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_PositionSetPoint_Actual"])
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Velocity_Actual"])
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Current_Direct_Actual"])
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Current_Quadrature_Actual"])
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Status_Word"])
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_STO_Status"])
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"].append(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDOitem_Error_Last_HexCode"])
                ##########################################################################################################

                ##########################################################################################################
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("Position_Actual_EncoderTicks")
                #self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("PositionSetPoint_Actual_EncoderTicks")
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("Velocity_Actual_EncoderTicks")
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("Current_Direct_Actual")
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("Current_Quadrature_Actual")
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("Status_Word")
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("STO_Status")
                self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["PDO_ListOfRPDOvariableNames"].append("Error_Last_HexCode")
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                rpdo_map_TEMP, tpdo_map_TEMP = self.IngeniaMotionControllerObject.capture.pdo.create_pdo_maps(self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"],
                                                                                                              self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"])
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################

                self.IngeniaMotionControllerObject.capture.pdo.subscribe_to_receive_process_data(partial(self.FunctionList_NotifyAllRPDOvariablesActualValue[SlaveID_Int-1],
                                                                                                         self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfRPDOitems"]))
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.IngeniaMotionControllerObject.capture.pdo.subscribe_to_send_process_data(partial(self.FunctionList_UpdateAllTPDOvariables[SlaveID_Int-1],
                                                                                                      self.IngeniaMotionController_RPDOandTPDOobjectsOnlyDict[SlaveID_Int]["ListOfTPDOitems"]))
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.IngeniaMotionControllerObject.capture.pdo.set_pdo_maps_to_slave(rpdo_map_TEMP,
                                                                                     tpdo_map_TEMP,
                                                                                     servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                #self.IngeniaMotionControllerObject.communication.sdo_write(0x1010, 0x01, (0x65766173).to_bytes(4, byteorder="little"))
                #self.IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MAX", int(PositionMax_EncoderTicks), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"]) #User maximum allowed position.

                #self.IngeniaMotionControllerObject.configuration.store_configuration(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                #self.IngeniaMotionControllerObject.configuration.save_configuration(os.path.join(os.getcwd(), "foo.xcf"), servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                print("InitializeAndStartPDOdataExchange: PDO mapping stored to NVM via 0x1010:01 and save XCF file locally.")
                ##########################################################################################################
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.IngeniaMotionControllerObject.capture.pdo.start_pdos(refresh_rate=self.PDO_UpdateDeltaTinSeconds)

            print("InitializeAndStartPDOdataExchange event fired!")
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("InitializeAndStartPDOdataExchange, exceptions %s" % exceptions)
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopPDOdataExchange(self):

        try:
            pass
            #self.IngeniaMotionControllerObject.capture.pdo.stop_pdos()

        except:
            exceptions = sys.exc_info()[0]
            print("StopPDOdataExchange, exceptions %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsDedicatedPDOthreadStillRunning(self):

        return self.DedicatedPDOthread_StillRunningFlag
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StartPDOdedicatedThread(self):

        #########################################################
        #########################################################
        self.DedicatedPDOthread_ThreadingObject = threading.Thread(target=self.DedicatedPDOthread, args=())
        self.DedicatedPDOthread_ThreadingObject.start()
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedPDOthread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedPDOthread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedPDOthread_StillRunningFlag = 1

        time.sleep(1.0)

        ##########################################################################################################
        if self.UsePDOflag == 1:
            self.InitializeAndStartPDOdataExchange()
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.CurrentTime_CalculatedFromDedicatedPDOThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedPDOThread
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                self.UpdateFrequencyCalculation_DedicatedPDOThread_Filtered()
                ##########################################################################################################
                ##########################################################################################################
     
                ##########################################################################################################
                ##########################################################################################################
                self.DedicatedPDOThread_TimeToSleepEachLoop = 0.010
                
                if self.DedicatedPDOThread_TimeToSleepEachLoop > 0.0:
                    if self.DedicatedPDOThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.DedicatedPDOThread_TimeToSleepEachLoop - 0.001)  # The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.DedicatedPDOThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedPDOthread, exceptions %s" % exceptions)
                traceback.print_exc()

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################


        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            self.StopPDOdataExchange()
        except:
            pass

        try:
            for SlaveID_Int in self.DetectedSlaveID_List:
                self.IngeniaMotionControllerObject.motion.motor_disable(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionControllerObject.communication.disconnect(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedPDOthread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedPDOthread_StillRunningFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedTxThread(self):

        #########################################################
        #########################################################
        self.MyPrint_WithoutLogFile("Started DedicatedTxThread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 1

        #for SlaveID_Int in self.DetectedSlaveID_List:
        #    self.SetEnabledState_ExternalProgram(SlaveID_Int, self.EnableMotorAtStartOfProgramFlag, PrintDebugFlag=0) Taken care of in Initializtion routine

        self.StartingTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString()
        #########################################################
        #########################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedTxThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                for SlaveID_Int in self.DetectedSlaveID_List:

                    ##########################################################################################################
                    ##########################################################################################################
                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                        ##########################################################################################################
                        if self.EnableMotorAutomaticallyAfterEstopRestorationFlag == 1:
                            if self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status"] != self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status_last"] and self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status_last"] == self.STO_EstopPRESSEDValue:

                                print("SlaveID_Int = " + str(SlaveID_Int) + ", STO fault was cleared, re-enabling motor.")

                                self.SetEnabledState_ExternalProgram(SlaveID_Int, 1, PrintDebugFlag=0)
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_NeedsToBeSetFlag"] == 1:
                            
                            self.__SetEnabledState(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["ResetFaults_EventNeedsToBeFiredFlag"] == 1:
                            
                            self.__ResetFaults(SlaveID_Int, PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["ResetFaults_EventNeedsToBeFiredFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_NeedsToBeSetFlag"] == 1:
                            
                            self.__SetDynamicBrakingEnabledState(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["ZeroEncoder_EventNeedsToBeFiredFlag"] == 1:
                            
                            self.SetPosition_ExternalProgram(SlaveID_Int, 0) #OTHERWISE THE MOTOR WILL JUMP BECAUSE ITS TARGET IS NO-ZERO WHEN ITS ENCODER IS RESET TO ZERO

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_ToBeSet"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_Actual_EncoderTicks"]
                            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_NeedsToBeSetFlag"] = 1

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["ZeroEncoder_EventNeedsToBeFiredFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_NeedsToBeSetFlag"] == 1:

                            self.__SetEncoderOffset(SlaveID_Int, 0.0, PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderOffset_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["FaultReset_EventNeedsToBeFiredFlag"] == 1:
                            
                            self.__ResetFaults(SlaveID_Int, PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["FaultReset_EventNeedsToBeFiredFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinAndMaxInEncoderTicks_NeedsToBeSetFlag"] == 1:

                            self.__SetPositionMinAndMaxInEncoderTicks(SlaveID_Int,
                                                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"]["EncoderTicks"],
                                                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"]["EncoderTicks"],
                                                                        PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinAndMaxInEncoderTicks_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindowTimeoutAndFaultParameters_NeedsToBeSetFlag"] == 1:

                            Window = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_ToBeSet"]
                            Timeout = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_ToBeSet"]
                            FaultModeInt = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_ToBeSet"]

                            self.__SetPositionFollowingErrorWindowTimeoutAndFaultParameters(SlaveID_Int, Window, Timeout, FaultModeInt, PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindowTimeoutAndFaultParameters_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_NeedsToBeSetFlag"] == 1:

                            self.__SetPositionPIDgains(SlaveID_Int,
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"],
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"],
                                                       self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"],
                                                       PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_NeedsToBeSetFlag"] == 1:

                            self.__SetVelocityPIDgains(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kp_ToBeSet"], self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Ki_ToBeSet"], self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_Kd_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["VelocityPIDgains_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_NeedsToBeSetFlag"] == 1:
                            
                            self.__SetCurrentDirectPIgains(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_ToBeSet"], self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_NeedsToBeSetFlag"] == 1:

                            self.__SetCurrentQuadraturePIgains(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"], self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_NeedsToBeSetFlag"] == 1:

                            self.__SetMaxVelocity(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVelocity_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_NeedsToBeSetFlag"] == 1:

                            self.__SetMaxProfileVelocity(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_NeedsToBeSetFlag"] == 1:

                            self.__SetMaxProfileAcceleration(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_NeedsToBeSetFlag"] == 1:

                            self.__SetMaxCurrentHardLimit(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################
                        
                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_NeedsToBeSetFlag"] == 1:

                            self.__SetMaxContinuousCurrent(SlaveID_Int, self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_ToBeSet"], PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                        ########################################################################################################## dragon
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValueTimeAndFaultParameters_NeedsToBeSetFlag"] == 1:

                            Value = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_ToBeSet"]
                            Time = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTimeMilliseconds_ToBeSet"]
                            FaultModeInt = self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_ToBeSet"]

                            self.__SetPeakCurrentValueTimeAndFaultParameters(SlaveID_Int, Value, Time, FaultModeInt, FaultReactionTimeoutMilliseconds_ToBeSet=1, PrintDebugFlag=1)

                            self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValueTimeAndFaultParameters_NeedsToBeSetFlag"] = 0
                        ##########################################################################################################

                    ##########################################################################################################
                    ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedTxThread, exceptions on SlaveID_Int = " + str(SlaveID_Int) + ": %s" % exceptions)
                #traceback.print_exc()

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.UpdateFrequencyCalculation_DedicatedTxThread_Filtered()
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            if self.DedicatedTxThread_TimeToSleepEachLoop > 0.0:
                if self.DedicatedTxThread_TimeToSleepEachLoop > 0.001:
                    time.sleep(self.DedicatedTxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                else:
                    time.sleep(self.DedicatedTxThread_TimeToSleepEachLoop)
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:
            for SlaveID_Int in self.DetectedSlaveID_List:
                self.IngeniaMotionControllerObject.motion.motor_disable(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                self.IngeniaMotionControllerObject.communication.disconnect(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
        except:
            pass
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedTxThread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedRxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedRxThread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 1

        self.StartingTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromDedicatedRxThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromDedicatedRxThread
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            try:

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if self.SDOcommands_Rx_EnabledFlag == 1: #GLOBAL, SET AT TOP OF THE CLASS

                    for SlaveID_Int in self.DetectedSlaveID_List:

                        ##########################################################################################################
                        ##########################################################################################################
                        ##########################################################################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"] == 1:

                            ##########################################################################################################
                            ##########################################################################################################
                            if self.IngeniaMotionController_MainDict[SlaveID_Int]["GetSDOvariablesEveryNloopsCycles"] > 0:

                                ##########################################################################################################
                                if self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] == 0:

                                    ####################################################
                                    self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] + 1
                                    ####################################################

                                    ####################################################
                                    #print("ListOfVariableNameStringsToGetViaSDO: " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]))

                                    if "STO_Status" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status"] = self.IngeniaMotionControllerObject.configuration.get_STO_Status(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for STO_Status on SlaveID_Int = " + str(SlaveID_Int))

                                    if "Status_Word" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["Status_Word"] = self.IngeniaMotionControllerObject.configuration.get_status_word(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for Status_Word on SlaveID_Int = " + str(SlaveID_Int))

                                    if "Position_Actual_EncoderTicks" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_Actual_EncoderTicks"] = self.IngeniaMotionControllerObject.motion.get_actual_position(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for Position_Actual_EncoderTicks on SlaveID_Int = " + str(SlaveID_Int))

                                    if "Velocity_Actual_EncoderTicks" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["Velocity_Actual_EncoderTicks"] = self.IngeniaMotionControllerObject.motion.get_actual_velocity(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for Velocity_Actual_EncoderTicks on SlaveID_Int = " + str(SlaveID_Int))

                                    if "Current_Direct_Actual" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Direct_Actual"] = self.IngeniaMotionControllerObject.motion.get_actual_current_direct(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for Current_Direct_Actual on SlaveID_Int = " + str(SlaveID_Int))

                                    if "Current_Quadrature_Actual" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_Actual"] = self.IngeniaMotionControllerObject.motion.get_actual_current_quadrature(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for Current_Quadrature_Actual on SlaveID_Int = " + str(SlaveID_Int))

                                    if "EnabledState_Actual" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_Actual"] = self.IngeniaMotionControllerObject.configuration.is_motor_enabled(servo=self.IngeniaMotionController_MainDict[SlaveID_Int]["AliasOrServoName_String"])
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for EnabledState_Actual on SlaveID_Int = " + str(SlaveID_Int))

                                    if "HallEffectValue_Actual_Int" in self.IngeniaMotionController_MainDict[SlaveID_Int]["ListOfVariableNameStringsToGetViaSDO"]:
                                        self.__GetHallEffectValue(SlaveID_Int, PrintDebugFlag=0)
                                        if self.SDOcommands_Rx_PrintDebuggingStatementsFlag == 1:
                                            print("DedicatedRxThread, SDO query made for HallEffectValue_Actual_Int on SlaveID_Int = " + str(SlaveID_Int))
                                    ####################################################

                                    ####################################################
                                    self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status_last"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status"]
                                    ####################################################

                                ##########################################################################################################
                                else:
                                    self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] + 1

                                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] >= self.IngeniaMotionController_MainDict[SlaveID_Int]["GetSDOvariablesEveryNloopsCycles"]:
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["AskForInfrequentDataReadLoopCounter"] = 0
                                ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################

                        ##########################################################################################################
                        ##########################################################################################################
                        ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                for SlaveID_Int in self.DetectedSlaveID_List:
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["StatusWordFlagStates_DictEnglishNameAsKey"] = self.StatusWordInterpretation(self.IngeniaMotionController_MainDict[SlaveID_Int]["Status_Word"])
                    self.IngeniaMotionController_MainDict[SlaveID_Int]["STOstatusFlagStates_DictEnglishNameAsKey"] = self.STOstatusInterpretation(self.IngeniaMotionController_MainDict[SlaveID_Int]["STO_Status"])

                    self.IngeniaMotionController_MainDict[SlaveID_Int]["Error_Last_EnglishName"] = self.ErrorHexCodeInterpretation(self.IngeniaMotionController_MainDict[SlaveID_Int]["Error_Last_HexCode"])

                    self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["StatusWordFlagStates_DictEnglishNameAsKey"]["OperationEnabled"] #unicorn


                    self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_FOCcombinedDQ_Actual"] = self.sign(self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_Actual"])*math.sqrt(math.pow(self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Direct_Actual"], 2) + math.pow(self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_Actual"], 2))


                ##########################################################################################################

                ##########################################################################################################
                self.MostRecentDataDict["IngeniaMotionController_MainDict"] = self.IngeniaMotionController_MainDict.copy()  # Don't need deepcopy as there are only numbers being copied
                ##########################################################################################################

                ##########################################################################################################
                self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                self.MostRecentDataDict["CurrentTime_CalculatedFromDedicatedTxThread"] = self.CurrentTime_CalculatedFromDedicatedTxThread
                self.MostRecentDataDict["CurrentTime_CalculatedFromDedicatedRxThread"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedTxThread
                self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedRxThread
                self.MostRecentDataDict["DetectedSlaveID_List"] = self.DetectedSlaveID_List
                ##########################################################################################################


                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                self.UpdateFrequencyCalculation_DedicatedRxThread_Filtered()

                if self.DedicatedRxThread_TimeToSleepEachLoop > 0.0:
                    if self.DedicatedRxThread_TimeToSleepEachLoop > 0.001:
                        time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                    else:
                        time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop)
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################

            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedRxThread, exceptions: %s" % exceptions)
                traceback.print_exc()

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished DedicatedRxThread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ErrorHexCodeInterpretation(self, ErrorHexCodeToIntrepret, PrintDebugFlag=0):

        try:

            if PrintDebugFlag == 1:
                print("ErrorHexCodeInterpretation: ErrorHexCodeToIntrepret = " + str(ErrorHexCodeToIntrepret))

            if ErrorHexCodeToIntrepret in self.ErrorCodes_DictHexNumberAsKey:
                return self.ErrorCodes_DictHexNumberAsKey[ErrorHexCodeToIntrepret]

            else:
                return ""

        except:
            exceptions = sys.exc_info()[0]
            print("ErrorHexCodeInterpretation, exceptions: %s" % exceptions)
            return self.ErrorCodes_DictHexNumberAsKey.copy()
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################


    ##########################################################################################################
    ##########################################################################################################
    def STOstatusInterpretation(self, STOstatusToIntrepret):

        '''
        https://drives.novantamotion.com/summit/0x251a-sto-status
        
        15-5: Reserved
        4: STO Report
        3: STO Abnormal Fault
        2: /STO Supply Fault
        1: STO2 State
        0: STO1 State

        '''

        try:
            STOstatusFlagStates_DictEnglishNameAsKey_TEMP = self.STOstatusFlagStates_DictEnglishNameAsKey.copy()

            ##########################################################################################################
            for BitNumber in self.STOstatusFlagNames_DictBitNumberAsKey:
                EnglishName = self.STOstatusFlagNames_DictBitNumberAsKey[BitNumber]
                State = STOstatusToIntrepret & (1 << BitNumber)

                STOstatusFlagStates_DictEnglishNameAsKey_TEMP[EnglishName] = bool(State)

                if EnglishName in ["STO1state", "STO2state", "STOreport"]:
                    STOstatusFlagStates_DictEnglishNameAsKey_TEMP[EnglishName] = not STOstatusFlagStates_DictEnglishNameAsKey_TEMP[EnglishName] #The standard logic goes against my intuition

            ##########################################################################################################

            return STOstatusFlagStates_DictEnglishNameAsKey_TEMP

        except:
            exceptions = sys.exc_info()[0]
            print("STOstatusInterpretation, exceptions: %s" % exceptions)
            return self.STOstatusFlagStates_DictEnglishNameAsKey.copy()
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StatusWordInterpretation(self, StatusWordToIntrepret):

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
            StatusWordFlagStates_DictEnglishNameAsKey_TEMP = self.StatusWordFlagStates_DictEnglishNameAsKey.copy()

            ##########################################################################################################
            for BitNumber in self.StatusWordFlagNames_DictBitNumberAsKey:
                EnglishName = self.StatusWordFlagNames_DictBitNumberAsKey[BitNumber]
                State = StatusWordToIntrepret & (1 << BitNumber)

                StatusWordFlagStates_DictEnglishNameAsKey_TEMP[EnglishName] = bool(State)
            ##########################################################################################################

            return StatusWordFlagStates_DictEnglishNameAsKey_TEMP

        except:
            exceptions = sys.exc_info()[0]
            print("StatusWordInterpretation, exceptions: %s" % exceptions)
            return self.StatusWordFlagStates_DictEnglishNameAsKey.copy()
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for IngeniaBLDC_ReubenPython3Class object")

        self.EXIT_PROGRAM_FLAG = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateGUIobjects(self, TkinterParent):

        print("IngeniaBLDC_ReubenPython3Class, CreateGUIobjects event fired.")

        #################################################
        #################################################
        #################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150)  # RGB
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightBlueColor = '#%02x%02x%02x' % (150, 150, 255)  # RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleLabelWidth = 30
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)
        self.DeviceInfo_Label["text"] = (self.NameToDisplay_UserSet)
        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.AllMotorsInfoFrame = Frame(self.myFrame)
        self.AllMotorsInfoFrame.grid(row = 2, column = 0, padx = self.GUI_PADX, pady = self.GUI_PADY, rowspan = 1, columnspan = 2)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        for SlaveID_Int in self.DetectedSlaveID_List:
        
            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoFrame"] = Frame(self.AllMotorsInfoFrame)
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoFrame"]["borderwidth"] = 2
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoFrame"]["relief"] = "ridge"
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoFrame"].grid(row=0, column=SlaveID_Int-1, padx=self.GUI_PADX, pady=self.GUI_PADY, rowspan=1, columnspan=1)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"] = Canvas(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoFrame"])
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"].grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, rowspan=1, columnspan=1)

            #self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas_Scrollbar"] = Scrollbar(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoFrame"], orient='vertical')
            #self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas_Scrollbar"].grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas_Scrollbar"].config(command = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"].yview)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"] = Label(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"],
                                                                                                              text="IndividualMotorInfo_Label " + str(SlaveID_Int),
                                                                                                              width=55)

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"].grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_ButtonsFrame"] = Frame(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"])
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_ButtonsFrame"].grid(row=1, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, rowspan=1, columnspan=1)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EnabledState_Button"] = Button(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_ButtonsFrame"],
                                                                                                         text="EnabledState" + str(SlaveID_Int), state="normal",
                                                                                                         width=10,
                                                                                                         bg=self.TKinter_LightYellowColor,
                                                                                                         command=lambda name=SlaveID_Int: self.EnabledState_Button_Response(name))

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EnabledState_Button"].grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["ZeroEncoder_Button"] = Button(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_ButtonsFrame"],
                                                                                                         text="ZeroEncoder" + str(SlaveID_Int), state="normal",
                                                                                                         width=10,
                                                                                                         bg=self.TKinter_DefaultGrayColor,
                                                                                                         command=lambda name=SlaveID_Int: self.ZeroEncoder_Button_Response(name))

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowEncoderToBeZeroedFlag"] == 0:
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["ZeroEncoder_Button"]["state"] = "disabled"

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["ZeroEncoder_Button"].grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["FaultReset_Button"] = Button(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_ButtonsFrame"],
                                                                                                         text="FaultReset" + str(SlaveID_Int), state="normal",
                                                                                                         width=10,
                                                                                                         bg=self.TKinter_DefaultGrayColor,
                                                                                                         command=lambda name=SlaveID_Int: self.FaultReset_Button_Response(name))

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["FaultReset_Button"].grid(row=0, column=2, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################
            #################################################
            
            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["DynamicBrakingEnabledState_Button"] = Button(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_ButtonsFrame"],
                                                                                                         text="DynamicBraking" + str(SlaveID_Int), state="normal",
                                                                                                         width=14,
                                                                                                         bg=self.TKinter_DefaultGrayColor,
                                                                                                         command=lambda name=SlaveID_Int: self.DynamicBrakingEnabledState_Button_Response(name))

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["DynamicBrakingEnabledState_Button"].grid(row=0, column=3, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################
            #################################################

            #################################################
            #################################################
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict"] = dict([("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                                                                    ("GUI_ROW", 3),
                                                                                                                                                    ("GUI_COLUMN", 0),
                                                                                                                                                    ("GUI_PADX", 1),
                                                                                                                                                    ("GUI_PADY", 1),
                                                                                                                                                    ("GUI_ROWSPAN", 1),
                                                                                                                                                    ("GUI_COLUMNSPAN", 1)])

            EntryWidth = 10
            LabelWidth = 40
            FontSize = 8

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_Variables_ListOfDicts"] = [dict([("Name", "PositionPIDgains_Kp_ToBeSet"),("Type", "float"),("StartingVal", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"]),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                                                                                               dict([("Name", "PositionPIDgains_Ki_ToBeSet"),("Type", "float"),("StartingVal", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"]),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                                                                                               dict([("Name", "PositionPIDgains_Kd_ToBeSet"),("Type", "float"),("StartingVal", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"]),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_Variables_ListOfDicts"] = [dict([("Name", "CurrentQuadraturePIgains_Kp_ToBeSet"),("Type", "float"),("StartingVal", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"]),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                                                                                               dict([("Name", "CurrentQuadraturePIgains_Ki_ToBeSet"),("Type", "float"),("StartingVal", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"]),("MinVal", -1000000.0),("MaxVal", 1000000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_Variables_ListOfDicts"] = []

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict"] = dict([("GUIparametersDict", self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict"]),
                                                                                                                                                  ("EntryListWithBlinking_Variables_ListOfDicts", self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_Variables_ListOfDicts"]),
                                                                                                                                                  ("DebugByPrintingVariablesFlag", 0),
                                                                                                                                                  ("LoseFocusIfMouseLeavesEntryFlag", 0)])

            try:
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"] = EntryListWithBlinking_ReubenPython2and3Class(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict"])
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_OPEN_FLAG"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].OBJECT_CREATED_SUCCESSFULLY_FLAG
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber"] = 0
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last"] = -1
                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedFromExternalSourceFlag"] = 0

                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].CreateGUIobjects(TkinterParent=self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"]) #unicorn

            except:
                exceptions = sys.exc_info()[0]
                print("GUI_Thread EntryListWithBlinking_ReubenPython2and3ClassObject: Exceptions: %s" % exceptions)
                traceback.print_exc()
            #################################################
            #################################################

            #################################################
            #################################################

            ################################################# Frame
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Frame"] = Frame(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfoCanvas"])
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Frame"].grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, rowspan=1, columnspan=1)
            #################################################

            ################################################# Label
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Label"] = Label(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Frame"],
                                                                                                              text="EncTicks",
                                                                                                              width=10)
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Label"].grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################

            ################################################# Scale
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Value"] = DoubleVar()

            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":

                GUIscale_ScaleObject_FROM = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"]["EncoderTicks"]
                GUIscale_ScaleObject_TO = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"]["EncoderTicks"]
                GUIscale_ScaleObject_RESOLUTION = 1

                if GUIscale_ScaleObject_FROM == 0.0 and GUIscale_ScaleObject_TO == 0.0:
                    GUIscale_ScaleObject_FROM = -1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_Actual"] #Still want to be able to use sliders even with infinite rotation enabled
                    GUIscale_ScaleObject_TO = self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_Actual"] #Still want to be able to use sliders even with infinite rotation enabled

            elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                GUIscale_ScaleObject_FROM = -1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"]
                GUIscale_ScaleObject_TO = self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_ToBeSet"]
                GUIscale_ScaleObject_RESOLUTION = 0.01

            elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                GUIscale_ScaleObject_FROM = -24.0 #-1.0*self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVoltage_ToBeSet"] #WHERE SHOULD THESE NUMBERS COME FROM?
                GUIscale_ScaleObject_TO = 24.0 #self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxVoltage_ToBeSet"] #WHERE SHOULD THESE NUMBERS COME FROM?
                GUIscale_ScaleObject_RESOLUTION = 0.01

            else:
                GUIscale_ScaleObject_FROM = -11111.0
                GUIscale_ScaleObject_TO = 11111.0
                GUIscale_ScaleObject_RESOLUTION = 1

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"] = Scale(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Frame"],
                                                                                                                                       from_=GUIscale_ScaleObject_FROM,
                                                                                                                                       to=GUIscale_ScaleObject_TO,
                                                                                                                                       orient=HORIZONTAL,
                                                                                                                                       borderwidth=2,
                                                                                                                                       showvalue=True,
                                                                                                                                       width=self.TkinterScaleWidth,
                                                                                                                                       length=self.TkinterScaleLength,
                                                                                                                                       resolution=GUIscale_ScaleObject_RESOLUTION,
                                                                                                                                       variable=self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Value"])

            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].bind('<Button-1>', lambda event, name=SlaveID_Int: self.IndividualMotorMotionSetpoint_GUIscale_EventResponse(event, name))
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].bind('<B1-Motion>', lambda event, name=SlaveID_Int: self.IndividualMotorMotionSetpoint_GUIscale_EventResponse(event, name))
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].bind('<ButtonRelease-1>', lambda event, name=SlaveID_Int: self.IndividualMotorMotionSetpoint_GUIscale_EventResponse(event, name))
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].set(self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_EncoderTicks"])
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] = 0
            #################################################

            ################################################# Button
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ZeroScaleButton"] = Button(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_Frame"],
                                                                                                         text="GoTo0",
                                                                                                         state="normal",
                                                                                                         width=5,
                                                                                                         bg=self.TKinter_DefaultGrayColor,
                                                                                                         command=lambda name=SlaveID_Int: self.ZeroScale_Button_Response(name))
            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ZeroScaleButton"].grid(row=0, column=2, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
            #################################################

            #################################################
            #################################################

        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=3, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################
        #################################################

        #################################################
        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EnabledState_Button_Response(self, name):

        SlaveID_Int = int(name)

        ##########################################################################################################
        if self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_Actual"] == 1:
            self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_ToBeSet"] = 0
        else:
            self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_ToBeSet"] = 1
        ##########################################################################################################

        ##########################################################################################################
        self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_NeedsToBeSetFlag"] = 1
        ##########################################################################################################

        ##########################################################################################################
        #print("EnabledState_Button_Response: Event fired for SlaveID_Int = " + str(SlaveID_Int) +
        #      ", EnabledState_ToBeSet = " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_ToBeSet"]))
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ZeroEncoder_Button_Response(self, name):

        SlaveID_Int = int(name)

        ##########################################################################################################
        self.IngeniaMotionController_MainDict[SlaveID_Int]["ZeroEncoder_EventNeedsToBeFiredFlag"] = 1
        ##########################################################################################################

        ##########################################################################################################
        print("ZeroEncoder_Button_Response: Event fired for SlaveID_Int = " + str(SlaveID_Int))
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def FaultReset_Button_Response(self, name):

        SlaveID_Int = int(name)

        ##########################################################################################################
        self.IngeniaMotionController_MainDict[SlaveID_Int]["FaultReset_EventNeedsToBeFiredFlag"] = 1
        ##########################################################################################################

        ##########################################################################################################
        print("FaultReset_Button_Response: Event fired for SlaveID_Int = " + str(SlaveID_Int))
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DynamicBrakingEnabledState_Button_Response(self, name):

        SlaveID_Int = int(name)

        ##########################################################################################################
        if self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_Actual"] == 1:
            self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_ToBeSet"] = 0
        else:
            self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_ToBeSet"] = 1

        self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_NeedsToBeSetFlag"] = 1
        ##########################################################################################################

        ##########################################################################################################
        print("DynamicBrakingEnabledState_Button_Response: Event fired for SlaveID_Int = " + str(SlaveID_Int))
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IndividualMotorMotionSetpoint_GUIscale_EventResponse(self, event, name):

        SlaveID_Int = int(name)

        GUIscale_Value = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].get()

        ##########################################################################################################
        if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
            self.LimitValue_ConvertUnits_And_SetVariable___PositionToBeSet(SlaveID_Int, GUIscale_Value, "EncoderTicks", PrintDebugFlag=0)
            #self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_NeedsToBeSetFlag"] = 1 #Not needed when using TPDO
        ##########################################################################################################
        
        ##########################################################################################################
        elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_ToBeSet"] = GUIscale_Value
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_NeedsToBeSetFlag"] = 1
        ##########################################################################################################
        
        ##########################################################################################################
        elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_ToBeSet"] = GUIscale_Value
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_NeedsToBeSetFlag"] = 1
        ##########################################################################################################
        
        
        #print("IndividualMotorMotionSetpoint_GUIscale_EventResponse for SlaveID_Int = " + str(SlaveID_Int) +
        #      ", Position set to " + str(self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_EncoderTicks"]))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ZeroScale_Button_Response(self, name):

        SlaveID_Int = int(name)

        ##########################################################################################################
        if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
            self.LimitValue_ConvertUnits_And_SetVariable___PositionToBeSet(SlaveID_Int, 0, "EncoderTicks", PrintDebugFlag=0)
            # self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_NeedsToBeSetFlag"] = 1 #Not needed when using TPDO
        ##########################################################################################################

        ##########################################################################################################
        elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_ToBeSet"] = 0
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_NeedsToBeSetFlag"] = 1
        ##########################################################################################################

        ##########################################################################################################
        elif self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_ToBeSet"] = 0
            self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_NeedsToBeSetFlag"] = 1
        ##########################################################################################################

        ##########################################################################################################
        self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] = 1
        ##########################################################################################################

        ##########################################################################################################
        print("ZeroScale_Button_Response: Event fired for SlaveID_Int = " + str(SlaveID_Int))
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                #######################################################
                #######################################################
                try:

                    #######################################################
                    #######################################################
                    #######################################################
                    self.Data_Label["text"] = "Time, PDO callback Tx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromTPDOcallback, 0, 3) +\
                                                "\t\tTime, PDO callback Rx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromRPDOcallback, 0, 3) +\
                                                "\nPDO callback Frequency, Tx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromTPDOcallback, 0, 3) +\
                                                "\t\tPDO callback Frequency, Rx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromRPDOcallback, 0, 3)

                    self.Data_Label["text"] = self.Data_Label["text"] + "\n\nTime, Main PDO: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromDedicatedPDOThread, 0, 3) +\
                                              "\tTime, Main Tx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromDedicatedTxThread, 0, 3) +\
                                              "\tTime, Main Rx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromDedicatedRxThread, 0, 3) + \
                                              "\nFrequency, Main PDO: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromDedicatedPDOThread, 0, 3) + \
                                              "\tFrequency, Main Tx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromDedicatedTxThread, 0, 3) +\
                                              "\tFrequency, Main Rx: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromDedicatedRxThread, 0, 3) +\
                                              "\tFrequency, GUI: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromGUIthread, 0, 3)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    for SlaveID_Int in self.DetectedSlaveID_List:

                        #######################################################
                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_Actual"] == 1:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EnabledState_Button"]["bg"] = self.TKinter_LightGreenColor

                        elif self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_Actual"] == 0:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EnabledState_Button"]["bg"] = self.TKinter_LightRedColor

                        else:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EnabledState_Button"]["bg"] = self.TKinter_LightYellowColor
                        #######################################################
                        #######################################################
                        
                        #######################################################
                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_Actual"] == 1:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["DynamicBrakingEnabledState_Button"]["bg"] = self.TKinter_LightGreenColor

                        elif self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_Actual"] == 0:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["DynamicBrakingEnabledState_Button"]["bg"] = self.TKinter_LightRedColor

                        else:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["DynamicBrakingEnabledState_Button"]["bg"] = self.TKinter_LightYellowColor
                        #######################################################
                        #######################################################

                        #######################################################
                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["Error_Last_EnglishName"] != "NoError":
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["FaultReset_Button"]["bg"] = self.TKinter_LightBlueColor

                        else:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["FaultReset_Button"]["bg"] = self.TKinter_DefaultGrayColor
                        #######################################################
                        #######################################################

                        #######################################################
                        #######################################################
                        DictToDisplay = dict([("JointEnglishName", self.IngeniaMotionController_MainDict[SlaveID_Int]["JointEnglishName"]),
                                            ("SerialNumber_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["SerialNumber_Actual"]),
                                            ("SlaveID_Int", self.IngeniaMotionController_MainDict[SlaveID_Int]["SlaveID_Int"]),
                                            ("BusVoltage", self.IngeniaMotionController_MainDict[SlaveID_Int]["BusVoltage"]),
                                            ("AllowWritingOfControllerConfigurationFlag", self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowWritingOfControllerConfigurationFlag"]),
                                            ("MotorConnectedFlag", self.IngeniaMotionController_MainDict[SlaveID_Int]["MotorConnectedFlag"]),
                                            ("CommutationMode_Actual_EnglishName", self.IngeniaMotionController_MainDict[SlaveID_Int]["CommutationMode_Actual_EnglishName"]),
                                            ("OperationMode_Actual_EnglishName", self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode_Actual_EnglishName"]),
                                            ("EncoderTicksPerRevolution_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["EncoderTicksPerRevolution_Actual"]),
                                            ("EnabledState_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["EnabledState_Actual"]),
                                            ("DynamicBrakingEnabledState_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["DynamicBrakingEnabledState_Actual"]),
                                            ("Error_Last_HexCode", self.IngeniaMotionController_MainDict[SlaveID_Int]["Error_Last_HexCode"]),
                                            ("Error_Last_EnglishName", self.IngeniaMotionController_MainDict[SlaveID_Int]["Error_Last_EnglishName"]),
                                            ("Position_ToBeSet_EncoderTicks", self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_EncoderTicks"]),
                                            ("Current_Quadrature_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_ToBeSet"]),
                                            ("Voltage_Quadrature_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_ToBeSet"]),
                                            ("MaxCurrentHardLimit_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxCurrentHardLimit_Actual"]),
                                            ("MaxContinuousCurrent_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxContinuousCurrent_Actual"]),

                                            ("CurrentDirectPIgains_Kp_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Kp_Actual"]),
                                            ("CurrentDirectPIgains_Ki_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirectPIgains_Ki_Actual"]),
                                            ("CurrentDirect_CL_CUR_D_MAX_OUT_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirect_CL_CUR_D_MAX_OUT_Actual"]),
                                            ("CurrentDirect_CL_CUR_D_MIN_OUT_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentDirect_CL_CUR_D_MIN_OUT_Actual"]),
                                            ("CurrentQuadraturePIgains_Kp_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_Actual"]),
                                            ("CurrentQuadraturePIgains_Ki_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_Actual"]),
                                            ("CurrentQuadrature_CL_CUR_Q_MAX_OUT_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadrature_CL_CUR_Q_MAX_OUT_Actual"]),
                                            ("CurrentQuadrature_CL_CUR_Q_MIN_OUT_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadrature_CL_CUR_Q_MIN_OUT_Actual"]),
                                              
                                            ("PeakCurrentValue_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_Actual"]),
                                            ("PeakCurrentTime_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTime_Actual"]),
                                            ("PeakCurrentFaultModeInt_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_Actual"]),
                                            ("Current_Direct_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Direct_Actual"]),
                                            ("Current_Quadrature_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_Actual"]),
                                            ("MaxProfileVelocity_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileVelocity_Actual"]),
                                            ("MaxProfileAcceleration_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["MaxProfileAcceleration_Actual"]),
                                            ("PositionMin_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_EncoderTicks_Actual"]),
                                            ("PositionMax_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_EncoderTicks_Actual"]),
                                            ("AllowEncoderToBeZeroedFlag", self.IngeniaMotionController_MainDict[SlaveID_Int]["AllowEncoderToBeZeroedFlag"])])

                        '''
                        ("PositionMin_AllUnitsDict", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_AllUnitsDict"]),
                        ("PositionMax_AllUnitsDict", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_AllUnitsDict"]),
                        ("PositionMinRange_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinRange_EncoderTicks_Actual"]),
                        ("PositionMaxRange_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMaxRange_EncoderTicks_Actual"]),
                        ("PositionFollowingErrorWindow_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorWindow_Actual"]),
                        ("PositionFollowingErrorTimeoutMilliseconds_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorTimeoutMilliseconds_Actual"]),
                        ("PositionFollowingErrorFaultModeInt_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionFollowingErrorFaultModeInt_Actual"])
                        ("PeakCurrentValue_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentValue_Actual"]),
                        ("PeakCurrentTime_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentTime_Actual"]),
                        ("PeakCurrentFaultModeInt_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PeakCurrentFaultModeInt_Actual"])
                        ("PositionMinRange_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMinRange_EncoderTicks_Actual"]),
                        ("PositionMaxRange_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMaxRange_EncoderTicks_Actual"]),
                        ("PositionMin_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMin_EncoderTicks_Actual"]),
                        ("PositionMax_EncoderTicks_Actual", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionMax_EncoderTicks_Actual"])
                        '''

                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
                            DictToDisplay["PositionPIDgains_Kp_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_Actual"]
                            DictToDisplay["PositionPIDgains_Ki_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_Actual"]
                            DictToDisplay["PositionPIDgains_Kd_Actual"] =  self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_Actual"]
                            #DictToDisplay["PositionPIDgains_PIDcontrollerMaxOutputUmax_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_PIDcontrollerMaxOutputUmax_Actual"]
                            #DictToDisplay["PositionPIDgains_PIDcontrollerMinOutputUmin_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_PIDcontrollerMinOutputUmin_Actual"]
                        #######################################################

                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                            DictToDisplay["CurrentQuadraturePIgains_Kp_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_Actual"]
                            DictToDisplay["CurrentQuadraturePIgains_Ki_Actual"] = self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_Actual"]
                        #######################################################

                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                            pass
                        #######################################################

                        #######################################################
                        self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(DictToDisplay,
                                                                                                                                                                                NumberOfDecimalsPlaceToUse = 4,
                                                                                                                                                                                NumberOfEntriesPerLine = 1,
                                                                                                                                                                                NumberOfTabsBetweenItems = 1)
                        #######################################################

                        #######################################################
                        self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["text"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["text"] +\
                                                                self.ConvertDictToProperlyFormattedStringForPrinting(self.IngeniaMotionController_MainDict[SlaveID_Int]["StatusWordFlagStates_DictEnglishNameAsKey"], 0, 2, 2) + \
                                                                "\n\n" + \
                                                                self.ConvertDictToProperlyFormattedStringForPrinting(self.IngeniaMotionController_MainDict[SlaveID_Int]["STOstatusFlagStates_DictEnglishNameAsKey"], 0, 2, 2)

                        #######################################################

                        #######################################################
                        self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["text"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["text"] + \
                                                                                                                            "\nPosition ToBeSet: " + \
                                                                                                                            self.ConvertDictToProperlyFormattedStringForPrinting(self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_AllUnitsDict"], 3, 1, 1) +\
                                                                                                                            "\nPosition Actual: " +\
                                                                                                                            self.ConvertDictToProperlyFormattedStringForPrinting(self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_Actual_AllUnitsDict"], 3, 1, 1) + \
                                                                                                                            "\nHallEffect Actual: " + \
                                                                                                                            str(self.IngeniaMotionController_MainDict[SlaveID_Int]["HallEffectValue_Actual_Int"])
                        #######################################################
                        
                        #######################################################
                        #######################################################

                        ####################################################### Change the background color based on STOreport, NOT the motor's Operational State
                        #######################################################
                        if self.IngeniaMotionController_MainDict[SlaveID_Int]["STOstatusFlagStates_DictEnglishNameAsKey"]["STOreport"] == 1:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["bg"] = self.TKinter_LightRedColor

                        else:
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorInfo_Label"]["bg"] = self.TKinter_DefaultGrayColor
                        #######################################################
                        #######################################################

                        #######################################################
                        #######################################################
                        if self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] == 1:

                            #######################################################
                            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
                                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].set(self.IngeniaMotionController_MainDict[SlaveID_Int]["Position_ToBeSet_EncoderTicks"])
                            #######################################################

                            #######################################################
                            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].set(self.IngeniaMotionController_MainDict[SlaveID_Int]["Current_Quadrature_ToBeSet"])
                            #######################################################

                            #######################################################
                            if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject"].set(self.IngeniaMotionController_MainDict[SlaveID_Int]["Voltage_Quadrature_ToBeSet"])
                            #######################################################

                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["IndividualMotorMotionSetpoint_GUIscale_ScaleObject_ValueNeedsToBeUpdated"] = 0
                        #######################################################
                        #######################################################

                        #########################################################
                        #######################################################
                        if self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_OPEN_FLAG"] == 1:

                            #######################################################
                            if self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedFromExternalSourceFlag"] == 1:

                                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
                                    self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].SetEntryValue("PositionPIDgains_Kp_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"])
                                    self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].SetEntryValue("PositionPIDgains_Ki_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"])
                                    self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].SetEntryValue("PositionPIDgains_Kd_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"])

                                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                                    self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].SetEntryValue("CurrentQuadraturePIgains_Kp_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"])
                                    self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].SetEntryValue("CurrentQuadraturePIgains_Ki_ToBeSet", self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"])

                                if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                                    pass

                                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject_NeedsToBeUpdatedFromExternalSourceFlag"] = 0
                            #######################################################

                            #######################################################
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].GetMostRecentDataDict()
                            #print(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"])

                            if "DataUpdateNumber" in self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]:
                                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["DataUpdateNumber"]

                            if self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber"] != self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last"]:
                                self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["DataUpdateNumber"]

                                if self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber"] >= 1:

                                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicPosition":
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kp_ToBeSet"] = float(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["PositionPIDgains_Kp_ToBeSet"])
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Ki_ToBeSet"] = float(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["PositionPIDgains_Ki_ToBeSet"])
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_Kd_ToBeSet"] = float(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["PositionPIDgains_Kd_ToBeSet"])
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["PositionPIDgains_NeedsToBeSetFlag"] = 1
                                        
                                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Kp_ToBeSet"] = float(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["CurrentQuadraturePIgains_Kp_ToBeSet"])
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_Ki_ToBeSet"] = float(self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict"]["CurrentQuadraturePIgains_Ki_ToBeSet"])
                                        self.IngeniaMotionController_MainDict[SlaveID_Int]["CurrentQuadraturePIgains_NeedsToBeSetFlag"] = 1

                                    if self.IngeniaMotionController_MainDict[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                                        pass
                            #######################################################

                            #######################################################
                            self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_ReubenPython2and3ClassObject"].GUI_update_clock()
                            #######################################################

                        #######################################################
                        #######################################################

                        ###################################################
                        #######################################################
                        self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last"] = self.IngeniaMotionController_GUIobjectsOnlyDict[SlaveID_Int]["EntryListWithBlinking_MostRecentDict_DataUpdateNumber"]
                        ###################################################
                        #######################################################

                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################
                    #######################################################
                    #######################################################

                    #######################################################
                    #######################################################
                    #######################################################
                    self.UpdateFrequencyCalculation_GUIthread_Filtered()
                    #######################################################
                    #######################################################
                    #######################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("IngeniaBLDC_ReubenPython3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                    traceback.print_exc()
                #######################################################
                #######################################################
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

        number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

        ListOfStringsToJoin = []

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if isinstance(input, str) == 1:
            ListOfStringsToJoin.append(input)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
            element = float(input)
            prefix_string = "{:." + str(number_of_decimal_places) + "f}"
            element_as_string = prefix_string.format(element)

            ##########################################################################################################
            ##########################################################################################################
            if element >= 0:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
                element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
            else:
                element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
            ##########################################################################################################
            ##########################################################################################################

            ListOfStringsToJoin.append(element_as_string)
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, list) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, tuple) == 1:

            if len(input) > 0:
                for element in input: #RECURSION
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a list() or []
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif isinstance(input, dict) == 1:

            if len(input) > 0:
                for Key in input: #RECURSION
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

            else: #Situation when we get a dict()
                ListOfStringsToJoin.append(str(input))

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        else:
            ListOfStringsToJoin.append(str(input))
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if len(ListOfStringsToJoin) > 1:

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            StringToReturn = ""
            for Index, StringToProcess in enumerate(ListOfStringsToJoin):

                ################################################
                if Index == 0: #The first element
                    if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                        StringToReturn = "{"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                        StringToReturn = "("
                    else:
                        StringToReturn = "["

                    StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
                ################################################

                ################################################
                elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                    StringToReturn = StringToReturn + StringToProcess + ", "
                ################################################

                ################################################
                else: #The last element
                    StringToReturn = StringToReturn + StringToProcess

                    if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                        StringToReturn = StringToReturn + "}"
                    elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                        StringToReturn = StringToReturn + ")"
                    else:
                        StringToReturn = StringToReturn + "]"

                ################################################

            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        elif len(ListOfStringsToJoin) == 1:
            StringToReturn = ListOfStringsToJoin[0]

        else:
            StringToReturn = ListOfStringsToJoin

        return StringToReturn
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        try:
            ProperlyFormattedStringForPrinting = ""
            ItemsPerLineCounter = 0

            for Key in DictToPrint:

                ##########################################################################################################
                if isinstance(DictToPrint[Key], dict): #RECURSION
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ":\n" + \
                                                         self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key],
                                                                                                              NumberOfDecimalsPlaceToUse,
                                                                                                              NumberOfEntriesPerLine,
                                                                                                              NumberOfTabsBetweenItems)

                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                         str(Key) + ": " + \
                                                         self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key],
                                                                                                                                               0,
                                                                                                                                               NumberOfDecimalsPlaceToUse)
                ##########################################################################################################

                ##########################################################################################################
                if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                    ItemsPerLineCounter = ItemsPerLineCounter + 1
                else:
                    ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                    ItemsPerLineCounter = 0
                ##########################################################################################################

            return ProperlyFormattedStringForPrinting

        except:
            exceptions = sys.exc_info()[0]
            print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
            return ""
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def sign(self, InputVal):

        ##########################################################################################################
        try:
            if InputVal >= 0.0:
                return 1.0
            else:
                return -1.0
        ##########################################################################################################

        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("sign, exceptions: %s" % exceptions)
            traceback.print_exc()
            #return 0.0
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
