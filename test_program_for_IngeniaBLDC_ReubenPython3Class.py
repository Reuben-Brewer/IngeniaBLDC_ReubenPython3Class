# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision I, 03/28/2025

Verified working on: Python 3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################
from CSVdataLogger_ReubenPython3Class import *
from ElevatePythonPermission_ReubenPython3Class import *
from EntryListWithBlinking_ReubenPython2and3Class import *
from IngeniaBLDC_ReubenPython3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
##########################################

##########################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
import keyboard
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

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0

        return ProperlyFormattedStringForPrinting

    except:
        exceptions = sys.exc_info()[0]
        print("ConvertDictToProperlyFormattedStringForPrinting, Exceptions: %s" % exceptions)
        return ""
        # traceback.print_exc()
#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global LoopCounter_CalculatedFromGUIthread
    global CurrentTime_CalculatedFromGUIthread
    global StartingTime_CalculatedFromGUIthread
    global LastTime_CalculatedFromGUIthread
    global DataStreamingFrequency_CalculatedFromGUIthread
    global DataStreamingDeltaT_CalculatedFromGUIthread

    global IngeniaBLDC_Object
    global IngeniaBLDC_OPEN_FLAG
    global SHOW_IN_GUI_IngeniaBLDC_FLAG
    global IngeniaBLDC_MostRecentDict
    global IngeniaBLDC_MostRecentDict_Label

    global EntryListWithBlinking_ReubenPython2and3ClassObject
    global EntryListWithBlinking_OPEN_FLAG

    global CSVdataLogger_ReubenPython3ClassObject
    global CSVdataLogger_OPEN_FLAG
    global SHOW_IN_GUI_CSVdataLogger_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################
        #########################################################

            #########################################################
            #########################################################
            try:
                #########################################################
                CurrentTime_CalculatedFromGUIthread = getPreciseSecondsTimeStampString() - StartingTime_CalculatedFromGUIthread
                [LoopCounter_CalculatedFromGUIthread, LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread, DataStreamingDeltaT_CalculatedFromGUIthread] = UpdateFrequencyCalculation(LoopCounter_CalculatedFromGUIthread, CurrentTime_CalculatedFromGUIthread,
                                                                                                                                                                                                                  LastTime_CalculatedFromGUIthread, DataStreamingFrequency_CalculatedFromGUIthread,
                                                                                                                                                                                                                  DataStreamingDeltaT_CalculatedFromGUIthread)
                #########################################################

                #########################################################
                IngeniaBLDC_MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(IngeniaBLDC_MostRecentDict, NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=3, NumberOfTabsBetweenItems=1)
                #########################################################

                #########################################################
                if IngeniaBLDC_OPEN_FLAG == 1 and SHOW_IN_GUI_IngeniaBLDC_FLAG == 1:
                    IngeniaBLDC_Object.GUI_update_clock()
                #########################################################

                #########################################################
                if EntryListWithBlinking_OPEN_FLAG == 1:
                    EntryListWithBlinking_ReubenPython2and3ClassObject.GUI_update_clock()
                #########################################################

                #########################################################
                if CSVdataLogger_OPEN_FLAG == 1 and SHOW_IN_GUI_CSVdataLogger_FLAG == 1:
                    CSVdataLogger_ReubenPython3ClassObject.GUI_update_clock()
                #########################################################

                #########################################################
                if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                    MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
                #########################################################

                #########################################################
                root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
                #########################################################

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            except:
                exceptions = sys.exc_info()[0]
                print("GUI_update_clock(), Exceptions: %s" % exceptions)
                traceback.print_exc()
            #########################################################
            #########################################################

        #########################################################
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def UpdateFrequencyCalculation(LoopCounter, CurrentTime, LastTime, DataStreamingFrequency, DataStreamingDeltaT):

    try:

        DataStreamingDeltaT = CurrentTime - LastTime

        ##########################
        if DataStreamingDeltaT != 0.0:
            DataStreamingFrequency = 1.0/DataStreamingDeltaT
        ##########################

        LastTime = CurrentTime

        LoopCounter = LoopCounter + 1

        return [LoopCounter, LastTime, DataStreamingFrequency, DataStreamingDeltaT]

    except:
        exceptions = sys.exc_info()[0]
        print("UpdateFrequencyCalculation, exceptions: %s" % exceptions)
        return [-11111.0]*4
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_IngeniaBLDC
    global Tab_MyPrint
    global Tab_CSVdataLogger

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_IngeniaBLDC = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_IngeniaBLDC, text='   IngeniaBLDC   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        Tab_CSVdataLogger = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_CSVdataLogger, text='   CSVdataLogger   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_IngeniaBLDC = root
        Tab_MyPrint = root
        Tab_CSVdataLogger = root
        #################################################

    ##########################################################################################################

    #################################################
    #################################################
    global IngeniaBLDC_MostRecentDict_Label
    IngeniaBLDC_MostRecentDict_Label = Label(Tab_MainControls, text="IngeniaBLDC_MostRecentDict_Label", width=120, font=("Helvetica", 10))
    IngeniaBLDC_MostRecentDict_Label.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ButtonsFrame
    ButtonsFrame = Frame(Tab_MainControls)
    ButtonsFrame.grid(row = 0, column = 0, padx = 10, pady = 10, rowspan = 1, columnspan = 1)
    #################################################
    #################################################

    #################################################
    #################################################
    global ZeroEncoderOffsetOnAllMotors_Button
    ZeroEncoderOffsetOnAllMotors_Button = Button(ButtonsFrame, text="Toggle Enable", state="normal", width=20, command=lambda: ZeroEncoderOffsetOnAllMotors_Button_Response())
    ZeroEncoderOffsetOnAllMotors_Button.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
    #################################################
    #################################################

    ##########################################################################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_IngeniaBLDC_ReubenPython3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ZeroEncoderOffsetOnAllMotors_Button_Response():
    global ZeroEncoderOffsetOnAllMotors_EventNeedsToBeFiredFlag

    ZeroEncoderOffsetOnAllMotors_EventNeedsToBeFiredFlag = 1

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    #ElevatePythonPermission_ReubenPython3Class.RunPythonAsAdmin()
    #time.sleep(5.0)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_IngeniaBLDC_FLAG
    USE_IngeniaBLDC_FLAG = 1

    global USE_EntryListWithBlinking_FLAG
    USE_EntryListWithBlinking_FLAG = 0

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 0

    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1 #unicorn

    global USE_CSVdataLogger_FLAG
    USE_CSVdataLogger_FLAG = 1

    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1

    global USE_SINUSOIDAL_INPUT_FLAG
    USE_SINUSOIDAL_INPUT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_IngeniaBLDC_FLAG
    SHOW_IN_GUI_IngeniaBLDC_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1

    global SHOW_IN_GUI_CSVdataLogger_FLAG
    SHOW_IN_GUI_CSVdataLogger_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_IngeniaBLDC
    global GUI_COLUMN_IngeniaBLDC
    global GUI_PADX_IngeniaBLDC
    global GUI_PADY_IngeniaBLDC
    global GUI_ROWSPAN_IngeniaBLDC
    global GUI_COLUMNSPAN_IngeniaBLDC
    GUI_ROW_IngeniaBLDC = 0

    GUI_COLUMN_IngeniaBLDC = 0
    GUI_PADX_IngeniaBLDC = 1
    GUI_PADY_IngeniaBLDC = 1
    GUI_ROWSPAN_IngeniaBLDC = 1
    GUI_COLUMNSPAN_IngeniaBLDC = 2

    global GUI_ROW_EntryListWithBlinking
    global GUI_COLUMN_EntryListWithBlinking
    global GUI_PADX_EntryListWithBlinking
    global GUI_PADY_EntryListWithBlinking
    global GUI_ROWSPAN_EntryListWithBlinking
    global GUI_COLUMNSPAN_EntryListWithBlinking
    GUI_ROW_EntryListWithBlinking = 1

    GUI_COLUMN_EntryListWithBlinking = 0
    GUI_PADX_EntryListWithBlinking = 1
    GUI_PADY_EntryListWithBlinking = 1
    GUI_ROWSPAN_EntryListWithBlinking = 1
    GUI_COLUMNSPAN_EntryListWithBlinking = 1

    global GUI_ROW_CSVdataLogger
    global GUI_COLUMN_CSVdataLogger
    global GUI_PADX_CSVdataLogger
    global GUI_PADY_CSVdataLogger
    global GUI_ROWSPAN_CSVdataLogger
    global GUI_COLUMNSPAN_CSVdataLogger
    GUI_ROW_CSVdataLogger = 2

    GUI_COLUMN_CSVdataLogger = 0
    GUI_PADX_CSVdataLogger = 1
    GUI_PADY_CSVdataLogger = 1
    GUI_ROWSPAN_CSVdataLogger = 1
    GUI_COLUMNSPAN_CSVdataLogger = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 3

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 1
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    #################################################
    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0
    #################################################

    #################################################
    global LoopCounter_CalculatedFromGUIthread
    LoopCounter_CalculatedFromGUIthread = 0

    global CurrentTime_CalculatedFromGUIthread
    CurrentTime_CalculatedFromGUIthread = -11111.0

    global StartingTime_CalculatedFromGUIthread
    StartingTime_CalculatedFromGUIthread = -11111.0

    global LastTime_CalculatedFromGUIthread
    LastTime_CalculatedFromGUIthread = -11111.0

    global DataStreamingFrequency_CalculatedFromGUIthread
    DataStreamingFrequency_CalculatedFromGUIthread = -1

    global DataStreamingDeltaT_CalculatedFromGUIthread
    DataStreamingDeltaT_CalculatedFromGUIthread = -1
    #################################################

    global root

    global root_Xpos
    root_Xpos = 870

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1600

    global root_height
    root_height = 1200

    global TabControlObject
    global Tab_MainControls
    global Tab_IngeniaBLDC
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 5
    
    global ZeroEncoderOffsetOnAllMotors_EventNeedsToBeFiredFlag
    ZeroEncoderOffsetOnAllMotors_EventNeedsToBeFiredFlag = 0

    #''' #CyclicPosition
    global SinusoidalMotionInput_MinValue
    SinusoidalMotionInput_MinValue = -360.0 #degrees

    global SinusoidalMotionInput_MaxValue
    SinusoidalMotionInput_MaxValue = 360.0 #degrees
    #''' #CyclicPosition

    ''' #CyclicCurrent
    global SinusoidalMotionInput_MinValue
    SinusoidalMotionInput_MinValue = -0.9

    global SinusoidalMotionInput_MaxValue
    SinusoidalMotionInput_MaxValue = 0.9
    ''' #CyclicCurrent

    ''' #CyclicVoltage
    global SinusoidalMotionInput_MinValue
    SinusoidalMotionInput_MinValue = -0.5

    global SinusoidalMotionInput_MaxValue
    SinusoidalMotionInput_MaxValue = 0.5
    ''' #CyclicVoltage

    global SinusoidalMotionInput_ROMtestTimeToPeakAngle
    SinusoidalMotionInput_ROMtestTimeToPeakAngle = 2.0

    global SinusoidalMotionInput_TimeGain
    SinusoidalMotionInput_TimeGain = math.pi / (2.0 * SinusoidalMotionInput_ROMtestTimeToPeakAngle)

    global SinusoidalMotionInput_CommandedValue
    SinusoidalMotionInput_CommandedValue = 0.0

    global DesiredSlaves_DictOfDicts
    '''
    DesiredSlaves_DictOfDicts = dict([(3, dict([("JointEnglishName", "Motor_3"),
                                                ("SlaveID_Int", 3),
                                                
                                                ("AllowWritingOfControllerConfigurationFlag", 1),
                                                                                                
                                                ("XDFfileDictionaryPath", os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"),

                                                ("OperationMode", "CyclicPosition"),

                                                ("ZeroEncoder_FireEventOnStartupFlag", 1),

                                                ("Position_Max_Rev", 0.0),
                                                ("Position_Min_Rev", 0.0),

                                                ("MaxCurrentHardLimit_ToBeSet", 10.00),
                                                ("MaxContinuousCurrent_ToBeSet", 4.24),
                                                ("PeakCurrentValue_ToBeSet", 8.48),
                                                ("PeakCurrentTimeMilliseconds_ToBeSet", 400),
                                                ("PeakCurrentFaultModeInt_ToBeSet", 0),

                                                ("PositionFollowingErrorWindow_ToBeSet", 10000000),
                                                ("PositionFollowingErrorTimeoutMilliseconds_ToBeSet", 2),
                                                ("PositionFollowingErrorFaultModeInt_ToBeSet", 0),

                                                ("MaxVelocity_ToBeSet", 3.0),
                                                ("MaxProfileVelocity_ToBeSet", 3.0),
                                                ("MaxProfileAcceleration_ToBeSet", 30.0),

                                                ("EncoderTicksPerRevolution_ToBeSet", 5000.0), #unicorn

                                                ("PositionPIDgains_Kp_ToBeSet", 0.1),
                                                ("PositionPIDgains_Ki_ToBeSet", 0.0),
                                                ("PositionPIDgains_Kd_ToBeSet", 0.0),

                                                ("CurrentQuadraturePIgains_Kp_ToBeSet", 1.8),
                                                ("CurrentQuadraturePIgains_Ki_ToBeSet", 2500.0)])),

                                      (1, dict([("JointEnglishName", "Motor_1"), ("SlaveID_Int", 1), ("AllowWritingOfControllerConfigurationFlag", 0), ("XDFfileDictionaryPath", os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"), ("OperationMode", "CyclicPosition"), ("ZeroEncoder_FireEventOnStartupFlag", 1), ("Position_Max_Rev", 0.0), ("Position_Min_Rev", 0.0), ("MaxCurrentHardLimit_ToBeSet", 4.21), ("MaxProfileVelocity_ToBeSet", 50000), ("MaxProfileAcceleration_ToBeSet", 100000), ("EncoderTicksPerRevolution_ToBeSet", 8192.0), ("PositionPIDgains_Kp_ToBeSet", 0.01), ("PositionPIDgains_Ki_ToBeSet", 0.2), ("PositionPIDgains_Kd_ToBeSet", 0.1)]))])
                                      #(3, dict([("JointEnglishName", "Motor_3"), ("SlaveID_Int", 3), ("AllowWritingOfControllerConfigurationFlag", 0), ("XDFfileDictionaryPath", os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"), ("OperationMode", "CyclicPosition"), ("ZeroEncoder_FireEventOnStartupFlag", 1), ("Position_Max_Rev", 0.0), ("Position_Min_Rev", 0.0), ("MaxCurrentHardLimit_ToBeSet", 4.21), ("MaxProfileVelocity_ToBeSet", 50000), ("MaxProfileAcceleration_ToBeSet", 100000), ("EncoderTicksPerRevolution_ToBeSet", 8192.0), ("PositionPIDgains_Kp_ToBeSet", 0.01), ("PositionPIDgains_Ki_ToBeSet", 0.2), ("PositionPIDgains_Kd_ToBeSet", 0.1)])),
                                      #(4, dict([("JointEnglishName", "Motor_4"), ("SlaveID_Int", 4), ("AllowWritingOfControllerConfigurationFlag", 0), ("XDFfileDictionaryPath", os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"), ("OperationMode", "CyclicPosition"), ("ZeroEncoder_FireEventOnStartupFlag", 1), ("Position_Max_Rev", 0.0), ("Position_Min_EncoderTicks", 0.0), ("MaxCurrentHardLimit_ToBeSet", 4.21), ("MaxProfileVelocity_ToBeSet", 50000), ("MaxProfileAcceleration_ToBeSet", 100000), ("EncoderTicksPerRevolution_ToBeSet", 8192.0), ("PositionPIDgains_Kp_ToBeSet", 0.01), ("PositionPIDgains_Ki_ToBeSet", 0.2), ("PositionPIDgains_Kd_ToBeSet", 0.1)])),
                                      #(5, dict([("JointEnglishName", "Motor_5"), ("SlaveID_Int", 5), ("AllowWritingOfControllerConfigurationFlag", 0), ("XDFfileDictionaryPath", os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "den-xcr-e_eoe_2.5.0.xdf"), ("OperationMode", "CyclicPosition"), ("ZeroEncoder_FireEventOnStartupFlag", 1), ("Position_Max_EncoderTicks", 10000.00), ("Position_Min_EncoderTicks", -10000.00), ("MaxCurrentHardLimit_ToBeSet", 3.5), ("MaxProfileVelocity_ToBeSet", 50000), ("MaxProfileAcceleration_ToBeSet", 100000), ("EncoderTicksPerRevolution_ToBeSet", 8192.0), ("PositionPIDgains_Kp_ToBeSet", 0.0055), ("PositionPIDgains_Ki_ToBeSet", 0.015), ("PositionPIDgains_Kd_ToBeSet", 0.0055)]))])
    '''

    #'''
    DesiredSlaves_DictOfDicts = dict([(1, dict([("JointEnglishName", "Motor_1"),
                                                ("SlaveID_Int", 1),

                                                ("AllowWritingOfControllerConfigurationFlag", 1),

                                                ("XDFfileDictionaryPath", os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"),

                                                ("OperationMode", "CyclicPosition"),

                                                ("EncoderTicksPerRevolution_ToBeSet", 8192.0),
                                                ("ZeroEncoder_FireEventOnStartupFlag", 1),

                                                ("Position_Max_Rev", 0.0),
                                                ("Position_Min_Rev", 0.0),

                                                ("MaxCurrentHardLimit_ToBeSet", 10.00),
                                                ("MaxContinuousCurrent_ToBeSet", 4.24),
                                                ("PeakCurrentValue_ToBeSet", 5.48),
                                                ("PeakCurrentTimeMilliseconds_ToBeSet", 500),
                                                ("PeakCurrentFaultModeInt_ToBeSet", 0),

                                                ("PositionFollowingErrorWindow_ToBeSet", 1000000),
                                                ("PositionFollowingErrorTimeoutMilliseconds_ToBeSet", 2),
                                                ("PositionFollowingErrorFaultModeInt_ToBeSet", 0),

                                                ("MaxVelocity_ToBeSet", 3.0),
                                                ("MaxProfileVelocity_ToBeSet", 3.0),
                                                ("MaxProfileAcceleration_ToBeSet", 30.0),

                                                ("PositionPIDgains_Kp_ToBeSet", 0.002),
                                                ("PositionPIDgains_Ki_ToBeSet", 0.0),
                                                ("PositionPIDgains_Kd_ToBeSet", 0.0),

                                                ("CurrentQuadraturePIgains_Kp_ToBeSet", 1.8),
                                                ("CurrentQuadraturePIgains_Ki_ToBeSet", 2500.0)]))])
    #'''

    #################################################
    #################################################

    #################################################
    #################################################
    global IngeniaBLDC_Object

    global IngeniaBLDC_OPEN_FLAG
    IngeniaBLDC_OPEN_FLAG = 0

    global IngeniaBLDC_MostRecentDict
    IngeniaBLDC_MostRecentDict = dict()

    global IngeniaBLDC_MostRecentDict_Time
    IngeniaBLDC_MostRecentDict_Time = 0.0

    global IngeniaBLDC_MostRecentDict_DetectedSlaveID_List
    IngeniaBLDC_MostRecentDict_DetectedSlaveID_List = []
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_ReubenPython3ClassObject

    global CSVdataLogger_OPEN_FLAG
    CSVdataLogger_OPEN_FLAG = -1

    global CSVdataLogger_MostRecentDict
    CSVdataLogger_MostRecentDict = dict()

    global CSVdataLogger_MostRecentDict_Time
    CSVdataLogger_MostRecentDict_Time = -11111.0

    global CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList
    CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList = []
    #################################################
    #################################################

    #################################################
    #################################################
    global EntryListWithBlinking_ReubenPython2and3ClassObject

    global EntryListWithBlinking_OPEN_FLAG
    EntryListWithBlinking_OPEN_FLAG = -1

    global EntryListWithBlinking_MostRecentDict
    EntryListWithBlinking_MostRecentDict = dict()

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber = 0

    global EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last
    EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = -1

    EntryWidth = 10
    LabelWidth = 40
    FontSize = 8
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_IngeniaBLDC = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################

    #################################################
    #################################################

    #################################################
    global IngeniaBLDC_GUIparametersDict
    IngeniaBLDC_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_IngeniaBLDC_FLAG),
                                    ("root", Tab_IngeniaBLDC),
                                    ("EnableInternal_MyPrint_Flag", 0),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_IngeniaBLDC),
                                    ("GUI_COLUMN", GUI_COLUMN_IngeniaBLDC),
                                    ("GUI_PADX", GUI_PADX_IngeniaBLDC),
                                    ("GUI_PADY", GUI_PADY_IngeniaBLDC),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_IngeniaBLDC),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_IngeniaBLDC)])
    #################################################


    #################################################
    global IngeniaBLDC_setup_dict
    IngeniaBLDC_setup_dict = dict([("GUIparametersDict", IngeniaBLDC_GUIparametersDict),
                                    ("NameToDisplay_UserSet", "IngeniaBLDC"),
                                    ("DesiredInterfaceName", "Realtek USB GbE Family Controller"), #likely "Intel(R) Ethernet Connection (2) I219-LM" or "Realtek USB GbE Family Controller"
                                    ("DesiredInterfaceName_MustItBeExactMatchFlag", 1), #IMPORTANT
                                    ("DesiredSlaves_DictOfDicts", DesiredSlaves_DictOfDicts),
                                    ("LaunchFlag_MotionLab3_IngEcatGateway_EoEservice", 0),
                                    ("DedicatedRxThread_TimeToSleepEachLoop", 0.002),
                                    ("DedicatedTxThread_TimeToSleepEachLoop", 0.002),
                                    ("PDO_UpdateDeltaTinSeconds", 0.020),
                                    ("EnableMotorAutomaticallyAfterEstopRestorationFlag", 1),
                                    ("EnableMotorAtStartOfProgramFlag", 1),
                                    ("GetSDOvariablesEveryNloopsCycles", 1),
                                    ("ListOfVariableNameStringsToGetViaSDO", []),
                                    ("CheckDetectedVsDesiredSlaveListFlag", 0)])
    #################################################

    #################################################
    if USE_IngeniaBLDC_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            IngeniaBLDC_Object = IngeniaBLDC_ReubenPython3Class(IngeniaBLDC_setup_dict)
            IngeniaBLDC_OPEN_FLAG = IngeniaBLDC_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("IngeniaBLDC_ReubenPython3ClassObject __init__, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_IngeniaBLDC_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if IngeniaBLDC_OPEN_FLAG != 1:
                print("Failed to open IngeniaBLDC_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict
    CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_CSVdataLogger_FLAG),
                                    ("root", Tab_CSVdataLogger),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_CSVdataLogger),
                                    ("GUI_COLUMN", GUI_COLUMN_CSVdataLogger),
                                    ("GUI_PADX", GUI_PADX_CSVdataLogger),
                                    ("GUI_PADY", GUI_PADY_CSVdataLogger),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_CSVdataLogger),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_CSVdataLogger)])

    #################################################
    #################################################

    #################################################
    CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList = ["Time (S)"]
    #################################################

    #################################################
    #################################################
    global CSVdataLogger_ReubenPython3ClassObject_setup_dict
    CSVdataLogger_ReubenPython3ClassObject_setup_dict = dict([("GUIparametersDict", CSVdataLogger_ReubenPython3ClassObject_GUIparametersDict),
                                                                                ("NameToDisplay_UserSet", "CSVdataLogger"),
                                                                                ("CSVfile_DirectoryPath", "C:\\CSVfiles"),
                                                                                ("FileNamePrefix", "CSV_file_"),
                                                                                ("VariableNamesForHeaderList", CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList),
                                                                                ("MainThread_TimeToSleepEachLoop", 0.002),
                                                                                ("SaveOnStartupFlag", 0)])

    if USE_CSVdataLogger_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            CSVdataLogger_ReubenPython3ClassObject = CSVdataLogger_ReubenPython3Class(CSVdataLogger_ReubenPython3ClassObject_setup_dict)
            CSVdataLogger_OPEN_FLAG = CSVdataLogger_ReubenPython3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("CSVdataLogger_ReubenPython3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_CSVdataLogger_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if CSVdataLogger_OPEN_FLAG != 1:
                print("Failed to open CSVdataLogger_ReubenPython3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    global EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict
    EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict = dict([("root", Tab_IngeniaBLDC), #Tab_MainControls
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_EntryListWithBlinking),
                                    ("GUI_COLUMN", GUI_COLUMN_EntryListWithBlinking),
                                    ("GUI_PADX", GUI_PADX_EntryListWithBlinking),
                                    ("GUI_PADY", GUI_PADY_EntryListWithBlinking),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_EntryListWithBlinking),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_EntryListWithBlinking)])

    global EntryListWithBlinking_Variables_ListOfDicts
    EntryListWithBlinking_Variables_ListOfDicts = [dict([("Name", "USE_SINUSOIDAL_INPUT_FLAG"),("Type", "float"),("StartingVal", USE_SINUSOIDAL_INPUT_FLAG),("MinVal", 0.0),("MaxVal", 1.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "SinusoidalMotionInput_MaxValue"),("Type", "float"),("StartingVal", SinusoidalMotionInput_MaxValue),("MinVal", 0.0),("MaxVal", 3600000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)]),
                                                   dict([("Name", "SinusoidalMotionInput_ROMtestTimeToPeakAngle"),("Type", "float"),("StartingVal", SinusoidalMotionInput_ROMtestTimeToPeakAngle),("MinVal", 0.0),("MaxVal", 3600000.0),("EntryBlinkEnabled", 0),("EntryWidth", EntryWidth),("LabelWidth", LabelWidth),("FontSize", FontSize)])]

    global EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict
    EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", EntryListWithBlinking_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                          ("EntryListWithBlinking_Variables_ListOfDicts", EntryListWithBlinking_Variables_ListOfDicts),
                                                                          ("DebugByPrintingVariablesFlag", 0),
                                                                          ("LoseFocusIfMouseLeavesEntryFlag", 0)])
    if USE_EntryListWithBlinking_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            EntryListWithBlinking_ReubenPython2and3ClassObject = EntryListWithBlinking_ReubenPython2and3Class(EntryListWithBlinking_ReubenPython2and3ClassObject_setup_dict)
            EntryListWithBlinking_OPEN_FLAG = EntryListWithBlinking_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("EntryListWithBlinking_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_EntryListWithBlinking_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if EntryListWithBlinking_OPEN_FLAG != 1:
                print("Failed to open EntryListWithBlinking_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MyPrint_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList = ["Direct", "Quad", "FOCcombbinedFOC", "Channel3", "Channel4", "Channel5"]

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_ColorList
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_ColorList = ["Red", "Green", "Blue", "Black", "Purple", "Orange"]

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 700),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 0),
                                                                                                ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("MarkerSize", 3),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists",
                                                                                            dict([("NameList", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList),
                                                                                                  ("ColorList", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_ColorList)])),
                                                                                        ("NumberOfDataPointToPlot", 50),
                                                                                        ("XaxisNumberOfTickMarks", 10),
                                                                                        ("YaxisNumberOfTickMarks", 10),
                                                                                        ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("XaxisAutoscaleFlag", 1),
                                                                                        ("YaxisAutoscaleFlag", 1),
                                                                                        ("X_min", 0.0),
                                                                                        ("X_max", 20.0),
                                                                                        ("Y_min", -1.00),
                                                                                        ("Y_max", 1.00),
                                                                                        ("XaxisDrawnAtBottomOfGraph", 0),
                                                                                        ("XaxisLabelString", "Time (sec)"),
                                                                                        ("YaxisLabelString", "Y-units (units)"),
                                                                                        ("ShowLegendFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterClass_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    #################################################
    #################################################

    #################################################
    #################################################
    if IngeniaBLDC_OPEN_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:

        #################################################
        IngeniaBLDC_MostRecentDict = IngeniaBLDC_Object.GetMostRecentDataDict()
        IngeniaBLDC_MostRecentDict_DetectedSlaveID_List = IngeniaBLDC_MostRecentDict["DetectedSlaveID_List"]
        #################################################

        ################################################# Uncomment this section only to test certain "_ExternalProgram" functions!
        for SlaveID_Int in IngeniaBLDC_MostRecentDict_DetectedSlaveID_List:
            dummy = 0
            #IngeniaBLDC_Object.SetPositionPIDgains_ExternalProgram(SlaveID_Int, Kp_ToBeSet=0.005, Ki_ToBeSet=0.001, Kd_ToBeSet=0.001, PrintDebugFlag=1)
            #IngeniaBLDC_Object.SetCurrentQuadraturePIgains_ExternalProgram(SlaveID_Int, Kp_ToBeSet=1.81, Ki_ToBeSet=2501.00, PrintDebugFlag=1)
            #IngeniaBLDC_Object.SetMaxCurrentHardLimit_ExternalProgram(SlaveID_Int, 2.0, PrintDebugFlag=1)
            #IngeniaBLDC_Object.SetMaxProfileVelocity_ExternalProgram(SlaveID_Int, 50000.0, PrintDebugFlag=1)
            #IngeniaBLDC_Object.SetMaxProfileAcceleration_ExternalProgram(SlaveID_Int, 100000.0, PrintDebugFlag=1)
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    if IngeniaBLDC_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:

        #################################################
        for SlaveID_Int in IngeniaBLDC_MostRecentDict_DetectedSlaveID_List:
            CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList.append("Position (Deg) Slave " + str(SlaveID_Int))
            CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList.append("Current Quadrature (A) Slave " + str(SlaveID_Int))
        #################################################

        #################################################
        print("CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList: " + str(CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList))
        CSVdataLogger_ReubenPython3ClassObject_setup_dict["VariableNamesForHeaderList"] = CSVdataLogger_ReubenPython3ClassObject_setup_dict_VariableNamesForHeaderList
        CSVdataLogger_ReubenPython3ClassObject.UpdateSetupDictParameters(CSVdataLogger_ReubenPython3ClassObject_setup_dict)
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    if EXIT_PROGRAM_FLAG == 0:
        print("Starting main loop 'test_program_for_IngeniaBLDC_ReubenPython3Class.")
        StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()
    #################################################
    #################################################

    while(EXIT_PROGRAM_FLAG == 0):

        ###################################################
        ###################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ###################################################
        ###################################################

        ####################################################
        ####################################################

        ################################################### GET's
        if EntryListWithBlinking_OPEN_FLAG == 1:

            EntryListWithBlinking_MostRecentDict = EntryListWithBlinking_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "DataUpdateNumber" in EntryListWithBlinking_MostRecentDict and EntryListWithBlinking_MostRecentDict["DataUpdateNumber"] != EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last:
                EntryListWithBlinking_MostRecentDict_DataUpdateNumber = EntryListWithBlinking_MostRecentDict["DataUpdateNumber"]
                #print("DataUpdateNumber = " + str(EntryListWithBlinking_MostRecentDict_DataUpdateNumber) + ", EntryListWithBlinking_MostRecentDict: " + str(EntryListWithBlinking_MostRecentDict))

                if EntryListWithBlinking_MostRecentDict_DataUpdateNumber > 1:
                    USE_SINUSOIDAL_INPUT_FLAG = int(EntryListWithBlinking_MostRecentDict["USE_SINUSOIDAL_INPUT_FLAG"])
                    SinusoidalMotionInput_MaxValue = EntryListWithBlinking_MostRecentDict["SinusoidalMotionInput_MaxValue"]
                    SinusoidalMotionInput_ROMtestTimeToPeakAngle = EntryListWithBlinking_MostRecentDict["SinusoidalMotionInput_ROMtestTimeToPeakAngle"]
        ###################################################

        ###################################################
        EntryListWithBlinking_MostRecentDict_DataUpdateNumber_last = EntryListWithBlinking_MostRecentDict_DataUpdateNumber
        ###################################################

        ####################################################
        ####################################################

        ################################################### GET's
        ###################################################
        if IngeniaBLDC_OPEN_FLAG == 1:
            if IngeniaBLDC_Object.IsDedicatedPDOthreadStillRunning() == 0:
                IngeniaBLDC_Object.StartPDOdedicatedThread()
        ###################################################
        ###################################################

        ################################################### GET's
        ###################################################
        if IngeniaBLDC_OPEN_FLAG == 1:

            IngeniaBLDC_MostRecentDict = IngeniaBLDC_Object.GetMostRecentDataDict()
            #print("IngeniaBLDC_MostRecentDict: " + str(IngeniaBLDC_MostRecentDict))

            if "Time" in IngeniaBLDC_MostRecentDict:
                IngeniaBLDC_MostRecentDict_Time = IngeniaBLDC_MostRecentDict["Time"]

        ###################################################
        ###################################################

        ################################################### SET's
        ###################################################
        if IngeniaBLDC_OPEN_FLAG == 1:

            ###################################################
            if ZeroEncoderOffsetOnAllMotors_EventNeedsToBeFiredFlag == 1:
                for SlaveID_Int in DesiredSlaves_DictOfDicts:
                    IngeniaBLDC_Object.SetEncoderOffset_ExternalProgram(SlaveID_Int, 0.0, PrintDebugFlag=1)

                ZeroEncoderOffsetOnAllMotors_EventNeedsToBeFiredFlag = 0
            ###################################################

            ###################################################
            if USE_SINUSOIDAL_INPUT_FLAG == 1:

                SinusoidalMotionInput_TimeGain = math.pi / (2.0 * SinusoidalMotionInput_ROMtestTimeToPeakAngle)
                
                SinusoidalMotionInput_CommandedValue = (SinusoidalMotionInput_MaxValue + SinusoidalMotionInput_MinValue)/2.0 + \
                                                       0.5*abs(SinusoidalMotionInput_MaxValue - SinusoidalMotionInput_MinValue)*math.sin(SinusoidalMotionInput_TimeGain*CurrentTime_MainLoopThread)

                SinusoidalMotionInput_CommandedValue = SinusoidalMotionInput_CommandedValue

                for SlaveID_Int in DesiredSlaves_DictOfDicts:
                    #SinusoidalMotionInput_CommandedValue_TEMP = SlaveID_Int*SinusoidalMotionInput_CommandedValue
                    SinusoidalMotionInput_CommandedValue_TEMP = SinusoidalMotionInput_CommandedValue

                    if DesiredSlaves_DictOfDicts[SlaveID_Int]["OperationMode"] == "CyclicPosition":
                        IngeniaBLDC_Object.SetPosition_ExternalProgram(SlaveID_Int, SinusoidalMotionInput_CommandedValue_TEMP, "Deg")

                    if DesiredSlaves_DictOfDicts[SlaveID_Int]["OperationMode"] == "CyclicCurrent":
                        IngeniaBLDC_Object.SetCurrent_Quadrature_ExternalProgram(SlaveID_Int, SinusoidalMotionInput_CommandedValue_TEMP)

                    if DesiredSlaves_DictOfDicts[SlaveID_Int]["OperationMode"] == "CyclicVoltage":
                        IngeniaBLDC_Object.SetVoltage_Quadrature_ExternalProgram(SlaveID_Int, SinusoidalMotionInput_CommandedValue_TEMP)


            ###################################################

        ###################################################
        ###################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if IngeniaBLDC_OPEN_FLAG == 1 and CSVdataLogger_OPEN_FLAG == 1:

            ####################################################
            ####################################################
            ListToWrite = []
            ListToWrite.append(CurrentTime_MainLoopThread)

            for SlaveID_Int in IngeniaBLDC_MostRecentDict_DetectedSlaveID_List:
                ListToWrite.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Position_Actual_AllUnitsDict"]["Deg"])

                ListToWrite.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Current_Direct_Actual"])
                ListToWrite.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Current_Quadrature_Actual"])
                ListToWrite.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Current_FOCcombinedDQ_Actual"])

            #print("ListToWrite: " + str(ListToWrite))
            ####################################################
            ####################################################

            CSVdataLogger_ReubenPython3ClassObject.AddDataToCSVfile_ExternalFunctionCall(ListToWrite)
        ####################################################
        ####################################################
        ####################################################

        #################################################### SET's
        ####################################################
        ####################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
            try:
                ####################################################
                ####################################################
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

                if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict:
                    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                    if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                        if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= 0.030:

                            ####################################################
                            ListOfValuesToPlot = []
                            for SlaveID_Int in IngeniaBLDC_MostRecentDict_DetectedSlaveID_List:
                                #ListOfValuesToPlot.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Position_Actual_AllUnitsDict"]["Deg"])
                                ListOfValuesToPlot.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Current_Direct_Actual"])
                                ListOfValuesToPlot.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Current_Quadrature_Actual"])
                                ListOfValuesToPlot.append(IngeniaBLDC_MostRecentDict["IngeniaMotionController_MainDict"][SlaveID_Int]["Current_FOCcombinedDQ_Actual"])
                            ####################################################

                            ####################################################
                            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_NameList[0:len(ListOfValuesToPlot)],
                                                                                                                                    [CurrentTime_MainLoopThread]*len(ListOfValuesToPlot),
                                                                                                                                    ListOfValuesToPlot)
                            ####################################################

                            ####################################################
                            LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
                            ####################################################

                ####################################################
                ####################################################

            except:
                exceptions = sys.exc_info()[0]
                print("test_program_for_IngeniaBLDC_ReubenPython3Class, if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1: SET's, Exceptions: %s" % exceptions)
                traceback.print_exc()
        ####################################################
        ####################################################
        ####################################################

        time.sleep(0.002)
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_IngeniaBLDC_ReubenPython3Class.")

    #################################################
    if IngeniaBLDC_OPEN_FLAG == 1:
        IngeniaBLDC_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if CSVdataLogger_OPEN_FLAG == 1:
        CSVdataLogger_ReubenPython3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if EntryListWithBlinking_OPEN_FLAG == 1:
        EntryListWithBlinking_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################

##########################################################################################################
##########################################################################################################