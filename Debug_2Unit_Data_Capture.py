import pandas as pd         
import visa, time    

def measure1():
    temp1['A_Time'] =1
    
def measure2():
    temp2['A_Time'] =2
  
results1 = pd.DataFrame()
results2 = pd.DataFrame()

while 1:
       
    time.sleep(10)   # Delay in seconds before capturing results
    temp1 = {}
    temp2 = {}
    #measure()
    measure1()
    measure2()
    
    results1 = results1.append(temp1, ignore_index=True)
    results2 = results2.append(temp2, ignore_index=True)
    
    results1.to_csv('Results1.csv')
    results2.to_csv('Results2.csv')
    time.sleep(10)              
print('finished')