print ('hello')
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.registger_read_message import ReadInputRegisterResponse

client = ModbusClient(method = 'rtu' , port = 'COM9' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
#client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, bytesize=8, parity ='N', baudrate='115200' ,timeout=0.5)
#client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, bytesize=8, parity ='N', baudrate='9600' ,timeout=0.3)



#client = ModbusClient(me)


connection = client.connect()
print(connection)

client.write_register(5054, 17530)
client.write_register(5055, 0)

time.sleep(3)

response = client.read_holding_registers(5047,12,unit=1)
print response.registers
print response.registers[0]
print ('xXx')

#Read input reg
response = client.read_input_registers(5001,2,unit=1)
print response.registers
print hex(response.registers[0])
print hex(response.registers[1])
print ('xXx')
