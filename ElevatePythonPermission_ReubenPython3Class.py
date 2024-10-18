# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision A, 10/17/2024

Verified working on: Python 3.12 for Windows 10 64-bit.
'''

__author__ = 'reuben.brewer'

###########################################################
import os
import sys
import ctypes
import time
import datetime
import traceback
###########################################################

class ElevatePythonPermission_ReubenPython3Class():

    ##########################################################################################################
    ##########################################################################################################
    def RunPythonAsAdmin():

        #Bottom-most answer from this thread: https://stackoverflow.com/questions/19672352/how-to-run-script-with-elevated-privilege-on-windows

        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("ElevatePythonPermission_ReubenPython3Class, RunPythonAsAdmin: Requesting Admin rights.")
            args = f'"{sys.argv[0]}" {" ".join(sys.argv[1:])}'
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, args, None, 1)
    ##########################################################################################################
    ##########################################################################################################
