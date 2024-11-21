# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 11/20/2024

Verified working on: Python 3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

##########################################
import os
import sys
import time
import math
import traceback
import keyboard
from ingeniamotion import MotionController
from ingeniamotion.enums import OperationMode
##########################################

##########################################################################################################
##########################################################################################################
def StatusWordInterpretation(StatusWordToIntrepret):
    global StatusWordFlagNames_DictBitNumberAsKey

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
def ExitProgram_Callback(OptionalArugment = 0):
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    print("Starting program!")

    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

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

    ########################################################################################################## unicorn. Set this based on what you need!
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG
    ApplyNewSettingsToMotorFlag = 0
    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG

    DesiredInterfaceName = "Realtek USB GbE Family Controller" ##likely "Intel(R) Ethernet Connection (2) I219-LM" or "Realtek USB GbE Family Controller"

    XDFfileDictionaryPath = os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "den-xcr-e_eoe_2.5.0.xdf"  # "cap-xcr-e_eoe_2.4.1.xdf"  #den-xcr-e_eoe_2.5.0.xdf

    OperationModeSelected = "CyclicPosition"
    #DO NOT TRY OperationModeSelected = "CyclicCurrent" #If we try this right after having tried "CyclicPosition", then the motor will move in one direction and then stop.
    #DO NOT TRY OperationModeSelected = "CyclicTorque" #If we try this right after having tried "CyclicPosition", then the motor will move in one direction and then stop.

    SinusoidalMotionInput_MinValue_PositionControl = 0
    SinusoidalMotionInput_MaxValue_PositionControl = 0.5*(2048*4)
    SinusoidalMotionInput_ROMtestTimeToPeakAngle_PositionControl = 1.0

    SinusoidalMotionInput_MinValue_TorqueControl = -1.0 #Still experimenting with, do not use!
    SinusoidalMotionInput_MaxValue_TorqueControl = 1.0 #Still experimenting with, do not use!
    SinusoidalMotionInput_ROMtestTimeToPeakAngle_TorqueControl = 1.0 #Still experimenting with, do not use!

    MaxCurrent = 4.24

    MinPosition_EncoderTicks = -1000.0
    MaxPosition_EncoderTicks = 1000.0

    MaxProfileVelocity = 50000.0
    MaxProfileAcceleration = 20000.0

    PositionPIDgains_Kp_ToBeSet = 0.003
    PositionPIDgains_Ki_ToBeSet = 0.002
    PositionPIDgains_Kd_ToBeSet = 0.001

    PrintDebugFlag = 0

    try:
        DesiredSlaveID_Int = int(input("Enter the SlaveID_Int (e.g. 1, 2, 3, etc.) and press ENTER."))
    except:
        pass

    print("DesiredSlaveID_Int: " + str(DesiredSlaveID_Int))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    keyboard.on_press_key("esc", ExitProgram_Callback)
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
        IngeniaMotionControllerObject = MotionController()
    
        InterfaceList = IngeniaMotionControllerObject.communication.get_interface_name_list()
        print("List of interfaces:")
    
        CorrectInterfaceIndex = -1
        for Index, Interface in enumerate(InterfaceList):
            print(f"{Index}: {Interface}")
    
            if Interface == DesiredInterfaceName:
                CorrectInterfaceIndex = Index
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        if CorrectInterfaceIndex != -1:
            Interface_Index = CorrectInterfaceIndex
        else:
            print("Could not locate the interface '" + DesiredInterfaceName + ", exiting...")
            exit()
    
        InterfaceSelected = IngeniaMotionControllerObject.communication.get_ifname_by_index(Interface_Index)
        print("Interface selected:")
        print(f"- Index Interface: {Interface_Index}")
        print(f"- Interface identifier: {InterfaceSelected}")
        print(f"- Interface name: {InterfaceList[Interface_Index]}")
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        DetectedSlaveID_List = IngeniaMotionControllerObject.communication.scan_servos_ethercat(InterfaceSelected)
    
        if not DetectedSlaveID_List:
            print(f"No slave detected on Interface: {InterfaceList[Interface_Index]}")
        else:
            print(f"Found slaves: {DetectedSlaveID_List}")
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        OperationMode_ListOfAcceptableValuesStrings = ["CyclicPosition", "CyclicCurrent", "CyclicTorque"]

        if OperationModeSelected not in OperationMode_ListOfAcceptableValuesStrings:
            print("Error: " + OperationModeSelected + " is not in OperationMode_ListOfAcceptableValuesStrings = " + str(OperationMode_ListOfAcceptableValuesStrings))
            exit()
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        IngeniaMotionControllerObject.communication.connect_servo_ethercat(InterfaceSelected, DesiredSlaveID_Int, XDFfileDictionaryPath)

        IngeniaMotionControllerObject.motion.fault_reset()
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        if OperationModeSelected == "CyclicPosition":
            IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_POSITION)

            ##########################################################################################################
            if ApplyNewSettingsToMotorFlag == 1:
                IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KP", PositionPIDgains_Kp_ToBeSet)
                IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KI", PositionPIDgains_Ki_ToBeSet)
                IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KD", PositionPIDgains_Kd_ToBeSet)
                print("Applying new motor settings in CyclicPosition mode.")
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        elif OperationMode == "CyclicCurrent":

            IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.OperationMode.CURRENT) #CYCLIC_CURRENT

            ##########################################################################################################
            if ApplyNewSettingsToMotorFlag == 1:
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_KP", 1.8) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_KI", 2500.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_MAX_OUT", 48.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_MIN_OUT", -48.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_KP", 1.8) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_KI", 3500.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_MAX_OUT", 48.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_MIN_OUT", -48.0) #Still experimenting with these values
                print("Applying new motor settings in CyclicCurrent mode.")
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        elif OperationMode == "CyclicTorque":

            IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_TORQUE) #CYCLIC_TORQUE

            ##########################################################################################################
            if ApplyNewSettingsToMotorFlag == 1:
                IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_KP", 1.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_KI", 2500.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_MAX_OUT", 48.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_TOR_PID_MIN_OUT", -48.0) #Still experimenting with these values
                print("Applying new motor settings in CyclicTorque mode.")
                #INVESTIGATE CL_TOR_SET_POINT_VALUE and CL_TOR_CMD_VALUE
            ##########################################################################################################
                
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        #IngeniaMotionControllerObject.motion.target_latch() What does this do?

        ##########################################################################################################
        if ApplyNewSettingsToMotorFlag == 1:
            IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MIN_RANGE", int(MinPosition_EncoderTicks))
            IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MAX_RANGE", int(MaxPosition_EncoderTicks))
    
            IngeniaMotionControllerObject.communication.set_register("CL_CUR_REF_MAX", MaxCurrent)
    
            IngeniaMotionControllerObject.configuration.set_max_profile_velocity(MaxProfileVelocity)  # Set all registers needed before activating the trapezoidal profiler
            IngeniaMotionControllerObject.configuration.set_max_profile_acceleration(MaxProfileAcceleration)
            IngeniaMotionControllerObject.configuration.set_max_profile_deceleration(MaxProfileAcceleration)
            print("Applying new motor settings that are common to all modes.")
            
        ##########################################################################################################

        IngeniaMotionControllerObject.motion.motor_enable()
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        serial_number = IngeniaMotionControllerObject.configuration.get_serial_number()
        print("serial_number: " + str(serial_number))
    
        vendor_id = IngeniaMotionControllerObject.configuration.get_vendor_id()
        print("vendor_id: " + str(vendor_id))
    
        product_code = IngeniaMotionControllerObject.configuration.get_product_code()
        print("product_code: " + str(product_code))
    
        fw_version = IngeniaMotionControllerObject.configuration.get_fw_version()
        print("fw_version: " + str(fw_version))
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
        print("Initializing motors, exceptions: %s" % exceptions)
        #sys.exit()
        traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("********** TO QUIT, PRESS THE ESC KEY **********")
    StartingTime_MainLoopThread = time.time()
    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            CurrentTime_MainLoopThread = time.time() - StartingTime_MainLoopThread
            
            SinusoidalMotionInput_TimeGain_PositionControl = math.pi / (2.0 * SinusoidalMotionInput_ROMtestTimeToPeakAngle_PositionControl)
            SinusoidalMotionInput_CommandedValue_PositionControl = ((SinusoidalMotionInput_MaxValue_PositionControl + SinusoidalMotionInput_MinValue_PositionControl) / 2.0 + 
                                             0.5 * abs(SinusoidalMotionInput_MaxValue_PositionControl - SinusoidalMotionInput_MinValue_PositionControl) * math.sin(SinusoidalMotionInput_TimeGain_PositionControl * CurrentTime_MainLoopThread))
            
            SinusoidalMotionInput_TimeGain_TorqueControl = math.pi / (2.0 * SinusoidalMotionInput_ROMtestTimeToPeakAngle_TorqueControl)
            SinusoidalMotionInput_CommandedValue_TorqueControl = ((SinusoidalMotionInput_MaxValue_TorqueControl + SinusoidalMotionInput_MinValue_TorqueControl) / 2.0 + 
                                             0.5 * abs(SinusoidalMotionInput_MaxValue_TorqueControl - SinusoidalMotionInput_MinValue_TorqueControl) * math.sin(SinusoidalMotionInput_TimeGain_TorqueControl * CurrentTime_MainLoopThread))
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            if OperationModeSelected == "CyclicPosition":
                ##########################################################################################################
                IngeniaMotionControllerObject.motion.move_to_position(int(SinusoidalMotionInput_CommandedValue_PositionControl))

                if PrintDebugFlag == 1:
                    print("CyclicPosition: SlaveID_Int =  " + str(DesiredSlaveID_Int) + ", IngeniaMotionControllerObject.motion.move_to_position, SinusoidalMotionInput_CommandedValue_PositionControl = " + str(SinusoidalMotionInput_CommandedValue_PositionControl))
                ##########################################################################################################

            elif OperationModeSelected == "CyclicCurrent":
                ##########################################################################################################
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_SET_POINT", SinusoidalMotionInput_CommandedValue_TorqueControl)
                #IngeniaMotionControllerObject.communication.set_register("CL_CUR_D_SET_POINT", SinusoidalMotionInput_CommandedValue_TorqueControl)
                #IngeniaMotionControllerObject.motion.set_current_quadrature(SinusoidalMotionInput_CommandedValue_TorqueControl) #Only goes 1 direction! Works in OperationMode.CYCLIC_CURRENT, not in OperationMode.CYCLIC_TORQUE.
                #IngeniaMotionControllerObject.motion.set_current_direct(SinusoidalMotionInput_CommandedValue_TorqueControl) #Only goes 1 direction! Works in OperationMode.CYCLIC_CURRENT, not in OperationMode.CYCLIC_TORQUE.

                if PrintDebugFlag == 1:
                    print("CyclicCurrent: SlaveID_Int =  " + str(DesiredSlaveID_Int) + ", IngeniaMotionControllerObject.motion.set_current_quadrature, SinusoidalMotionInput_CommandedValue_TorqueControl = " + str(SinusoidalMotionInput_CommandedValue_TorqueControl))
                ##########################################################################################################

            elif OperationModeSelected == "CyclicTorque":
                ##########################################################################################################
                IngeniaMotionControllerObject.communication.set_register("CL_TOR_SET_POINT_VALUE", SinusoidalMotionInput_CommandedValue_TorqueControl)

                if PrintDebugFlag == 1:
                    print("CyclicTorque: SlaveID_Int =  " + str(DesiredSlaveID_Int) + ", IngeniaMotionControllerObject.motion.set_current_quadrature, SinusoidalMotionInput_CommandedValue_TorqueControl = " + str(SinusoidalMotionInput_CommandedValue_TorqueControl))
                ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            Status_Word = IngeniaMotionControllerObject.configuration.get_status_word()
            StatusWordFlagStates_DictEnglishNameAsKey = StatusWordInterpretation(Status_Word)

            if PrintDebugFlag == 1:
                print("StatusWordFlagStates_DictEnglishNameAsKey: " + str(StatusWordFlagStates_DictEnglishNameAsKey))
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            time.sleep(0.001)
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
            print("while(EXIT_PROGRAM_FLAG == 0): section, exceptions: %s" % exceptions)
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
    IngeniaMotionControllerObject.motion.motor_disable()
    IngeniaMotionControllerObject.communication.disconnect()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    print("Ending program!")
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################