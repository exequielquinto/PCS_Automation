import pandas as pd         
import visa, time    
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

#Connect to Instruments
#rm = visa.ResourceManager()
#meter = rm.open_resource('USB0::0x0A69::0x083E::636002000532::0::INSTR')  #Power Meter
client = ModbusClient('127.0.0.1', 502)    #MODBUS TCP/IP
#client = ModbusClient(method = 'rtu' , port = 'COM10' , stopbits=1, bytesize=8, parity ='N', baudrate='115200', timeout=0.5)  #RS485

#Verify Connection
#meter.query('*IDN?')
connection = client.connect()
print(connection)

#For load sequence
bi_time=15     #Burn In time in seconds
capture_time=10   #time in seconds for each successive eff capture
#Discharge Eff
steps=(0,1,2,3,4,5,6,7,8,9,10)
discharge_msb=(17820,17804,17786,17754,17723,17692,17658,17595,17530,17402,0) #Register 5054
discharge_lsb=(16384,40960,0,49152,32768,16384,0,32768,0,0,0)                 #Register 5055

#Charge discharge efficiency
#steps=(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21)
#discharge_msb=(17820,17804,17786,17754,17723,17692,17658,17595,17530,17402,0,50588,50572,50554,50522,50491,50460,50426,50363,50298,50170,0) #Register 5054
#discharge_lsb=(16384,40960,0,49152,32768,16384,0,32768,0,0,0,16384,40960,0,49152,32768,16384,0,32768,0,0,0)                 #Register 5055

#Charge Efficiency
#steps=(0,1,2,3,4,5,6,7,8,9,10)
#charge_msb=(50588,50572,50554,50522,50491,50460,50426,50363,50298,50170,0)    #Register 5054
#charge_lsb=(16384,40960,0,49152,32768,16384,0,32768,0,0,0)                    #Register 5055



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
        client.write_registers(5054, discharge_msb[10])
        client.write_register(5055, discharge_lsb[10])
    except:
        try:
            print('pac set error1')
            client.write_registers(5054, discharge_msb[10])
            client.write_register(5055, discharge_lsb[10])
        except:
            print('pac set error2')
            client.write_registers(5054, discharge_msb[10])
            client.write_register(5055, discharge_lsb[10]) 
    
def measure():
    #Vin_dc Measure
    temp['A_Vin'] = Vin
    #Iin_dc Measure
    temp['B_Iin'] = Iin
    #Pin_dc Measure
    temp['C_Pin'] = Pin
    #Vgrid_ac Measure
    temp['D_Vgrid'] = Vgrid
    #Igrid_ac Measure
    temp['E_Igrid'] = Igrid
    #Freq_grid
    temp['F_Fgrid'] = Fgrid
    #PF_grid
    temp['G_PFgrid'] = PFgrid
    #Pin_grid
    temp['H_Pin'] = Pgrid 
    #Efficiency
    temp['I_Efficiency'] = Pgrid*100/Pin
    ##### ....
    #I_crest factor grid
    #V_crest factor grid
    #I_thd grid
    #U_thd grid

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
    #temp = {}
    #measure()
    #try:
    #    measure()
    #except:
    #    try:
    #        print('measure error1')
    #        measure()
    #    except:
    #        print('measure error2')
    #        measure()
    #
    #results = results.append(temp, ignore_index=True)    # 17
    #print results
    #print "%.2fV\t%.3fA" % (temp['C_Ch1_Vout'],temp['K_Efficiency'])    # ? on print formatting
    #results.to_csv('Results.csv')
min_load()                
print('finished')

#response = client.read_holding_registers(5055,4,unit=1)
#print response.registers
#print response.registers[0]
#print ('xXx')

