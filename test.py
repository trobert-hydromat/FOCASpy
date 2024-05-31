"""
Thomas Robert
2024-05-31
trobert@hydromat.com

test.py
    Sample functions
"""
# Imports functions
from FocasInterface import *

# Creates new CNC object
cnc1 = FocasInterface()
# Sets HSSB connection configuration
cnc1.HSSB()
# Connects to CNC
print(cnc1.Connect())

# Read CNC Parameter
print(cnc1.ReadParameter(3202))             
# Read Axis Parameter
print(cnc1.ReadParameter(12,2))             
# Read Path Parameter
print(cnc1.ReadParameter(3141, 1))          
print(chr(cnc1.ReadParameter(3141, 1)))

# Write CNC Byte Parameter
print(cnc1.WriteByteParameter(3202, 0))
# Write Axis Byte Parameter
print(cnc1.WriteByteParameter(12,128, 2))
# Write Path Parameter (Doesn't work)
#print(cnc1.WriteWordParameter(3141, 97, 1))
# Write CNC Numeric Parameter
print(cnc1.WriteShortParameter(3211, 123))  

# Read PMC Byte
print(cnc1.ReadPMCByte(Focas1.focas_pmc_address_type.K, 15))
# Read PMC Bit
print(cnc1.ReadPMCBool(Focas1.focas_pmc_address_type.K, 15, 0 ))

# Read PMC Byte from Address
print(cnc1.ReadPMCAddress("K13"))
# Read PMC Bit from Address
print(cnc1.ReadPMCAddress("K13.0"))