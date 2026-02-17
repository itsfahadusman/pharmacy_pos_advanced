Set WshShell = CreateObject("WScript.Shell")

' Run BAT file hidden
WshShell.Run """" & WScript.ScriptFullName & "\..\pharmacy.bat""", 0

' Wait 2 seconds
WScript.Sleep 2000

' Open browser
WshShell.Run "http://127.0.0.1:5002"
