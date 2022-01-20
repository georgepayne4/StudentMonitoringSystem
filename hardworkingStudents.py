"""
@author: George Payne
Created on Thu Jan 13 18:24:16 2022
"""
# Import libraries
import pandas as pd
import sqlite3

# Import external functions
from DAFunction import *

def hardworkingStudents(database, root, tables):
    """ Function producing summary of hardworking students by 
    pre-defined conditions (within README file).Inputs are as follows:
    database = file name of .db file housing marks
    root = GUI tkinter window frame
    tables = tables in database """
    
    # Clear GUI frame for next display
    clear_all_output(root)
    
    # Load StudentRate csv (student survey)
    rate = pd.read_csv('StudentRate.csv', index_col = False)
    
    # Clean StudentRate for efficient use
    rate.columns.str.strip()
    rate = rate.rename(columns = {'research id':'research_id',
            'What level programming knowledge do you have?':'experience'})
    rate = rate.loc[:, ['research_id','experience']]
    
    # Filter StudentRate by 'experience' is 'Beginner' or 'Below beginner'
    rate.drop(rate.index[rate['experience'] != 'Beginner'] & 
              rate.index[rate['experience'] != 'Below beginner'], inplace = True)
    
    # Define list of all Beginners by student ID
    beginners = list(rate.iloc[:,0])
    
    # Load SumTest grades from the Resultsdatabase file
    results = sqlite3.connect(database)
    
    # Define list of grades for each student and assign
    grades = []
    for s in range(0,len(beginners)):
        table = pd.read_sql('''SELECT * FROM dfFormattedCleanSumTest 
                            WHERE research_id == ''' + str(beginners[s]), results)
        if table.empty == True:
            grades.append(0)
        else:
            grades.append(table.loc[0,'grade'])
    
    rate_grades = rate.assign(grade = grades)
    
    # Filter by grades greater than 60 (drop all grades lower than 60)
    hardworking = rate_grades.drop(rate_grades.index[rate_grades['grade'] < 60])
    
    # Sort students by descending order of their grades
    hardworking.sort_values(['grade'], ascending = False, inplace = True)
    
    # Round values to 2 d.p by calling function
    round_dataframe_values(hardworking, 'last')
    
    # Call display table functionality within tkinter window
    Output = hardworking
    outputTable(Output, root, 'Hardworking', tables)
    
    # Print summary in console (not neccessary for output)
    pd.options.display.float_format = "{:,.2f}".format
    print('Hardworking Students:')
    print(Output)
    
    # Close the database
    results.close()
    

