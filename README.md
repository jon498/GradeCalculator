# Grade Calculator
#### Video Demo: https://youtu.be/XHzunF0s5vU
#### Description:
General: My project is a weighted grade calculator, which allows users to be able to calculate grades with weights as well as input future assingments, tests, or quizzes to see how they would input their grade. Users are also able to create an account where they can save their courses, so they don't have to continuously reenter the categories that make up their grade. Once they have saved courses, they are able to update/edit these courses to their desire and later use these courses to again figure out how certain assignments would impact their grade.

index.html: This file contains the outline for the home page of the webiste. It includes the name of the webiste, the logo, the motto, and two button for the user to choose from. The first button is always an 'input grades' button, which allows the user to go to the main page of the website, and the second button varies on whether or not the user is logged in. If they are not, the second button is a button that takes the user to a login page, but if they are, then the second button will take the user to the 'courses' page.

register.html/login.html: These two files include the outlines for the register page and the login page, which are very similar to each other. On the register page, the user is able to make an account in order to access different features on the website. Inside the register file is an html form with three input fields for the user to input a username, password, and password confirmation, followed by a button that submits the form if all of the fields are filled out. On the login, page, there are the same features as on the register page minus the password confirmation. There is also a link that redirects users to the register page in case they do not yet have an account.

layout.html: This file includes the layout for the rest of the html files. Inside the file is a navbar that the user can use to traverse the different pages of the webiste (If they are logged in, it changes to show the 'courses' page as well rather than just the 'grades' page in they are not logged in). There is also jinja code allowing flashed messages to be seen by the user at the top of the screen.

grades.html: This file is the main page of the website, and includes multiple different aspects inside the main block continuing layout.html. The first form included is a way for users to input current categories of a course. The form allows a category name, a fraction for the current grade in the category, and a percentage for the weight of the course to be inputted and submitted. Next, it contains a table that displays all of the different categories they have entered so far through the first form. The second form includes a select box that allows the users to choose and delete a category that they have inputted through the first form. The third form includes a text input and that gives the users the option to save the all of the categories to 'courses' after inputted a name (This option only appears if the user is logged in). The final two forms, which inlcude multiple input boxes and a select box, allow the user to put a future grade into a specified category in order to see how a certain score would impact their grade. Finally, the total grade percentage with the future grade is shown at the bottom of the page.

courses.html: This file contains the saved courses that the user (if logged in) has saved. Similarly to the 'grades' page, it continues layout.html and has multiples forms that the user is able to submit. The page first includes a table with all of the courses they have saved, sorting them by the course name that the user inputted. The first form included in this page is a select box with a button for the user to user one of the course templates that they have saved in order to find how assignments will inpact their grade. The second form also includes a select box with a button to allow the user to update the contents inside of the chosen course. The final form contains a select box and button as well to allow the user to delete a course from their saved courses.

update.html: This file includes two different pages - one if the user has chosen to edit the course categories, and another if they are just updating the course. Within both parts, a table is included to display the different categories that the user has inputted into the course. For the first instance of the page, after the table, there is a form that contains a select box to select a category to change, and then multiple input boxes to give the user a place to input new values for the category. In the second instance of the page, there is again a table at the start, and then a form that allows the user to go to the other 'edit' category. Following the edit form is a form that includes three input boxes for the user to add a category to the course. There is also a 'delete' form that allows the user to delete a category from the course. Finally, at the end of both instances, there is a 'back' form that allows the user to press a button to go back to the previous page they were at.

style.css: This file contains the css code that details all of the style for the the different pages.

login.py: This file includes one function that allows python app routes to only be plausible if the user is logged in.

app.py: This file contains all of the python code that allows the program to be user-interactive and functional.
    /register: Gathers the inputted information, makes sure the information was inputted correctly, and creates a new row in 'users' table with the inputted information for the new user.

    /login: Gathers inputted information, makes sure it was inputted correctly, checks to see if there is a matching row in the 'users' table for the inputted information, and redirects them to the home page in if there is.

    /logout: Clears the current session id and redirects the user to the home page.

    /grades: Makes sure information was inputted correctly, inserts the information into a new row in the 'grades' table, sets the id id for the row, and returns the information from the grades table in a table displayed to the user. (Clears table if method was 'GET')

    /grades2: Makes sure information was inputted correctly, gets row that matches with information inputted, and deletes the category from the table before displaying it to the user.

    /grades3: Makes sure information was inputted correctly, gets information from 'grades' table, makes calculations to determine the new grade with the addition of the inputted grade, and returns the template for 'grades.html' with the new grade displayed.

    /courses: Makes sure information was inputted correctly, adds all of the information currently in the 'grades' table to the 'courses' table, and clears the 'grades' table before returning the 'grades.html' template.

    /courses1: Gets value from the select box, takes information for selected course, and inputs the contents of the course into the 'update1' table before returning the 'update.html' template with the course selected displayed in a table.

    /courses2: Gets value from the select box, locates information for selected course in 'courses' table, and deletes information from table before returning the 'courses.html' template with the course deleted from the table.

    /update: Makes sure information was inputted correctly, takes information the user inputted, and updates current information from 'update1' and 'courses' table to fit what user inputted. Returns 'update.html' with the information updated.

    /update1: Makes sure information was inputted correctly, takes information the user inputted, and inserts a new row into the current course they are editing. Returns 'update.html' with the category added to the 'update1' table.

    /update2: Makes sure information was inputted correctly, takes information the user inputted to locate row that matches in the 'update1' table, and deletes the row from the 'update1' and 'courses' table. Returns 'update.html' with the category deleted from the 'update1' table.

    /edit: Changes the value of the variable edit in order to change the update.html page to the condition where edit is True.

    /back: Changes the value of the variable edit in order to change the update.html page to the condition where edit is False.

    /back2: Changes the current page from 'update.html' to courses.html'

    /use: Gets value from the select box in order to figure out which course the user wants to use as the template. Takes information for that course from the 'courses' table and inserts that information into the 'grades table before returning the 'grades.html' page for the user to input a future grade and see how it would impact their grade in that course.