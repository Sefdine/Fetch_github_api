# Import python packages
import time 
import pandas as pd
import missingno as msno

# Import model
from Src.model import *
from Config.helpers import *

# Fetch data 
def fetch_data():
    print('Chargement...')
    query = 'stars:>0'
    res = get_github_repositories(query)
    data = res['data']
    final_data = data

    if data and len(data)>0:
        display_data_size(final_data)
        continue_res = continue_fetching_data_from_api()

        while data[-1]['stargazers_count'] > 10 and continue_res == '1':
            print('Chargement...')
            time.sleep(60)
            query = f"stars:<{data[-1]['stargazers_count']}"
            res = get_github_repositories(query)
            data = res['data'] 
            if not data or len(data)<=0:
                display_error_message_api()
                break
            else:
                final_data.extend(data)
                display_data_size(final_data)
            continue_res = continue_fetching_data_from_api()
    else:
        display_error_message_api()
    print('\nFin du processus')
    return final_data

# Mirror_url null values
def handle_mirror_url_null_values(df, has_null_columns):
    if 'mirror_url' in has_null_columns:
        print('La colonne mirroir represente une copie du dépot dans un autre emplacement.\nCette colonne ne nous sera pas utile pour ce projet.')
        print('Voulez vous supprimer la supprimé ?')
        delete_mirror_url_res = input('Taper 1 pour oui 0 pour non : ')
        delete_mirror_url_res = handle_answer(delete_mirror_url_res)
        if delete_mirror_url_res == '1':
            df.drop('mirror_url', axis=1, inplace=True)
            print('La suppression a reussi\n')
    return df

# Homepage null values
def handle_homepage_null_values(df, has_null_columns):
    if 'homepage' in has_null_columns:
        print('La colonne homepage fait reference aux pages d\'accueil de contribution.\nCette colonne ne nous sera pas utile pour ce projet')
        print('Voulez vous supprimer la supprimé ?')
        delete_homepage_res = input('Taper 1 pour oui 0 pour non : ')
        delete_homepage_res = handle_answer(delete_homepage_res)
        if delete_homepage_res == '1':
            df.drop('homepage', axis=1, inplace=True)
            print('La suppression a reussi\n')
    return df

# License null values
def handle_license_null_values(df, has_null_columns):
    if 'license' in has_null_columns:
        print('La colonne license décrit les licences utilisé dans un dépôt. Elle contient dans notre dataframe, un objet de type dictionnaire.\n')
        print('Voici un example d\'un element dans la colonne license')
        license_example = df.loc[df['license'].notnull(), 'license'][0]
        print(license_example)
        print('\nOn vous propose de prendre uniquement les noms pour chaque licence\n')
        print('Voulez vous garder la colonne license en entier ?')
        licence_all_res = input('Taper 1 pour oui 0 pour non : ')
        licence_all_res = handle_answer(licence_all_res)
        if licence_all_res == '0':
            print('Veuillez écrire les noms exactes des champs que vous voulez garder : \n')
            license_columns_to_keep = []
            while True:
                print('Entrer q pour quitter')
                column = input(f"Entrer le champ n°{len(license_columns_to_keep)+1} : ")
                if column == 'q':
                    if len(license_columns_to_keep) == 0:
                        print('Vous n\'avez choisis aucun champ. La colonne license va être supprimée.\n')
                        print('Êtes vous sur de vouloir supprimé la colonne license en entier ?')
                        licence_all_delete_res = input('Taper 1 pour oui 0 pour non : ')
                        licence_all_delete_res = handle_answer(licence_all_delete_res)
                        if licence_all_delete_res == '1':
                            # Drop license column
                            df.drop('license', axis=1, inplace=True)
                            print('La colonne license a bien été supprimée\n')
                            break
                    else:
                        print('Voici les champs choisi : ',license_columns_to_keep)
                        break
                elif column in license_example.keys():
                    if column not in license_columns_to_keep:
                        license_columns_to_keep.append(column)
                    else:
                        print('Vous avez déjà choisi ce champs. Veuillez indiquer un autre\n.')
                else:
                    print('Le champs choisi n\'exist pas en tant que clé de la colonne license\n')
            # Create new columns based on license
            if len(license_columns_to_keep) > 0:
                for name in license_columns_to_keep:
                    df['license'+str.capitalize(name)] = df['license'].apply(lambda x: x[name] if pd.notnull(x) else None)
                    print(f"La colonne {'license'+str.capitalize(name)} a bien été crée")
                df.drop('license', axis=1, inplace=True)
    return df

# Language null values
def handle_language_null_values(df, has_null_columns):
    if 'language' in has_null_columns:
        print('\nLa colonne language montre le language principale utilisé dans un dépôt')
        print('Les lignes n\'ayant pas de language sont font reference à des dépôts d\'annuaire pour des livres ou autres chose')
        print('Il est essentiel dans notre projet d\'avoir un language de programmation.\n')
        print('\nDe ce fait, nous te conseillons de supprimer tous les lignes n\'ayant pas de language.')
        print('\nVoulez vous supprimé les lignes qui n\'ont pas de language ?')

        delete_language_res = input('Taper 1 pour oui 0 pour non : ')
        delete_language_res = handle_answer(delete_language_res)
        if delete_language_res == '1':
            # Delete language null values
            df.dropna(subset=['language'], inplace=True)
            print('La suppression a bien été effectué\n')
    return df

# Language null values
def handle_description_null_values(df, has_null_columns):
    if 'description' in has_null_columns:
        print('La colonne description montre une description du projet.\nCe n\'est pas pertinent de supprimer les lignes ne contenant pas de description car vous riquez de perdre d\'autres informations pertinentes')
        print('Nous vous proposons de changer les valeurs nulles de cette colonne par "No description"')
        print('\nVoulez vous changer les descriptions nulles par "No description" ?')
        change_description_res = input('Taper 1 pour oui 0 pour non : ')
        change_description_res = handle_answer(change_description_res)
        if change_description_res == '1':
            # Fill null descriptions
            df['description'].fillna('No description', inplace=True)
            print('Les descriptions nulles ont bien été changé\n')
    return df  

# Display percentages of null values in columns
def display_null_values_column(df):
    has_null_columns = has_null_values_column(df)
    if len(has_null_columns) > 0:
        print('\nCes colonnes contient n% de valeurs nulles.')
        for i in has_null_columns:
            print(i, '\t => ',round((has_null_columns[i] / len(df)*100), 2),'%')
    return has_null_columns

# Clean and save data
def clean_data(data):
    df = pd.DataFrame(data)
    # Display data size
    print(f"La taille de vos données est de {df.shape[0]} lignes et {df.shape[1]} colonnes")
    # Drop unnamed column
    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    # Check column that contain object
    object_columns = get_columns_name_type_dict_list(df)
    
    # Display missing values 
    has_null_columns = display_null_values_column(df)
    if len(has_null_columns) > 0:
        print('\n----------------- Traitement des valeurs nulles --------------\n')
        # ************ Mirror_url *************
        df = handle_mirror_url_null_values(df, has_null_columns)
        # ************ Homepage *************
        df = handle_homepage_null_values(df, has_null_columns)
        # ************ Licence *************
        df = handle_license_null_values(df, has_null_columns)
        # ************ Language *************
        df = handle_language_null_values(df, has_null_columns)
        # ************ Description *************
        df = handle_description_null_values(df, has_null_columns)

    has_null_columns = display_null_values_column(df)

    # # Display columns with list or dict dtype
    # object_columns = get_columns_name_type_dict_list(df)
    # if object_columns:
    #     print('Ces colonnes de votre dataset contiennet des objets')
    #     print(df[object_columns].head())
    #     print('Voulez vous les supprimés ?')
    #     # Ask to delete columns with object dict and list
    #     dict_list_res = input('Taper 1 pour oui 0 pour non : ')
    #     dict_list_res = handle_answer(dict_list_res)

    #     if dict_list_res == '1':
    #         df.drop(object_columns, axis=1, inplace=True)
    
    # # Display available columns
    # print('\nVoici les colonnes de vos données')
    # time.sleep(1)
    # print(df.columns)

    # # Ask to keep with all columns
    # print('\nSouhaitez vous conserver toutes les colonnes ?')
    # keep_columns_re = input('Taper 1 pour oui 0 pour non : ')
    # keep_columns_re = handle_answer(keep_columns_re)
    # if keep_columns_re == '0':
    #     # Demand of the needed columns
    #     print('\nVeuillez entrez les noms exacts des colonnes que vous voulez conserver')
    #     conserved_columns = []
    #     while True:
    #         conserved_column = input(f"\nTaper q pour quitter\nEntrez le nom exact de la colonne N° {len(conserved_columns)+1}: ")
    #         if conserved_column in df.columns:
    #             conserved_columns.append(conserved_column)
    #         elif conserved_column == 'q':
    #             if len(conserved_columns) > 0:
    #                 print('\nVoici les colonnes choisis :')
    #                 print(conserved_columns)
    #                 time.sleep(1)
    #             else:
    #                 print('\nVous n\'avez choisis aucune colonne.\nVos données contiennent donc toutes les colonnes initiales')
    #             break
    #         else:
    #             print('\nErreur: la colonne choisis n\'existe pas')
    # else:
    #     conserved_columns = df.columns
    # # Create final dataframe
    # df_final = df[conserved_columns]

    # # Drop duplicates
    # object_columns = list(set(object_columns).intersection(df_final.columns))
    # duplicated_rows = df_final[df_final.duplicated(subset=df_final.columns.difference(object_columns))].shape[0]

    # if duplicated_rows > 0:
    #     print(f"\nVous avez {duplicated_rows} lignes dupliquées. \nVoulez vous les supprimées ?")
    #     duplicated_res = input('Taper 1 pour Oui, 0 pour non : ')
    #     duplicated_res = handle_answer(duplicated_res)
        
    #     if duplicated_res == '1':
    #         df_final.drop_duplicates(subset=df_final.columns.difference(object_columns), inplace=True)
    #         print('\nLes données dupliquées ont été suprimés')
    #         print('La taille de vos données sont de ',df_final.shape[0])
    #         time.sleep(1)
    
    # print(f"\nLa taille de vos données est de {df_final.shape[0]} lignes et de {df_final.shape[1]} colonnes")
    # print('Voulez vous sauvergarder vos données sous forme csv ?')
    # save_to_csv_res = input('Taper 1 pour oui 0 pour non : ')
    # save_to_csv_res = handle_answer(save_to_csv_res)

    # if save_to_csv_res == '0':
    #     print('\nVos données ne seront pas sauvegarder. Etes vous sur ?')
    #     final_res = input('Taper 1 pour oui 0 pour non : ')
    #     final_res = handle_answer(final_res)
    #     if final_res == '0':
    #         # Save data to csv
    #         csv_save_res = save_data_to_csv(df_final, 'github_repos.csv')
    #         handle_csv_create_file(csv_save_res)
    #     else:
    #         print('\nTres bien, au revoir !')
    # else:
    #     # Save data to csv
    #     csv_save_res = save_data_to_csv(df_final, 'github_repos.csv')
    #     handle_csv_create_file(csv_save_res)