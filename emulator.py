import storage as stor
import hexmath

#https://problemkaputt.de/2k6specs.htm

class Emulator():
    def __init__(self, pc = 0xF000):
        self.storage = stor.Storage()   #Rom and rams
        self.ac = 0x00                  #Accumulutor
        self.xr = 0x00                  #X-register
        self.yr = 0x00                  #Y-register
        self.sr = 0b00110110            #set status register NV-BDIZC -> Negative overflow - break decimal interrupts zero carry
        self.sp = 0x00                  #stack pointer
        self.pc = pc                    #program counter
        self.__instructionSet = {
                0x78: ["sei", 0, self.__i_78],
                0xd8: ["cld", 0, self.__i_d8],
                0xf8: ["sed", 0, self.__i_f8],
                0xa2: ["ldx", 1, self.__i_a2],
                0x9a: ["txs", 0, self.__i_9a],
                0xa9: ["lda", 1, self.__i_a9],
                0x95: ["sta", 1, self.__i_95],
                0x99: ["sta", 2, self.__pass],
                0xca: ["dex", 0, self.__i_ca],
                0xd0: ["bne", 1, self.__i_d0],
                0x85: ["sta", 1, self.__i_85],
                0x4c: ["jmp", 2, self.__i_4c],
                0x00: [".word", 1, self.__pass],
                0x00: ["ff", 0, self.__pass]
                }
    
    def run(self, stepByStep=False):
        while (self.pc != 0xFFFF):
            if (stepByStep):
                self.__instruct(debug=True)
                input()
            else:
                self.__instruct()

    
    def __instruct(self, debug=False):
        values = []
        opCode = self.storage.get(self.pc)
        insAddress = self.pc
        if (opCode in self.__instructionSet):
            instruction = self.__instructionSet[opCode]
            self.pc += 1
            for i in range(instruction[1]):
                values.append(self.storage.get(self.pc))
                self.pc += 1
            instruction[2](values)
            if(debug):
                print(f"{hexmath.asHex(insAddress,4)} {hexmath.asHex(opCode, 2)} {values}")
                self.printRegisters()
        else:
            print(f"Error unknown instruction. Address: {hexmath.asHex(insAddress, 4)} opCode: {opCode}")

    def printRegisters(self):
        print(f"ac xr yr sr sp NV-BDIZC\n{hexmath.asHex(self.ac, 2)} {hexmath.asHex(self.xr, 2)} {hexmath.asHex(self.yr, 2)} {hexmath.asHex(self.sr, 2)} {hexmath.asHex(self.sp, 2)} {hexmath.get_bit(self.sr, 7)}{hexmath.get_bit(self.sr, 6)}{hexmath.get_bit(self.sr, 5)}{hexmath.get_bit(self.sr, 4)}{hexmath.get_bit(self.sr, 3)}{hexmath.get_bit(self.sr, 2)}{hexmath.get_bit(self.sr, 1)}{hexmath.get_bit(self.sr, 0)}")
    
    def __setFlags(self, d):
        d = hexmath.hex2signedDecimal(d)
        if (d < 0):
            self.sr = hexmath.set_bit(self.sr, 7)     #negative to 1
            self.sr = hexmath.clear_bit(self.sr, 1)   #zero to 0
        elif (d == 0):
            self.sr = hexmath.clear_bit(self.sr, 7)   #negative to 0
            self.sr = hexmath.set_bit(self.sr, 1)     #zero to 1
        else:
            self.sr = hexmath.clear_bit(self.sr, 7)   #negative to 0
            self.sr = hexmath.clear_bit(self.sr, 1)   #zero to 0
    
    def __pass(self, values):
        pass

    def __i_f8(self, values):   #sed
        #enable BCD math mode
        self.sr = hexmath.set_bit(self.sr, 3)     #decimal to 1

    def __i_d8(self, values):   #cld
        #disable BCD math mode
        self.sr = hexmath.clear_bit(self.sr, 3)   #decimal to 0
    
    def __i_78(self, values):   #sei
        #disable interrupts
        self.sr = hexmath.set_bit(self.sr, 2)   #interrupts to 1
    
    def __i_a2(self, values):   #ldx
        #load index xr with immediate
        self.__setFlags(values[0])
        self.xr = values[0]
    
    def __i_9a(self, values):   #txs
        #transfer index xr to stack register
        self.sp = self.xr
    
    def __i_a9(self, values):   #lda
        #load ac with immediate
        self.__setFlags(values[0])
        self.ac = values[0]
    
    def __i_95(self, values):   #sta
        #store ac register at (immediate + x)
        self.storage.set(values[0] + self.xr, self.ac)

    def __i_ca(self, values):   #dex
        #decrement index xr by 1
        self.xr -= 1
        self.__setFlags(self.xr)
    
    def __i_d0(self, values):
        if (hexmath.get_bit(self.sr, 1) != 1): # if z != 1
            self.pc += hexmath.hex2signedDecimal(values[0])

    def __i_4c(self, values):
        self.pc = values[1]*16*16 + values[0]

    def __i_85(self, values):
        self.storage.set(values[0], self.ac)