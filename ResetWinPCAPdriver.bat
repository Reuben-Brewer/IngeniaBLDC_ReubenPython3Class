REM This is a comment. First we CD into the disk drive (like "C" or "G"), so that our fullpath python commands will work.
REM This is a comment. Second we CD into the specific code working directory so that running this BAT file from the command prompt will keep us in the same directory.
REM This is a comment. We could issue the fullpath python command without this second CD into the specific folder, but then we'd be changed to "C:" or "G:" instead of our code directory.

set CurrentDiskDrive=%CD:~0,3%
set CurrentDirectoryFullPath=%~dp0

echo "CurrentDiskDrive:%CurrentDiskDrive%"
echo "CurrentDirectoryFullPath:%CurrentDirectoryFullPath%"

cd %CurrentDiskDrive%
cd %CurrentDirectoryFullPath%

python "%CurrentDirectoryFullPath%ResetWinPCAPdriver.py"

TIMEOUT 1