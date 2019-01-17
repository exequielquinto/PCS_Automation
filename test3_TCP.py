print ('hello')
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.registger_read_message import ReadInputRegisterResponse

client = ModbusClient('127.0.0.1', 502)

#client = ModbusClient(me)


connection = client.connect()
print(connection)

#value=client.read_coils(5, 1).bits
value = client.write_coil(10,1)
#value = client.read_input_registers(300, 4, unit=0x01)  #300 is address, 4 is size, 0x01 is slave ID
print value