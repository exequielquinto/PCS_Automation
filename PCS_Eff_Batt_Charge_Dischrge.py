import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient

client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
#client = ModbusClient('127.0.0.1', 502)    #MODBUS TCP/IP

connection = client.connect()
print(connection)

#For load sequence
bi_time=900  #115minsBurn In time in seconds
capture_time=180   # 3mins //time in seconds for each successive eff capture
#Discharge and Charge Eff
steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45)
discharge_charge_msb=(17820,17812,17804,17796,17786,17770,17754,17742,17739,17723,17707,17692,17676,17658,17626,17614,17595,17564,17530,17467,17402,17274,0,50588,50580,50572,50564,50554,50538,50522,50510,50507,50491,50475,50460,50444,50426,50394,50382,50363,50332,50298,50235,50170,50042,0) #Register 5054  FROM 4kW to 0
discharge_charge_lsb=(16384,28672,40960,53248,0,24576,49152,16384,8192,32768,57344,16384,40960,0,49152,16384,32768,16384,0,32768,0,0,0,16384,28672,40960,53248,0,24576,49152,16384,8192,32768,57344,16384,40960,0,49152,16384,32768,16384,0,32768,0,0,0)                      #Register 5055

print steps
print discharge_charge_lsb
print discharge_charge_msb

print len(steps)
print len(discharge_charge_msb)
print len(discharge_charge_lsb)

#FUNTIONS
def pac_set():
    try:
        client.write_registers(5054, discharge_charge_msb[step])
        client.write_register(5055, discharge_charge_lsb[step])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_charge_msb[step])
            client.write_register(5055, discharge_charge_lsb[step])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_charge_msb[step])
            client.write_register(5055, discharge_charge_lsb[step])
    
def min_load():
    try:
        client.write_registers(5054, discharge_charge_msb[16])
        client.write_register(5055, discharge_charge_lsb[16])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_charge_msb[16])
            client.write_register(5055, discharge_charge_lsb[16])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_charge_msb[16])
            client.write_register(5055, discharge_charge_lsb[16])


for step in steps:
    if step==0 or step==23:
        test_time=bi_time
        print step
        print ('burn in... time now is ' + time.ctime())
    else:
        test_time=capture_time
        print step
        print ('capturing... time now is ' + time.ctime())
    
    time2=time.time()
    while (time.time()-time2) < test_time:
        pac_set()
        time.sleep(3)
        #print('testing2')

    print('measure')

min_load()                
print('finished')