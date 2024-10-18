# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Software Revision A, 10/17/2024

Verified working on: Python 3.12 for Windows 10, 11 64-bit and Raspberry Pi Buster (may work on Mac in non-GUI mode, but haven't tested yet).
'''

__author__ = 'reuben.brewer'

##########################################
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
import threading
import traceback
import subprocess
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
##########################################

##########################################
from ingeniamotion import MotionController #Installation folder: C:\Anaconda3\Lib\site-packages\ingeniamotion
from ingeniamotion.enums import OperationMode
##########################################

##########################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
##########################################

class IngeniaBLDC_ReubenPython3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, setup_dict): #Subclass the Tkinter Frame

        print("#################### IngeniaBLDC_ReubenPython3Class __init__ starting. ####################")

        #########################################################
        #########################################################

        self.PrintAllReceivedSerialMessageForDebuggingFlag = 0

        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.MotorConnectedFlag = 0

        self.DedicatedTxThread_TxMessageToSend_Queue = Queue.Queue()

        self.SerialNumber_Actual = -1
        self.VendorID_Actual = -1
        self.ProductCode_Actual = -1
        self.FWversion_Actual = -1

        self.STO_EstopPRESSEDValue = 0x4
        self.STO_EstopNOTpressedValue = 0x17

        self.STO_status = -1

        self.STO_status_last = -1

        self.Status_Word = -1

        self.Position_Actual = -11111.0
        self.Velocity_Actual = -11111.0
        self.Current_Direct_Actual = -11111.0
        self.Current_Quadrature_Actual = -11111.0

        self.EnabledState_ToBeSet = 0
        self.EnabledState_NeedsToBeSetFlag = 0

        self.EnabledState = 0
        self.EnabledState_Actual = -1

        #########################################################
        self.PositionPIDgains_Kp_Actual = -11111.0
        self.PositionPIDgains_Ki_Actual = -11111.0
        self.PositionPIDgains_Kd_Actual = -11111.0

        self.PositionPIDgains_Kp_ToBeSet = -11111.0
        self.PositionPIDgains_Ki_ToBeSet = -11111.0
        self.PositionPIDgains_Kd_ToBeSet = -11111.0

        self.PositionPIDgains_NeedsToBeSetFlag = 0
        #########################################################
        
        #########################################################
        self.VelocityPIDgains_Kp_Actual = -11111.0
        self.VelocityPIDgains_Ki_Actual = -11111.0
        self.VelocityPIDgains_Kd_Actual = -11111.0

        self.VelocityPIDgains_Kp_ToBeSet = -11111.0
        self.VelocityPIDgains_Ki_ToBeSet = -11111.0
        self.VelocityPIDgains_Kd_ToBeSet = -11111.0

        self.VelocityPIDgains_NeedsToBeSetFlag = 0
        #########################################################
        
        #########################################################
        self.MaxCurrent_Actual = -11111.0
        
        self.MaxCurrent_ToBeSet = -11111.0

        self.MaxCurrent_NeedsToBeSetFlag = 0
        #########################################################
        
        self.MostRecentDataDict = dict()

        self.Position_ToBeSet = 0.0
        self.Position_NeedsToBeSetFlag = 0

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.CurrentTime_CalculatedFromDedicatedTxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedTxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedTxThread_2 = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedTxThread = -11111.0

        self.LastTimeHeartbeatWasSent_CalculatedFromDedicatedTxThread = -11111.0

        self.CurrentTime_CalculatedFromDedicatedRxThread = -11111.0
        self.LastTime_CalculatedFromDedicatedRxThread = -11111.0
        self.StartingTime_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromDedicatedRxThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromDedicatedRxThread = -11111.0
        
        self.CurrentTime_CalculateMeasurementForceDerivative = -11111.0
        self.LastTime_CalculateMeasurementForceDerivative = -11111.0
        self.DataStreamingDeltaT_CalculateMeasurementForceDerivative = -11111.0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        '''
        self.ControlModes_AcceptableStringValuesList = [    VOLTAGE = 0x00
        CURRENT_AMPLIFIER = 0x01
        CURRENT = 0x02
        CYCLIC_CURRENT = 0x22
        VELOCITY = 0x03
        PROFILE_VELOCITY = 0x13
        CYCLIC_VELOCITY = 0x23
        POSITION = 0x04
        PROFILE_POSITION = 0x14 #WHAT'S DIFFERENCE BETWEEN PROFILE AND CYCLIC POSITION?
        CYCLIC_POSITION = 0x24
        PROFILE_POSITION_S_CURVE = 0x44
        INTERPOLATED_POSITION = 0xA4
        PVT = 0xB4
        HOMING = 0x113
        TORQUE = 0x05
        CYCLIC_TORQUE = 0x25]
        '''
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
            if "root" in self.GUIparametersDict:
                self.root = self.GUIparametersDict["root"]
            else:
                print("IngeniaBLDC_ReubenPython3Class __init__: ERROR, must pass in 'root'")
                return
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
        if "DesiredSerialNumber" in setup_dict:
            self.DesiredSerialNumber = setup_dict["DesiredSerialNumber"]

        else:
            self.DesiredSerialNumber = -1

        print("IngeniaBLDC_ReubenPython3Class __init__: DesiredSerialNumber: " + str(self.DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredSlaveID" in setup_dict:
            self.DesiredSlaveID = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DesiredSlaveID", setup_dict["DesiredSlaveID"], 1, 255))

        else:
            self.DesiredSlaveID = 1

        print("IngeniaBLDC_ReubenPython3Class __init__: DesiredSlaveID: " + str(self.DesiredSlaveID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "XDFfileDictionaryPath" in setup_dict:
            self.XDFfileDictionaryPath = str(setup_dict["XDFfileDictionaryPath"])

        else:
            print("IngeniaBLDC_ReubenPython3Class __init__: ERROR, must initialize object with 'XDFfileDictionaryPath' argument.")
            return

        print("IngeniaBLDC_ReubenPython3Class __init__: XDFfileDictionaryPath: " + str(self.XDFfileDictionaryPath))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath" in setup_dict:
            self.MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath = str(setup_dict["MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath"])

        else:
            print("IngeniaBLDC_ReubenPython3Class __init__: ERROR, must initialize object with 'MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath' argument.")
            return

        print("IngeniaBLDC_ReubenPython3Class __init__: MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath: " + str(self.MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath))
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

        #########################################################
        #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value
        self.LowPassFilterForDictsOfLists_ReubenPython2and3ClassObject_DictOfVariableFilterSettings = dict([("DataStreamingFrequency_CalculatedFromDedicatedTxThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)])),
                                                                                                             ("DataStreamingFrequency_CalculatedFromDedicatedRxThread", dict([("UseMedianFilterFlag", 1), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", 0.05)]))])

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

        ######################################################### unicorn WHY CANT WE USE THE MOTOR WITHOUT STARTING THE EoE service?
        #########################################################
        self.EoEserviceIsRunningFlag = self.StartEoEservice()
        print("self.EoEserviceIsRunningFlag: " + str(self.EoEserviceIsRunningFlag))

        if self.EoEserviceIsRunningFlag == 0:
            print("IngeniaBLDC_ReubenPython3Class __init__: Error, EoEservice isn't running, exiting now.")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            self.InitializeMotors()

            #########################################################
            if self.MotorConnectedFlag != 1:
                print("IngeniaBLDC_ReubenPython3Class __init__: InitializeMotors failed!")
                return
            #########################################################

        except:
            exceptions = sys.exc_info()[0]
            print("IngeniaBLDC_ReubenPython3Class __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
            return
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
        if self.USE_GUI_FLAG == 1:
            self.StartGUI(self.root)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        time.sleep(0.25)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __del__(self):
        pass
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
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a numerical value, Exceptions: %s" % exceptions)

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

                print("PassThrough0and1values_ExitProgramOtherwise Error. '" +
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
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

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
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)

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
                print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
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
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

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
    ##########################################################################################################
    def StartEoEservice(self):

        try:

            ##########################################################################################################
            ##########################################################################################################
            [PID_DictWithPIDasKey, PID_DictWithEXEenglishNameAsKey] = GetPIDsByProcessEnglishName("IngEcatGateway")
            print("$$$$$$$$$$$$ PID_DictWithPIDasKey: " + str(PID_DictWithPIDasKey) + ", PID_DictWithEXEenglishNameAsKey: " + str(PID_DictWithEXEenglishNameAsKey) + " $$$$$$$$$$$$")

            if len(PID_DictWithPIDasKey) == 0: #IngEcatGateway.exe isn't running

                ##########################################################################################################
                try:
                    print("@@@@@@@@@@@@@@@@@@@ StartEoEservice: launching IngEcatGateway.exe @@@@@@@@@@@@@@@@@@@")

                    #shell_command_to_issue = "\"" + os.getcwd() + "\\InstallFiles_and_SupportDocuments\\EoE_start.bat\" " + "\"" + self.MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath + "\""
                    #shell_command_to_issue = "\"" + self.MotionLab3_IngEcatGateway_EoEservice_EXEfullFilePath + "\""
                    shell_command_to_issue = "python \"G:\\My Drive\\CodeReuben\\ElevatePythonPermission_ReubenPython3Class\\test_program_for_ElevatePythonPermission_ReubenPython3Class.py\""

                    print("shell_command_to_issue: " + shell_command_to_issue)

                    #process = subprocess.Popen([shell_command_to_issue], shell=True)  # subprocess.Popen doesn't wait for process to terminate
                    time.sleep(2.0)

                    return 1

                except:
                    exceptions = sys.exc_info()[0]
                    print("StartEoEservice, subprocess.Popen failed to launch IngEcatGateway.exe, Exceptions: %s" % exceptions)
                    #return 0
                    traceback.print_exc()
                ##########################################################################################################

            else:
                ##########################################################################################################
                print("StartEoEservice: IngEcatGateway.exe is already running, no further action necessary.")
                return 1
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("StartEoEservice, exceptions: %s" % exceptions)
            return 0
            #traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def InitializeMotors(self):

        try:

            ################################################################################
            self.IngeniaMotionControllerObject = MotionController()

            InterfaceList = self.IngeniaMotionControllerObject.communication.get_interface_name_list()
            print("InterfaceList:")

            CorrectInterfaceIndex = -1
            for Index, Interface in enumerate(InterfaceList):
                print("Index: " + str(Index) + ", InterfaceName: " + str(Interface))

                if Interface == self.DesiredInterfaceName:
                    CorrectInterfaceIndex = Index
            ################################################################################

            ################################################################################
            if CorrectInterfaceIndex == -1:
                print("InitializeMotors: Could not locate CorrectInterfaceIndex = " + CorrectInterfaceIndex)
                return

            InterfaceSelected = self.IngeniaMotionControllerObject.communication.get_ifname_by_index(CorrectInterfaceIndex)
            print("InterfaceSelected:")
            print("Interface index: " + str(CorrectInterfaceIndex))
            print("Interface identifier: " + str(InterfaceSelected))
            print("Interface name: " + str(InterfaceList[CorrectInterfaceIndex]))

            SlaveID_List = self.IngeniaMotionControllerObject.communication.scan_servos_ethercat(InterfaceSelected)

            print("Found " + str(len(SlaveID_List)) + " slaves: " + str(SlaveID_List))
            ################################################################################

            ################################################################################
            self.IngeniaMotionControllerObject.communication.connect_servo_ethercat(InterfaceSelected, self.DesiredSlaveID, self.XDFfileDictionaryPath)
            print("Drive is connected.")
            ################################################################################

            ################################################################################
            self.SerialNumber_Actual = self.IngeniaMotionControllerObject.configuration.get_serial_number()
            print("SerialNumber_Actual: " + str(self.SerialNumber_Actual))

            self.VendorID_Actual = self.IngeniaMotionControllerObject.configuration.get_vendor_id()
            print("VendorID_Actual: " + str(self.VendorID_Actual))

            self.ProductCode_Actual = self.IngeniaMotionControllerObject.configuration.get_product_code()
            print("ProductCode_Actual: " + str(self.ProductCode_Actual))

            self.FWversion_Actual = self.IngeniaMotionControllerObject.configuration.get_fw_version()
            print("FWversion_Actual: " + str(self.FWversion_Actual))
            ################################################################################

            ################################################################################ In the future, pass these into the class via setup_dict.
            max_velocity = 100000000.0
            max_acceleration_deceleration = 20000.0

            self.IngeniaMotionControllerObject.configuration.set_max_velocity(max_velocity)
            self.IngeniaMotionControllerObject.configuration.set_max_profile_velocity(max_velocity)

            #self.IngeniaMotionControllerObject.configuration.set_max_acceleration(max_acceleration_deceleration) #deprecated
            self.IngeniaMotionControllerObject.configuration.set_max_profile_acceleration(max_acceleration_deceleration)
            self.IngeniaMotionControllerObject.configuration.set_max_profile_deceleration(max_acceleration_deceleration)
            ################################################################################

            ################################################################################
            self.MotorConnectedFlag = 1
            ################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("InitializeMotors, exceptions: %s" % exceptions)
            self.MotorConnectedFlag = 0
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetPosition(self, PositionTarget, PrintDebugFlag = 0):
        try:

            if self.MotorConnectedFlag == 1:
                self.IngeniaMotionControllerObject.motion.move_to_position(int(PositionTarget))  # , blocking=False, timeout=2.0

                if PrintDebugFlag == 1:
                    print("__SetPosition event fired for PositionTarget = " + str(PositionTarget))

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPosition, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPosition_ExternalProgram(self, PositionTarget):
        try:

            self.Position_ToBeSet = PositionTarget
            self.Position_NeedsToBeSetFlag = 1

        except:
            exceptions = sys.exc_info()[0]
            print("SetPosition_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetEnabledState(self, EnabledState, PrintDebugFlag = 0):
        try:
            if self.MotorConnectedFlag == 1:
                if EnabledState in [0, 1]:
                    
                    if EnabledState == 0:
                        self.IngeniaMotionControllerObject.motion.motor_disable()
                        
                    if EnabledState == 1:
                        self.IngeniaMotionControllerObject.motion.motor_enable()
                        
                    self.EnabledState = EnabledState

                    if PrintDebugFlag == 1:
                        print("__SetEnabledState event fired for EnabledState = " + str(EnabledState))
                    
                else:
                    print("__SetEnabledState: Error, EnabledState must be 0 or 1.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetEnabledState, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEnabledState_ExternalProgram(self, EnabledStateTarget, PrintDebugFlag = 0):
        try:

            self.EnabledState_ToBeSet = EnabledStateTarget
            self.EnabledState_NeedsToBeSetFlag = 1

            if PrintDebugFlag == 1:
                print("SetEnabledState_ExternalProgram event fire for EnabledStateTarget = " + str(EnabledStateTarget))

        except:
            exceptions = sys.exc_info()[0]
            print("SetEnabledState_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetPositionPIDgains(self, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag=0):
        try:
            if self.MotorConnectedFlag == 1:

                self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KP", Kp_ToBeSet)
                self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KI", Ki_ToBeSet)
                self.IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KD", Kd_ToBeSet)

                time.sleep(0.001)

                self.__GetPositionPIDgains()

                if PrintDebugFlag == 1:
                    print("__SetPositionPIDgains event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetPositionPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPositionPIDgains_ExternalProgram(self, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag = 0):
        try:

            self.PositionPIDgains_Kp_ToBeSet = Kp_ToBeSet
            self.PositionPIDgains_Ki_ToBeSet = Ki_ToBeSet
            self.PositionPIDgains_Kd_ToBeSet = Kd_ToBeSet

            self.PositionPIDgains_NeedsToBeSetFlag = 1

            if PrintDebugFlag == 1:
                print("SetPositionPIDgains_ExternalProgram event fired!")

        except:
            exceptions = sys.exc_info()[0]
            print("SetPositionPIDgains_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetPositionPIDgains(self, PrintDebugFlag=0):
        try:
            if self.MotorConnectedFlag == 1:

                self.PositionPIDgains_Kp_Actual = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KP")
                self.PositionPIDgains_Ki_Actual = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KI")
                self.PositionPIDgains_Kd_Actual = self.IngeniaMotionControllerObject.communication.get_register("CL_POS_PID_KD")

                if PrintDebugFlag == 1:
                    print("__GetPositionPIDgains event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("__GetPositionPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    
    ##########################################################################################################
    ##########################################################################################################
    def __SetVelocityPIDgains(self, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag=0):
        try:
            if self.MotorConnectedFlag == 1:

                self.IngeniaMotionControllerObject.communication.set_register("CL_POS_VEL_KP", Kp_ToBeSet)
                self.IngeniaMotionControllerObject.communication.set_register("CL_POS_VEL_KI", Ki_ToBeSet)
                self.IngeniaMotionControllerObject.communication.set_register("CL_POS_VEL_KD", Kd_ToBeSet)

                time.sleep(0.001)

                self.__GetVelocityPIDgains()

                if PrintDebugFlag == 1:
                    print("__SetVelocityPIDgains event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetVelocityPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################
    
    ###########################################################################################################
    ##########################################################################################################
    def SetVelocityPIDgains_ExternalProgram(self, Kp_ToBeSet, Ki_ToBeSet, Kd_ToBeSet, PrintDebugFlag = 0):
        try:

            self.VelocityPIDgains_Kp_ToBeSet = Kp_ToBeSet
            self.VelocityPIDgains_Ki_ToBeSet = Ki_ToBeSet
            self.VelocityPIDgains_Kd_ToBeSet = Kd_ToBeSet

            self.VelocityPIDgains_NeedsToBeSetFlag = 1

            if PrintDebugFlag == 1:
                print("SetVelocityPIDgains_ExternalProgram event fired!")

        except:
            exceptions = sys.exc_info()[0]
            print("SetVelocityPIDgains_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetVelocityPIDgains(self, PrintDebugFlag=0):
        try:
            if self.MotorConnectedFlag == 1:

                self.VelocityPIDgains_Kp_Actual = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_PID_KP")
                self.VelocityPIDgains_Ki_Actual = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_PID_KI")
                self.VelocityPIDgains_Kd_Actual = self.IngeniaMotionControllerObject.communication.get_register("CL_VEL_PID_KD")

                if PrintDebugFlag == 1:
                    print("__GetVelocityPIDgains event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("__GetVelocityPIDgains, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __SetMaxCurrent(self, MaxCurrent_ToBeSet, PrintDebugFlag=0):
        try:
            if self.MotorConnectedFlag == 1:

                self.IngeniaMotionControllerObject.communication.set_register("CL_CUR_REF_MAX", MaxCurrent_ToBeSet) #MAX_CURRENT_REGISTER = "CL_CUR_REF_MAX"

                time.sleep(0.001)

                self.__GetMaxCurrent()

                if PrintDebugFlag == 1:
                    print("__SetMaxCurrent event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("__SetMaxCurrent, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetMaxCurrent_ExternalProgram(self, MaxCurrent_ToBeSet, PrintDebugFlag = 0):
        try:

            self.MaxCurrent_ToBeSet = MaxCurrent_ToBeSet
            
            self.MaxCurrent_NeedsToBeSetFlag = 1

            if PrintDebugFlag == 1:
                print("SetMaxCurrent_ExternalProgram event fired!")

        except:
            exceptions = sys.exc_info()[0]
            print("SetMaxCurrent_ExternalProgram, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def __GetMaxCurrent(self, PrintDebugFlag=0):
        try:
            if self.MotorConnectedFlag == 1:

                self.MaxCurrent_Actual = self.IngeniaMotionControllerObject.configuration.get_max_current()

                if PrintDebugFlag == 1:
                    print("__GetMaxCurrent event fired.")

        except:
            exceptions = sys.exc_info()[0]
            print("__GetMaxCurrent, exceptions: %s" % exceptions)
            traceback.print_exc()

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def DedicatedTxThread(self):

        self.MyPrint_WithoutLogFile("Started DedicatedTxThread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedTxThread_StillRunningFlag = 1

        if self.EnableMotorAtStartOfProgramFlag == 1:
            self.SetEnabledState_ExternalProgram(1, PrintDebugFlag=0)
        else:
            self.SetEnabledState_ExternalProgram(0, PrintDebugFlag=0)

        self.StartingTime_CalculatedFromDedicatedTxThread = self.getPreciseSecondsTimeStampString()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        while self.EXIT_PROGRAM_FLAG == 0:

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
            try:

                ##########################################################################################################
                ##########################################################################################################
                if self.MotorConnectedFlag == 1:

                    ##########################################################################################################
                    if self.EnableMotorAutomaticallyAfterEstopRestorationFlag == 1:
                        if self.STO_status != self.STO_status_last and self.STO_status_last == self.STO_EstopPRESSEDValue:
                            print("STO fault was cleared, re-enabling motor.")
                            self.SetEnabledState_ExternalProgram(1, PrintDebugFlag=0)
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.EnabledState_NeedsToBeSetFlag == 1:
                        self.__SetEnabledState(self.EnabledState_ToBeSet, PrintDebugFlag=1)
                        self.EnabledState_NeedsToBeSetFlag = 0
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.PositionPIDgains_NeedsToBeSetFlag == 1:
                        self.__SetPositionPIDgains(self.PositionPIDgains_Kp_ToBeSet, self.PositionPIDgains_Ki_ToBeSet, self.PositionPIDgains_Kd_ToBeSet, PrintDebugFlag=1)
                        self.PositionPIDgains_NeedsToBeSetFlag = 0
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.VelocityPIDgains_NeedsToBeSetFlag == 1:
                        self.__SetVelocityPIDgains(self.VelocityPIDgains_Kp_ToBeSet, self.VelocityPIDgains_Ki_ToBeSet, self.VelocityPIDgains_Kd_ToBeSet, PrintDebugFlag=1)
                        self.VelocityPIDgains_NeedsToBeSetFlag = 0
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.MaxCurrent_NeedsToBeSetFlag == 1:
                        self.__SetMaxCurrent(self.MaxCurrent_ToBeSet, PrintDebugFlag=1)
                        self.MaxCurrent_NeedsToBeSetFlag = 0
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.EnabledState_Actual == 1:
                        if self.Position_NeedsToBeSetFlag == 1:
                            self.__SetPosition(self.Position_ToBeSet, PrintDebugFlag=0)
                            self.Position_NeedsToBeSetFlag = 0
                    ##########################################################################################################

                    #IngeniaMotionControllerObject.motion.set_voltage_direct() #PWM control
                    #IngeniaMotionControllerObject.motion.set_velocity() #velocity control
                    #IngeniaMotionControllerObject.motion.set_current_quadrature(current) #torque control, don't use set_current_direct()

                    ##########################################################################################################
                    self.UpdateFrequencyCalculation_DedicatedTxThread_Filtered()
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

            except:
                exceptions = sys.exc_info()[0]
                print("DedicatedTxThread, exceptions: %s" % exceptions)
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
        try:
            self.IngeniaMotionControllerObject.motion.motor_disable()
            self.IngeniaMotionControllerObject.communication.disconnect()
        except:
            pass
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

    ########################################################################################################## unicorn
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
        while self.EXIT_PROGRAM_FLAG == 0:

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
            try:

                ##########################################################################################################
                ##########################################################################################################
                if self.MotorConnectedFlag == 1:

                    ##########################################################################################################
                    #self.STO_status = self.IngeniaMotionControllerObject.configuration.get_sto_status()
                    #self.Status_Word = self.IngeniaMotionControllerObject.configuration.get_status_word()
                    self.Position_Actual = self.IngeniaMotionControllerObject.motion.get_actual_position()
                    self.Velocity_Actual = self.IngeniaMotionControllerObject.motion.get_actual_velocity()
                    self.Current_Direct_Actual = self.IngeniaMotionControllerObject.motion.get_actual_current_direct()
                    self.Current_Quadrature_Actual = self.IngeniaMotionControllerObject.motion.get_actual_current_quadrature()
                    self.EnabledState_Actual = self.IngeniaMotionControllerObject.configuration.is_motor_enabled()

                    '''
                    #self.IngeniaMotionControllerObject.configuration.is_sto1_active()
                    #self.IngeniaMotionControllerObject.configuration.is_motor_enabled()
                    #self.IngeniaMotionControllerObject.configuration.load_configuration()
                    '''
                    ##########################################################################################################

                    ##########################################################################################################
                    self.STO_status_last = self.STO_status
                    ##########################################################################################################

                    ##########################################################################################################
                    self.UpdateFrequencyCalculation_DedicatedRxThread_Filtered()
                    ##########################################################################################################

                    ##########################################################################################################
                    self.MostRecentDataDict["Time"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                    self.MostRecentDataDict["CurrentTime_CalculatedFromDedicatedTxThread"] = self.CurrentTime_CalculatedFromDedicatedTxThread
                    self.MostRecentDataDict["CurrentTime_CalculatedFromDedicatedRxThread"] = self.CurrentTime_CalculatedFromDedicatedRxThread
                    self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedTxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedTxThread
                    self.MostRecentDataDict["DataStreamingFrequency_CalculatedFromDedicatedRxThread"] = self.DataStreamingFrequency_CalculatedFromDedicatedRxThread

                    self.MostRecentDataDict["STO_status"] = self.STO_status
                    self.MostRecentDataDict["Status_Word"] = self.Status_Word
                    self.MostRecentDataDict["Position_Actual"] = self.Position_Actual
                    self.MostRecentDataDict["Velocity_Actual"] = self.Velocity_Actual
                    self.MostRecentDataDict["Current_Direct_Actual"] = self.Current_Direct_Actual
                    self.MostRecentDataDict["Current_Quadrature_Actual"] = self.Current_Quadrature_Actual
                    self.MostRecentDataDict["EnabledState_Actual"] = self.EnabledState_Actual

                    self.MostRecentDataDict["SerialNumber_Actual"] = self.SerialNumber_Actual
                    self.MostRecentDataDict["VendorID_Actual"] = self.VendorID_Actual
                    self.MostRecentDataDict["ProductCode_Actual"] = self.ProductCode_Actual
                    self.MostRecentDataDict["FWversion_Actual"] = self.FWversion_Actual

                    self.MostRecentDataDict["PositionPIDgains_Kp_Actual"] = self.PositionPIDgains_Kp_Actual
                    self.MostRecentDataDict["PositionPIDgains_Ki_Actual"] = self.PositionPIDgains_Ki_Actual
                    self.MostRecentDataDict["PositionPIDgains_Kd_Actual"] = self.PositionPIDgains_Kd_Actual
                    
                    self.MostRecentDataDict["VelocityPIDgains_Kp_Actual"] = self.VelocityPIDgains_Kp_Actual
                    self.MostRecentDataDict["VelocityPIDgains_Ki_Actual"] = self.VelocityPIDgains_Ki_Actual
                    self.MostRecentDataDict["VelocityPIDgains_Kd_Actual"] = self.VelocityPIDgains_Kd_Actual

                    self.MostRecentDataDict["MaxCurrent_Actual"] = self.MaxCurrent_Actual
                    ##########################################################################################################

                    ##########################################################################################################
                    if self.DedicatedRxThread_TimeToSleepEachLoop > 0.0:
                        if self.DedicatedRxThread_TimeToSleepEachLoop > 0.001:
                            time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                        else:
                            time.sleep(self.DedicatedRxThread_TimeToSleepEachLoop)
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

        self.MyPrint_WithoutLogFile("Finished DedicatedRxThread for IngeniaBLDC_ReubenPython3Class object.")
        self.DedicatedRxThread_StillRunningFlag = 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
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
    def StartGUI(self, GuiParent):

        self.GUI_Thread(GuiParent)
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_Thread(self, parent):

        print("Starting the GUI_Thread for IngeniaBLDC_ReubenPython3Class object.")

        #################################################
        #################################################
        self.root = parent
        self.parent = parent
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
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
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
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=50)

        self.DeviceInfo_Label["text"] = (self.NameToDisplay_UserSet + \
                                        "\nSerialNumber_Actual: " + str(self.SerialNumber_Actual) + \
                                        "\nVendorID_Actual: " + str(self.VendorID_Actual) + \
                                        "\nProductCode_Actual: " + str(self.ProductCode_Actual) + \
                                        "\nFWversion_Actual: " + str(self.FWversion_Actual))

        self.DeviceInfo_Label.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.Data_Label = Label(self.myFrame, text="Data_Label", width=120)
        self.Data_Label.grid(row=0, column=1, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.ButtonsFrame = Frame(self.myFrame)
        self.ButtonsFrame.grid(row = 1, column = 0, padx = self.GUI_PADX, pady = self.GUI_PADY, rowspan = 1, columnspan = 2)
        #################################################
        #################################################

        #################################################
        #################################################
        self.EnabledState_Button = Button(self.ButtonsFrame, text="EnabledState_Button", state="normal", width=20, bg=self.TKinter_LightYellowColor, command=lambda: self.EnabledState_Button_Response())
        self.EnabledState_Button.grid(row=0, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=self.GUI_PADX, pady=self.GUI_PADY, columnspan=10, rowspan=10)
        #################################################
        #################################################

        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def EnabledState_Button_Response(self):

        if self.EnabledState == 1:
            self.EnabledState_ToBeSet = 0
        else:
            self.EnabledState_ToBeSet = 1

        self.EnabledState_NeedsToBeSetFlag = 1

        self.MyPrint_WithoutLogFile("EnabledState_Button_Response: Event fired!")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:

                    #######################################################
                    self.Data_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                    NumberOfDecimalsPlaceToUse = 5,
                                                                                                    NumberOfEntriesPerLine = 1,
                                                                                                    NumberOfTabsBetweenItems = 3)
                    #######################################################

                    #######################################################
                    if self.EnabledState_Actual == 1:
                        self.EnabledState_Button["bg"] = self.TKinter_LightGreenColor

                    elif self.EnabledState_Actual == 0:
                        self.EnabledState_Button["bg"] = self.TKinter_LightRedColor

                    else:
                        self.EnabledState_Button["bg"] = self.TKinter_LightYellowColor
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
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

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     Key + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
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
    ##########################################################################################################
    ##########################################################################################################
