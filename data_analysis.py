import pandas as pd
import numpy as np

df = pd.read_csv('vehicle_data.csv')



#Fuel consumption file
fcf = pd.read_csv('fuel_consumption.csv')



# Converting 2-D Look-up table to a two column and result format
fcf = pd.melt(fcf, id_vars=['Speed'], value_vars=['15.0','30.0','45.0','60.0','75.0','90.0','105.0','120.0','135.0','150.0','165.0','180.0'])
# Converting str to number
fcf['variable'] = pd.to_numeric(fcf['variable'])   
fcf = fcf.rename({'variable':'Torque'}, axis=1)
fcf = fcf.rename({'value':'FuelConsumption'}, axis=1)


max_speed = df['Speed(RPM)'].max()
max_torque = df['Torque(Nm)'].max()





'''
Function filters data using look-up table parameters and then 
fills data using look-up table fuel_consumption data
'''
def look_up_table(max_speed, min_speed, max_torque, min_torque ):

    is_speed_torque_vd = (df['Speed(RPM)'].between(min_speed,max_speed)) & (df['Torque(Nm)'].between(min_torque,max_torque)) 
    
    if(min_speed == 4000):
        is_speed_torque_fc = (fcf['Speed'] == 4000) & (fcf['Torque'] == 15)

    else:
        is_speed_torque_fc = (fcf['Speed'] == max_speed) & (fcf['Torque'] == max_torque)

    # Filter [speed][torque] in vehicle data
    filt_is_speed_torque_vd = df[is_speed_torque_vd]
    # Filter [speed][torque] in fuel_consumption.csv. 
    filt_is_speed_torque_fc = fcf[is_speed_torque_fc]

    # Only one index here. This is looking up the fuel consumption for a 
    # particular [speed][torque]
    if((not filt_is_speed_torque_fc.empty ) and (not filt_is_speed_torque_vd.empty) ):

        # Getting fuel consumption from look-up table
        look_up_fuel_consumption = filt_is_speed_torque_fc.loc[filt_is_speed_torque_fc.index,'FuelConsumption']
        print(look_up_fuel_consumption)
    
    '''
    ISSUE WITH 'look_up_fuel_consumption' ERROR: Incompatible indexer with Series
    '''
        # for index in filt_is_speed_torque_vd.index:
        #     df.loc[index, 'FuelConsumption'] = look_up_fuel_consumption


# Creating new column with all zeroes
df['FuelConsumption'] = 0.0

look_up_table(max_speed, 4000, 15, 0)
look_up_table(4000, 3500, 15, 0)
look_up_table(3500, 3250, 15, 0)

df.to_csv('test.csv')

# filt_index = 

# for index, row in fcf.iterrows():
#     if(index == 0):
#         print(row['Speed'], row['Torque'])
