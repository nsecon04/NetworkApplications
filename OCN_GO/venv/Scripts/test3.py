import subprocess


credentials = "Get-Credential -Credential .\\administrator"
h_md5 = "set-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Hashes\MD5' -Name 'Enabled' -Value '0x00000001'"
successMsg = h_md5 + " : Apply Success : "
failedMsg = h_md5 + " : Apply Failed : "
connectCmd = "try {} catch {} finall"
#connectCmd = "try {" + h_md5 + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"
#connectCmd = "try {Enter-PSSession -ComputerName " + remoteserver + " -Credential " + credential + "; " + cmd + "; Write-Output " + successMsg + " } catch { Write-Output " + failedMsg + " } finally {}"
# invokeRemoteCmd1 = "Invoke-Command -ComputerName " + remoteserver + " -ScriptBlock { " + connectCmd + " }"
# invokeRemoteCmd = "Invoke-Command -ComputerName " + remoteserver + " -Credential " + credential + " -ScriptBlock { " + connectCmd + " }"
process = subprocess.Popen(["powershell", connectCmd], stdout=subprocess.PIPE);
answer = process.communicate()[0]
answer01 = str(answer.decode()).replace("\n", " ")
print(answer01)