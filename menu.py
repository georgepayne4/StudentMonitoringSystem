"""
@author: George Payne
Created on Fri Jan  7 16:43:42 2022
"""
# Import Modules
import sqlite3
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Import external functions
from testResults import *
from studentPerformance import *
from underperformingStudents import *
from hardworkingStudents import *
from DAFunction import *


# Define database tables (tests) for the monitoring system
con = sqlite3.connect('Resultdatabase.db')
cursor = con.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
db_tables = cursor.fetchall()
con.close()

# Clean output to obtain lists for keys and values
db_table_vals = []
test_options = []
for v in range(0, len(db_tables)):
    db_tables[v] = str(db_tables[v]).replace("',)",'')
    db_tables[v] = str(db_tables[v]).replace("('",'')
    db_table_vals.append(db_tables[v].replace('dfFormattedClean',''))
    
# Zip keys and values creating a dictionary of tables within database
table_dict = dict(zip(db_tables, db_table_vals))


def Main():
    """ Function housing the tkinter GUI dashboard used to 
    run the functionality of finding result information """
    
    ## CREATE GUI 
    root = tk.Tk()
    root.resizable(False, False)
    dash_font_header = 'Bahnschrift SemiBold SemiConde'
    dash_font_body = 'Bahnschrift Light'
    
    # Define interface design
    page = tk.Frame(root, width = 1450, height = 25, bg = '#751973')
    page.grid(columnspan = 6)
    
    page_input = tk.Frame(root, width = 1450, height = 350, bg = 'white')
    page_input.grid(columnspan = 6, rowspan = 10)
    
    page_output = tk.Frame(root, width = 1450, height = 350, bg = 'white')
    page_output.grid(columnspan = 6, rowspan = 30)
    
    # Add margin to base of menu file window
    page = tk.Frame(root, width = 1450, height = 50, bg = '#751973')
    page.grid(columnspan = 6)
    
    
    # Initial instructions
    instructions = tk.Label(root, 
                            text = 'Welcome to your monitoring system!',
                            font = (dash_font_header, 25), bg = 'white')
    instructions.grid(columnspan = 6, column = 0, row = 1)
    
    instructions_1 = tk.Label(root, 
                            text = 'Select an option:',
                            font = (dash_font_body, 10), bg = 'white')
    instructions_1.grid(columnspan = 6, column = 0, row = 2)
    
    
    ## Create the input boxes
    
    # testResults input and label for student ID
    stu_id_label_1 = tk.Label(root, 
                            text = 'Enter student ID:*', fg = '#751973',
                            font = (dash_font_body, 10), bg = 'white')
    stu_id_label_1.grid(column = 1, row = 5)
    studentID_box_1 = tk.Entry(root, width = 30, bg = 'white')
    studentID_box_1.grid(column = 1, row = 6)
    
    # studentPerformance input and label for student ID
    stu_id_label_2 = tk.Label(root, 
                            text = 'Enter student ID:*', fg = '#751973',
                            font = (dash_font_body, 10), bg = 'white')
    stu_id_label_2.grid(column = 2, row = 5)
    studentID_box_2 = tk.Entry(root, width = 30, bg = 'white')
    studentID_box_2.grid(column = 2, row = 6)
    
    # studentPerformance drop-down input and label for test name
    test_id_label = tk.Label(root, 
                            text = 'Select exam from dropdown:*', fg = '#751973',
                            font = (dash_font_body, 10), bg = 'white')
    test_id_label.grid(column = 2, row = 7)
    inside_txt_drop = tk.StringVar()
    inside_txt_drop.set(next(iter(table_dict.values())))
    test_id_dropbox = tk.StringVar(root)
    test_id_dropbox = tk.OptionMenu(root, inside_txt_drop, *table_dict.values())
    test_id_dropbox.config(width = 25, height = 1, bg = 'white', 
                           fg = '#751973', borderwidth = 0)
    test_id_dropbox.grid(column = 2, row = 8)
    
    
    ## Navigation Buttons with functionality
    
    # Student Test Results by student ID (testResults.py)
    Stu_TR_text = tk.StringVar()
    Stu_TR_btn = tk.Button(root, textvariable = Stu_TR_text, 
                           command = lambda:testResults(table_dict, 
                                                        studentID_box_1.get(),
                                                        'Resultdatabase.db', 
                                                        page_output),
                           font = (dash_font_body, 10),
                           bg = '#751973', fg = 'white', height = 2, width = 30)
    Stu_TR_text.set('Test Results by Student ID')
    Stu_TR_btn.grid(column = 1, row = 4)
    
    # Student marks by student ID and test (studentPerformance.py)
    Stu_Perf_text = tk.StringVar()
    Stu_Perf_btn = tk.Button(root, textvariable = Stu_Perf_text, 
                           command = lambda:studentPerformance(table_dict, 
                                                               studentID_box_2.get(), 
                                                               inside_txt_drop.get(),
                                                               'Resultdatabase.db', 
                                                               page_output),
                           font = (dash_font_body, 10),
                           bg = '#751973', fg = 'white', height = 2, width = 30)
    Stu_Perf_text.set('Student Performance')
    Stu_Perf_btn.grid(column = 2, row = 4)
    
    # Underperforming students (underperformingStudents.py)
    underPerf_text = tk.StringVar()
    underPerf_btn = tk.Button(root, textvariable = underPerf_text, 
                           command = lambda:underperformingStudents(table_dict, 
                                                                    'Resultdatabase.db',
                                                                    page_output),
                           font = (dash_font_body, 10),
                           bg = '#751973', fg = 'white', height = 2, width = 30)
    underPerf_text.set('Underperforming Students')
    underPerf_btn.grid(column = 3, row = 4)
    
    # Hardworking students (hardworkingStudents.py)
    hardWrk_text = tk.StringVar()
    hardWrk_btn = tk.Button(root, textvariable = hardWrk_text, 
                           command = lambda:hardworkingStudents('Resultdatabase.db', 
                                                                page_output, 
                                                                table_dict),
                           font = (dash_font_body, 10),
                           bg = '#751973', fg = 'white', height = 2, width = 30)
    hardWrk_text.set('Hardworking Students')
    hardWrk_btn.grid(column = 4, row = 4)
    
    
    # Close the GUI loop
    root.mainloop()


# Call the GUI interface function
Main()
