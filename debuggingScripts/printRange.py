#!/usr/bin/env python2.7

import gdb      #not stand alone

###################################### FUNCTIONS ##################################
#<editor-fold desc='initialize'>
#</editor-fold>
def initialize():
    print("\033[93mInitializing L2\n") #setting console to yellow
    gdb.execute("monitor reset init")
    gdb.execute("delete")
    gdb.execute("break config.c:39")
    gdb.execute("continue")
    gdb.execute('set pagination off')
    gdb.execute('set confirm off')
    pp('reset',"")

#<editor-fold desc='PP'>
'''
brief: colorises messages (strings)

'''
#</editor-fold>
def pp(type, string):
    if type == "blue":
        print('\033[34m' + string + '\033[0m')
    elif type == 'cyan':
        print("\033[96m" + string + '\033[0m')
    elif type == 'yellow':
        print("\033[93m" + string + '\033[0m')
    elif type == "red":
        print('\033[31m' + string + '\033[0m')
    elif type == "magenta":
        print('\033[95m' + string + '\033[0m')
    elif type == "green":
        print('\033[92m' + string + '\033[0m')
    elif type == "reset":
        print('\033[0m')
    else:
        print('\033[31m'+ "Wrong colour type:\t"+type+'\033[0m')


initialize()


pp('blue','NVIC->ISER')
for i in range(7):
    base = 0xE000E100 + (0x4*i)
    # print hex(base)
    gdb.execute("x /x " + str(base))

print("\n")
pp('blue','NVIC->IPR')
for i in range(59):
    base = 0xE000E400 + (0x4*i)
    # print hex(base)
    gdb.execute("x /x " + str(base))

# gdb.execute("x /x 0xE000E100")
# gdb.execute("x /x 0xE000E104")
