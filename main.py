import glob
import os
import csv
import errno
from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np
import xlrd

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

def merge_csv(path_to_load_list):
    batch_folder = os.path.dirname(path_to_load_list)
    new_csv_file = r'ARK_Complete.csv'
    missing_csv_file = r'Missing_Patients.csv'
    temp_load_list = r'Temp_Loadlist.csv'
    
    out_csv_file = os.path.join(batch_folder, new_csv_file)
    silent_remove(out_csv_file)

    out_missing_file = os.path.join(batch_folder, missing_csv_file)
    silent_remove(out_missing_file)

    with open(out_missing_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['#', 'Accession Number', 'Panel'])


    temp_loadlist_file = os.path.join(batch_folder, temp_load_list)
    silent_remove(temp_loadlist_file)
    
    list_of_files = glob.glob(os.path.join(batch_folder, '*.csv'))
    
    df = pd.concat((pd.read_csv(f) for f in list_of_files))
    df.sort_values(['Patient No', 'Component Name'], ascending=[True, True], inplace=True)
    df.set_index(['Patient No'], drop=True, inplace=True)

    load_df = pd.read_excel(path_to_load_list)
    load_df.to_csv(temp_loadlist_file)
    check_patients_tested(temp_loadlist_file, df, out_missing_file)
    
    df.drop(['Sample Name', 'Medication'], axis=1, inplace=True)
    df['Calculated Concentration'].fillna('N/A', inplace=True)
    df.rename(columns={'Sample ID': 'Sample Name', 'Component Name': 'Compound Name'},
              inplace=True)
    df.to_csv(out_csv_file)
    silent_remove(temp_loadlist_file)

    
def check_patients_tested(load_list, result_df, out_missing_file):
    grouped = result_df.groupby('Sample ID')
    
    with open(load_list, 'r') as infile, open(out_missing_file, 'a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        next(reader)
        for row in reader:
            if result_df["Sample ID"].isin([row[2]]).any():
                patient = grouped.get_group(row[2])["Sample ID"]
                count = patient.count()
                if count == 66:
                    row.insert(3, 'Remove Dextromethorphan')
                    writer.writerow(row[1:4])
                elif count == 65:
                    pass
                elif count in (59, 60):
                    row.insert(3, 'Missing THC')
                    writer.writerow(row[1:4])
                elif count == 6:
                    row.insert(3, 'Missing PP')
                    writer.writerow(row[1:4])
                else:
                    row.insert(3, 'Missing one or  more')
                    writer.writerow(row[1:4])
                    
            else:
                row.insert(3, 'Not in this data')
                writer.writerow(row[1:4])
        


def make_file_dialog():
    root = Tk()
    root.withdraw()
    root.file_name = filedialog.askopenfilename(parent=root, title='Choose the load list')

    if not root.file_name:
        sys.exit(0)

    merge_csv(root.file_name)

if __name__ == "__main__":
    make_file_dialog()
