import shlex
import subprocess

def execute_cmd(args, useBash = False, printOutput=True):
    """
    Execute the external command and get its exitcode, stdout are yield.
    """

    if useBash:
        args = 'bash.exe -c "' + ' '.join(args) + '"'
    
    print('running: ' + str(args))

    if printOutput:
        popen = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ''):
            print(stdout_line, end='')

        popen.stdout.close()
    else:
        popen = subprocess.Popen(args)

    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, args)

