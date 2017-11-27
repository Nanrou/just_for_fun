import os
import pickle

from write_sheet import sheet_one, sheet_two

def do_it():
    filenames = os.listdir('./pickle_folder')
    for filename in filenames:
        with open('./pickle_folder/{}'.format(filename), 'rb') as rf:
            data = pickle.load(rf)
        sheet_one(data)
        print('done {}'.format(filename))

        
def do_that():
    filenames = os.listdir('./pickle_folder/water')
    for filename in filenames:
        with open('./pickle_folder/water/{}'.format(filename), 'rb') as rf:
            data = pickle.load(rf)
        sheet_two(data)
        print('done {}'.format(filename))
        

if __name__ == '__main__':
    do_it()

        