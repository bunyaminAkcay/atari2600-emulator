import emulator

fileName = "hello.a26"

emu = emulator.Emulator()
emu.storage.CartridgeMemory.writeFromFile(fileName=fileName)
#print(emu.storage.CartridgeMemory)
#emu.storage.CartridgeMemory.printRaw()
emu.run(stepByStep=True)