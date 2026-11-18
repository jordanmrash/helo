param([Parameter(Mandatory=$true)][string]$OutputPath,[string]$KeyId="primary-2026-11")
Set-StrictMode -Version Latest
$ErrorActionPreference="Stop"
$bytes=New-Object byte[] 32
[Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
$protected=[Security.Cryptography.ProtectedData]::Protect($bytes,[Text.Encoding]::UTF8.GetBytes($KeyId),[Security.Cryptography.DataProtectionScope]::LocalMachine)
$obj=@{key_id=$KeyId;protected_key=[Convert]::ToBase64String($protected);scope="LocalMachine"}
[IO.File]::WriteAllText($OutputPath,($obj|ConvertTo-Json -Compress),[Text.UTF8Encoding]::new($false))
& icacls.exe $OutputPath /inheritance:r /grant:r "SYSTEM:F" "BUILTIN\Administrators:F"
if($LASTEXITCODE -ne 0){throw "Secret ACL failed"}
Write-Output "HELO_ROTATABLE_DPAPI_KEY_CREATED key_id=$KeyId path=$OutputPath"
