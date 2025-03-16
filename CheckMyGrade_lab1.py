import csv
import base64
import os
import time
import unittest

# Constants for CSV file names
# Note: The PDF specifies four CSV files (Student.csv, Course.csv, Professor.csv, and Login.csv).
# Here, we've added Grades.csv to handle the Grades functionality as an extension.
STUDENT_FILE = 'Student.csv'
COURSE_FILE = 'Course.csv'
PROFESSOR_FILE = 'Professor.csv'
LOGIN_FILE = 'Login.csv'
GRADES_FILE = 'Grades.csv'  # Extension for Grades functionality

# Utility functions for CSV file operations
def load_csv(file, headers):
    data = []
    if os.path.exists(file):
        with open(file, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    else:
        # Create the file with headers if it doesn't exist
        with open(file, mode='w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
    return data

def save_csv(file, data, headers):
    with open(file, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# ========================
# Class Definitions
# ========================

class Student:
    def __init__(self, first_name, last_name, email_address, course_id, grade, marks):
        self.first_name = first_name
        self.last_name = last_name
        self.email_address = email_address   # Acts as a unique student ID
        self.course_id = course_id
        self.grade = grade  # Expected to store a grade identifier (referencing the Grades class)
        self.marks = marks  # Stored as string, but used for numerical sorting
    
    def display(self):
        print(f"{self.first_name} {self.last_name} | Email: {self.email_address} | "
              f"Course: {self.course_id} | Grade: {self.grade} | Marks: {self.marks}")

    def to_dict(self):
        return {
            'email_address': self.email_address,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'course_id': self.course_id,
            'grade': self.grade,
            'marks': self.marks
        }
    
    def update(self, first_name=None, last_name=None, course_id=None, grade=None, marks=None):
        if first_name:
            self.first_name = first_name
        if last_name:
            self.last_name = last_name
        if course_id:
            self.course_id = course_id
        if grade:
            self.grade = grade
        if marks is not None:
            self.marks = marks

class Course:
    def __init__(self, course_id, course_name, credits, description=""):
        self.course_id = course_id  # Must be unique and not null
        self.course_name = course_name
        self.credits = credits
        self.description = description
    
    def display(self):
        print(f"Course ID: {self.course_id} | Name: {self.course_name} | "
              f"Credits: {self.credits} | Description: {self.description}")
    
    def to_dict(self):
        return {
            'course_id': self.course_id,
            'course_name': self.course_name,
            'credits': self.credits,
            'description': self.description
        }

class Professor:
    def __init__(self, professor_id, name, rank, course_id):
        self.professor_id = professor_id  # Unique identifier (typically email)
        self.name = name
        self.rank = rank
        self.course_id = course_id

    def display(self):
        print(f"Professor ID: {self.professor_id} | Name: {self.name} | "
              f"Rank: {self.rank} | Course: {self.course_id}")

    def to_dict(self):
        return {
            'professor_id': self.professor_id,
            'name': self.name,
            'rank': self.rank,
            'course_id': self.course_id
        }

class Grades:
    # This Grades class is added as an extension.
    # The PDF did not originally specify a separate CSV for grades.
    def __init__(self, grade_id, grade, marks_range):
        self.grade_id = grade_id
        self.grade = grade
        self.marks_range = marks_range  # For example, "90-100"

    def display_grade_report(self):
        print(f"Grade ID: {self.grade_id} | Grade: {self.grade} | Marks Range: {self.marks_range}")

    def to_dict(self):
        return {
            'grade_id': self.grade_id,
            'grade': self.grade,
            'marks_range': self.marks_range
        }

    def modify_grade(self, grade=None, marks_range=None):
        if grade:
            self.grade = grade
        if marks_range:
            self.marks_range = marks_range

class LoginUser:
    def __init__(self, email_id, password, role):
        self.email_id = email_id
        # Encrypt the password before storing it.
        self.password = self.encrypt_password(password)
        self.role = role

    def encrypt_password(self, password):
        encoded_bytes = base64.b64encode(password.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def decrypt_password(self):
        decoded_bytes = base64.b64decode(self.password.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    
    def to_dict(self):
        return {
            'email_id': self.email_id,
            'password': self.password,
            'role': self.role
        }

# ========================
# Main Application Class
# ========================

class CheckMyGradeApp:
    def __init__(self):
        self.students = []    # List of Student objects
        self.courses = []     # List of Course objects
        self.professors = []  # List of Professor objects
        self.grades = []      # List of Grades objects (extension)
        self.login_users = [] # List of LoginUser objects
        self.load_data()
    
    def load_data(self):
        # Load Student records from CSV
        student_headers = ['email_address', 'first_name', 'last_name', 'course_id', 'grade', 'marks']
        student_data = load_csv(STUDENT_FILE, student_headers)
        for row in student_data:
            student = Student(row['first_name'], row['last_name'],
                              row['email_address'], row['course_id'],
                              row['grade'], row['marks'])
            self.students.append(student)
        
        # Load Course records from CSV
        course_headers = ['course_id', 'course_name', 'credits', 'description']
        course_data = load_csv(COURSE_FILE, course_headers)
        for row in course_data:
            course = Course(row['course_id'], row['course_name'],
                            row['credits'], row.get('description', ""))
            self.courses.append(course)
        
        # Load Professor records from CSV
        professor_headers = ['professor_id', 'name', 'rank', 'course_id']
        professor_data = load_csv(PROFESSOR_FILE, professor_headers)
        for row in professor_data:
            professor = Professor(row['professor_id'], row['name'],
                                  row['rank'], row['course_id'])
            self.professors.append(professor)
        
        # Load Login Users from CSV
        login_headers = ['email_id', 'password', 'role']
        login_data = load_csv(LOGIN_FILE, login_headers)
        for row in login_data:
            user = LoginUser(row['email_id'], row['password'], row['role'])
            # If loading from file, the password is already encrypted.
            user.password = row['password']
            self.login_users.append(user)
        
        # Load Grades records from CSV (extension)
        grades_headers = ['grade_id', 'grade', 'marks_range']
        grades_data = load_csv(GRADES_FILE, grades_headers)
        for row in grades_data:
            grade_obj = Grades(row['grade_id'], row['grade'], row['marks_range'])
            self.grades.append(grade_obj)
    
    def save_data(self):
        # Save Student records to CSV
        student_headers = ['email_address', 'first_name', 'last_name', 'course_id', 'grade', 'marks']
        student_data = [s.to_dict() for s in self.students]
        save_csv(STUDENT_FILE, student_data, student_headers)
        
        # Save Course records to CSV
        course_headers = ['course_id', 'course_name', 'credits', 'description']
        course_data = [c.to_dict() for c in self.courses]
        save_csv(COURSE_FILE, course_data, course_headers)
        
        # Save Professor records to CSV
        professor_headers = ['professor_id', 'name', 'rank', 'course_id']
        professor_data = [p.to_dict() for p in self.professors]
        save_csv(PROFESSOR_FILE, professor_data, professor_headers)
        
        # Save Login Users to CSV
        login_headers = ['email_id', 'password', 'role']
        login_data = [u.to_dict() for u in self.login_users]
        save_csv(LOGIN_FILE, login_data, login_headers)
        
        # Save Grades records to CSV (extension)
        grades_headers = ['grade_id', 'grade', 'marks_range']
        grades_data = [g.to_dict() for g in self.grades]
        save_csv(GRADES_FILE, grades_data, grades_headers)
    
    # ========================
    # Student Operations
    # ========================
    def add_student(self, first_name, last_name, email_address, course_id, grade, marks):
        # Ensure unique student email (acting as unique student ID)
        if any(s.email_address == email_address for s in self.students):
            print("A student with this email already exists.")
            return
        student = Student(first_name, last_name, email_address, course_id, grade, marks)
        self.students.append(student)
        self.save_data()
        print("Student added successfully.")

    def delete_student(self, email_address):
        initial_count = len(self.students)
        self.students = [s for s in self.students if s.email_address != email_address]
        if len(self.students) < initial_count:
            self.save_data()
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def update_student(self, email_address, **kwargs):
        found = False
        for s in self.students:
            if s.email_address == email_address:
                s.update(**kwargs)
                found = True
                break
        if found:
            self.save_data()
            print("Student updated successfully.")
        else:
            print("Student not found.")

    def search_students(self, search_term):
        start_time = time.time()
        results = [s for s in self.students if (search_term.lower() in s.email_address.lower() or 
                                                 search_term.lower() in s.first_name.lower() or 
                                                 search_term.lower() in s.last_name.lower())]
        end_time = time.time()
        print(f"Search completed in {end_time - start_time:.4f} seconds")
        return results

    def sort_students_by_marks(self, reverse=False):
        start_time = time.time()
        sorted_students = sorted(self.students, key=lambda s: float(s.marks), reverse=reverse)
        end_time = time.time()
        print(f"Sorting completed in {end_time - start_time:.4f} seconds")
        return sorted_students
    
    def display_all_students(self):
        print("\n--- Student Records ---")
        for s in self.students:
            s.display()
    
    # ========================
    # Course Operations
    # ========================
    def add_course(self, course_id, course_name, credits, description=""):
        if any(c.course_id == course_id for c in self.courses):
            print("A course with this ID already exists.")
            return
        course = Course(course_id, course_name, credits, description)
        self.courses.append(course)
        self.save_data()
        print("Course added successfully.")
    
    def delete_course(self, course_id):
        initial_count = len(self.courses)
        self.courses = [c for c in self.courses if c.course_id != course_id]
        if len(self.courses) < initial_count:
            self.save_data()
            print("Course deleted successfully.")
        else:
            print("Course not found.")
    
    def update_course(self, course_id, **kwargs):
        found = False
        for c in self.courses:
            if c.course_id == course_id:
                if 'course_name' in kwargs:
                    c.course_name = kwargs['course_name']
                if 'credits' in kwargs:
                    c.credits = kwargs['credits']
                if 'description' in kwargs:
                    c.description = kwargs['description']
                found = True
                break
        if found:
            self.save_data()
            print("Course updated successfully.")
        else:
            print("Course not found.")
    
    def display_all_courses(self):
        print("\n--- Course Records ---")
        for c in self.courses:
            c.display()
    
    # ========================
    # Professor Operations
    # ========================
    def add_professor(self, professor_id, name, rank, course_id):
        if any(p.professor_id == professor_id for p in self.professors):
            print("A professor with this ID already exists.")
            return
        professor = Professor(professor_id, name, rank, course_id)
        self.professors.append(professor)
        self.save_data()
        print("Professor added successfully.")
    
    def delete_professor(self, professor_id):
        initial_count = len(self.professors)
        self.professors = [p for p in self.professors if p.professor_id != professor_id]
        if len(self.professors) < initial_count:
            self.save_data()
            print("Professor deleted successfully.")
        else:
            print("Professor not found.")
    
    def update_professor(self, professor_id, **kwargs):
        found = False
        for p in self.professors:
            if p.professor_id == professor_id:
                if 'name' in kwargs:
                    p.name = kwargs['name']
                if 'rank' in kwargs:
                    p.rank = kwargs['rank']
                if 'course_id' in kwargs:
                    p.course_id = kwargs['course_id']
                found = True
                break
        if found:
            self.save_data()
            print("Professor updated successfully.")
        else:
            print("Professor not found.")
    
    def display_all_professors(self):
        print("\n--- Professor Records ---")
        for p in self.professors:
            p.display()
    
    # ========================
    # Grades Operations (Extension)
    # ========================
    def add_grade(self, grade_id, grade, marks_range):
        if any(g.grade_id == grade_id for g in self.grades):
            print("A grade with this ID already exists.")
            return
        grade_obj = Grades(grade_id, grade, marks_range)
        self.grades.append(grade_obj)
        self.save_data()
        print("Grade added successfully.")
    
    def delete_grade(self, grade_id):
        initial_count = len(self.grades)
        self.grades = [g for g in self.grades if g.grade_id != grade_id]
        if len(self.grades) < initial_count:
            self.save_data()
            print("Grade deleted successfully.")
        else:
            print("Grade not found.")
    
    def modify_grade(self, grade_id, grade=None, marks_range=None):
        found = False
        for g in self.grades:
            if g.grade_id == grade_id:
                g.modify_grade(grade, marks_range)
                found = True
                break
        if found:
            self.save_data()
            print("Grade updated successfully.")
        else:
            print("Grade not found.")
    
    def display_all_grades(self):
        print("\n--- Grades Records ---")
        for g in self.grades:
            g.display_grade_report()
    
    # ========================
    # Login Operations
    # ========================
    def add_login_user(self, email_id, password, role):
        if any(u.email_id == email_id for u in self.login_users):
            print("A login user with this email already exists.")
            return
        user = LoginUser(email_id, password, role)
        self.login_users.append(user)
        self.save_data()
        print("Login user added successfully.")
    
    def validate_login(self, email_id, password):
        for u in self.login_users:
            if u.email_id == email_id and u.decrypt_password() == password:
                return True
        return False

# ========================
# Unit Tests using unittest
# ========================

class TestCheckMyGradeApp(unittest.TestCase):
    def setUp(self):
        # Initialize the application with empty data for testing.
        # This clears the in-memory data (CSV files may persist from previous runs).
        self.app = CheckMyGradeApp()
        self.app.students = []
        self.app.courses = []
        self.app.professors = []
        self.app.grades = []
        self.app.login_users = []
    
    def test_add_and_search_student(self):
        self.app.add_student("Alice", "Smith", "alice@example.com", "CS101", "A", "90")
        results = self.app.search_students("alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].email_address, "alice@example.com")
    
    def test_update_student(self):
        self.app.add_student("David", "Evans", "david@example.com", "CS101", "B", "80")
        self.app.update_student("david@example.com", marks="88")
        results = self.app.search_students("david")
        self.assertEqual(results[0].marks, "88")
    
    def test_sort_students_by_marks(self):
        self.app.add_student("Bob", "Brown", "bob@example.com", "CS101", "B", "85")
        self.app.add_student("Charlie", "Davis", "charlie@example.com", "CS101", "A", "95")
        sorted_students = self.app.sort_students_by_marks(reverse=False)
        # Check ascending order by marks.
        self.assertEqual(sorted_students[0].email_address, "bob@example.com")
        self.assertEqual(sorted_students[1].email_address, "charlie@example.com")
    
    def test_large_number_of_students_and_search_timing(self):
        # Add 1000 student records.
        self.app.students = []
        for i in range(1000):
            self.app.add_student(f"First{i}", f"Last{i}", f"student{i}@example.com", "CS101", "A", str(70 + (i % 30)))
        self.assertEqual(len(self.app.students), 1000)
        # Search for a common term and print timing.
        start_time = time.time()
        results = self.app.search_students("student")
        end_time = time.time()
        total_search_time = end_time - start_time
        print(f"Total time taken for searching 1000 records: {total_search_time:.4f} seconds")
        self.assertTrue(len(results) >= 1000)
    
    def test_sorting_timing(self):
        # Add 100 student records.
        self.app.students = []
        for i in range(100):
            self.app.add_student(f"First{i}", f"Last{i}", f"student{i}@example.com", "CS101", "A", str(70 + i))
        # Sort ascending.
        start_time = time.time()
        sorted_students_asc = self.app.sort_students_by_marks(reverse=False)
        asc_time = time.time() - start_time
        print(f"Sorting (ascending) 100 records took: {asc_time:.4f} seconds")
        # Sort descending.
        start_time = time.time()
        sorted_students_desc = self.app.sort_students_by_marks(reverse=True)
        desc_time = time.time() - start_time
        print(f"Sorting (descending) 100 records took: {desc_time:.4f} seconds")
        self.assertEqual(sorted_students_asc[0].marks, "70")
    
    def test_course_crud(self):
        # Test adding a course.
        self.app.courses = []
        self.app.add_course("CS101", "Intro to CS", "3", "Basic Course")
        self.assertEqual(len(self.app.courses), 1)
        # Test updating the course.
        self.app.update_course("CS101", course_name="Introduction to Computer Science", credits="4")
        self.assertEqual(self.app.courses[0].course_name, "Introduction to Computer Science")
        self.assertEqual(self.app.courses[0].credits, "4")
        # Test deleting the course.
        self.app.delete_course("CS101")
        self.assertEqual(len(self.app.courses), 0)
    
    def test_professor_crud(self):
        # Test adding a professor.
        self.app.professors = []
        self.app.add_professor("prof@example.com", "Dr. Smith", "Senior", "CS101")
        self.assertEqual(len(self.app.professors), 1)
        # Test updating the professor.
        self.app.update_professor("prof@example.com", name="Dr. John Smith", rank="Chief")
        self.assertEqual(self.app.professors[0].name, "Dr. John Smith")
        self.assertEqual(self.app.professors[0].rank, "Chief")
        # Test deleting the professor.
        self.app.delete_professor("prof@example.com")
        self.assertEqual(len(self.app.professors), 0)
    
    def test_add_and_modify_grade(self):
        self.app.add_grade("G1", "A", "90-100")
        # Modify the grade definition.
        self.app.modify_grade("G1", grade="A+", marks_range="95-100")
        grade_record = [g for g in self.app.grades if g.grade_id == "G1"]
        self.assertEqual(len(grade_record), 1)
        self.assertEqual(grade_record[0].grade, "A+")
        self.assertEqual(grade_record[0].marks_range, "95-100")

# ========================
# Main CLI for the Application
# ========================

if __name__ == '__main__':
    # To run unit tests, uncomment the line below:
    # unittest.main()
    
    # Create an instance of the application and present a CLI menu.
    app = CheckMyGradeApp()
    
    while True:
        print("\n--- CheckMyGrade Application ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. Display All Students")
        print("5. Search Students")
        print("6. Sort Students by Marks")
        print("7. Add Course")
        print("8. Display All Courses")
        print("9. Add Professor")
        print("10. Display All Professors")
        print("11. Add Login User")
        print("12. Validate Login")
        print("13. Display All Grades")
        print("14. Add Grade")
        print("15. Update Grade")
        print("16. Delete Grade")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        if choice == "1":
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email_address = input("Email Address: ")
            course_id = input("Course ID: ")
            grade = input("Grade (grade id): ")
            marks = input("Marks: ")
            app.add_student(first_name, last_name, email_address, course_id, grade, marks)
        elif choice == "2":
            email_address = input("Enter Email Address to delete: ")
            app.delete_student(email_address)
        elif choice == "3":
            email_address = input("Enter Email Address to update: ")
            print("Leave field empty if no change.")
            first_name = input("New First Name: ")
            last_name = input("New Last Name: ")
            course_id = input("New Course ID: ")
            grade = input("New Grade (grade id): ")
            marks = input("New Marks: ")
            kwargs = {}
            if first_name:
                kwargs['first_name'] = first_name
            if last_name:
                kwargs['last_name'] = last_name
            if course_id:
                kwargs['course_id'] = course_id
            if grade:
                kwargs['grade'] = grade
            if marks:
                kwargs['marks'] = marks
            app.update_student(email_address, **kwargs)
        elif choice == "4":
            app.display_all_students()
        elif choice == "5":
            term = input("Enter search term (name or email): ")
            results = app.search_students(term)
            for student in results:
                student.display()
        elif choice == "6":
            order = input("Sort in descending order? (yes/no): ")
            reverse = True if order.lower() == "yes" else False
            sorted_students = app.sort_students_by_marks(reverse)
            for student in sorted_students:
                student.display()
        elif choice == "7":
            course_id = input("Course ID: ")
            course_name = input("Course Name: ")
            credits = input("Credits: ")
            description = input("Description: ")
            app.add_course(course_id, course_name, credits, description)
        elif choice == "8":
            app.display_all_courses()
        elif choice == "9":
            professor_id = input("Professor ID (Email): ")
            name = input("Name: ")
            rank = input("Rank: ")
            course_id = input("Course ID: ")
            app.add_professor(professor_id, name, rank, course_id)
        elif choice == "10":
            app.display_all_professors()
        elif choice == "11":
            email_id = input("Login Email: ")
            password = input("Password: ")
            role = input("Role: ")
            app.add_login_user(email_id, password, role)
        elif choice == "12":
            email_id = input("Login Email: ")
            password = input("Password: ")
            if app.validate_login(email_id, password):
                print("Login successful!")
            else:
                print("Invalid credentials.")
        elif choice == "13":
            app.display_all_grades()
        elif choice == "14":
            grade_id = input("Grade ID: ")
            grade = input("Grade: ")
            marks_range = input("Marks Range (e.g., 90-100): ")
            app.add_grade(grade_id, grade, marks_range)
        elif choice == "15":
            grade_id = input("Grade ID to update: ")
            new_grade = input("New Grade (leave empty if no change): ")
            new_range = input("New Marks Range (leave empty if no change): ")
            app.modify_grade(grade_id, grade=new_grade if new_grade else None, marks_range=new_range if new_range else None)
        elif choice == "16":
            grade_id = input("Grade ID to delete: ")
            app.delete_grade(grade_id)
        elif choice == "0":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")
