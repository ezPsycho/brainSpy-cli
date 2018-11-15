@ECHO OFF
SETLOCAL EnableDelayedExpansion

SET pathToInsert=%~dp0
SET newValue=%PATH%;%pathToInsert%;

IF "!path:%pathToInsert%=!" EQU "%path%" REG ADD HKEY_CURRENT_USER\Environment /F /V Path /D "%newValue%"
