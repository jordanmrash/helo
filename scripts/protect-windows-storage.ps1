param([Parameter(Mandatory=$true)][string]$DatabaseDirectory,[Parameter(Mandatory=$true)][string]$ServiceIdentity)
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$dir=[IO.Path]::GetFullPath($DatabaseDirectory)
if(!(Test-Path -LiteralPath $dir -PathType Container)){New-Item -ItemType Directory -Path $dir|Out-Null}
& icacls.exe $dir /inheritance:r /grant:r "${ServiceIdentity}:(OI)(CI)F" "BUILTIN\Administrators:(OI)(CI)F" /remove:g "BUILTIN\Users" "Authenticated Users" /T /C
if($LASTEXITCODE -ne 0){throw "ACL provisioning failed"}
& icacls.exe $dir /verify /T /C
if($LASTEXITCODE -ne 0){throw "ACL verification failed"}
Write-Output "HELO_NTFS_ACL_VERIFIED path=$dir identity=$ServiceIdentity"
