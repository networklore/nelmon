Option Explicit
'==========================================================
' LANG : VBScript
' NAME : nm_check_available_updates.vbs
' AUTHOR : Patrick Ogenstad
' VERSION : 1.2.1
' DATE : 2014-02-09
' Description : Checks for available updates
'
' Nelmon Homepage:
' http://networklore.com/nelmon/
'
' Guidelines and updates:
' http://networklore.com/check-available-updates/
'
' Feedback: Please send feedback:
' http://networklore.com/contact/
'
'==========================================================
'==========================================================
' SCRIPT SETTINGS
'==========================================================
'==========================================================
Dim nRebootStatusOption
Dim cCriticalSecurityOption, cImportantSecurityOption
Dim cModerateSecurityOption, cLowSecurityOption
Dim cCriticalUpdateOption, cImportantUpdateOption
Dim wCriticalSecurityOption, wImportantSecurityOption
Dim wModerateSecurityOption, wLowSecurityOption
Dim wCriticalUpdateOption, wImportantUpdateOption
CONST rOK = 0
CONST rWarning = 1
CONST rCritical = 2
CONST rUnknown = 3

' If you don't want to use the default settings and don't want
' to allow arguments in NSClient++, allow_arguments=1 in NSC.ini
' you can change the default settings below. However in that case
' you need to do this on a per server basis instead of just using
' different services in Nagios.

nRebootStatusOption = rWarning
cCriticalSecurityOption = True
cImportantSecurityOption = False
cModerateSecurityOption = False
cLowSecurityOption = False
cCriticalUpdateOption = True
cImportantUpdateOption = False
wCriticalSecurityOption = False
wImportantSecurityOption = True
wModerateSecurityOption = True
wLowSecurityOption = True
wCriticalUpdateOption = False
wImportantUpdateOption = True



'==========================================================
'==========================================================
' VARIABLES AND DECLARATIONS
'==========================================================
'==========================================================


Dim objUpdateSession, objUpdateSearcher, colSearchResult, objUpdate, i, y
Dim strCriticalSecurity, strImportantSecurity, strModerateSecurity, strLowSecurity
Dim blnCriticalSecurity, blnImportantSecurity, blnModerateSecurity, blnLowSecurity

Dim strCriticalUpdate, strImportantUpdate
Dim blnCriticalUpdate, blnImportantUpdate
Dim strReturnSummary, strReturnDetails, strReturnText

Dim strScriptVersion
Dim nCriticalSecurity, nImportantSecurity, nModerateSecurity, nLowSecurity, nCriticalUpdate, nImportantUpdate
Dim bInvalidArgument, bDisplayHelp
strScriptVersion = "1.2"

Set objUpdateSession = CreateObject("Microsoft.Update.Session")
Set objUpdateSearcher = objUpdateSession.CreateUpdateSearcher()


blnCriticalSecurity = False
blnImportantSecurity = False


'==========================================================
'==========================================================
' MAIN BODY
'==========================================================
'==========================================================



' Get Options from user
GetOptions

If (bDisplayHelp) Then
	DisplayHelp
ElseIf (bInvalidArgument) Then
	DisplayInvalidArgument
Else
	CheckUpdates
End If


'==========================================================
'==========================================================
' SUBROUTINES AND FUNCTIONS
'==========================================================
'==========================================================


Sub CheckUpdates
	Dim colCategory, blnIsCritical
	Set colSearchResult = objUpdateSearcher.Search("IsInstalled=0 and Type='Software'")

	For i = 0 To colSearchResult.Updates.Count-1
		Set objUpdate = colSearchResult.Updates.Item(i)
		If (objUpdate.MsrcSeverity = "Critical") Then
			blnCriticalSecurity = True
			If (Len(strCriticalSecurity) = 0) Then
				strCriticalSecurity = "Critical Security Updates missing:" 
			End If
			strCriticalSecurity = strCriticalSecurity & vbCrLF & objUpdate.Title
			nCriticalSecurity = nCriticalSecurity + 1
		Elseif (objUpdate.MsrcSeverity = "Important") Then
			blnImportantSecurity = True
			If (Len(strImportantSecurity) = 0) Then
				strImportantSecurity = "Important Security Updates missing:"
			End If
			strImportantSecurity = strImportantSecurity & vbCrLF & objUpdate.Title
			nImportantSecurity = nImportantSecurity + 1
		Elseif (objUpdate.MsrcSeverity = "Moderate") Then
			blnModerateSecurity = True
			If (Len(strModerateSecurity) = 0) Then
				strModerateSecurity = "Moderate Security Updates missing:"
			End If
			strModerateSecurity = strModerateSecurity & vbCrLF & objUpdate.Title
			nModerateSecurity = nModerateSecurity + 1
		Elseif (objUpdate.MsrcSeverity = "Low") Then
			blnLowSecurity = True
			If (Len(strLowSecurity) = 0) Then
				strLowSecurity = "Low Security Updates missing:"
			End If
			strLowSecurity = strLowSecurity & vbCrLF & objUpdate.Title
			nLowSecurity = nLowSecurity + 1
		Elseif (objUpdate.AutoSelectOnWebSites = True) Then
			blnIsCritical = False
			For Each colCategory in objUpdate.Categories
				If (colCategory.Name = "Critical Updates") Then
					blnIsCritical = True
				End If
			Next
			If (blnIsCritical) Then
				blnCriticalUpdate = True
				If (Len(strCriticalUpdate) = 0) Then
					strCriticalUpdate = "Critical Updates missing:"
				End If
				strCriticalUpdate = strCriticalUpdate & vbCrLF & objUpdate.Title
				nCriticalUpdate = nCriticalUpdate + 1
			Else
				blnImportantUpdate = True
				If (Len(strImportantUpdate) = 0) Then
					strImportantUpdate = "Important Updates missing:"
				End If
				strImportantUpdate = strImportantUpdate & vbCrLF & objUpdate.Title
				nImportantUpdate = nImportantUpdate + 1
			End If
		End If
	Next

	If (blnCriticalSecurity) Then
		strReturnSummary = nCriticalSecurity & " Critical Security"
		strReturnDetails = strCriticalSecurity
	End If
	If (blnImportantSecurity) Then
		If (Len(strReturnSummary) = 0) Then
			strReturnSummary = nImportantSecurity & " Important Security"
		Else
			strReturnSummary = strReturnSummary & ", " & nImportantSecurity & " Important Security"
		End If
		If (Len(strReturnDetails) = 0) Then
			strReturnDetails = strImportantSecurity
		Else
			strReturnDetails = strReturnDetails & vbCrLf & strImportantSecurity
		End If		
	End If
	If (blnModerateSecurity) Then
		If (Len(strReturnSummary) = 0) Then
			strReturnSummary = nModerateSecurity & " Moderate Security"
		Else
			strReturnSummary = strReturnSummary & ", " & nModerateSecurity & " Moderate Security"
		End If
		If (Len(strReturnDetails) = 0) Then
			strReturnDetails = strModerateSecurity
		Else
			strReturnDetails = strReturnDetails & vbCrLf & strModerateSecurity
		End If		
	End If
	If (blnLowSecurity) Then
		If (Len(strReturnSummary) = 0) Then
			strReturnSummary = nLowSecurity & " Low Security"
		Else
			strReturnSummary = strReturnSummary & ", " & nLowSecurity & " Low Security"
		End If
		If (Len(strReturnDetails) = 0) Then
			strReturnDetails = strLowSecurity
		Else
			strReturnDetails = strReturnDetails & vbCrLf & strLowSecurity
		End If		
	End If

	If (blnCriticalUpdate) Then
		If (Len(strReturnSummary) = 0) Then
			strReturnSummary = nCriticalUpdate & " Critical Updates"
		Else
			strReturnSummary = strReturnSummary & ", " & nCriticalUpdate & " Critical Updates"
		End If
		If (Len(strReturnDetails) = 0) Then
			strReturnDetails = strCriticalUpdate
		Else
			strReturnDetails = strReturnDetails & vbCrLf & strCriticalUpdate
		End If		
	End If
	
	If (blnImportantUpdate) Then
		If (Len(strReturnSummary) = 0) Then
			strReturnSummary = nImportantUpdate & " Important Updates"
		Else
			strReturnSummary = strReturnSummary & ", " & nImportantUpdate & " Important Updates"
		End If
		If (Len(strReturnDetails) = 0) Then
			strReturnDetails = strImportantUpdate
		Else
			strReturnDetails = strReturnDetails & vbCrLf & strImportantUpdate
		End If		
	End If
	
	strReturnText = ""
	If (Len(strReturnSummary) > 0) Then
		strReturnText = strReturnSummary & vbCrLf & strReturnDetails
	End If
	If (Len(strReturnText) > 1023) Then
		strReturnText = Left(strReturnText, 1020) & "..."
	End If

	
	If (blnCriticalSecurity = True And cCriticalSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rCritical)
	Elseif (blnImportantSecurity = True And cImportantSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rCritical)
	Elseif (blnModerateSecurity = True And cModerateSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rCritical)
	Elseif (blnLowSecurity = True And cLowSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rCritical)
	Elseif (blnCriticalUpdate = True And cCriticalUpdateOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rCritical)
	Elseif (blnImportantUpdate = True And cImportantUpdateOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rCritical)
	Elseif (blnCriticalSecurity = True And wCriticalSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rWarning)
	Elseif (blnImportantSecurity = True And wImportantSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rWarning)
	Elseif (blnModerateSecurity = True And wModerateSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rWarning)
	Elseif (blnLowSecurity = True And wLowSecurityOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rWarning)
	Elseif (blnCriticalUpdate = True And wCriticalUpdateOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rWarning)
	Elseif (blnImportantUpdate = True And wImportantUpdateOption = True) Then
		Wscript.Echo strReturnText
		Wscript.Quit(rWarning)	
	Else
		Dim objUpdateSystemInfo, blnRebootRequired
		Set objUpdateSystemInfo = CreateObject("Microsoft.Update.SystemInfo")
		blnRebootRequired = objUpdateSystemInfo.RebootRequired
		
		If (blnRebootRequired = True And nRebootStatusOption > 0) Then
			Wscript.Echo "A reboot is required"
			Wscript.Quit(nRebootStatusOption)
		End If
		If (Len(strReturnText) > 0) Then
			Wscript.Echo strReturnText
		Else
			Wscript.Echo "OK: No Important or Critical patches missing (" & strScriptVersion & ")"
		End If
		Wscript.Quit(rOK)	
	End If
	
End Sub ' CheckUpdates

Sub DisplayHelp
	WScript.Echo "Check Available Updates v." & strScriptVersion
	Wscript.Echo "----------------------------------------------"
	WScript.Echo "http://networklore.com/check-available-updates"
	Wscript.Echo "----------------------------------------------"
	WScript.Echo "Usage: cscript.exe check_available_updates.vbs [options]"
	WScript.Echo "Examples: "
	Wscript.Echo " cscript.exe check_available_updates.vbs.vbs -cSs -wCiml"
	Wscript.Echo "  - Return CRITICAL for Critical and Important Security Updates,"
	Wscript.Echo "    return WARNING for missing critical updates and important updates,"
	Wscript.Echo "    and moderate or low security updates"
	Wscript.Echo ""
	WScript.Echo " cscript.exe check_available_updates.vbs.vbs -c -wSs"
	Wscript.Echo "  - Return WARNING for Critical and Important Security Updates,"
	Wscript.Echo "    return OK for other updates, including moderate or low security"
	Wscript.Echo "    updates"
	Wscript.Echo ""
	WScript.Echo " cscript.exe check_available_updates.vbs.vbs -rc"
	Wscript.Echo "  - Default settings for updates, return CRITICAL if a reboot is"
	Wscript.Echo "    required"
	WScript.Echo ""
	WScript.Echo "Options"
	WScript.Echo " -c	- Critical Options (Default: -ccU)"
 	WScript.Echo "   c	- Critical Security Updates (MSRC Rating)"
	WScript.Echo "   i	- Important Security Update"
	WScript.Echo "   m	- Moderate Security Update"
	WScript.Echo "   l	- Low Security Update"
	WScript.Echo "   U	- Critical Update (not security related)"
	WScript.Echo "   u	- Important Update (not security related)"
	WScript.Echo " -w	- Warning Options (Default: -wimlu)"
 	WScript.Echo "   c	- Critical Security Updates (MSRC Rating)"
	WScript.Echo "   i	- Important Security Update"
	WScript.Echo "   m	- Moderate Security Update"
	WScript.Echo "   l	- Low Security Update"
	WScript.Echo "   U	- Critical Update (not security related)"
	WScript.Echo "   u	- Important Update (not security related)"
 	WScript.Echo " -r	- Set reboot required check (Default: -rw)"
	WScript.Echo "   c	- Return CRITICAL if a reboot is required"
	WScript.Echo "   o	- Return OK if a reboot is required"
	WScript.Echo "   w	- Return WARNING if a reboot is required"
	WScript.Echo "        (The reboot status is only shown if updates aren't missing)"
 	'WScript.Echo " -v	- Check for latest version (requires Internet access)"
 	WScript.Echo VbCrLf
 	WScript.Echo " -h	- Display help"
	Wscript.Quit(rUnknown)
End Sub ' DisplayHelp


Sub GetOptions()
	Dim objArgs, nArgs

	Set objArgs = WScript.Arguments
	If (objArgs.Count > 0) Then
		For nArgs = 0 To objArgs.Count - 1
			SetOptions objArgs(nArgs)
		Next
	End If
End Sub ' GetOptions

Sub DisplayInvalidArgument()
	Wscript.Echo "Invalid arguments, check help with cscript.exe check_available_updates.vbs -h"
	Wscript.Quit(rUnknown)	
End Sub ' DisplayInvalidArgument

Sub SetOptions(strOption)
	Dim strFlag, strParameter
	Dim nArguments
	nArguments = Len(strOption)
	If (nArguments < 2) Then
		bInvalidArgument = True
	Else
		strFlag = Left(strOption,2)
		Select Case strFlag
			Case "-c"
				cCriticalSecurityOption = False
				cImportantSecurityOption = False
				cModerateSecurityOption = False
				cLowSecurityOption = False
				cCriticalUpdateOption = False
				cImportantUpdateOption = False
				If (nArguments > 2) Then
					For i = 3 To nArguments
						strParameter = Mid(strOption,i,1)
						Select Case strParameter
							Case "c"
								cCriticalSecurityOption = True
							Case "i"
								cImportantSecurityOption = True
							Case "m"
								cModerateSecurityOption = True
							Case "l"
								cLowSecurityOption = True
							Case "U"
								cCriticalUpdateOption = True
							Case "u"
								cImportantUpdateOption = True
							Case Else
								bInvalidArgument = True
						End Select
					Next
				End If
			Case "-w"
				wCriticalSecurityOption = False
				wImportantSecurityOption = False
				wModerateSecurityOption = False
				wLowSecurityOption = False
				wCriticalUpdateOption = False
				wImportantUpdateOption = False
				If (nArguments > 2) Then
					For i = 3 To nArguments
						strParameter = Mid(strOption,i,1)
						Select Case strParameter
							Case "c"
								wCriticalSecurityOption = True
							Case "i"
								wImportantSecurityOption = True
							Case "m"
								wModerateSecurityOption = True
							Case "l"
								wLowSecurityOption = True
							Case "U"
								wCriticalUpdateOption = True
							Case "u"
								wImportantUpdateOption = True
							Case Else
								bInvalidArgument = True
						End Select
					Next
				End If
			Case "-r"
				nRebootStatusOption = rOK
				If (nArguments > 2) Then
					For i = 3 To nArguments
						strParameter = Mid(strOption,i,1)
						Select Case strParameter
							Case "o"
								nRebootStatusOption = rOK
							Case "w"
								nRebootStatusOption = rWarning
							Case "c"
								nRebootStatusOption = rCritical
							Case Else
								bInvalidArgument = True
						End Select
					Next
				End If
			
			'Case "-v"
			'		bCheckVersion = True
			Case "-h"
				bDisplayHelp = True
			Case Else
				bInvalidArgument = True
		End Select
	End If
End Sub ' SetOptions


