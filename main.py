import glob
import os
import csv
import errno
from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

def merge_csv(path_to_directory):
##    batch_folder = os.path.dirname(path_to_directory)
    new_csv_file = r'ARK_Complete.csv'
    out_csv_file = os.path.join(path_to_directory, new_csv_file)
    silent_remove(out_csv_file)
    list_of_files = glob.glob(os.path.join(path_to_directory, '*.csv'))
##    header_csv = csv.writer(open(out_csv_file, 'w'))
##    headers = ['Sample Name', 'Patient No', 'Component Name', 'Calculated Concentration',
##               'Medication', 'Sample ID']
##    header_csv.writerow(headers)
##
##    for file in list_of_files:
##        with open(file, 'r') as infile, open(out_csv_file, 'a') as outfile:
##            next(infile, None)
##            reader = csv.reader(infile)
##            writer = csv.writer(outfile)
##            for row in reader:
##                writer.writerow(row)
    
    df = pd.concat((pd.read_csv(f) for f in list_of_files))
    df.sort_values(['Patient No', 'Component Name'], ascending=[True, True], inplace=True)
    df.set_index(['Patient No'], drop=True, inplace=True)
    df.drop(['Sample Name', 'Medication'], axis=1, inplace=True)
    df['Calculated Concentration'].fillna('N/A', inplace=True)
    df.rename(columns={'Sample ID': 'Sample Name', 'Component Name': 'Compound Name'},
              inplace=True)
    df.to_csv(out_csv_file)
##    Need to update to take loadlist as file, then use directory for ark raw
    load_list = r'C:\Users\massspec\Downloads\Batch 709 - ARK.xlsx'
    check_patients_tested(load_list, df)
    
def check_patients_tested(load_list, result_df):
    load_df = pd.read_excel(load_list)
    
    
    print(result_df.loc[result_df['Sample Name'].isin(list(load_df.columns[1]))].head())


    print(load_df[load_df.columns[1]].head())
    print(result_df['Sample Name'].head())

def make_file_dialog():
    root = Tk()
    root.withdraw()
    root.file_name = filedialog.askdirectory(parent=root, title='Choose a TXT folder')

    if not root.file_name:
        sys.exit(0)

    merge_csv(root.file_name)

merge_csv(r'\\192.168.0.242\profiles$\massspec\Desktop\ARK_RAw')
##if __name__ == "__main__":
##    make_file_dialog()
