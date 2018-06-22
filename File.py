'''
This module contains a class File which contains information about different files in the directory.
'''

import os


class File:
    
    ''' 
    A constructor function for File class.
    Parameters:
        (string) path - Path of the file in system.
    '''
    def __init__(self , path):
        self.path = path
        
        # Check for any problem in openning the file. (Like - Permission denied.)
        try:
            open(self.path , "rb")
            self.name = os.path.basename(self.path)
        except IOError as e:
            print (e)
            self.path = None
     
    '''
    A funtion to get the size of the file.   
    
    Return:
        Size of the file.        
    '''
    def size(self):
        if self.path == None:
            return 0
        file_object = open(self.path , "rb")
        file_object.seek(0 , 2)
        return file_object.tell()
