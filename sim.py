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

    printl(code_commands)
    printl(code_operand1)
    printl(code_operand2)


def input_memory () :

    print("Type esc to stop input!")

    line = ""
    i = 0 
    while line != "esc ".upper() : #stops sim program when 'hlt' is the input
        line = input().upper() + " "
        if line != "esc ".upper() :
            memory_location[i] = line [:line.find(" ")]
            memory_values[i] = line [line.find(" ")+1 : line.find(" ")+3]
        i += 1
    
    printl(memory_location)
    printl(memory_values)

def interpret() :
    
    
    commanding = {
        'LDA' : LDA,
        'LXI' : LXI,
    }

    index = 0 # acts like the program counter
    while code_commands[index] != "HLT":
        commanding[code_commands[index]] ( code_operand1[index] ,  code_operand2[index]  )
        index += 1
    
#command Fucntions
def LDA ( address = -1 , op2 = 0 ) :
    
    if(address != -1) :
        reg.registers['A'] = int (memory_values[memory_location.index(address)])

def LXI ( address = -1 , value = -1 ) :
    
    if(address != -1) :
        reg.registers[address] = value


#Main function
def main() :
    
    code_input()
    input_memory()
    interpret()
    print(reg.registers)

if __name__ == '__main__':
    main()

    