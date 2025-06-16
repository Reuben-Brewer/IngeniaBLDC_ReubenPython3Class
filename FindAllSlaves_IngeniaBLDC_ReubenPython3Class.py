# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision L, 06/16/2025

Verified working on: Python 3.11/3.12 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'



'''
PySOEM is calling C++ from within SOEM, and that prints to the screen: "could not open with pcap" https://github.com/OpenEtherCATsociety/SOEM/blob/master/oshw/win32/nicdrv.c
Because it's printing from C++, it's difficult to suppress in Python (can't catch it in stdout or stderr).
'''

#######################################################################################################################
#######################################################################################################################
import sys

#######################################################################################################################
class RedirectStderrClass:
    def __init__(self, StreamFileIn, PrintFlag=1):
        self.StreamFileIn = StreamFileIn
        self.PrintFlag = PrintFlag

    def write(self, StringFromStderr): #Has to be named "write"
        ListOfBannedStrings = ["Kvaser"]
        for BannedString in ListOfBannedStrings:
            if StringFromStderr.find(BannedString) != -1:
                return

        if self.PrintFlag == 1:
            print("RedirectStderrClass: " + str(StringFromStderr), file=self.StreamFileIn)
#######################################################################################################################

#######################################################################################################################
class RedirectStdoutClass:
    def __init__(self, StreamFileIn):
        self.StreamFileIn = StreamFileIn

    def write(self, StringFromStdout): #Has to be named "write"
        print("" + str(StringFromStdout.strip()), file=self.StreamFileIn)
#######################################################################################################################

#sys.stderr = RedirectStderrClass(sys.stderr, PrintFlag=0)
#sys.stdout = RedirectStdoutClass(sys.stdout)
#######################################################################################################################
#######################################################################################################################

##########################################
import os
import time
import math
import json
from copy import * #for deepcopy
import traceback
from ingeniamotion import MotionController
##########################################

#######################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_AddDictKeysToGlobalsDict(GlobalsDict, JSONfilepathFull, USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS = 0, PrintResultsFlag = 0, PauseForInputOnException = 1):

    try:
        #################################

        ##############
        with open(JSONfilepathFull) as ParametersToBeLoaded_JSONfileObject:
            ParametersToBeLoaded_JSONfileParsedIntoDict = json.load(ParametersToBeLoaded_JSONfileObject)

        ParametersToBeLoaded_JSONfileObject.close()
        ##############

        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        ##############
        for key, value in ParametersToBeLoaded_JSONfileParsedIntoDict.items():
            if USE_PassThrough0and1values_ExitProgramOtherwise_FOR_FLAGS == 1:
                if key.upper().find("_FLAG") != -1:
                    GlobalsDict[key] = PassThrough0and1values_ExitProgramOtherwise(key, value)
                else:
                    GlobalsDict[key] = value
            else:
                GlobalsDict[key] = value

            if PrintResultsFlag == 1:
                print(key + ": " + str(value))

        ##############
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

        return ParametersToBeLoaded_JSONfileParsedIntoDict
        #################################

    except:
        #################################
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_AddDictKeysToGlobalsDict failed for " + JSONfilepathFull + ", exceptions: %s" % exceptions)

        traceback.print_exc()

        if PauseForInputOnException == 1:
            input("Please press any kery to continue")

        return dict()
        #################################

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def PassThrough0and1values_ExitProgramOtherwise(InputNameString, InputNumber, ExitProgramIfFailureFlag = 0):

    #######################################################################################################################
    #######################################################################################################################
    try:

        #######################################################################################################################
        InputNumber_ConvertedToFloat = float(InputNumber)
        #######################################################################################################################

    except:

        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a numerical value, Exceptions: %s" % exceptions)

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -1
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    try:

        #######################################################################################################################
        if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
            return InputNumber_ConvertedToFloat

        else:

            print(TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error. '" +
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

        #######################################################################################################################

    except:

        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -1
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def PassThroughFloatValuesInRange_ExitProgramOtherwise(InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag = 0):

    #######################################################################################################################
    #######################################################################################################################
    try:
        #######################################################################################################################
        InputNumber_ConvertedToFloat = float(InputNumber)
        #######################################################################################################################

    except:
        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber '" + InputNameString + "' must be a float value, Exceptions: %s" % exceptions)
        traceback.print_exc()

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -11111.0
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################
    try:

        #######################################################################################################################
        InputNumber_ConvertedToFloat_Limited = LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

        if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
            print(TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
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
        #######################################################################################################################

    except:
        #######################################################################################################################
        exceptions = sys.exc_info()[0]
        print(TellWhichFileWereIn() + ", PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
        traceback.print_exc()

        ##########################
        if ExitProgramIfFailureFlag == 1:
            sys.exit()
        else:
            return -11111.0
        ##########################

        #######################################################################################################################

    #######################################################################################################################
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3, PrintPlusSignFlag=1):

    try:
        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems, PrintPlusSignFlag)

            else:
                if isinstance(DictToPrint[Key], int)  == 1:
                    NumberOfDecimalsPlaceToUse_Mod = 0
                else:
                    NumberOfDecimalsPlaceToUse_Mod = NumberOfDecimalsPlaceToUse

                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse_Mod, PrintPlusSignFlag)

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
        traceback.print_exc()
        return ""

#######################################################################################################################
#######################################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3, PrintPlusSignFlag=1):
    number_of_decimal_places_original = number_of_decimal_places
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

    if number_of_decimal_places_original == 0:
        DecimalIndex = StringToReturn.find(".")
        if  DecimalIndex != -1:
            StringToReturn = StringToReturn[:DecimalIndex]

    if PrintPlusSignFlag == 0:
        StringToReturn = StringToReturn.replace("+","")

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

########################################################################################################################
#######################################################################################################################
def LoadAndParseJSONfile_PrototypesIngeniaSerialNumberToJointEnglishName():
    global ParametersToBeLoaded_PrototypesIngeniaSerialNumberToJointEnglishName_Dict

    global PrototypesIngeniaSerialNumberToJointEnglishNameDict
    global IngeniaControllerProductCodeToEnglishNameDict

    #######################################################################################################################
    try:
        #################################
        JSONfilepathFull_PrototypesIngeniaSerialNumberToJointEnglishName = ParametersToBeLoaded_Directory_TO_BE_USED + "//ParametersToBeLoaded_PrototypesIngeniaSerialNumberToJointEnglishName.json"
        ParametersToBeLoaded_PrototypesIngeniaSerialNumberToJointEnglishName_Dict = LoadAndParseJSONfile_AddDictKeysToGlobalsDict(globals(), JSONfilepathFull_PrototypesIngeniaSerialNumberToJointEnglishName, 1, 1)
        #################################

        #################################
        PrototypesIngeniaSerialNumberToJointEnglishNameDict_TEMP = deepcopy(PrototypesIngeniaSerialNumberToJointEnglishNameDict)
        for Key in PrototypesIngeniaSerialNumberToJointEnglishNameDict_TEMP:
            PrototypesIngeniaSerialNumberToJointEnglishNameDict[int(Key)] = PrototypesIngeniaSerialNumberToJointEnglishNameDict[Key] #The IngeniaBLDC object wants to use integers as dict keys, but they have to be strings in the JSON file.
            PrototypesIngeniaSerialNumberToJointEnglishNameDict.pop(Key, None)
        #################################

        #################################
        IngeniaControllerProductCodeToEnglishNameDict_TEMP = deepcopy(IngeniaControllerProductCodeToEnglishNameDict)
        for Key in IngeniaControllerProductCodeToEnglishNameDict_TEMP:
            IngeniaControllerProductCodeToEnglishNameDict[int(Key)] = IngeniaControllerProductCodeToEnglishNameDict[Key] #The IngeniaBLDC object wants to use integers as dict keys, but they have to be strings in the JSON file.
            IngeniaControllerProductCodeToEnglishNameDict.pop(Key, None)
        #################################

        #print("PrototypesIngeniaSerialNumberToJointEnglishNameDict: " + str(PrototypesIngeniaSerialNumberToJointEnglishNameDict))
        #print("IngeniaControllerProductCodeToEnglishNameDict: " + str(IngeniaControllerProductCodeToEnglishNameDict))

    #######################################################################################################################

    #######################################################################################################################
    except:
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_PrototypesIngeniaSerialNumberToJointEnglishName, exceptions: %s" % exceptions)
        traceback.print_exc()
    #######################################################################################################################

#######################################################################################################################
#######################################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def FindAllIngeniaSlavesOnAllNetworkInterfaces():
    global PrototypesIngeniaSerialNumberToJointEnglishNameDict
    global IngeniaControllerProductCodeToEnglishNameDict

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    try:

        IngeniaMotionControllerObject = MotionController()

        NetworkInterface_List = IngeniaMotionControllerObject.communication.get_interface_name_list()

        NetworkInterface_Dict = dict()

        ##########################################################################################################
        print("### Start of NetworkInterface_List:\n")
        for IntegerIndex, EnglishName in enumerate(NetworkInterface_List):
            print(str(IntegerIndex) + ": " + str(EnglishName) + "\n")
        print("### End of NetworkInterface_List:\n")
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        for NetworkInterface_Index, NetworkInterface_Name in enumerate(NetworkInterface_List):

            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            NetworkInterface_Identifier = IngeniaMotionControllerObject.communication.get_ifname_by_index(NetworkInterface_Index)

            NetworkInterface_Dict[NetworkInterface_Name] = dict([("NetworkInterface_Name", NetworkInterface_Name),
                                                                 ("NetworkInterface_Index", NetworkInterface_Index),
                                                                 ("NetworkInterface_Identifier", NetworkInterface_Identifier),
                                                                 ("DetectedSlaves_DictOfDicts", dict())])
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

                try:
                    DetectedSlaveID_List = IngeniaMotionControllerObject.communication.scan_servos_ethercat(NetworkInterface_Identifier) #unicorn
                except:
                    DetectedSlaveID_List = []

                #print("DetectedSlaveID_List: " + str(DetectedSlaveID_List))
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                ##########################################################################################################
                if len(DetectedSlaveID_List) > 0:

                    #print("SUCCESS: 'FindAllIngeniaSlavesOnAllNetworkInterfaces, IngeniaMotionControllerObject.communication.scan_servos_ethercat(NetworkInterface_Identifier)', NetworkInterface_Name = " + NetworkInterface_Name + ", DetectedSlaveID_List = " + str(DetectedSlaveID_List))

                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    ##########################################################################################################
                    try:

                        ##########################################################################################################
                        ##########################################################################################################
                        ##########################################################################################################
                        for SlaveID_Int in DetectedSlaveID_List:

                            ##########################################################################################################
                            ##########################################################################################################
                            try:
                                IngeniaMotionControllerObject.communication.connect_servo_ethercat(NetworkInterface_Identifier, SlaveID_Int, XDFfileDictionaryPath) #unicorn

                                IngeniaControllerConfirmedFlag = 1

                                NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int] = dict([("serial_number", -1),
                                                                                                                                ("vendor_id", -1),
                                                                                                                                ("product_code", -1),
                                                                                                                                ("product_name", "unknown"),
                                                                                                                                ("fw_version", -1)])

                                NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["DetectedSlaveID_Int"] = SlaveID_Int

                                try:
                                    NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["serial_number"] = int(IngeniaMotionControllerObject.configuration.get_serial_number()) #unicorn
                                    NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["vendor_id"] = int(IngeniaMotionControllerObject.configuration.get_vendor_id())
                                    NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["product_code"] = int(IngeniaMotionControllerObject.configuration.get_product_code())
                                    NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["fw_version"] = IngeniaMotionControllerObject.configuration.get_fw_version()
                                except:
                                    pass

                                if NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["product_code"] in IngeniaControllerProductCodeToEnglishNameDict:
                                    NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["product_name"] = IngeniaControllerProductCodeToEnglishNameDict[NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["product_code"]]

                                ###################################################
                                for KnownSerialNumberFromCuratedList in PrototypesIngeniaSerialNumberToJointEnglishNameDict:

                                    if NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["serial_number"] == KnownSerialNumberFromCuratedList:
                                        NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["PrototypesIngeniaSerialNumberToJointEnglishNameDict"] = deepcopy(PrototypesIngeniaSerialNumberToJointEnglishNameDict[KnownSerialNumberFromCuratedList])
                                        break
                                    else:
                                        NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaves_DictOfDicts"][SlaveID_Int]["PrototypesIngeniaSerialNumberToJointEnglishNameDict"] = dict([("PrototypeName", "Uknown"),
                                                                                                                                                                                               ("JointName", "Unknown"),
                                                                                                                                                                                               ("DesiredSlaveID_Int", -1)])
                                ###################################################

                            ##########################################################################################################
                            ##########################################################################################################

                            ##########################################################################################################
                            ##########################################################################################################
                            except:
                                pass
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
                        print("FindAllIngeniaSlavesOnAllNetworkInterfaces, NetworkInterface_Name = " + NetworkInterface_Name + ", connect_servo_ethercat, exceptions: %s" % exceptions)
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
                else:
                    IngeniaControllerConfirmedFlag = 0
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
            ##########################################################################################################
            ##########################################################################################################
            except:
                exceptions = sys.exc_info()[0]
                #print("FindAllIngeniaSlavesOnAllNetworkInterfaces, NetworkInterface_Name = " + NetworkInterface_Name + ", scan_servos_ethercat, exceptions: %s" % exceptions)
                #traceback.print_exc()

                DetectedSlaveID_List = []
                IngeniaControllerConfirmedFlag = 0
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################
            ##########################################################################################################

            NetworkInterface_Dict[NetworkInterface_Name]["DetectedSlaveID_List"] = DetectedSlaveID_List
            NetworkInterface_Dict[NetworkInterface_Name]["IngeniaControllerConfirmedFlag"] = IngeniaControllerConfirmedFlag

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
            for NetworkInterface_Name in NetworkInterface_Dict:


                if NetworkInterface_Dict[NetworkInterface_Name]["IngeniaControllerConfirmedFlag"] == 1:
                    print("##########")
                    print(ConvertDictToProperlyFormattedStringForPrinting(NetworkInterface_Dict[NetworkInterface_Name], NumberOfDecimalsPlaceToUse=3, NumberOfEntriesPerLine=1, NumberOfTabsBetweenItems=3, PrintPlusSignFlag=0))
                    print("##########\n")
                else:
                    pass
                    #print("########## " + NetworkInterface_Name + " ##########\n")

        except:
            exceptions = sys.exc_info()[0]
            print("FindAllIngeniaSlavesOnAllNetworkInterfaces, printing NetworkInterface_Dict, exceptions: %s" % exceptions)
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
        print("FindAllIngeniaSlavesOnAllNetworkInterfaces, outermost exceptions: %s" % exceptions)
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
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    print("Starting 'FindAllSlaves_IngeniaBLDC_ReubenPython3Class.py'.")

    ##########################################################################################################
    ##########################################################################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    XDFfileDictionaryPath = os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "cap-xcr-e_eoe_2.4.1.xdf"
    #XDFfileDictionaryPath = os.getcwd() + "\\InstallFiles_and_SupportDocuments\\" + "den-xcr-e_eoe_2.5.0.xdf"

    ParametersToBeLoaded_Directory_TO_BE_USED = os.getcwd().replace("\\", "//") + "//ParametersToBeLoaded"

    PrintDebugFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    global PrototypesIngeniaSerialNumberToJointEnglishNameDict
    global IngeniaControllerProductCodeToEnglishNameDict

    try:

        if EXIT_PROGRAM_FLAG == 0:
            LoadAndParseJSONfile_PrototypesIngeniaSerialNumberToJointEnglishName()

        EXIT_PROGRAM_FLAG = 0
    except:
        exceptions = sys.exc_info()[0]
        print("LoadAndParseJSONfile_PrototypesIngeniaSerialNumberToJointEnglishName, exceptions: %s" % exceptions)
        traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    while(EXIT_PROGRAM_FLAG == 0):

        try:

            ##########################################################################################################
            FindAllIngeniaSlavesOnAllNetworkInterfaces()
            UserInput = input("Press ENTER if you would like to scan again; press 0 if you would like to exit.")
            if UserInput == "0":
                EXIT_PROGRAM_FLAG = 1
            ##########################################################################################################

        except:
            exceptions = sys.exc_info()[0]
            print("FindAllIngeniaSlavesOnAllNetworkInterfaces, while(EXIT_PROGRAM_FLAG == 0): section, exceptions: %s" % exceptions)
            #traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    print("Ending 'FindAllSlaves_IngeniaBLDC_ReubenPython3Class.py'.")

##########################################################################################################
##########################################################################################################
##########################################################################################################