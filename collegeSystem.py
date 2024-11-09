import mysql.connector as mysql

# Attempt to establish database connection
try:
    db = mysql.connect(host='localhost', user='root', password='', database='college')
    command_handler = db.cursor(buffered=True)
    print("Database connection established successfully.")
except mysql.Error as err:
    print(f"Error connecting to database: {err}")
    exit()  # Stop the program if there's a connection error



def admin_session():
    while True: 
        print("")
        print("Admin Menu")
        print("1. Register new student")
        print("2. Register new teacher")
        print("3. Deleting existing student")
        print("4. Deleting existing teachert")
        print("5. Log Out")
        user_option = input("Option : ")
        if user_option == "1":
           print("Register new student")
           username = input("Student username : ")
           password = input("Student password : ")
           query_vals = (username, password)
           command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, 'student')", query_vals)
           db.commit()
           print(username + " becomes a student")
           
        elif user_option == "2":
           print("Register new teacher")
           username = input("Teacher username : ")
           password = input("Teacher password : ")
           query_vals = (username, password)
           command_handler.execute("INSERT INTO users (username, password, privilege) VALUES (%s, %s, 'teacher')", query_vals)
           db.commit()
           print(username + " becomes a teacher")
        elif user_option == "3":
            print("")
            print("Remove the existing student from the database!")
            username = input("Student username : ")
            query_vals = (username, "student")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()
            if command_handler.rowcount < 1:
               print("User not found")
            else:
               print(username + " is removed from the database")
        elif user_option == "4":
           print("")
           print("Remove the existing Teacher3 from the database!")
           username = input("Teacher username : ")
           query_vals = (username, "teacher")
           command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
           db.commit()
           if command_handler.rowcount < 1:
               print("User not found")
           else:
               print(username + " is removed from the database")
        elif user_option == "5":
            return main()
        else:
            print("No valid option was selected. Please try again.")
    
        print("Log in  is successful. Welcome Admin")
    

def auth_admin():
    print("\nAdmin login\n")
    userName = input("Username: ").strip()  # Strip leading/trailing whitespace
    password = input("Password: ").strip()   # Strip leading/trailing whitespace

    # Debug: Print values for troubleshooting
    print(f"Debug - Entered Username: '{userName}', Entered Password: '{password}'")  

    if userName == "admin" and password == "password":
        print("Admin login successful!")  # Confirmation of successful login
        admin_session()  # Start admin session without returning to main
    else:
        print("Login details are not recognized!")

    

def teacher_session():
    while True: 
        print("")
        print("Teacher's Menu")
        print("1. Mark student register")
        print("2. View register")
        print("3. Log out")
        user_option = input("Option: ") 
        if user_option == "1":
            print("")
            print("Mark student register")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input("Date: DD/MM/YYYY : ")
            for record in records: 
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                # Present | Absent | Late
                status = input("Status for "+ str(record) + "P/A/L : ")
                query_vals = (str(record), date, status)
                command_handler.execute("INSERT INTO attendance (username, date, status) VALUES (%s, %s, %s)", query_vals)
                db.commit()  # Commit the transaction
                print(record + " is marked as " + status)
        elif user_option == '2':
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            print("Displaying all registers")
            for record in records:
                print(record)
        elif user_option == "3":
            return main()
        else: 
            print("No valid option was selected.")
            
def auth_student(): 
    print("")
    print("Student's login")
    print("")
    username = input("Username : ")
    password = input("Password : ")
    query_vals = (username, password, 'student')
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s", query_vals)
 
    if command_handler.rowcount <= 0:
        print("Login fails")
    else: 
        student_session(username)
        

def student_session(username):
    while True :
        print("")
        print("1. View register")
        print("2. Download register")
        print("3. Logout")
        user_option = input("Option : ")
        if user_option == "1":
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
             print(record)
        elif user_option == "2":
            print("Downloading Register")
            username = (str(username),)
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
             with open('register.txt',"w" ) as f:
                 f.write(str(record)+"\n")
            f.close()
            print("All records are saved")
        else:
            main()
            
    
        
    
def auth_teacher():
    print("")
    print("Teacher's login")
    print("")
    username = input("Username: ")
    password = input("Password: ")
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege ='teacher'", query_vals)
    if command_handler.rowcount <= 0: 
        print("Login not recognized.")
    else:
        teacher_session()
        print("welcome teacher!")


def main():
    while True:
        print("\nWelcome to the college system\n")
        print("1. Log in as student")
        print("2. Log in as teacher")
        print("3. Log in as admin")
        
        user_option = input("Option: ")
        print("User selected:", user_option)  # Debug line to check input
        
        if user_option == "1":
           auth_student()
            # Implement student login logic here
            # Temporarily comment out `break` to see if the loop continues
            # break
        elif user_option == "2":
            auth_teacher()
            # Implement teacher login logic here
            # break
        elif user_option == "3":
            auth_admin()
            # Implement admin login logic here
            # break
        else:
            print("No valid option was selected. Please try again.")
        
        print("End of loop iteration.")  # Debug statement to indicate loop progression

main()
