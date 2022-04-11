#!/usr/bin/env python2.7

import gdb      #not stand alone
import re       # string comparison
###################################### FUNCTIONS ##################################
#<editor-fold desc='initialize'>
#</editor-fold>
def initialize():
    print("\033[93mInitializing L2\n") #setting console to yellow
    gdb.execute("monitor reset init")
    gdb.execute("break main.c:10")
    gdb.execute("continue")
    pp('reset',"")

#<editor-fold desc='clock_check'>
'''
source: system_stm32f4xx.c
'''
#</editor-fold>
def clockReport(rcc_dict):
    debug = config["debug"]
    SWS = 0b0011 # sws mask
    SW = 0b1100 # sw mask
    PLLSRC = 1<<22
    PLLN = 0b111111111<<6
    PLLM = 0b111111
    PLLP = 0b11<<16
    HSE = 25000000
    HSI = 16000000

    SWS = int(rcc_dict["CFGR"], 2) & SWS
    # SW = (int(rcc_dict["CFGR"], 2) & SW) >> 2
    PLLSRC = (int(rcc_dict["PLLCFGR"], 2) & PLLSRC) >>22
    PLLN = (int(rcc_dict["PLLCFGR"], 2) & PLLN) >>6
    PLLM = (int(rcc_dict["PLLCFGR"], 2) & PLLM)
    PLLP = (((int(rcc_dict["PLLCFGR"], 2) & PLLP) >>16) + 1) *2

    if SWS == 0:
        pp("magenta",'System Clock: HSI')
    elif SWS == 1:
        pp("magenta",'System Clock: HSE')
    elif SWS == 2:
        pp("magenta",'System Clock: PLL')

    if PLLSRC == 0:
    	pp("magenta",'Oscillator Clock: HSI')
        freq = (HSI*PLLN)/(PLLM*PLLP)
    elif PLLSRC == 1:
        pp("magenta",'Oscillator Clock: HSE')
        freq = (HSE*PLLN)/(PLLM*PLLP)

    tmp = "PLL output clock frequency: "+str(freq)+"Hz"
    pp("magenta", tmp)

    if debug:
        print 'CFGR:\t',rcc_dict["CFGR"]
        print 'PLLCFGR:\t',rcc_dict["PLLCFGR"]
        print 'SWS:\t', SWS
        print 'SW:\t', SW
        print 'PLLSRC:\t', PLLSRC
        print 'PLLN:\t', PLLN
        print 'PLLM:\t', PLLM
        print 'PLLP:\t', PLLP

#<editor-fold desc='reg_query'>
'''
Brief:
    Converts gdb struct reply into a dictionary
        C sdtruct => Python dictionary

In: register name
Output:
    dictionary containing all fields
    note:
        if the register does not contain *:
                returns a binary number
                !: we may have to add if conditions, so we could skip some of the code

eg:
$3 = {MODER = 0x0, OTYPER = 0x0, OSPEEDR = 0x0, PUPDR = 0x0, IDR = 0x0, ODR = 0x0, BSRRL = 0x0, BSRRH = 0x0, LCKR = 0x0, AFR = {0x0, 0x0}}
dict = {"MODER":0, "OTYPER":0, "OSPEEDR":0, "PUPDR":0, "IDR":0, "ODR":0, "BSRRL":0, "BSRRH":0, "LCKR":0, "AFR":{0, 0}}
'''
#</editor-fold>
def reg_query(register):
    debug = config["debug"]
    gdbReply = gdb.execute("p /t"+register, False, True) #query to GDB
    pattern1 = re.compile('=\s(.*)$')   #gets everything between braces
    braces = pattern1.search(gdbReply).group(1) #everything including curly braces
    pattern2 = re.compile('([A-Z0-9]{1,})\s=')     #matching keys
    quotecoln = pattern2.sub(r'"\1":', braces) #adding quotes, and inserting colons
    pattern3 = re.compile(':(\s)')  #matching all spaces next to colons
    final = pattern3.sub(r':', quotecoln) #removing spaces

    if debug:
        message1 = "\nregister:\t" + register
        message2 = "\ngdbReply:\t" + gdbReply
        message3 = "\nbraces:\t" + braces
        message4 = "\nquotecoln:\t" + quotecoln
        message5 = "\nfinal:\t" + final
        pp("yellow", message1)
        pp("yellow", message2)
        pp("yellow", message3)
        pp("yellow", message4)
        pp("yellow", message5)

    Dict = eval(final)   #creates a dictionary with final content

    #deleting reserved keys
    patReserved = re.compile('(RESERVED)[0-9]{1,}')
    subregList = list(Dict.keys()) # get all key names: dictionary size change during iteration
    for key in subregList:
        found = patReserved.search(key)
        if found:
            # print("Keys:"+key)
            Dict.pop(key)

    # "Binary int" to binary
    for key in Dict:
        Dict[key] = bin(int(str(Dict[key]), 2))

    return Dict

#<editor-fold desc='availableRegs'>
'''
brief: this function scans the header file "stm32f4xx.h" for "defines|_BASE" terms on the second column
        in other words: this function load the registers "containing" rspective sub registers
Input: file
Output:
    regs: set containing registers related to a C struct
'''
#</editor-fold>
def availableRegs(file):
    regs = set()   #using a list, so we can append
    with open(file, 'rt') as f: #holding every line
        data = f.readlines()
        f.close()

    # !:not sure qhich one is better
    pattern = re.compile('\#define\s{1,}([a-zA-Z0-9_]{1,})_BASE')    #extracting register names
    # pattern = re.compile('\#define\s{1,}([a-zA-Z0-9_]{1,})\s{1,}[^_BASE]\s{1,}')    #extracting register names

    for line in data:
        debug = config["debug"]
        if debug:
            message = "line:\t" + line
            pp("yellow", message)
        found = pattern.search(line)
        if found:
            if debug:
                message = "found:\t" + found.group(1)
                pp("yellow", message)
            regs.add(found.group(1))
    if debug:
        regmessage = ' '.join(regs) #set to string
        pp("yellow", regmessage)
    return regs

#<editor-fold desc='printDict'>
'''
brief:
    Prints out the content of each incoming dictionary
    If the value is a set: prints each element
in: dictionary
out: NA
'''
#</editor-fold>
def printDict(register,dictionary):
    string = "{0:"+str(10)+"} {1}" #used for formating
    print('\033[34m') # setting console to blue
    print "\n\n"+register+":"
    for key in dictionary:
        if (isinstance(dictionary[key], set)):
            for element in dictionary[key]:
                print string.format(key, element)
        else:
            print string.format(key, dictionary[key])
    pp('reset','')

#<editor-fold desc='external_readfile'>
#</editor-fold>
def external_readfile(fileIn):
    with open(file, 'rt') as f:
            data = f.readlines()

#<editor-fold desc='structfind'>
'''
notes:
    it needs to be modiufied "gdb.execute": watch error order
In: C struct
Out: None
    It prints only on screen for now
'''
#</editor-fold>
def structfind(regs):
    for i in regs:
        i = '*'+i   #appending pointer to register value
        try:
            gdb.execute("p /t" + i)
            print(i+"\n\n")
        except gdb.error as err:
            pp("error","structfind error")

#<editor-fold desc='Class Pycounter'>

#</editor-fold>
class Pycounter:
  def __init__(self):
      self.create_gdbvar()

  def create_gdbvar(self):
      gdb.execute('init-if-undefined $pyCounter =0') #it will create $var only if it is not already

  def read_gdb_val(self):
      pycounter = gdb.execute('print $pyCounter', False, True)
      pattern_gdb_var = re.compile('=\s(\d){1,}$')
      pycounter = pattern_gdb_var.search(pycounter) #typecast1:searchType
      pycounter = int(pycounter.group(1)) #typecast2:int
      return pycounter

  def increase(self): #the increase is based on gdb
      gdbval = self.read_gdb_val() + 1
      gdb.execute('set $pyCounter='+str(gdbval))

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

#<editor-fold desc='write2file'>
'''
Set of dictionaries
'''
#</editor-fold>
def write2file(list):
    with open('ucshark.log', 'wt') as f:
        for item in list:
            print >> f, item
##################### CODE SECTION ########################### start ##########################
#<editor-fold desc='config'>
'''
centralized script configuration
file type:
    h stm32 header file
    e external pre parsed file

NOTE:
    !: it may need a function to verify configuration
'''
#</editor-fold>
config = {
  'debug': False,    # turns debug messages on
  'check': 'RCC',   # options: GPIO(A-J)|RCC|all|GPIOx
  'report': True,   # goes a level into
  'file' : ["h", '../STM32F4xx_DSP_StdPeriph_Lib_V1.8.0/Libraries/CMSIS/Device/ST/STM32F4xx/Include/stm32f4xx.h'], # (type, path)
}

#<editor-fold desc="INIT">
gdb.execute('set pagination off')
gdb.execute('set confirm off')
#initialize Lvl2
if config["debug"] == True:
    message = 'Initializing Lvl1'
    pp("yellow", message)

gdbcount = Pycounter() #class instance

if config["debug"] == True:
    message = "read_gdb_val:\t" + str(gdbcount.read_gdb_val())
    pp("yellow", message)

if (gdbcount.read_gdb_val() == 0):
    initialize()

gdbcount.increase() #place here to avoid else
#</editor-fold>

############# MAIN
try:
    reg = config["check"]
    pattern1 = re.compile('^GPIO([a-jA-J])$')   #extracts port char
    foundgpio = pattern1.search(reg)
    if foundgpio:
        gpio_dict = reg_query("*GPIO"+foundgpio.group(1)) #adds letter [A-J]
        printDict(reg, gpio_dict)
        pp('cyan', "0 => Reset value | set to 0 | Clock gating disabled")
    elif reg == "RCC":
        rcc_dict = reg_query("*RCC")
        printDict(reg, rcc_dict)
        if config["report"] == True:
            report = clockReport(rcc_dict) #report is a dictionary
    elif reg == "all":
        registers  = availableRegs(config["file"][1]) #register names
        # print(len(regs))
        # write2file(regs)
    elif reg == "GPIOx":
        for x in [chr(i) for i in range(ord('A'),ord('K'))]:
            gpio = '*GPIO'+x
            gpio_dict = reg_query(gpio)
            printDict(gpio, gpio_dict)
        pp('cyan', "0 => Reset value | set to 0 | Clock gating disabled")
except gdb.error:
    pp("error","Err 10: gdb.error")
finally:
    pp("reset"," ") # sets termial to default (last call before exit)

#<editor-fold desc='NOTES'>
'''
Current:

todo:
    RESERVEDn:
        RCC output spitting reserved
            change to typedef?
    PLLCFGRL??? @RCC
        CKGATENR????
    GPIO report... compare each field against function with template dictionary
    add func read from file
    add config to always save to file
        config["save"] ~ path
    Decipher clock configuartion check
        for each register in RCC

Notes:
    perhaps we could test all registers, regardless of the _BASE
        it may be better idea to get all the register names from a group of files
            use instead??
                _TypeDef
                }\s{1,}(.*)_TypeDef;

Debate:
    should I accept arguments using command line
        the arguments will usualy come from the make file
            hard coded
                hard code flags in code seems better alternative
                    it does not require GDB to understand them with extra flags
                        NO: do it locally
    usage methods:
        unatended
            it is meant to be used along side "normal" gdb troubleshooting
            So it makes more sense to have a config section for its behaviour
        menued
    Scalability:
        in order to avoid the rabbit hole
            this script will be built from a spefic case to gneral
    read *.h file VS Pre parsed file containing the registers
        read *.h file: specific to STM32
        Pre parsed:
            could be any
            it has to be done only once
    colours (terminal text)
        to create colorized prints, format:
            colour text + string + (appColour|resetColour)
        to save typing this will be handled by function
        Easier to troubleshoot
    register class ????
        it may be convenient to create a report
            built in troubleshooting

Check:
    all
        displays all raw available registers configurations
    gpio
        displays all raw gpio available registers configurations
    clock
        prints raw clock struct elements
    clock:HSI|HSW|PLL
    gpiox
        prints raw gpio struct elements
    gpiox:input|output

Brief:
    This script checks the state of the microcontrollers registers

general usage:
    if you know the register name:
        registerName => reg_query => print report|give insight?
    if you don't know the register name:
        availableRegs => reg_query => print report

Notes:
    gdb.execute('next')

troubleshooting:
    gdb:
        show convenience
        set $pyCounter=0
            causes to reset target on next script run

bug:
    ocassionaly the target gets a reset signal

kill -9 `ps -aux | awk '/gdbc/ && !/awk/ {print $2}'`
diagram@D:\KeepUpdating\coding\python\uShark
source ../debuggingScripts/gdbCheckTest1.py
'''
#</editor-fold>
