#!/usr/bin/env python3

"""CSVtoDash imports snippets from CSV files into the sqlite3 db used by Dash"""


import csv
import os.path
import sqlite3


def locate_file(file_type):
    while True:
        file_path = input(f'Enter path to your {file_type} file: ')
        if os.path.exists(file_path):
            head, tail = os.path.split(file_path)
            if tail.endswith(f'.{file_type.lower()}'):
                break
            else:
                print(f'{tail} is not a {file_type} file, please check and try again.')
        else:
            print('That file wasn\'t found, please check and try again.')
    return file_path


def get_files():
    csv = locate_file('csv')
    dash = locate_file('dash')
    return csv, dash


def load_csv_data(my_file):
    snippets = []
    with open(my_file, newline='') as csvfile:
        reader = csv.reader(csvfile, dialect='excel')
        for row in reader:
            snippets.append(row)
    return snippets


def main():
    # get files, connect to db
    csv_file, dash_file = get_files()
    csvsnippets = load_csv_data(csv_file)
    conn = sqlite3.connect(dash_file)
    c = conn.cursor()

    # loop through and insert csv data
    for s in csvsnippets:
        c.execute("INSERT INTO snippets (title, body, syntax, usageCount) VALUES ('{0}', '{1}', 'None', 0 )".format(s[1], s[2]))
    conn.commit()
    conn.close()
    print('Operation complete')


if __name__ == "__main__":
    main()
