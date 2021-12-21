from numpy.lib.arraysetops import unique
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


# max_speed = df['Speed(RPM)'].max()
# max_torque = df['Torque(Nm)'].max()





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
        look_up_fuel_consumption = filt_is_speed_torque_fc.iloc[0, 2]
    
        for index in filt_is_speed_torque_vd.index:
            df.loc[index, 'FuelConsumption'] = look_up_fuel_consumption



unique_speeds = fcf['Speed'].unique()
unique_speeds.sort()

unique_torque = fcf['Torque'].unique()
unique_torque.sort()

# Difference between elements in list
unique_speeds_diff = np.diff(unique_speeds)
unique_torque_diff = np.diff(unique_torque)


max_speed_in_df = df['Speed(RPM)'].max()
max_torque_in_df = df['Torque(Nm)'].max()
min_torque_in_df = df['Torque(Nm)'].min()



# Creating new column with all zeroes
df['FuelConsumption'] = 0.0

print(unique_speeds)
print(unique_torque)


# for num_of_torque in zip(unique_torque)

# look_up_table(50, 0, max_torque, num_of_torque )


'''
Iterating through rows in fuel consumption look-up table and comparing look-up table values
with df values. If the same, then fuel consumption value is placed in the appropriate index
'''
for index, row in fcf.iterrows():
    for min_speed,min_torque,speed_dif,torque_diff in zip(unique_speeds, unique_torque, unique_speeds_diff, unique_torque_diff):

        # Last elements in array, special condition
        if(row['Speed'] == 4000 and row['Torque'] == 180):
            look_up_table(max_speed_in_df, row['Speed'], max_torque_in_df, row['Torque'])
        
        # Last element in speed array
        elif(row['Speed'] == 4000):
            max_torque = torque_diff + row['Torque']
            look_up_table(max_speed_in_df, row['Speed'], max_torque, row['Torque'])
        
        # Last element in torque array
        elif(row['Torque'] == 180):
            max_speed = speed_dif + row['Speed']
            look_up_table(max_speed, row['Speed'], max_torque_in_df, row['Torque'])

        # Normal condition 
        else:
            max_speed = speed_dif + row['Speed']
            max_torque = torque_diff + row['Torque']
            look_up_table(max_speed, row['Speed'], max_torque, row['Torque'])

        

            
                
# Copying data to a test.csv to see the results
df.to_csv('test.csv')



# for index, row in fcf.iterrows():
    
#     print(row['Speed'], row['Torque'])







# # Creating new column with all zeroes
# df['FuelConsumption'] = 0.0

# look_up_table(max_speed, 4000, 15, 0)
# look_up_table(4000, 3500, 15, 0)
# look_up_table(3500, 3250, 15, 0)




# filt_index = 

# for index, row in fcf.iterrows():
#     if(index == 0):
#         print(row['Speed'], row['Torque'])
