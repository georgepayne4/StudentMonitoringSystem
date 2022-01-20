"""
@author: B810449
Created on Thu Jan  6 15:08:27 2022
"""
# Import libraries
import pandas as pd
import sqlite3

# Import external functions
from DAFunction import *

# Define Function: Summary of grade by test
def testResults(tables, student_id, database, root):
    
    """ Takes student ID as input to pull graph of their
    performance across all tests. Variables are as follows:
    tables = tables in database
    student_id = ID to be specified by user
    database = file name of .db file housing marks
    root = GUI tkinter window frame """
    
    # Clear GUI frame for next display
    clear_all_output(root)

    # Check valid student ID
    validity = valid_student(tables, student_id, database, 'all_')
    if validity == 'invalid':
        # Call error pop up function for invalid student ID
        error()
    else:
        # Access database
        results = sqlite3.connect(database)
    
        # Define dataframe housing grades for each test
        stu_summary = pd.DataFrame(index = tables.keys(), columns = ['totals'])
    
        # Populate dataframe
        for l in range(0, len(tables.keys())):
            identifier = ' WHERE research_id == ' + str(student_id)
            exam_ref = str(list(tables.keys())[l])
            test = pd.read_sql('SELECT * FROM ' + exam_ref + identifier, results)
    
            if test.empty == True:
                stu_summary.iloc[l, :] = 0
            else:
                stu_summary.iloc[l, :] = test.loc[:,'grade']
        
        # Store axes for plotting
        x = tables.values()
        y = stu_summary['totals']
        
        # Dummy varaibles to run plot function
        x2 = 0
        y2 = 0
        
        # Close the database
        results.close()
        
        # Call plot functionality within tkinter window
        outputGraph('testResults', x, y, x2, y2, student_id, root, 'all_')
        






