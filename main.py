
# Import modules
from Src.controller import *

# Get data from github
data = fetch_data()

# Save data to csv file
if data:
    clean_data(data)

