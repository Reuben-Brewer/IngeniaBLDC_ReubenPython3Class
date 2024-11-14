# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision E, 11/13/2024

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
if __name__ == '__main__':

    print("Starting program!")

    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    ########################################################################################################## unicorn. Set this based on what you need!
    ##########################################################################################################
    ##########################################################################################################
    DesiredInterfaceName = "Realtek USB GbE Family Controller" ##likely "Intel(R) Ethernet Connection (2) I219-LM" or "Realtek USB GbE Family Controller"

    XDFfileDictionaryPath = os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "den-xcr-e_eoe_2.5.0.xdf"  # "cap-xcr-e_eoe_2.4.1.xdf"  #den-xcr-e_eoe_2.5.0.xdf
    
    SinusoidalMotionInput_MinValue_PositionControl = 0
    SinusoidalMotionInput_MaxValue_PositionControl = 10.0*(2048*4)
    SinusoidalMotionInput_ROMtestTimeToPeakAngle = 1.0

    PrintDebugFlag = 0

    #DesiredSlaveID_Int = 4  # Note that the SlaveID's must be integers and appear in-order, starting with 1, 2, 3....

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
    keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    try:

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
        DetectedSlaveID_List = IngeniaMotionControllerObject.communication.scan_servos_ethercat(InterfaceSelected)
    
        if not DetectedSlaveID_List:
            print(f"No slave detected on Interface: {InterfaceList[Interface_Index]}")
        else:
            print(f"Found slaves: {DetectedSlaveID_List}")
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        IngeniaMotionControllerObject.communication.connect_servo_ethercat(InterfaceSelected, DesiredSlaveID_Int, XDFfileDictionaryPath)
    
        IngeniaMotionControllerObject.motion.set_operation_mode(OperationMode.CYCLIC_POSITION)
    
        IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KP", 0.005)
        IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KI", 0.002)
        IngeniaMotionControllerObject.communication.set_register("CL_POS_PID_KD", 0.003)
    
        max_velocity = 50000.0
        max_acceleration_deceleration = 20000.0
        IngeniaMotionControllerObject.configuration.set_max_profile_acceleration(max_acceleration_deceleration)
        IngeniaMotionControllerObject.configuration.set_max_profile_deceleration(max_acceleration_deceleration)
    
        IngeniaMotionControllerObject.configuration.set_max_profile_velocity(max_velocity) # Set all registers needed before activating the trapezoidal profiler
        IngeniaMotionControllerObject.configuration.set_max_profile_acceleration(max_acceleration_deceleration)
        IngeniaMotionControllerObject.configuration.set_max_profile_deceleration(max_acceleration_deceleration)
    
        IngeniaMotionControllerObject.motion.motor_enable()
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
    except:
        exceptions = sys.exc_info()[0]
        print("Initializing motors, exceptions: %s" % exceptions)
        traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    StartingTime_MainLoopThread = time.time()
    while(EXIT_PROGRAM_FLAG == 0):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            CurrentTime_MainLoopThread = time.time() - StartingTime_MainLoopThread
            SinusoidalMotionInput_TimeGain = math.pi / (2.0 * SinusoidalMotionInput_ROMtestTimeToPeakAngle)

            SinusoidalMotionInput_CommandedValue = ((SinusoidalMotionInput_MaxValue_PositionControl + SinusoidalMotionInput_MinValue_PositionControl) / 2.0 + 
                                             0.5 * abs(SinusoidalMotionInput_MaxValue_PositionControl - SinusoidalMotionInput_MinValue_PositionControl) * math.sin(SinusoidalMotionInput_TimeGain * CurrentTime_MainLoopThread))
            ##########################################################################################################

            ##########################################################################################################
            IngeniaMotionControllerObject.motion.move_to_position(int(SinusoidalMotionInput_CommandedValue))

            if PrintDebugFlag == 1:
                print("SlaveID_Int =  " + str(DesiredSlaveID_Int) + ", IngeniaMotionControllerObject.motion.move_to_position, SinusoidalMotionInput_CommandedValue = " + str(SinusoidalMotionInput_CommandedValue))
            ##########################################################################################################

            ##########################################################################################################
            time.sleep(0.030)
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
    IngeniaMotionControllerObject.motion.motor_disable()
    IngeniaMotionControllerObject.communication.disconnect()
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    print("Ending program!")
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################