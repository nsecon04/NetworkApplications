import subprocess

#try:
#Checking Memory
#   output = subprocess.check_output(
#              ["powershell.exe", "Get-Counter",
#               "-Counter "+r'"\memory\available mbytes"',
#               "-MaxSamples 10", "-SampleInterval 1"],
#              shell=True)
#except subprocess.CalledProcessError as e:
#    print ("subproces CalledProcessError.output =", e.output)
#print (output.decode())

# Checking ipconfig
with subprocess.Popen(["ipconfig"], stdout=subprocess.PIPE) as proc:
    print((proc.stdout.read()).decode())

#subprocess.Popen('powershell.exe [my command')
subprocess.call("ipconfig")             # Pass string to cmd

# Access 64-bit ps from 32-bit
powershell64 = os.path.join(os.environ['SystemRoot'],
    'SysNative' if platform.architecture()[0] == '32bit' else 'System32',
    'WindowsPowerShell', 'v1.0', 'powershell.exe')