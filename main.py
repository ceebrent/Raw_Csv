import glob
import os
import csv
import errno
import tkinter as tk
from tkinter import filedialog


def merge_txt_to_csv(path_to_directory):
    """ Takes list of files from directory, makes file new each time and sets designated header values"""
    list_of_files = glob.glob(os.path.join(path_to_directory, '*.txt'))
    batch_folder = os.path.dirname(path_to_directory)
    raw_folder = os.path.join(batch_folder, 'RAW')
    os.makedirs(raw_folder, exist_ok=True)

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
        patient_number = headers_in_file[0][headers_in_file[0].index('Patient No')]
        headers = [sample_name, patient_number, component_name, concentration, medication]
        out_csv.writerow(headers)
        # out_csv_opened = csv.writer(open(out_csv_file, 'a', newline=''))
        in_file = list(csv.reader(open(file, 'rt'), delimiter='\t'))
        for rows in in_file:
            if rows[in_file[0].index('Sample Type')] in 'Unknown' and \
                    rows[in_file[0].index('Component Name')].endswith('1'):
                component_name = rows[in_file[0].index('Component Name')]
                sample_name = rows[in_file[0].index('Sample Name')]
                concentration = rows[in_file[0].index('Calculated Concentration')]
                if 'N/A' not in concentration:
                    concentration = '{0:.2f}'.format(float(concentration))
                medication = rows[in_file[0].index('Medication')]
                patient_number = rows[in_file[0].index('Patient No')]

                values = [sample_name, patient_number, component_name, concentration, medication]
                out_csv.writerow(values)

def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

def main():
    root = tk.Tk()
    root.withdraw()
    file_path = tk.filedialog.askdirectory()
    raw_folder = os.path.dirname(file_path)
    merge_txt_to_csv(file_path)

main()