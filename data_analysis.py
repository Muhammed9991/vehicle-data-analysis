import pandas as pd
import numpy as np

df = pd.read_csv('vehicle_data.csv')

#Fuel consumption file
fcf = pd.read_csv('fuel_consumption.csv')

# Converting 2-D Look-up table to a two column and result format
fcf = pd.melt(fcf, id_vars=['Speed'], value_vars=['15.0','30.0','45.0','60.0','75.0','90.0','105.0','120.0','135.0','150.0','165.0','180.0'])

# Converting str to number
fcf['variable'] = pd.to_numeric(fcf['variable'])   
fcf = fcf.rename({'variable':'Torque(Nm)'}, axis=1)
fcf = fcf.rename({'value':'Fuel Consumption(g/s)'}, axis=1)


print(fcf[fcf['Speed']> 3000] & fcf[fcf['Speed'] < 4000])

# score = -75
# match = (lookup['Lower_Boundary'] <= score) & (lookup['Upper_Boundary'] > score)
# grade = lookup['Grade'][match]

# speed_between_3000_4001 = fcf['Speed'].between(3000, 4001, inclusive=False)
# torque_between_0_16 = fcf['variable'].between(3000, 4001, inclusive=False)
# df["Fuel Consumption(g/s)"] = ""

# df["Fuel Consumption(g/s)"] = df[['Speed(RPM)', 'Torque(Nm)']].apply(lookup_grade)




