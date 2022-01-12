# vehicle-data-analysis

This script reads csv file with vehicle data and then uses look-up tables from othere csv files and works out fuel consumption of the vehicle.


Two arguments are taken:
- Name of file containing dataframe
- Nme of file containing look-up table

Currently this script only works for a 2-D Look-up table of fuel consumption. This mini-project was more of a curiosity project. In university we got given similar data and had to manually use the look-up table. Pandas does not have native support for using look-up tables, especially 2-D look-up tables. 

**In future**:
- I would like to create a generic function, to which we can pass a 2-d Look-up table and data frame. Then the script can automatically use look-up table to fill in a new column.
- Test above functionality using the other csv files present in this rep


***Note: This script requires pandas data analysis software***
