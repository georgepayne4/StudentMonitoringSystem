"""
@author: George Payne
Created on Mon Jan 10 18:09:07 2022
"""
# Import libraries
import pandas as pd
import numpy as np
import sqlite3

# Import external functions
from DAFunction import *

def underperformingStudents(tables, database, root):
    """ Function producing summary of underperforming students by 
    pre-defined conditions (within README file).Inputs are as follows:
    tables = tables in database
    database = file name of .db file housing marks
    root = GUI tkinter window frame """
    
    # Clear GUI frame for next display
    clear_all_output(root)
    
    # Pull test results from the database file
    results = sqlite3.connect(database)
    
    ## Filter underperforming by results less than 60%
    # Define dataframe storing grades for students with less than 60% in SumTest
    cols = ['student_id'] + list(tables.values())
    u_perf_stus = pd.DataFrame(columns = cols)
    sumTest_underperfs = pd.read_sql('''SELECT * FROM dfFormattedCleanSumTest
                                     WHERE grade < 60''', results)
    u_perf_stus.loc[:,'student_id'] = sumTest_underperfs.loc[:,'research_id']
    
    # Populate dataframe with grades for students with less than 60% in SumTest
    for i in range(0, len(u_perf_stus.loc[:,'student_id'])):
        for l in range(1, len(tables.keys())+1):
            identifier = ' WHERE research_id == ' + str(u_perf_stus.iloc[i,0])
            exam_ref = str(list(tables.keys())[l-1])
            test = pd.read_sql('SELECT * FROM '+ exam_ref + identifier, results)
            if test.empty == True:
                u_perf_stus.iloc[i, l] = 0
            else:
                u_perf_stus.iloc[i, l] = test.loc[:,'grade']
    
    # Set student_id as index
    u_perf_stus.set_index('student_id', inplace = True)
    
    # Create list of all students by ID
    u_perf = u_perf_stus.index.values.tolist()
    
    # Additional Criteria:
        # Delete more than two grades == 0
        # Delete more than one grade > 60 across other test
    
    # Set criteria checkpoints
    for student in u_perf:
        large_grade = []
        for cols in u_perf_stus.columns:
            if u_perf_stus.loc[student, cols] > 60.0:
                large_grade.append(u_perf_stus.loc[student,cols])
                
        large_grade_count = len(large_grade)
        disengaged = list(u_perf_stus.loc[student,:]).count(0)
        
        # Drop students who do not fit the required criteria 
        if disengaged > 2:
            u_perf_stus = u_perf_stus.drop(index = student, axis = 0)
        elif large_grade_count > 1:
            u_perf_stus = u_perf_stus.drop(index = student, axis = 0)
    
    ## Style output dataframe 
    # Round values to 2 d.p by calling function
    round_dataframe_values(u_perf_stus, 'all_')
    
    # Style to dataframe to highlight lowest grade per student        
    for stu in range(0,len(u_perf_stus.index)):
        l_g = np.argmin(u_perf_stus.iloc[stu,:])
        u_perf_stus.iloc[stu,l_g] = '*' + str(u_perf_stus.iloc[stu,l_g]) + '*'
    
    # Sort values by grade of SumTest
    u_perf_stus.sort_values(['SumTest'], ascending = True, inplace = True) 
    
    # Call display table functionality within tkinter window
    Output = u_perf_stus
    outputTable(Output, root, 'Underperforming', tables)
    
    # Print summary in console (not neccessary for output)
    pd.options.display.float_format = "{:,.2f}".format
    print('Underperforming Students:')
    print(Output)
    
    # Close the database
    results.close()
    
