from inspyre_toolbox.syntactic_sweets import suppress_stdout, SUPPRESSED
from subprocess import run, PIPE
from sys import platform
import os

SUPPRESSED = SUPPRESSED


def noisy_operation_windows():
    with suppress_stdout():
        print(os.system('ipconfig /all'))



def noisy_operation_linux():
    with suppress_stdout():
        print(os.system('apt search python'))


def run_ops(op):
    global SUPPRESSED

    print('Running op without suppression first.')
    SUPPRESSED = False
    op()
    print('Now running with suppression')
    SUPPRESSED = True
    op()


if platform == "win32":
    op = noisy_operation_windows
elif platform == "linux":
    op = noisy_operation_linux

run_ops(op)
