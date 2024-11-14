###########################

IngeniaBLDC_ReubenPython3Class

Control class (including ability to hook to Tkinter GUI) for interfacing with Novanta, Ingenia BLDC motor controller (like Denali, Capitan, and Everest) through Ingenia's "ingeniamotion" Python module.

e.g. https://www.ingeniamc.com/servo-drives/capitan-xcr-panel-mount-ethercat/

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision E, 11/13/2024

Verified working on:

Python 3.12.

Windows 10, 11 64-bit

Note For test_program_for_IngeniaBLDC_ReubenPython3Class.py:

1.This is a slower way of interfacing with the controller and not the fast method of interfacing via an Ethercat Master like Beckhoff TwinCat or Acontis.
It uses PDO-callbacks for the majority of the data transfer (with only a smattering of SDO for infrequent calls, like gain setting), but it's still slower than
via an Ethercat Master like Beckhoff TwinCat or Acontis. Currently it's been verified as working well with up to 5 motors @ 50Hz Tx/Rx simultaneously as part of a larger
program with lots of other sensors/actuators being communicated with simultaneously.

2. You MUST install Ingenia's MotionLab3 BEFORE running this software, as this software relies on MotionLab3's EoE-service for the Ethercat communication.

3. If you're having trouble getting a motor to move with "test_program_for_IngeniaBLDC_ReubenPython3Class.py", then try "SimplestTest_SingleSlave_SDOnoPDO_IngeniaBLDC_ReubenPython3Class.py".

###########################

########################### Python module installation instructions, all OS's

Install WPcap 4.1.3 (https://www.winpcap.org/install/)

Install ingenialink-7.3.5-py3-none-any.whl (https://pypi.org/project/ingenialink/#files)

Alternatively, can issue the command "pip install ingenialink" (this will take care of installing the correct dependencies more than easily than when installing via the .whl file).

Second install ingeniamotion-0.8.5-py3-none-any.whl (https://pypi.org/project/ingeniamotion/#files)

Alternatively, can issue the command "pip install ingeniamotion" (this will take care of installing the correct dependencies more than easily than when installing via the .whl file).

############

test_program_for_IngeniaBLDC_ReubenPython3Class.py, ListOfModuleDependencies:

IngeniaBLDC_ReubenPython3Class, ListOfModuleDependencies: ['GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3', 'ingeniamotion', 'ingeniamotion.enums', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class']

IngeniaBLDC_ReubenPython3Class, ListOfModuleDependencies_TestProgram: ['CSVdataLogger_ReubenPython3Class', 'ElevatePythonPermission_ReubenPython3Class', 'EntryListWithBlinking_ReubenPython2and3Class', 'keyboard', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class']

IngeniaBLDC_ReubenPython3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil']

IngeniaBLDC_ReubenPython3Class, ListOfModuleDependencies_All:['CSVdataLogger_ReubenPython3Class', 'ElevatePythonPermission_ReubenPython3Class', 'EntryListWithBlinking_ReubenPython2and3Class', 'future.builtins', 'GetPIDsByProcessEnglishNameAndOptionallyKill_ReubenPython2and3', 'ingeniamotion', 'ingeniamotion.enums', 'keyboard', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'pexpect', 'psutil']

############

############

ExcelPlot_CSVdataLogger_ReubenPython3Code_IngeniaBLDC.py , ListOfModuleDependencies:

ExcelPlot_CSVdataLogger_ReubenPython3Code_IngeniaBLDC.py, ListOfModuleDependencies: ['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

ExcelPlot_CSVdataLogger_ReubenPython3Code_IngeniaBLDC.py, ListOfModuleDependencies_TestProgram: []

ExcelPlot_CSVdataLogger_ReubenPython3Code_IngeniaBLDC.py, ListOfModuleDependencies_NestedLayers: []

ExcelPlot_CSVdataLogger_ReubenPython3Code_IngeniaBLDC.py, ListOfModuleDependencies_All:['pandas', 'win32com.client', 'xlsxwriter', 'xlutils.copy', 'xlwt']

pip install pywin32         #version 305.1 as of 10/17/24

pip install xlsxwriter      #version 3.2.0 as of 10/17/24. Might have to manually delete older version from /lib/site-packages if it was distutils-managed. Works overall, but the function ".set_size" doesn't do anything.

pip install xlutils         #version 2.0.0 as of 10/17/24

pip install xlwt            #version 1.3.0 as of 10/17/24

############

###########################
