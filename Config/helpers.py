# Import python packages
import pandas as pd

# Save data to csv
def save_data_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename)

# Concatenate files
def concatenate_files(file1, file2, exportFile):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    concatenate_df = pd.concat([df1, df2], ignore_index=True)
    result = concatenate_df.to_csv(exportFile, index=False)
    
    if not result:
        print('CSV files concatenated successfully, size to ', concatenate_df.shape[0])
    else:
        print('Error :',result)

# Answer 1 or 0
def handle_answer(answer):
    while answer != '1' and answer != '0':
        answer = input('Veuillez choisir 1 pour oui, 0 pour non : ')
    return answer

# handle csv creating file
def handle_csv_create_file(answer):
    if not answer:
        print('\nLe fichier github_repos.csv a bien été créer')
    else:
        print('Erreur : ',answer)

# Display size of data
def display_data_size(data):
    print('La taille des données récuperer est de ',len(data))

# Display error message github api
def display_error_message_api():
    print('Erreur: Nous sommes désolé mais l\'API de github subi de nombreuses demande.')
    print('Veuillez réessayer ultérieurement')

# Ask to continue fetching data from github api
def continue_fetching_data_from_api():
    print('\nVoulez vous continuer ?')
    continue_res = input('Taper 1 pour oui 0 pour non : ')
    continue_res = handle_answer(continue_res)
    return continue_res

# Get columns name with dict or list dtypes
def get_columns_name_type_dict_list(df):
    # Get columns with object dtype
    object_columns = df.select_dtypes(include='object').columns

    # Create a list that will contain dict and list dtype
    columns_with_objects = []
    for column in object_columns:
        if df[column].apply(lambda x: isinstance(x, (dict, list))).any():
            columns_with_objects.append(column)
    return columns_with_objects

# Has null values in columns
def has_null_values_column(df):
    has_null_columns = {}
    for column in df.columns:
        null_length = df.loc[df[column].isnull()].shape[0]
        if null_length > 0:
            has_null_columns[column] = null_length
    return has_null_columns