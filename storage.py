import hexmath

class StorageUnit:
    def __init__(self, startingAddress, lastAddress, writable=False, fill=0x00):
        self.startingAddress = startingAddress
        self.lastAddress = lastAddress
        self.size = lastAddress - startingAddress +1
        self.writable = writable
        self.storage = [fill] * self.size
    
    def get(self, address):
        if (isinstance(address, str)):
            address = int(address, 16)
        address -= self.startingAddress
        return self.storage[address]
    
    def set(self, address, value):
        if (isinstance(address, str)):
            address = int(address, 16)
        address -= self.startingAddress
        self.storage[address] = value

    def __str__(self):
        storageStr = ""
        counter = 0
        size = 16
        for i in self.storage:
            if (counter%size == 0):
                storageStr += hexmath.asHex(self.startingAddress + counter, 4) + ": "
            storageStr += hexmath.asHex(i, 2) + " "
            if (counter%size == size -1):
                storageStr += "\n"
            counter +=1
        return storageStr

    def printRaw(self):
        storageStr = ""
        for i in self.storage:
            storageStr += hexmath.asHex(i, 2) + " "
        print(storageStr)

    def writeFromFile(self, fileName):
        counter = 0
        with open(fileName, "rb") as f:
            while (byte := f.read(1)):
                if (counter > self.size):
                    print("Error while inserting Rom, file is bigger than memory area.")
                    break
                self.storage[counter] = int(byte.hex(), 16)
                counter += 1

class Storage:
    def __init__(self):
        #memory map for Atari 2600
        self.TIA = StorageUnit(0x0000, 0x007F, writable=True)
        self.PIARAM = StorageUnit(0x0080, 0x00FF, writable=True)
        self.PIAPortsAndTimer = StorageUnit(0x0200, 0x02FF, writable=True)
        self.CartridgeMemory = StorageUnit(0xF000, 0xFFFF)

        self.memory = [self.TIA, self.PIARAM, self.PIAPortsAndTimer, self.CartridgeMemory]

    def get(self, address):
        result = 0
        resultFound = False
        if (isinstance(address, str)):
            address = int(address, 16)
        for unit in self.memory:
            if (unit.startingAddress <= address and unit.lastAddress >= address):
                result = unit.get(address=address)
                resultFound = True
        if (resultFound == False):
            print(f"Error: Emulator tries to reach out of scope. Adress: {address}")
        return result

    def set(self, address, value):
        targetFound = False
        if (isinstance(address, str)):
            address = int(address, 16)
        for unit in self.memory:
            if (unit.startingAddress <= address and unit.lastAddress >= address):
                result = unit.set(address=address, value=value)
                targetFound = True
        if (targetFound == False):
            print(f"Error: Emulator tries to reach out of scope. Adress: {address}")
