Option Explicit
'==========================================================
' LANG : VBScript
' NAME : check_reboot_status.vbs
' AUTHOR : Patrick Ogenstad
' VERSION : 1.0
' DATE : 2014-02-09
' Description : Checks to see if a Windows server needs a reboot
'
' Nelmon Homepage:
' http://networklore.com/nelmon/
'
' Guidelines and updates:
' http://networklore.com/check-reboot-status/
'
' Feedback: Please send feedback:
' http://networklore.com/contact/
'
'==========================================================
'==========================================================

Dim objUpdateSystemInfo, blnRebootRequired
CONST rOK = 0
CONST rWarning = 1
CONST rCritical = 2
CONST rUnknown = 3

' Currently the plugin doesn't use any options please make your own 
' modifications if you need a different status

Set objUpdateSystemInfo = CreateObject("Microsoft.Update.SystemInfo")
blnRebootRequired = objUpdateSystemInfo.RebootRequired

If (blnRebootRequired = True) Then
	Wscript.Echo  "WARNING : A reboot is required"
	Wscript.Quit(rWarning)
Else
	Wscript.Echo  "OK : A reboot is not required"
	Wscript.Quit(rOK)
End If
