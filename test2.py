print ('hello')
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.registger_read_message import ReadInputRegisterResponse

client = ModbusClient(method = 'rtu' , port = 'COM1' , stopbits=1, bytesize=8, parity ='N', baudrate='9600' ,timeout=0,3)
#client = ModbusClient(method = 'TCP/IP' , port = '502' , stopbits=1, bytesize=8, parity ='N', baudrate='9600' ,timeout=0,3)

#client = ModbusClient(me)


connection = client.connect()
print(connection)

#value=client.read_coils(address, count)
#value = client.read_input_registers(300, 4, unit=0x01)  #300 is address, 4 is size, 0x01 is slave ID
#print value