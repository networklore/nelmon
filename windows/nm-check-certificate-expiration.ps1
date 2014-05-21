#==========================================================
# LANG : Powershell
# NAME : nm-check-certificate-expiration.ps1
# AUTHOR : Patrick Ogenstad
# VERSION : 1.0
# DATE : 2014-02-09
# Description : Checks to see a certificate is about to
# expire.
#
# Information: The Script is part of Nelmon (NetworkLore
# Monitoring Pack for Nagios)
# http://networklore.com/nelmon/
#
# Guidelines and updates:
# http://networklore.com/windows-certificate-expiration/
#
# Feedback: Please send feedback:
# http://networklore.com/contact/
#
#==========================================================
#==========================================================

Param(
 [int]$critical = 10,
 [switch]$help,
 [int]$warning = 20
)

$scriptversion = "1.0"

$CERTDIR = "Cert:\LocalMachine\My"

$bReturnOK = $TRUE
$bReturnCritical = $FALSE
$bReturnWarning = $FALSE
$returnStateOK = 0
$returnStateWarning = 1
$returnStateCritical = 2
$returnStateUnknown = 3
$nWarning = $warning
$nCritical = $critical

$dtCurrent = Get-Date

$strCritical = ""
$strWarning = ""

if ($help)
{
 Write-Output ""
 Write-Output "---------------------------------------------"
 Write-Output "nm-check-certificate-expiration.ps1 v.$scriptversion"
 Write-Output "---------------------------------------------"
 Write-Output ""
 Write-Output "Options:"
 Write-Output "-c or -critical (number)"
 Write-Output "-h or -help display help"
 Write-Output "-w or -warning (number)"
 Write-Output "" 
 Write-Output "Example:"
 Write-Output ".\nm-check-certificate-expiration.ps1 -c 4 -w 10"
 Write-Output ""
 Write-Output "For more information visit:"
 Write-Output "http://networklore.com/nelmon/"
 Write-Output "http://networklore.com/windows-certificate-expiration/"
 Write-Output ""
 exit $returnStateUnknown
} 


$objCertificates = Get-Childitem $CERTDIR

if (-Not $objCertificates)
{ 
 Write-Output "No Certificates Found"
 exit $bReturnOK
}

foreach ($objCertificate in $objCertificates)
{
 $dtRemain =  $objCertificate.NotAfter - $dtCurrent
 $nRemainDays = $dtRemain.Days
 
 if ($nRemainDays -lt 0)
 {
	$strCritical = $strCritical + "EXPIRED " + $objCertificate.SubjectName.Name.ToString() + " expired " + $objCertificate.NotAfter.ToString() + "`n"
	$bReturnCritical = $TRUE
 } Elseif ( $nRemainDays -lt $nCritical)
 {
    $strCritical = $strCritical +  "Critical " + $objCertificate.SubjectName.Name.ToString() + " expires " + $objCertificate.NotAfter.ToString() + "`n"
	$bReturnCritical = $TRUE
 } Elseif ( $nRemainDays -lt $nWarning)
 {
    $strWarning = $strWarning + "Warning " + $objCertificate.SubjectName.Name.ToString() + " expires " + $objCertificate.NotAfter.ToString() + "`n"
	$bReturnWarning = $TRUE
 } Else
 {
	#Nothing for now
 }

}

if ($bReturnCritical)
{
 write-output $strCritical
 write-output $strWarning
 exit $returnStateCritical
} elseif ($bReturnWarning)
{
 write-output $strWarning
 exit $returnStateWarning
} else
{
 write-output "OK"
 exit $returnStateOK
}
