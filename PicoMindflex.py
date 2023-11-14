import board
import busio

class MindFlex:
    def __init__(self):
        self.uart = busio.UART(tx=board.GP0, rx=board.GP1, baudrate=9600)
        self.freshPacket = False
        self.inPacket = False
        self.packetLength = 0
        self.packetIndex = 0
        self.signalQuality = 200
        self.lastByte = None
        self.checksumAccumulator = b''
        self.packetData = [0]*32
        self.eegPower = [0]*8
        self.signalQuality = 0
        self.attention = 0
        self.meditation = 0
        self.hasPower = False
        self.freshPacket = False
        
    def readPacket(self):
        if self.freshPacket:
            freshPacket = False
        self.latestByte = self.uart.read(1)
        if self.latestByte is not None:
            if not self.inPacket and self.lastByte is not None:
                if int.from_bytes(self.latestByte, "little") == 170 and int.from_bytes(self.lastByte, "little") == 170:
                    self.inPacket = True
                    self.packetIndex = 0
                    self.checksumAccumulator = b''
            elif self.inPacket:
                if self.packetIndex == 0:
                    self.packetLength = int.from_bytes(self.latestByte, "little")
                    if self.packetLength > 32:
                        print("Error Packet too long")
                        inPacket = False
                elif self.packetIndex <= self.packetLength:
                    self.packetData[self.packetIndex-1]=self.latestByte
                    self.checksumAccumulator += self.latestByte
                elif self.packetIndex > self.packetLength:
                    checksum = self.latestByte
                    self.checksumAccumulator = 255 - (sum(self.checksumAccumulator)%256)
                    self.inPacket = False
                    if int.from_bytes(checksum, "little") == self.checksumAccumulator:
                        if self.parsePacket():
                            print("Packet received")
                            self.freshPacket = True
                        else:
                            print("Error parsing package")
                            
                    else:
                        print("Checksums don't match")
                
                
                self.packetIndex += 1  
            self.lastByte = self.latestByte
    
    def parsePacket(self):
        self.hasPower = False
        parseSuccess = True
        
        self.clearEegPower();
        
        i = 0
        while i < self.packetLength:
            data = self.packetData[i]
            if data == b'\x02':
                #signal quality
                i += 1
                self.signalQuality = int.from_bytes(self.packetData[i], "little")
            elif data == b'\x04':
                #attention
                i += 1
                self.attention = int.from_bytes(self.packetData[i], "little")
            elif data == b'\x05':
                #meditation
                i += 1
                self.meditation = int.from_bytes(self.packetData[i], "little")
            elif data == b'\x83':
                #eeg values
                #i +=25
                i += 1 # value not used
                for j in range(8):
                    i+=1
                    a = int.from_bytes(self.packetData[i], "little") << 16
                    i+=1
                    b = int.from_bytes(self.packetData[i], "little") << 8
                    i+=1
                    c = int.from_bytes(self.packetData[i], "little")
                    self.eegPower[j] = a | b | c
                self.hasPower = True
                
            elif data == b'\x80':
                #not used
                i+=3
            else:
                print("failed byte")
                print(data)
                parseSuccess = False
            
            i += 1
        return parseSuccess
    
    def readCSV(self):
        return "{},{},{},{},{},{},{},{},{},{},{}".format(
            self.signalQuality,
            self.attention,
            self.meditation,
            self.eegPower[0],
            self.eegPower[1],
            self.eegPower[2],
            self.eegPower[3],
            self.eegPower[4],
            self.eegPower[5],
            self.eegPower[6],
            self.eegPower[7]
            )
    
    def clearEegPower(self):
        self.eegPower = [0]*8
        
    def clearPacket(self):
        self.packetData = [0]*32
        
    def readSignalQuality(self):
        return self.signalQuality
    
    def readDelta(self):
        return self.eegPower[0]
        
    def readTheta(self):
        return self.eegPower[1]
    
    def readLowAlpha(self):
        return self.eegPower[2]
    
    def readHighAlpha(self):
        return self.eegPower[3]
    
    def readLowBeta(self):
        return self.eegPower[4]
    
    def readHighBeta(self):
        return self.eegPower[5]
    
    def readLowGamma(self):
        return self.eegPower[6]
    
    def readMidGamma(self):
        return self.eegPower[7]
        

