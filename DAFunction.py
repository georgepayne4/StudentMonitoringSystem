"""
@author: B810449
Created on Fri Jan  7 18:24:10 2022
"""
# Import libraries
import pandas as pd
import sqlite3
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import *


def get_key(test_name, table_dict):
    """Find key from given value for database tables dictionary"""
    
    # Find key from value in the tables dictionary
    for key, value in table_dict.items():
        if test_name == value:
            return str(key)


def valid_student(table_dict, ID, database, test_ref):
    """Checking the validity of the student ID using as
    inputs: tables in database, student ID value, database 
    and indicator of which tables to check in the database """
    
    # Connect to the database
    results = sqlite3.connect(database)
    
    # Initialise elemnet to inspect validity
    count = 0
    
    # Check input variable is correct type (deal with non-int values)
    try:
        ID = int(ID)
    except ValueError:
        count = len(table_dict.keys())
    
    # Check input variable is correct type (deal with blank values)
    if isinstance(ID, int) == False:
        count = len(table_dict.keys())
    else:
        # Run check of existance through required tables within database
        if str(test_ref) == 'all_':
            for i in range(0, len(table_dict.keys())):
                exam_ref = str(list(table_dict.keys())[i])
                identifier = ' WHERE research_id == ' + str(ID)
                table = pd.read_sql('SELECT grade FROM ' + exam_ref + identifier, results)
                if table.empty == True:
                    count += 1
                    i += 1
                else:
                    i += 1
        else:
            exam_ref = test_ref
            identifier = ' WHERE research_id == ' + str(ID)
            table = pd.read_sql('SELECT grade FROM ' + exam_ref + identifier, results)
            if table.empty == True:
                count = len(table_dict.keys())
            else:
                count = 0
    
    # Assess validity key (count) and assign meaning
    if count == len(table_dict.keys()):
        n = str('invalid')
    else:
        n = str('valid')
        
    # Close database 
    results.close()
    
    # Return validity as output
    return n

    
def error():
    """Display error box messgae for invalid student ID """
    tk.messagebox.showerror(title = 'Error', 
                            message = 'This Student ID is invalid:\nPlease try again.')


def outputTable(output, root, func_ref, table_dict):
    """Display table in the tkinter window. Inputs are as follows:
        output = table defined in function where this is called
        root = tkinter frame to display output
        func_ref = indicator for output style
        table_dict = dictionary of database tables """
        
    # Style configurations of table
    style = ttk.Style()
    style.configure(root, background = 'white')
    style.map('Treeview', background = [('selected', '#751973')])
    
    # Define title to display in tkinter frame 
    OutputLabel_txt = tk.StringVar()
    OutputLabel = tk.Label(root, textvariable = OutputLabel_txt, fg = '#751973',
                            font = ('Bahnschrift SemiBold SemiConde', 15), bg = 'white')
    OutputLabel_txt.set(str(func_ref) + ' Students')

    # Create table display    
    if str(func_ref) == 'Underperforming':
        cols = ['Student ID'] + list(table_dict.values())
        tab = ttk.Treeview(root, columns = cols, show = 'headings')
        for i in range(0, len(cols)):
            tab.heading(i, text = cols[i])
            tab.column(i)
        output.reset_index(inplace = True)
        for student in output.index:
            row = (output.iloc[student]).tolist()
            tab.insert('', 'end', values = (row))
        tab.grid(columnspan = 6, column = 0, row = 12)
        OutputLabel.grid(columnspan = 6, column = 0, row = 11)
    elif str(func_ref) == 'Hardworking':
        cols = ['Student_ID','Experience', 'Grade']
        tab = ttk.Treeview(root, columns = cols, show = 'headings')
        for i in range(0, len(cols)):
            tab.heading(i, text = cols[i])
            tab.column(i)
        output.reset_index(inplace = True)
        for student in output.index:
            row = (output.iloc[student]).tolist()
            row = row[1:]
            tab.insert('', 'end', values = (row))
        tab.grid(columnspan = 6, column = 0, row = 22)
        OutputLabel.grid(columnspan = 6, column = 0, row = 21)
    
    
def outputGraph(func_ref, x, y, x2, y2, student_id, root, test):
    """Plotting function taking axis values as inputs.
    func_ref = refers to which style to output
    x, y, x2, y2 = indicate axis values
    student_id = studetn ID
    root = tkinter frame display window
    test = test reference from database (from input value) """
    
    # Create plots and place in frame 
    if str(func_ref) == 'testResults':
        
        # Define figure plot
        fig = Figure(figsize=(5,5))
        g = fig.add_subplot(111)
        g.bar(x, y, color = '#751973')
        g.set_title('Student ' + str(student_id) + ': Grades')
        g.set_xlabel('Test')
        g.set_ylabel('Percentage Achieved')  
        
        # Place the plot in the window
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().grid(columnspan = 6, column = 0, row = 1)
        canvas.draw()
        
    elif str(func_ref) == 'stuPerformance':
        
        # Define title
        plots_title_txt = tk.StringVar()
        plots_title = tk.Label(root, textvariable = plots_title_txt, fg = '#751973',
                                font = ('Bahnschrift SemiBold SemiConde', 15), bg = 'white')
        plots_title_txt.set('Student #' + str(student_id) + ' Performance for ' + str(test))
        plots_title.grid(columnspan = 6, column = 0, row = 0)
        
        ## Define figure plots 
        
        # Plot 1 - create figure
        fig = Figure(figsize=(6,4))
        absolute = fig.add_subplot(111)
        absolute.bar(x, y, color = '#751973')
        absolute.set_title('Absolute Results')
        absolute.set_xlabel('Question Number')
        absolute.set_ylabel('Percentage Achieved')
        
        # Place the plot in the window
        canvas_1 = FigureCanvasTkAgg(fig, root)
        canvas_1.get_tk_widget().grid(columnspan = 3, column = 0, row = 1)
        canvas_1.draw()
        
        # Plot 2 - create figure
        fig = Figure(figsize=(6,4))
        absolute = fig.add_subplot(111)
        absolute.bar(x2, y2, color = '#751973')
        absolute.set_title('Relative Performance')
        absolute.set_xlabel('Question Number')
        absolute.set_ylabel('Relative Percentage')  

        # Place the plot in the window
        canvas_2 = FigureCanvasTkAgg(fig, root)
        canvas_2.get_tk_widget().grid(columnspan = 3, column = 3, row = 1)
        canvas_2.draw()
        
        
def round_dataframe_values(dataframe, elements_to_convert):
    """Rounding values within a dataframe taking inputs:
        dataframe = table to convert values
        elements_to_convert = indicate cols to round """
        
    # Round all columns    
    if str(elements_to_convert) == 'all_':
        for student in range(0, len(dataframe)):
            for cols in range(0, len(dataframe.columns)):
                val = dataframe.iloc[student, cols]
                dataframe.iloc[student, cols] = float("{0:.2f}".format(val))
    # Round last column only           
    elif str(elements_to_convert) == 'last':
        for student in range(0, len(dataframe)):
            last_col = len(dataframe.columns) - 1
            val = dataframe.iloc[student, last_col]
            dataframe.iloc[student, last_col] = float("{0:.2f}".format(val))
        
      
def clear_all_output(root):
    """Clear tkinter frame window where outputs are displayed """
    
    # Clear window referenced in input
    for widget in root.winfo_children():
        widget.destroy()
    # Define new frame to allow for next output
    root = tk.Frame(root, width = 1450, bg = 'white')
    root.grid(columnspan = 6, rowspan = 10)
        
