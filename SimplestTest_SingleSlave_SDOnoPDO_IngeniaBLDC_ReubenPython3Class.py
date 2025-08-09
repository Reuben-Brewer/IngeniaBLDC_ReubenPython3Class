# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision M, 08/08/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
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
##########################################################################################################
if __name__ == '__main__':

    print("Starting program!")

    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global OperationMode_DictIntNumberAsKey
    OperationMode_DictIntNumberAsKey = dict([(0, "Voltage"),
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
    ##########################################################################################################

    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG
    ApplyNewSettingsToMotorFlag = 0
    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG

    #DesiredInterfaceName = "ASIX USB to Gigabit Ethernet Family Adapter"
    #DesiredInterfaceName = "Intel(R) Ethernet Connection (2) I219-LM"
    #DesiredInterfaceName = "Realtek USB GbE Family Controller"
    #DesiredInterfaceName = "Dell Realtek USB GbE Family Controller"
    DesiredInterfaceName = "Realtek USB GbE Family Controller #2"

    XDFfileDictionaryPath = os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"
    #XDFfileDictionaryPath = os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "den-xcr-e_eoe_2.5.0.xdf"

    OperationModeSelected = "CyclicPosition"
    #OperationModeSelected = "CyclicCurrent"
    #OperationModeSelected = "CyclicVoltage"

    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG
    EncoderTicksPerRevolution = 2048*4 #CPR*4, Maxon
    #EncoderTicksPerRevolution = 145.1*1 #CPR*4, GoBilda 5203-2402-0005 (1150RPM)
    #EncoderTicksPerRevolution = 1234 #Random test value.
    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG

    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG
    SinusoidalMotionInput_MinValue = -1.0*EncoderTicksPerRevolution #PositionControl
    SinusoidalMotionInput_MaxValue = 1.0*EncoderTicksPerRevolution #PositionControl

    #SinusoidalMotionInput_MinValue = -4.24 #CurrentControl
    #SinusoidalMotionInput_MaxValue = 4.24 #CurrentControl
    
    #SinusoidalMotionInput_MinValue = -1.0 #VoltageControl
    #SinusoidalMotionInput_MaxValue = 1.0 #VoltageControl
    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG

    ###
    SinusoidalMotionInput_ROMtestTimeToPeakAngle = 2.0
    SquareWaveMotionInput_LogicalStateBoolean = 0
    SquareWaveMotionInput_LogicalStateBoolean_Last = -1
    ###

    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG
    UseBrakeFlag = 0
    ######## $$$$$$$ %%%%%%% ^^^^^^^ IMPORTANT FLAG

    MaxCurrentHardLimit = 4.24 #Maxon motor
    #MaxCurrentHardLimit = 10.0 #GoBilda 5203-2402-0005 (1150RPM)
    #MaxCurrentHardLimit = 0.1234 Random test value

    MinPosition_EncoderTicks = -12000.0
    MaxPosition_EncoderTicks = 11000.0

    #MinPosition_EncoderTicks = 45 #THIS LIMIT ISN'T WORKING!!! There's weird wrapping of the reported actual positoin around this limit.
    #MaxPosition_EncoderTicks = -45 #THIS LIMIT ISN'T WORKING!!! There's weird wrapping of the reported actual positoin around this limit.

    MaxProfileVelocity = 50000.0
    MaxProfileAcceleration = 20000.0

    '''
    PositionPIDgains_Kp_ToBeSet = 0.01
    PositionPIDgains_Ki_ToBeSet = 0.2
    PositionPIDgains_Kd_ToBeSet = 0.1
    '''

    #'''
    PositionPIDgains_Kp_ToBeSet = 0.01
    PositionPIDgains_Ki_ToBeSet = 0.0
    PositionPIDgains_Kd_ToBeSet = 0.0
    #'''

    MotorEnabled_State = 0

    PrintDebugFlag = 1

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
    ##########################################################################################################
    ##########################################################################################################
    try:

        ##########################################################################################################
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
        ##########################################################################################################
        ##########################################################################################################
        DetectedSlaveID_List = IngeniaMotionControllerObject.communication.scan_servos_ethercat(InterfaceSelected)
    
        if not DetectedSlaveID_List:
            print(f"No slave detected on Interface: {InterfaceList[Interface_Index]}")
            exit()
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

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        OperationMode_ListOfAcceptableValuesStrings = ["CyclicPosition", "CyclicCurrent", "CyclicVoltage"]

        if OperationModeSelected not in OperationMode_ListOfAcceptableValuesStrings:
            print("Error: " + OperationModeSelected + " is not in OperationMode_ListOfAcceptableValuesStrings = " + str(OperationMode_ListOfAcceptableValuesStrings))
            exit()
        ##########################################################################################################
        ##########################################################################################################
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
        ##########################################################################################################
        ##########################################################################################################
        if OperationModeSelected == "CyclicPosition":
            IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_POSITION)
            print("Setting drive to OperationMode CyclicPosition.")

            ##########################################################################################################
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

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif OperationModeSelected == "CyclicCurrent":

            IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_CURRENT)
            print("############################################################Setting drive to OperationMode CyclicCurrent.")

            ##########################################################################################################
            ##########################################################################################################
            if ApplyNewSettingsToMotorFlag == 1:
                MinPosition_EncoderTicks = 0.0 #If software position limits are enabled using this mode of operation, the drive will generate a fault if the position limits are exceeded. Set them to 0 to disable this functionality.
                MaxPosition_EncoderTicks = 0.0 #If software position limits are enabled using this mode of operation, the drive will generate a fault if the position limits are exceeded. Set them to 0 to disable this functionality.

                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_KP", 1.8) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_KI", 2500.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_MAX_OUT", 48.0) #Still experimenting with these values
                IngeniaMotionControllerObject.communication.set_register("CL_CUR_Q_MIN_OUT", -48.0) #Still experimenting with these values
                print("Applying new motor settings in CyclicCurrent mode.")
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        elif OperationModeSelected == "CyclicVoltage":

            IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.VOLTAGE)
            print("############################################################Setting drive to OperationMode CyclicVoltage.")

            ##########################################################################################################
            ##########################################################################################################
            if ApplyNewSettingsToMotorFlag == 1:

                MinPosition_EncoderTicks = 0.0 #If software position limits are enabled using this mode of operation, the drive will generate a fault if the position limits are exceeded. Set them to 0 to disable this functionality or disable the fault generation masking it.
                MaxPosition_EncoderTicks = 0.0 #If software position limits are enabled using this mode of operation, the drive will generate a fault if the position limits are exceeded. Set them to 0 to disable this functionality or disable the fault generation masking it.

                #If actuator velocity overcomes the max. velocity parameter using this mode of operation, the drive will generate a fault. Disable the fault generation masking it.
                #If current measurements surpass the max. current parameter using this mode of operation, the drive will generate a fault. Disable the fault generation masking it.
                #In this mode, this drive is still protected by the main protections such as over/under voltage, over/under temperature, short-circuits, and I2T.

                '''
                Related registers:
                Voltage quadrature set-point and voltage direct set-point
                Voltage quadrature demand and voltage direct demand
                Voltage quadrature command and voltage direct command
                Bus voltage value contains the instantaneous bus voltage reading
                Maximum duty cycle contains the maximum duty cycle provided
                Voltage phase A, Voltage phase B and Voltage phase C
                '''

                print("Applying new motor settings in CyclicVoltage mode.")
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        #IngeniaMotionControllerObject.motion.target_latch() What does this do?

        ##########################################################################################################
        ##########################################################################################################
        if ApplyNewSettingsToMotorFlag == 1:

            Position_EncoderTicks_Actual_Int = IngeniaMotionControllerObject.motion.get_actual_position()
            print("Position_EncoderTicks_Actual_Int: " + str(Position_EncoderTicks_Actual_Int))

            IngeniaMotionControllerObject.configuration.homing_on_current_position(0) #Does NOT require the motor to be enabled.

            IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MIN_RANGE", -2147483648) #Signed 32-bit int. Minimum position value range. On reaching or exceeding this limit, the position set-point and position actual are wrapped automatically to the other end of the range.
            IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MAX_RANGE", 2147483647) #Signed 32-bit int. Maximum position value range. On reaching or exceeding this limit, the position set-point and position actual are wrapped automatically to the other end of the range.\

            IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MIN", int(1.0*MinPosition_EncoderTicks)) #User minimum allowed position.
            IngeniaMotionControllerObject.communication.set_register("CL_POS_REF_MAX", int(1.0*MaxPosition_EncoderTicks)) #User maximum allowed position.

            IngeniaMotionControllerObject.communication.set_register("CL_CUR_REF_MAX", MaxCurrentHardLimit)

            IngeniaMotionControllerObject.configuration.set_max_profile_velocity(MaxProfileVelocity)  # Set all registers needed before activating the trapezoidal profiler
            IngeniaMotionControllerObject.configuration.set_max_profile_acceleration(MaxProfileAcceleration)
            IngeniaMotionControllerObject.configuration.set_max_profile_deceleration(MaxProfileAcceleration)

            print("Applying new motor settings that are common to all modes.")
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
        serial_number = IngeniaMotionControllerObject.configuration.get_serial_number()
        print("serial_number: " + str(serial_number))
    
        vendor_id = IngeniaMotionControllerObject.configuration.get_vendor_id()
        print("vendor_id: " + str(vendor_id))
    
        product_code = IngeniaMotionControllerObject.configuration.get_product_code()
        print("product_code: " + str(product_code))
    
        fw_version = IngeniaMotionControllerObject.configuration.get_fw_version()
        print("fw_version: " + str(fw_version))

        OperationMode_Actual_Int = IngeniaMotionControllerObject.communication.get_register("DRV_OP_VALUE")  # Indicates the mode of operation applied in the drive
        print("OperationMode_Actual_Int: " + str(OperationMode_Actual_Int))

        if OperationMode_Actual_Int in OperationMode_DictIntNumberAsKey:
            OperationMode_Actual_EnglishName =  OperationMode_DictIntNumberAsKey[OperationMode_Actual_Int]
            print("OperationMode_Actual_EnglishName: " + str(OperationMode_Actual_EnglishName))
        else:
            print("Error: OperationMode_Actual_Int not in OperationMode_DictIntNumberAsKey!")
        # DRV_OP_CMD #User requested mode of operation

        MinPositionRange_EncoderTicks_Actual_Int = IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MIN_RANGE")
        print("MinPositionRange_EncoderTicks_Actual_Int: " + str(MinPositionRange_EncoderTicks_Actual_Int))

        MaxPositionRange_EncoderTicks_Actual_Int = IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MAX_RANGE")
        print("MaxPositionRange_EncoderTicks_Actual_Int: " + str(MaxPositionRange_EncoderTicks_Actual_Int))

        MinPosition_EncoderTicks_Actual_Int = IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MIN")
        print("MinPosition_EncoderTicks_Actual_Int: " + str(MinPosition_EncoderTicks_Actual_Int))

        MaxPosition_EncoderTicks_Actual_Int = IngeniaMotionControllerObject.communication.get_register("CL_POS_REF_MAX")
        print("MaxPosition_EncoderTicks_Actual_Int: " + str(MaxPosition_EncoderTicks_Actual_Int))

        Position_EncoderTicks_Actual_Int = IngeniaMotionControllerObject.motion.get_actual_position()
        print("Position_EncoderTicks_Actual_Int: " + str(Position_EncoderTicks_Actual_Int))

        #BrakeActivationTimeMilliseconds_Actual_Int = IngeniaMotionControllerObject.communication.get_register("MOT_BRAKE_ACTIVATION_TIME")
        #print("BrakeActivationTimeMilliseconds_Actual_Int: " + str(BrakeActivationTimeMilliseconds_Actual_Int))

        #EXIT_PROGRAM_FLAG = 1

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
    except:
        exceptions = sys.exc_info()[0]
        print("Initializing motors, exceptions: %s" % exceptions)
        EXIT_PROGRAM_FLAG = 1
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
    print("********** TO QUIT, PRESS THE ESC KEY **********")
    StartingTime_MainLoopThread = time.time()
    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            CurrentTime_MainLoopThread = time.time() - StartingTime_MainLoopThread

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            SinusoidalMotionInput_TimeGain = math.pi / (2.0 * SinusoidalMotionInput_ROMtestTimeToPeakAngle)
            SinusoidalMotionInput_CommandedValue = ((SinusoidalMotionInput_MaxValue + SinusoidalMotionInput_MinValue) / 2.0 + 
                                             0.5 * abs(SinusoidalMotionInput_MaxValue - SinusoidalMotionInput_MinValue) * math.sin(SinusoidalMotionInput_TimeGain * CurrentTime_MainLoopThread))
            ##########################################################################################################

            ##########################################################################################################
            Squarewave_Threshold = (SinusoidalMotionInput_MaxValue + SinusoidalMotionInput_MinValue) / 2.0

            if SinusoidalMotionInput_CommandedValue >= Squarewave_Threshold:
                SquareWaveMotionInput_LogicalStateBoolean = 1
            else:
                SquareWaveMotionInput_LogicalStateBoolean = 0
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
            if MotorEnabled_State == 0:
                IngeniaMotionControllerObject.configuration.enable_brake() #Without this line, the brake will actuate due to the motor_enable() call below.
                IngeniaMotionControllerObject.motion.motor_enable()
                MotorEnabled_State = 1
                print("MotorEnabled_State: " + str(MotorEnabled_State))
            ##########################################################################################################

            ##########################################################################################################
            if OperationModeSelected == "CyclicPosition":
                IngeniaMotionControllerObject.motion.move_to_position(int(SinusoidalMotionInput_CommandedValue))
            ##########################################################################################################

            ##########################################################################################################
            elif OperationModeSelected == "CyclicCurrent":
                IngeniaMotionControllerObject.motion.set_current_quadrature(SinusoidalMotionInput_CommandedValue)
            ##########################################################################################################

            ##########################################################################################################
            elif OperationModeSelected == "CyclicVoltage":
                IngeniaMotionControllerObject.motion.set_voltage_quadrature(SinusoidalMotionInput_CommandedValue)
                #IngeniaMotionControllerObject.communication.set_register("CL_VOL_Q_SET_POINT", SinusoidalMotionInput_CommandedValue_VoltageControl)
            ##########################################################################################################

            ##########################################################################################################
            #if PrintDebugFlag == 1:
            #    print(OperationModeSelected + ": SlaveID_Int =  " + str(DesiredSlaveID_Int) + ", SinusoidalMotionInput_CommandedValue = " + str(SinusoidalMotionInput_CommandedValue))
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if UseBrakeFlag == 1:

                if SquareWaveMotionInput_LogicalStateBoolean != SquareWaveMotionInput_LogicalStateBoolean_Last:

                    ##########################################################################################################
                    IngeniaMotionControllerObject.motion.motor_disable()
                    MotorEnabled_State = 0
                    ##########################################################################################################

                    ##########################################################################################################
                    if SquareWaveMotionInput_LogicalStateBoolean == 1:
                        print("Brake release")

                        #https://drives.novantamotion.com/summit/0x2129-brake-override
                        #Warning: This parameter should only be modified when the power stage is disabled. When changed in "operation enable" state, the behaviour of the drive is unexpected.
                        IngeniaMotionControllerObject.configuration.release_brake()

                    else:
                        print("Brake lock")

                        #https://drives.novantamotion.com/summit/0x2129-brake-override
                        #Warning: This parameter should only be modified when the power stage is disabled. When changed in "operation enable" state, the behaviour of the drive is unexpected.
                        IngeniaMotionControllerObject.configuration.enable_brake()
                    ##########################################################################################################

                    ##########################################################################################################
                    IngeniaMotionControllerObject.motion.motor_enable()
                    MotorEnabled_State = 1
                    ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            Status_Word = IngeniaMotionControllerObject.configuration.get_status_word()
            StatusWordFlagStates_DictEnglishNameAsKey = StatusWordInterpretation(Status_Word)
            Position_EncoderTicks_Actual = IngeniaMotionControllerObject.motion.get_actual_position()

            if PrintDebugFlag == 1:
                print("SinusoidalMotionInput_CommandedValue: " + str(int(SinusoidalMotionInput_CommandedValue)) + ", Position_EncoderTicks_Actual: " + str(Position_EncoderTicks_Actual))# + "StatusWordFlagStates_DictEnglishNameAsKey: " + str(StatusWordFlagStates_DictEnglishNameAsKey)))
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            SquareWaveMotionInput_LogicalStateBoolean_Last = SquareWaveMotionInput_LogicalStateBoolean

            time.sleep(0.03)
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
            print("while(EXIT_PROGRAM_FLAG == 0): section, exceptions: %s" % exceptions)
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

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    try:

        IngeniaMotionControllerObject.configuration.enable_brake()  # Without this line, the brake will actuate due to the motor_enable() call below.

        IngeniaMotionControllerObject.motion.motor_disable()

        IngeniaMotionControllerObject.configuration.disable_brake_override()
        IngeniaMotionControllerObject.communication.disconnect()
    except:
        pass
    ##########################################################################################################
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
##########################################################################################################