"""
@author: George Payne
Created on Thu Jan  6 15:08:27 2022
"""
# Import libraries
import pandas as pd
import sqlite3

# Import external functions
from DAFunction import *

# Define Function: Summary of question performance by student and test
def studentPerformance(tables, student_id, test, database, root):
    """ Function producing summary of student performance by taking
    student ID and test as input to produce a breakdown of absolute
    and relative performance. Variable inputs are as follows:
    tables = tables in database
    student_id = ID to be specified by user
    test = tests wished to be analysed
    database = file name of .db file housing marks
    root = GUI tkinter window frame """
        
    # Clear GUI frame for next display
    clear_all_output(root)
    
    # Check valid student ID
    validity = valid_student(tables, student_id, database, str(get_key(test, tables)))
    if validity == 'invalid':
        # Call error pop up function for invalid student ID
        error()
    else:
        # Pull student results
        results = sqlite3.connect(database)
    
        # Define the Test to analyse (get_key function)
        exam_ref = str(get_key(test, tables))
    
        # Pull data from the database
        tab = pd.read_sql('SELECT * FROM ' + exam_ref, results)
        stu_record = pd.read_sql('SELECT * FROM ' + exam_ref + 
                                 ' WHERE research_id == ' + str(student_id), results)
    
        # Find mean grade per question
        mean = []
        for q in range(4, len(tab.columns)):
            mean.append(tab.iloc[:, q].mean())
            q += 1
        
        # Get student grade for each question
        absolute = []
        for a in range(4, len(tab.columns)):
            absolute.append(stu_record.iloc[0, a])
            a += 1
        
        # Create relative performance for each question
        relative = []
        for r in range(0, len(absolute)):
            relative.append(absolute[r] - mean[r])
        
        # Create dictionary of question numbers
        question_numbers = {}
        for n in range(0, len(absolute)):
            question_numbers[str(n)] = 'Q' + str(n+1)
            n += 1
            
        ## Store axes for plotting
        # Absolute performance
        x = question_numbers.values()
        y = absolute
        # Relative performance 
        x2 = question_numbers.values()
        y2 = relative
    
        # Close SQL database file
        results.close()
        
        # Call plot functionality within tkinter window
        outputGraph('stuPerformance', x, y, x2, y2, student_id, root, test)

