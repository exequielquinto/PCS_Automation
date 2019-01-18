print ('hello')
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.registger_read_message import ReadInputRegisterResponse

client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
#client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, bytesize=8, parity ='N', baudrate='115200' ,timeout=0.5)
#client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, bytesize=8, parity ='N', baudrate='9600' ,timeout=0.3)



#client = ModbusClient(me)


connection = client.connect()
print(connection)

response = client.read_holding_registers(5300,110,unit=1)
print response.registers
print response.registers[0]
print ('xXx')

#Read input reg not working???
#response = client.read_input_registers(35012,4,unit=1)
#print response
#print response.registers[0]
#print ('xXx')