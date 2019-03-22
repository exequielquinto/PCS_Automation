import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')

connection = client.connect()
print(connection)

#For load sequence
bi_time=900  #15mins Burn In time in seconds
capture_time=180   # 3mins //time in seconds for each successive eff capture

#For 65VDC  5kW
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22)
#discharge_msb=(17820,17812,17804,17796,17786,17770,17754,17742,17739,17723,17707,17692,17676,17658,17626,17614,17595,17564,17530,17467,17402,17274,0) #Register 5054  FROM 4kW to 0
#discharge_lsb=(16384,28672,40960,53248,0,24576,49152,16384,8192,32768,57344,16384,40960,0,49152,16384,32768,16384,0,32768,0,0,0)                      #Register 5055

#Discharge Eff 4kW
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
#discharge_msb=(17786,17770,17754,17739,17723,17707,17692,17676,17658,17626,17595,17564,17530,17467,17402,17274,0) #Register 5054  FROM 4kW to 0
#discharge_lsb=(0,24576,49152,8192,32768,57344,16384,40960,0,49152,32768,16384,0,32768,0,0,0)                      #Register 5055

#For 48VDCin 3.75kW
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
#discharge_msb=(17770,17754,17739,17723,17707,17692,17676,17658,17626,17595,17564,17530,17467,17402,17274,0) #Register 5054  FROM 4kW to 0
#discharge_lsb=(24576,49152,8192,32768,57344,16384,40960,0,49152,32768,16384,0,32768,0,0,0)                      #Register 5055

#For 44VDC input 3.5kW
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)
#discharge_msb=(17754,17739,17723,17707,17692,17676,17658,17626,17595,17564,17530,17467,17402,17274,0) #Register 5054  FROM 4kW to 0
#discharge_lsb=(49152,8192,32768,57344,16384,40960,0,49152,32768,16384,0,32768,0,0,0)                      #Register 5055

#For 40VDC input  3kW
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12)
#discharge_msb=(17723,17707,17692,17676,17658,17626,17595,17564,17530,17467,17402,17274,0) #Register 5054  FROM 4kW to 0
#discharge_lsb=(32768,57344,16384,40960,0,49152,32768,16384,0,32768,0,0,0)                      #Register 5055

#FOR SGIP 42-58.8V
steps=(0,1,2,3,4,5,6) # 10,20,30,50,75,100 % load
discharge_msb=(17820,17770,17692,17595,17530,17402,0)
discharge_lsb=(16384,24576,16384,32768,0,0,0)

#0-100% by 10's  with 75%
#steps=(0,1,2,3,4,5,6,7,8,9,10,11)
#discharge_msb=(17820,17804,17786,17770,17754,17723,17692,17658,17595,17530,17402,0)
#discharge_lsb=(16384,40960,0,24576,49152,32768,16384,0,32768,0,0,0)

print steps
print discharge_lsb
print discharge_msb

#FUNTIONS
def pac_set():
    try:
        client.write_registers(5054, discharge_msb[step])
        client.write_register(5055, discharge_lsb[step])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_msb[step])
            client.write_register(5055, discharge_lsb[step])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_msb[step])
            client.write_register(5055, discharge_lsb[step])    
def min_load():
    try:
        client.write_registers(5054, discharge_msb[max(steps)])
        client.write_register(5055, discharge_lsb[max(steps)])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_msb[max(steps)])
            client.write_register(5055, discharge_lsb[max(steps)])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_msb[max(steps)])
            client.write_register(5055, discharge_lsb[max(steps)])
    
for step in steps:
    if step == 0:
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