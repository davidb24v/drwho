'''

Indicator (light) class for "Dr Who" themed sound & light box


'''
from Adafruit_MCP230xx import *

class Indicators(object):

    __next = 0
    mcp = Adafruit_MCP230XX(address = 0x20, num_gpios = 8)

    def __init__(self):
        self.pin = Indicators.__next
        Indicators.__next += 1
        Indicators.mcp.config(self.pin, self.mcp.OUTPUT)
        self.off()

    def on(self):
        Indicators.mcp.output(self.pin, 1)

    def off(self):
        Indicators.mcp.output(self.pin, 0)

    def allOff(self):
        for pin in range(Indicators.__next):
            Indicators.mcp.output(pin, 0)


