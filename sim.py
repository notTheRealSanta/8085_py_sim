import numpy as np
from classes import Register as reg
from prerequisite import *

#Just some variables here
hun = 100   

code_location = [""] * hun
code_commands = [""] * hun
code_operand1 = [""] * hun
code_operand2 = [""] * hun

memory_location = [""] * hun
memory_values = [""] * hun

#Just some Functions
def code_input () :
    
    print("\nInput 8085 code : \nsyntax: <instruction><space><operand1><comma><space><operand2>, eg:MOV B, A\n(non-case-sensitive)\n\n")
    line = ""
    i = 0
    while line != "HLT ".upper() : #stops sim program when 'hlt' is the input
        line = input().upper() + " "
        
        code_location_end_index = 0
        if ":" in line:
            code_location[i] = line[ : line.find(":") ]
            code_location_end_index = line.find(":") +1
            code_commands[i] = line[ line.find(":")+2 : line.find(" ",code_location_end_index+1)]
        else :
            code_commands[i] = line[ : line.find(" ") ]
    
        command_end_index = line.find(" ",code_location_end_index+1)

        if "," in line :
            code_operand1[i] =  line[ command_end_index+1 : line.find(" ", command_end_index+1)-1 ]
            command_end_index = line.find(" ", command_end_index+1)
            code_operand2[i] =  line[ command_end_index+1 :line.find(" ", command_end_index+1) ]
        else :    
            code_operand1[i] =   line[ command_end_index+1 : line.find(" ", command_end_index+1)]

        i += 1

    # printl(code_commands)
    # printl(code_operand1)
    # printl(code_operand2)


def input_memory () :

    print("\nInput Memory Location and values. \nsyntax: <location><space><value>, eg:4000 f3\nType 'esc' to stop input!\n\n")

    line = ""
    i = 0 
    while line != "esc ".upper() : #stops sim program when 'hlt' is the input
        line = input().upper() + " "
        if line != "esc ".upper() :
            memory_location[i] = line [:line.find(" ")]
            memory_values[i] = line [line.find(" ")+1 : line.find(" ")+3]
            if memory_values[i] != "":
                memory_values[i] =  int(memory_values[i], 16) 
        i += 1
    

    # printl(memory_location)
    # printl(memory_values)
    print("\n\n")

def show_memory () :

    print("\nList of all memories used and their values \n\n")

    for i in range(len(memory_location)):
        if memory_location[i] != "" :
            print (memory_location[i], " : ", hex(int(memory_values[i])) ," (",memory_values[i],")")

def interpret() :
    
    
    commanding = {
        'LDA' : LDA,
        'LXI' : LXI,
        'STA' : STA,
        'MOV' : MOV,
        'MVI' : MVI,
        'INX' : INX,
        'ADD' : ADD
    }

    index = 0 # acts like the program counter
    while code_commands[index] != "HLT":
        commanding[code_commands[index]] ( code_operand1[index] ,  code_operand2[index]  )
        
        print ("\nInstruction :",code_commands[index])
        if code_operand1[index] != "" :
            print ("Operand1 :",code_operand1[index])
        if code_operand2[index] != "" :
            print ("Operand2 :",code_operand2[index])
        
        print(reg.registers)
        print("")
        index += 1
    
#command Fucntions
def LDA ( address = -1 , op2 = 0 ) :
    
    if(address != -1) :
        reg.registers['A'] = int (memory_values[memory_location.index(address)])

def LXI ( address = -1 , value = -1 ) :
    
    if(address != -1 and address != 'H') :
        reg.registers[address] = int (value, base = 16)
    if address == 'H':
        reg.registers[address] = int (value)

def STA (op1 = -1, op2 = 'A') :
    
    if(op1 in memory_location) :
        memory_values[memory_location.index(op1)] = reg.registers[op2]

    else :
        memory_location.append(op1)
        memory_values.append(reg.registers[op2])

def MOV (op1 = -1, op2 = -1) :
    
    if ( op1 in reg.registers and op2 in reg.registers):
        reg.registers[op1] = reg.registers[op2]

    if (op2 == 'M') :
        reg.registers[op1] = int (memory_values[memory_location.index(str(reg.registers['H']))]) 

    if (op1 == 'M') :
        STA (str(reg.registers['H']) , op2)    

def MVI (op1 = -1, op2 = -1) :
    
    if ( op1 in reg.registers ):
        reg.registers[op1] = op2

def INX (op1 = -1, op2 = -1) :

    if op1 != -1 :
        reg.registers[op1] = reg.registers[op1] + 1

def ADD (op1 = -1, op2 = -1) :
    
    if(op1 == 'M') :
        reg.registers['A'] += memory_values[memory_location.index(str(reg.registers['H']))]

    if ( op1 in reg.registers ):
        reg.registers['A'] += reg.registers[op1]

#Main function
def main() :
    
    code_input()
    input_memory()
    interpret()
    show_memory()

if __name__ == '__main__':
    main()

    