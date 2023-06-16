# Import python packages
import time 
import pandas as pd

# Import model
from Src.model import *
from Config.helpers import *

# Fetch data 
def fetch_data():
    query = 'stars:>0'
    res = get_github_repositories(query)
    data = res['data']
    final_data = data

    if data and len(data)>0:
        print('La taille est de :', len(final_data))

        while data[-1]['stargazers_count'] > 10:
            time.sleep(60)
            query = f"stars:<{data[-1]['stargazers_count']}"
            res = get_github_repositories(query)
            data = res['data'] 
            if not data or len(data)<=0:
                print('Data is ', data)
                break
            else:
                final_data.extend(data)
                print('La taille est de :', len(final_data))
    print('Fin du processus')
    return final_data

# Clean and save data
def clean_data(data):
    df = pd.DataFrame(data)
    # Display data size
    print(f"La taille de vos données est de {df.shape[0]} lignes et {df.shape[1]} colonnes")
    
    # Drop unnamed column
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Drop duplicates
    duplicated_rows = df[df.duplicated].shape[0]
    if duplicated_rows > 0:
        print(f"\nVous avez {duplicated_rows} lignes dupliquées. \nVoulez vous les supprimées ?")
        duplicated_res = input('Taper 1 pour Oui, 0 pour non : ')
        duplicated_res = handle_answer(duplicated_res)
        
        if duplicated_res == '1':
            df.drop_duplicates(inplace=True)
            print('\nLes données dupliquées ont été suprimés')
            print('La taille de vos données sont de ',df.shape[0])
            time.sleep(1)
    
    # Display available columns
    print('\nVoici les colonnes de vos données')
    time.sleep(1)
    print(df.columns)

    # Ask to keep with all columns
    print('\nSouhaitez vous conserver toutes les colonnes ?')
    keep_columns_re = input('Taper 1 pour oui 0 pour non : ')
    keep_columns_re = handle_answer(keep_columns_re)
    if keep_columns_re == '0':
        # Demand of the needed columns
        print('\nVeuillez entrez les noms exacts des colonnes que vous voulez conserver')
        conserved_columns = []
        while True:
            conserved_column = input(f"\nTaper q pour quitter\nEntrez le nom exact de la colonne N° {len(conserved_columns)+1}: ")
            if conserved_column in df.columns:
                conserved_columns.append(conserved_column)
            elif conserved_column == 'q':
                if len(conserved_columns) > 0:
                    print('\nVoici les colonnes choisis :')
                    print(conserved_columns)
                    time.sleep(1)
                else:
                    print('\nVous n\'avez choisis aucune colonne.\nVos données contiennent donc toutes les colonnes initiales')
                break
            else:
                print('\nErreur: la colonne choisis n\'existe pas')
    else:
        conserved_columns = df.columns
    # Create final dataframe
    df_final = df[conserved_columns]
    
    print(f"\nLa taille de vos données est de {df_final.shape[0]} lignes et de {df_final.shape[1]} colonnes")
    print('Voulez vous sauvergarder vos données sous forme csv ?')
    save_to_csv_res = input('Taper 1 pour oui 0 pour non : ')
    save_to_csv_res = handle_answer(save_to_csv_res)

    if save_to_csv_res == '0':
        print('\nVos données ne seront pas sauvegarder. Etes vous sur ?')
        final_res = input('Taper 1 pour oui 0 pour non : ')
        final_res = handle_answer(final_res)
        if final_res == '0':
            # Save data to csv
            csv_save_res = save_data_to_csv(df_final, 'github_repos.csv')
            handle_csv_create_file(csv_save_res)
        else:
            print('\nTres bien, au revoir !')
    else:
        # Save data to csv
        csv_save_res = save_data_to_csv(df_final, 'github_repos.csv')
        handle_csv_create_file(csv_save_res)