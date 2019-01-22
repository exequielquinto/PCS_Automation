print ('hello')
import time
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
#from pymodbus.registger_read_message import ReadInputRegisterResponse

client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, parity ='N', baudrate='115200' ,timeout=0.5)#, unit='0x01')
#client = ModbusClient('13.211.49.99', 502)

#client = ModbusClient(me)

connection = client.connect()
print(connection)

#For load sequence
bi_time=720  #12mins+3mins=15minsBurn In time in seconds
capture_time=180   # 3mins //time in seconds for each successive eff capture
#Discharge Eff
steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)
discharge_msb=(17786,17770,17754,17739,17723,17707,17692,17676,17658,17626,17595,17564,17530,17467,17402,17274,0) #Register 5054  FROM 4kW to 0
discharge_lsb=(0,24576,49152,8192,32768,57344,16384,40960,0,49152,32768,16384,0,32768,0,0,0)                      #Register 5055

print steps
print discharge_lsb
print discharge_msb

#FUNTIONS
def burn_in():
    try:
        client.write_registers(5054, discharge_msb[0])
        client.write_register(5055, discharge_lsb[0])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_msb[0])
            client.write_register(5055, discharge_lsb[0])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_msb[0])
            client.write_register(5055, discharge_lsb[0])

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
        client.write_registers(5054, discharge_msb[16])
        client.write_register(5055, discharge_lsb[16])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_msb[16])
            client.write_register(5055, discharge_lsb[16])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_msb[16])
            client.write_register(5055, discharge_lsb[16])
    
time1=time.time()
print ('warming up... time now is ' + time.ctime())
while (time.time()-time1) < bi_time:    
    burn_in()
    time.sleep(3)
    #print('testing1')
    
#results = pd.DataFrame()

for step in steps:
    print step
    time2=time.time()
    print ('capturing... time now is ' + time.ctime())
    while (time.time()-time2) < capture_time:
        pac_set()
        time.sleep(3)
        #print('testing2')

    print('measure')

min_load()                
print('finished')