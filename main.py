
# Import modules
from Src.controller import *

# Get data from github
# data = fetch_data()


import pandas as pd
data = pd.read_csv('data-1000.csv')
clean_data(data)

# Save data to csv file
# if data:
#     clean_data(data)

