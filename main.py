import glob
import os
import csv
import errno
from tkinter import *
from tkinter import filedialog
import pandas as pd
import numpy as np


def merge_txt_to_csv(path_to_directory):
    """ Takes list of files from directory, makes file new each time and sets designated header values"""
    list_of_files = glob.glob(os.path.join(path_to_directory, '*.txt'))
    batch_folder = os.path.dirname(path_to_directory)
    raw_folder = os.path.join(batch_folder, 'ARK_RAW')
    os.makedirs(raw_folder, exist_ok=True)
    skip_drugs = ['Modafinil 1', 'Norcodeine 1', 'Methylone 1', 'Mephedrone 1', 'MDPV 1',
                  'JWH-018N-PentanoicAcid 1', 'JWH-073-4OHbutyl 1', 'JWH-073-4OHbutyl 1',
                  'LSD 1', 'dextromethorphan 1', 'Ephedrine 1', 'Nalbuphine 1', 'pentazocine 1',
                  'JWH-073-N-Butanoic acid/JWH-018-5OHpentyl 1', 'Methcathinone 1']

    for file in list_of_files:
        new_csv_file = os.path.basename(file.replace('.txt', '.csv'))
        out_csv_file = os.path.join(raw_folder, new_csv_file)
        silent_remove(out_csv_file)
        out_csv = csv.writer(open(out_csv_file, 'a', newline=''))
        headers_in_file = list(csv.reader(open(file, 'rt'), delimiter='\t'))
        # print(headers_in_file)
        # original_filename = headers_in_file[0][headers_in_file[0].index('Original Filename')]
        sample_name = headers_in_file[0][headers_in_file[0].index('Sample Name')]
        component_name = headers_in_file[0][headers_in_file[0].index('Component Name')]
        concentration = headers_in_file[0][headers_in_file[0].index('Calculated Concentration')]
        medication = headers_in_file[0][headers_in_file[0].index('Medication')]
        sample_id = headers_in_file[0][headers_in_file[0].index('Sample ID')]
        try:
            patient_number = headers_in_file[0][headers_in_file[0].index('Patient No')]
        except ValueError:
            patient_number = headers_in_file[0][headers_in_file[0].index('Patient No.')]

        headers = [sample_name, patient_number, component_name, concentration, medication,
                   sample_id]
        out_csv.writerow(headers)
        # out_csv_opened = csv.writer(open(out_csv_file, 'a', newline=''))
        in_file = list(csv.reader(open(file, 'rt'), delimiter='\t'))
        for rows in in_file:
            if rows[in_file[0].index('Sample Type')] in 'Unknown' and \
                    rows[in_file[0].index('Component Name')].endswith('1') and \
                    rows[in_file[0].index('Component Name')] not in skip_drugs:
                component_name = rows[in_file[0].index('Component Name')]
                sample_name = rows[in_file[0].index('Sample Name')]
                concentration = rows[in_file[0].index('Calculated Concentration')]
                sample_id = rows[in_file[0].index('Sample ID')]

                if concentration not in ('N/A', '< 0'):
                    concentration = '{0:.2f}'.format(float(concentration))
                medication = rows[in_file[0].index('Medication')]
                try:
                    patient_number = rows[in_file[0].index('Patient No')]
                except ValueError:
                    patient_number = rows[in_file[0].index('Patient No.')]

                values = [sample_name, patient_number, component_name, concentration, medication,
                          sample_id]
                out_csv.writerow(values)


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
def make_file_dialog():
    root = Tk()
    root.withdraw()
    root.file_name = filedialog.askdirectory(parent=root, title='Choose a TXT folder')

    if not root.file_name:
        sys.exit(0)

    merge_csv(root.file_name)

##merge_csv(r'\\192.168.0.242\profiles$\massspec\Desktop\ARK_RAw')
if __name__ == "__main__":
    make_file_dialog()
