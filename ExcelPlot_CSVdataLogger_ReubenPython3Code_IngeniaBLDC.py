# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision P, 1/29/2026

Verified working on: Python 3.11/12/13 for Windows 10, 11 64-bit.
'''

__author__ = 'reuben.brewer'

#########################################################
import os
import sys
import traceback
import time
import datetime
from collections import OrderedDict
from copy import deepcopy
import glob #For getting a list of files in a directory with a certain extension
import subprocess
import platform
import argparse
import pandas
#########################################################

######################################################### For commanding Excel as a program
if platform.system() == "Windows":
    import win32com.client
#########################################################

######################################################### For writing excel files.
import xlwt
#########################################################

######################################################### For copying excel file when we create the excel file. HAVE TO INSTALL SEPARATELY FROM XLWT/XLRD.
from xlutils.copy import copy
#########################################################

#########################################################
#http://xlsxwriter.readthedocs.io/chart.html FOR MAKING CHARTS
#XlsxWriter can only create new files. It cannot read or modify existing files. Can only handle xlsx files, not xls
import xlsxwriter
#########################################################

##########################################################################################################
##########################################################################################################
def OpenXLSsndCopyDataToLists(FileName_full_path):

    DataOrderedDict = OrderedDict()

    try:

        ##########################################################################################################
        workbook = pandas.ExcelFile(FileName_full_path)

        sheet = workbook.parse("Sheet1")

        NumberOfRows = sheet.shape[0]
        NumberOfColumns = sheet.shape[1]

        header_variable_name_list = sheet.columns.values.tolist()
        for index, VariableName in enumerate(header_variable_name_list):

            if header_variable_name_list[index] == "NoteToAddToFile":
                pass

            header_variable_name_list[index] = VariableName.strip()

        print("Detected the following variable names: " + str(header_variable_name_list))
        ##########################################################################################################

        ##########################################################################################################
        ListOfColumnDataLists = []
        for column in range(0, NumberOfColumns):  # Iterate through columns
            ListOfColumnDataLists.append([])
        ##########################################################################################################

        ##########################################################################################################
        for row in range(0, NumberOfRows): # Iterate through rows
            for column in range(0, NumberOfColumns):  # Iterate through columns
                cell_value = sheet.iat[row, column]  # Get cell object by row, col
                ListOfColumnDataLists[column].append(cell_value.item()) #.item() converts numpy data types to regular python types, important for linux
        ##########################################################################################################

        ##########################################################################################################
        for column in range(0, NumberOfColumns):  # Iterate through columns
            DataOrderedDict[header_variable_name_list[column]] = ListOfColumnDataLists[column]
        ##########################################################################################################

        return DataOrderedDict

    except:
        exceptions = sys.exc_info()[0]
        print("OpenXLSsndCopyDataToLists, exceptions: %s" % exceptions)
        #traceback.print_exc()
        return DataOrderedDict

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def CreateExcelChart(FileName_to_save_full_path, DataOrderedDictToWrite):

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    try:

        ########################################################################################################## unicorn
        CSVdataLogger_VariableNamesForHeaderList = ["Time (S)",
                                                    "Position (Deg) Slave 1",
                                                    "Current Quadrature (A) Slave 1"]
        ##########################################################################################################

        ##########################################################################################################
        if CSVdataLogger_VariableNamesForHeaderList[0].lower().find("time") != -1:
            CSVdataLogger_VariableNamesForHeaderList[0] = "Time"
        ##########################################################################################################

        ##########################################################################################################
        workbook = xlsxwriter.Workbook(FileName_to_save_full_path, {"nan_inf_to_errors": True}) #Prevents "TypeError: NAN/INF not supported in write_number() without 'nan_inf_to_errors' Workbook() option"
        worksheet = workbook.add_worksheet()
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        AlphabetStringList = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                              "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ",
                              "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT", "BU", "BV", "BW", "BX", "BY", "BZ", ]

        numerical_index = 0
        NumberOfDataRows = -1
        for key in DataOrderedDictToWrite:

            starting_cell_string_identifier = AlphabetStringList[numerical_index] + "1"
            worksheet.write_column(starting_cell_string_identifier, [key] + DataOrderedDictToWrite[key])
            NumberOfDataRows = len(DataOrderedDictToWrite[key])
            worksheet.set_column(numerical_index, numerical_index, 20) #set column width of current column to 20

            numerical_index = numerical_index + 1
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ###########################################################################################################
        VariableNameVsExcelColumnLetterDict = dict()
        for Index, VariableName in enumerate(CSVdataLogger_VariableNamesForHeaderList):
            VariableNameVsExcelColumnLetterDict[VariableName] = AlphabetStringList[Index]
        ##########################################################################################################
        ##########################################################################################################

        ########################################################################################################## unicorn
        ##########################################################################################################
        VariableNamesListToInludeOnSinglePlotVsTime = ["Position (Deg) Slave 1", "Current Quadrature (A) Slave 1"]

        ##########################################################################################################
        LengthMax = 31 - 10  # Excel worksheet name must be <= 31 chars.
        VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited = list()
        SumOfAllVariableNamesAsString = ""
        for index, VariableName in enumerate(VariableNamesListToInludeOnSinglePlotVsTime):
            if len(VariableName) >= LengthMax: #Limit each, individual name for when it's printed on the plot
                VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited.append(VariableName[0:LengthMax])
            else:
                VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited.append(VariableName)

            if index != len(VariableNamesListToInludeOnSinglePlotVsTime) - 1:
                SumOfAllVariableNamesAsString = SumOfAllVariableNamesAsString + VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited[index] + ", "
            else:
                SumOfAllVariableNamesAsString = SumOfAllVariableNamesAsString + VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited[index]

        SumOfAllVariableNamesAsString = SumOfAllVariableNamesAsString[0:LengthMax] #Limit the overall Plot title length
        ##########################################################################################################

        print("VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited: " + str(VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited))
        print("SumOfAllVariableNamesAsString: " + str(SumOfAllVariableNamesAsString) + ", Length = " + str(len(SumOfAllVariableNamesAsString)))

        VariableName_vs_Time_Xaxis_Chart_sheet = workbook.add_chartsheet(SumOfAllVariableNamesAsString + " vs Time")
        VariableName_vs_Time_Xaxis_Chart = workbook.add_chart({'type': 'scatter'}) #http://xlsxwriter.readthedocs.io/example_chart_scatter.html

        ##########################################################################################################
        for index, VariableName in enumerate(VariableNamesListToInludeOnSinglePlotVsTime):
            VariableName_vs_Time_Xaxis_Chart.add_series({'name': VariableNamesListToInludeOnSinglePlotVsTime_NameLengthLimited[index] + ' vs Time','categories': "=Sheet1!$" + VariableNameVsExcelColumnLetterDict["Time"] + "$2:$" + VariableNameVsExcelColumnLetterDict["Time"] + "$"+str(NumberOfDataRows+1),'values': "=Sheet1!$" + VariableNameVsExcelColumnLetterDict[VariableName] + "$2:$" + VariableNameVsExcelColumnLetterDict[VariableName] + "$" + str(NumberOfDataRows+1)}) #X VALUES FIRST, THEN Y
        ##########################################################################################################

        VariableName_vs_Time_Xaxis_Chart.set_title ({'name': SumOfAllVariableNamesAsString + ' vs Time'})
        VariableName_vs_Time_Xaxis_Chart.set_x_axis({'name': 'Time (S)'})
        VariableName_vs_Time_Xaxis_Chart.set_y_axis({'name': SumOfAllVariableNamesAsString})
        VariableName_vs_Time_Xaxis_Chart_sheet.set_chart(VariableName_vs_Time_Xaxis_Chart)

        workbook.close()
        time.sleep(0.05)
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        if platform.system() == "Windows": #In windows, this makes the Excel-file open without any compatability-warnings. However, it's not strictly necessary.

            pywin32_FileName_xls = FileName_to_save_full_path
            pywin32_FileName_xls = pywin32_FileName_xls.replace("/", "\\") #This line is needed or else the Excel file will give you an error.

            xl = win32com.client.Dispatch("Excel.Application")
            xl.DisplayAlerts = False
            wb = xl.Workbooks.Open(pywin32_FileName_xls)
            wb.SaveAs(pywin32_FileName_xls, FileFormat = 56)
            wb.Close()
            xl.Quit()
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
        print("CreateExcelChart, exceptions: %s" % exceptions)
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
if __name__ == '__main__':

    global DataOrderedDictFromOriginalFile

    global FileDirectory
    FileDirectory = ""

    global ShowPlotOfMostRecentFileAtEndOfProgramFlag
    ShowPlotOfMostRecentFileAtEndOfProgramFlag = 1

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    print("$$$$$$$$$$$$$$$$")
    print("RUN THIS PROGRAM FROM COMMAND LINE LIKE THIS: 'python ExcelPlot_CSVdataLogger_ReubenPython3Code.py -f 'CSV-FILE-DIRECTORY-FULL-PATH' -o '0 or 1 ShowPlotOfMostRecentFileAtEndOfProgramFlag'.")
    print("$$$$$$$$$$$$$$$$")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    try:
        ARGV_Dict = dict()
        argparse_Object = argparse.ArgumentParser()
        argparse_Object.add_argument("-f", "--filepath", nargs='?', const='arg_was_not_given', required=False, help="Full filepath to CSV file.") #nargs='?', const='arg_was_not_given' is the key to allowing us to not input an argument (use Pycharm "run")
        argparse_Object.add_argument("-s", "--showplot", nargs='?', const='arg_was_not_given', required=False, help="Open the plotted data for the most-recent file at the end of the script.")
        ARGV_Dict = vars(argparse_Object.parse_args())

    ##########################################################################################################
    ##########################################################################################################
    except:
        exceptions = sys.exc_info()[0]
        print("argparse_Object, exceptions: %s" % exceptions)
        traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    if "filepath" in ARGV_Dict and ARGV_Dict["filepath"] != None:
        FileDirectory = str(ARGV_Dict["filepath"])

    else:

        if platform.system() == "Windows":
            #FileDirectory = os.getcwd() + "\\CSVfiles"
            FileDirectory = "C:\\CSVfiles"

        else:
            FileDirectory = os.getcwd() + "//CSVfiles" #Linux requires the opposite-direction slashes

    print("FileDirectory: " + str(FileDirectory))
    ##########################################################################################################

    ##########################################################################################################
    if "showplot" in ARGV_Dict and ARGV_Dict["showplot"] != None:
        ShowPlotOfMostRecentFileAtEndOfProgramFlag = int(ARGV_Dict["showplot"])

        if ShowPlotOfMostRecentFileAtEndOfProgramFlag not in [0, 1]:
            print("Error: ShowPlotOfMostRecentFileAtEndOfProgramFlag must be 0 or 1. Defaulting to 1.")
            ShowPlotOfMostRecentFileAtEndOfProgramFlag = 1

    print("ShowPlotOfMostRecentFileAtEndOfProgramFlag: " + str(ShowPlotOfMostRecentFileAtEndOfProgramFlag))
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
    if FileDirectory.find(":") == -1 and FileDirectory.find("/") == -1:
        print("ERROR: You must specify the FULL path, starting from the disk drive like 'C:'")
        exit()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    FileSuffixForChartFile = "_with_chart.xls"

    FileList_csv = glob.glob(FileDirectory + '/*.csv')
    FileList_xls = glob.glob(FileDirectory + '/*.xls')

    print("Found " + str(len(FileList_csv)) + " .csv files and " + str(len(FileList_xls)) + " .xls files.")
    #print("FileList_csv: " + str(FileList_csv))
    #print("FileList_xls: " + str(FileList_xls))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    for index, FileName_csv in enumerate(FileList_csv):
        FileName_xls = FileName_csv.replace(".csv", ".xls")
        FileName_WITH_CHART_xls = FileName_csv.replace(".csv", FileSuffixForChartFile)

        ##########################################################################################################
        ##########################################################################################################
        if FileName_xls not in FileList_xls: #Make sure we haven't already converted this csv to a xls file.

            print("Converting CSV file to xls file for " + FileName_csv)
            read_file = pandas.read_csv(FileName_csv)
            read_file.to_excel(FileName_xls, index=None, header=True, engine="xlsxwriter")

        else:
            print("xls file '" + FileName_xls + "' already exists so skipping csv-xls conversion.")
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        if FileName_WITH_CHART_xls not in FileList_xls: #Make sure we haven't already created a chart file for this csv.

            print("Creating xls chart file for " + FileName_csv)

            DataOrderedDictFromOriginalFile = OpenXLSsndCopyDataToLists(FileName_xls)

            CreateExcelChart(FileName_WITH_CHART_xls, DataOrderedDictFromOriginalFile)

        else:
            print("xls chart file already exists so skipping for " + FileName_csv)
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        if ShowPlotOfMostRecentFileAtEndOfProgramFlag == 1:

            ##########################################################################################################
            if platform.system() == "Windows":
                MostRecentFileIndex = len(FileList_csv) - 1
            else:
                MostRecentFileIndex = 0  # glob reverses the expected order in Linux over Windows.
            ##########################################################################################################

            ##########################################################################################################
            if index == MostRecentFileIndex:

                ######################################
                if platform.system() == "Windows":
                    cmd = "start Excel \"" + FileName_WITH_CHART_xls + "\""
                else:
                    cmd = "libreoffice " + FileName_WITH_CHART_xls
                ######################################

                ######################################
                print("cmd: " + cmd)
                subprocess.Popen(cmd, shell=True)
                ######################################

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

