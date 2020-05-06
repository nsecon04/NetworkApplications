import subprocess

#subprocess.Popen('powershell.exe [my command')
#subprocess.call("ipconfig")             # Pass string to cmd
cmd = ("get-ItemPropertyValue -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\SecurityProviders\SCHANNEL\Protocols\TLS 1.0\Client' -Name 'Enabled'")
process = subprocess.Popen(["powershell", cmd], stdout=subprocess.PIPE);
answer = process.communicate()[0]
#answer = str(answer.decode())
print(answer)
#print(type(answer))
