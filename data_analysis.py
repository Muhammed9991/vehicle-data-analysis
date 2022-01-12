from numpy.lib.arraysetops import unique
import pandas as pd
import numpy as np
import os 
import sys

'''
Function filters data using look-up table parameters and then 
fills data using look-up table fuel_consumption data
'''
def look_up_table(max_speed, min_speed, max_torque, min_torque, speed_dif,torque_diff, df, fcf ):

    # Filter raw data between the given speed and torque
    is_speed_torque_vd = (df['Speed(RPM)'].between(min_speed,max_speed)) & (df['Torque(Nm)'].between(min_torque,max_torque))

    if(min_speed == 4000 and min_torque == 180):
        in_speed_torque_fc = (fcf['Speed'] == 4000) & (fcf['Torque'] == 180)
        
    elif(min_speed == 4000 and max_torque == 15):
        in_speed_torque_fc = (fcf['Speed'] == 4000) & (fcf['Torque'] == 15)
    
    elif(max_speed == 0 and max_torque == 15):
        in_speed_torque_fc = (fcf['Speed'] == 0) & (fcf['Torque'] == 15)
    
    elif(max_torque == 15):
        in_speed_torque_fc = (fcf['Speed'] == (max_speed - speed_dif)) & (fcf['Torque'] == 15)
           
    # Last element in speed array
    elif(min_speed == 4000):
        in_speed_torque_fc = (fcf['Speed'] == 4000) & (fcf['Torque'] == (max_torque - torque_diff))
    
    # Last element in torque array
    elif(min_torque == 180):
        in_speed_torque_fc = (fcf['Speed'] == (max_speed - speed_dif)) & (fcf['Torque'] == 180)
    
    elif(max_speed == 0):
        in_speed_torque_fc = (fcf['Speed'] == 0) & (fcf['Torque'] == (max_torque - torque_diff))
    
    else:
        in_speed_torque_fc = (fcf['Speed'] == (max_speed - speed_dif)) & (fcf['Torque'] == (max_torque - torque_diff))
             
        
    # Filter [speed][torque] in vehicle data
    filt_in_speed_torque_vd = df[is_speed_torque_vd]

    filt_in_speed_torque_fc = fcf[in_speed_torque_fc]

    # Filter [speed][torque] in fuel_consumption.csv. 
    filt_in_speed_torque_fc = fcf[in_speed_torque_fc]

    # Only one index here. This is looking up the fuel consumption for a 
    # particular [speed][torque]
    if((not filt_in_speed_torque_fc.empty ) and (not filt_in_speed_torque_vd.empty) ):

        # Getting fuel consumption from look-up table
        look_up_fuel_consumption = filt_in_speed_torque_fc.iloc[0, 2]

        for index in filt_in_speed_torque_vd.index:
            df.loc[index, 'FuelConsumption'] = look_up_fuel_consumption




def  main(df_file_name, look_up_table_file_name):

    df = pd.read_csv(df_file_name)
    # #Fuel consumption file
    fcf = pd.read_csv(look_up_table_file_name)

    # For debugging use the file names below
    # df = pd.read_csv('vehicle_data.csv')
    #Fuel consumption file
    # fcf = pd.read_csv('fuel_consumption.csv')


    # Converting 2-D Look-up table to a two column and result format
    fcf = pd.melt(fcf, id_vars=['Speed'], value_vars=['15.0','30.0','45.0','60.0','75.0','90.0','105.0','120.0','135.0','150.0','165.0','180.0'])
    # Converting str to number
    fcf['variable'] = pd.to_numeric(fcf['variable'])   
    fcf = fcf.rename({'variable':'Torque'}, axis=1)
    fcf = fcf.rename({'value':'FuelConsumption'}, axis=1)
    fcf.to_csv('melt_fuel_consumption.csv')

    # Getting unique values in speed and torque column
    # and then sorting it in acending order
    unique_speeds = fcf['Speed'].unique()
    unique_speeds.sort()

    unique_torque = fcf['Torque'].unique()
    unique_torque.sort()

    # Difference between elements in list
    # unique_speeds_diff = np.diff(unique_speeds)
    # unique_torque_diff = np.diff(unique_torque)

    max_speed_in_df = df['Speed(RPM)'].max()
    min_speed_in_df = df['Speed(RPM)'].min()
    max_torque_in_df = df['Torque(Nm)'].max()
    min_torque_in_df = df['Torque(Nm)'].min()

    # Creating new column with all zeroes
    df['FuelConsumption'] = 0.0


    '''
    Iterating through rows in fuel consumption look-up table and comparing look-up table values
    with df values. If the same, then fuel consumption value is placed in the appropriate index
    '''
    #Iterating through look-up table
    for index, row in fcf.iterrows(): 

        # Iterating through the min speed and torque and the diff between each speed and each torque
        for min_speed,min_torque in zip(unique_speeds, unique_torque):
            
            torque_diff = 15

            # Setting speed diff values to be used in .between
            if(row['Speed'] == 50):
                speed_dif = 450
            
            elif(row['Speed'] == 0):
                speed_dif = 50

            elif(row['Speed'] == 500 or row['Speed'] == 3500):
                speed_dif = 500
            else:
                speed_dif = 250


            # Last elements in array, special condition
            if(row['Speed'] == 4000 and row['Torque'] == 180):
                look_up_table(max_speed_in_df, row['Speed'], max_torque_in_df, 180, speed_dif,torque_diff, df, fcf)
            
            elif(row['Speed'] == 4000 and row['Torque'] == 15):
                look_up_table(max_speed_in_df, 4000, 15, min_torque_in_df, speed_dif,torque_diff, df, fcf)
                
            # Lowest speed and lowest torque
            elif(row['Speed'] == 0 and row['Torque'] == 15):
                max_torque = torque_diff + row['Torque']
                look_up_table(0, min_speed_in_df, 15, min_torque_in_df, speed_dif,torque_diff, df, fcf)
                
            # Last element in speed array
            elif(row['Speed'] == 4000):
                max_torque = torque_diff + row['Torque']
                look_up_table(max_speed_in_df, 4000, max_torque, row['Torque'], speed_dif,torque_diff, df, fcf)
            
            # Last element in torque array
            elif(row['Torque'] == 180):
                max_speed = speed_dif + row['Speed']
                look_up_table(max_speed, row['Speed'], max_torque_in_df, 180, speed_dif,torque_diff, df, fcf)

            # Lowest torque
            elif(row['Torque'] == 15):
                max_speed = speed_dif + row['Speed']
                look_up_table(max_speed, row['Speed'], 15, min_torque_in_df, speed_dif,torque_diff, df, fcf)        
            
            # Lowest speed
            elif(row['Speed'] == 0):
                max_torque = torque_diff + row['Torque']
                look_up_table(0, min_speed_in_df, max_torque, row['Torque'], speed_dif,torque_diff, df, fcf)

            # Normal condition 
            else:
                max_speed = speed_dif + row['Speed']
                max_torque = torque_diff + row['Torque']
                look_up_table(max_speed, row['Speed'], max_torque, row['Torque'], speed_dif,torque_diff, df, fcf)
    
            

                
                    
    # Copying data to a test.csv to see the results
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    path_of_result = current_dir_path + '/complete_fuel_consumption.csv'
    df.to_csv(path_of_result)
    print()
    print(f'Data copied to {path_of_result} ')
    print()


'''
Function checks if path exists. If it does carrys on if not then exits
'''
def check_if_file_path_exists(file_path):
    is_exist = os.path.exists(file_path)

    if(is_exist):
        pass
    else:
        print(f'ERROR: {file_path} Not Found')
        sys.exit()



# Pass the file name to run script on without extension
if(len(sys.argv) > 2):
    # Finding path to current file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    # First Argument is data frame path
    full_path_of_csv = dir_path + '/' + sys.argv[1] + '.csv'
    check_if_file_path_exists(full_path_of_csv)

    # Second Argument is look-up table path
    full_path_look_up_table = dir_path + '/' + sys.argv[2] + '.csv'
    check_if_file_path_exists(full_path_look_up_table)

    main(full_path_of_csv, full_path_look_up_table)

    
else:
    print()
    sys.exit('Please re-run script and specify name of data_frame file and look-up table without extension')

