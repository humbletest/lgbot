python sbuild.py
start "temp" d
timeout /t 1
taskkill /IM cmd.exe /FI "WINDOWTITLE eq temp*"
taskkill /IM cmd.exe /FI "WINDOWTITLE eq debugger*"