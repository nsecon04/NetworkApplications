import subprocess
from subprocess import run
import os

process = subprocess.Popen(['ping', '-c 4', 'python.org'],
                           stdout=subprocess.PIPE,
                           universal_newlines=True)

while True:
    output = process.stdout.readline()
    print(output.strip())
    # Do something else
    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        # Process has finished, read rest of the output
        for output in process.stdout.readlines():
            print(output.strip())
        break

process = subprocess.run(['echo', 'Even more output'],
                         stdout=subprocess.PIPE,
                         universal_newlines=True)
process

import subprocess as Popen
import subprocess as sp
password = b''
prog = sp.Popen(['runas', '/noprofile', '/user:Administrator'],stdin=sp.PIPE)
prog.stdin.write(password)
prog.communicate()