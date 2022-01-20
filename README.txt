READ ME:

Submission for CW2 - Programming for Data Science - 21COP504 - B******

Student Monitoring System:

The system produces outputs based on a results database of grades for students 
by each test taken.

To launch the program, run the menu.py file. This will launch the GUI interface 
allowing functionality and interaction. 

To activate functionality the user should select the purple buttons.

If input fields are left blank, inputted incorrectly or invalid option an
error box will pop up to indicate this issue. 

The buttons provide the following respective outputs:
 - Test results (by student ID for all tests)
 - Student performance of marks per question (and relative marks)
    - Takes student ID (entry field) and
    - Specified test (drop down field) and produces absolute and relatve grade
    - Relative grade = Absolute grade - Mean grade per question
- Underperforming students produces a list of students classified as underperforming. 
    Criteria as follows:
    - SumTest is less than 60%
    - Students who don't have more than 2 grades of 0% (disengaged students)
    - Students who don't have more than 1 grades over 60% (not underperforming students)
- Hardworking students produces a list of students classified as hardworking.
    Criteria as follows:
    - Student self-identified as a beginner or below beginner knowledge of programming
    - SumTest grades lower than 60%
    
Outputs are all displayed within the GUI dashboard.

In order to call another function, simply populate fields if required and press the button. 
