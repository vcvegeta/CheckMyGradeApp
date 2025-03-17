import csv          # Importing the csv module to handle reading and writing CSV files.
import base64       # For encoding and decoding passwords securely.
import os           # For file handling operations.
import time         # To measure execution time for searching and sorting operations.
import unittest     # For unit testing the application.
import statistics   # For calculating medians.


# CSV File Constants (exact headers as in your screenshots)
# ============================================================
STUDENT_FILE = 'Student.csv'        # File storing student details (name, email, course, grade, marks).
COURSE_FILE = 'Course.csv'          # File storing course details.
PROFESSOR_FILE = 'Professor.csv'    # File storing professor details.
LOGIN_FILE = 'Login.csv'            # File storing user-login details/credentials.
GRADES_FILE = 'Grades.csv'          # File storing grade definitions.


# CSV Load/Save Utilities
# ============================                     
def load_csv(file, headers):
    data = []
    if os.path.exists(file):
        with open(file, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    else:
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


# Initialize CSVs with Sample Rows
# ============================================================
def initialize_csv_if_empty():
    # Student.csv
    student_headers = ["Email_address", "First_name", "Last_name", "Course.id", "grades", "Marks"]
    if len(load_csv(STUDENT_FILE, student_headers)) == 0:
        with open(STUDENT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=student_headers)
            writer.writeheader()
            writer.writerow({
                "Email_address": "sam@mycsu.edu",
                "First_name": "Sam",
                "Last_name": "Carpenter",
                "Course.id": "DATA200",
                "grades": "A",
                "Marks": "96"
            })

    # Course.csv – three fields: Course_id, Course_name, Description.
    course_headers = ["Course_id", "Course_name", "Description"]
    if len(load_csv(COURSE_FILE, course_headers)) == 0:
        with open(COURSE_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=course_headers)
            writer.writeheader()
            writer.writerow({
                "Course_id": "DATA200",
                "Course_name": "Data Science",
                "Description": "Provides insight about DS and Python"
            })

    # Professor.csv
    prof_headers = ["Professor_id", "Professor Name", "Rank", "Course.id"]
    if len(load_csv(PROFESSOR_FILE, prof_headers)) == 0:
        with open(PROFESSOR_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=prof_headers)
            writer.writeheader()
            writer.writerow({
                "Professor_id": "micheal@mycsu.edu",
                "Professor Name": "Micheal John",
                "Rank": "Senior Professor",
                "Course.id": "DATA200"
            })

    # Login.csv
    login_headers = ["User_id", "Password", "Role"]
    if len(load_csv(LOGIN_FILE, login_headers)) == 0:
        with open(LOGIN_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=login_headers)
            writer.writeheader()
            writer.writerow({
                "User_id": "micheal@mycsu.edu",
                "Password": "AQ10134",  # Sample row stored as plain text.
                "Role": "professor"
            })
    # Grades.csv remains empty unless new grades are added.


# Populate 100 Dummy Student Records
# ============================================================
def populate_dummy_students(app):
    """
    Populates the Student CSV with 100 dummy records.
    Dummy records are identified by emails starting with "dummy".
    """
    existing_dummies = [s for s in app.students if s.Email_address.startswith("dummy")]
    num_to_add = 100 - len(existing_dummies)
    if num_to_add <= 0:
        print("Student file already has 100 or more dummy records.")
        return
    for i in range(num_to_add):
        first = f"DummyFirst{i}"
        last = f"DummyLast{i}"
        email = f"dummy{i}@example.com"
        course = "CS101"  # Default dummy course.
        grade = "A"
        marks = str(70 + (i % 30))  # Marks between 70 and 99.
        app.add_student(first, last, email, course, grade, marks)
    print("100 dummy student records have been populated.")


# Class Definitions
# ============================================================
class Student:
    def __init__(self, First_name, Last_name, Email_address, Course_id, grades, Marks):
        self.First_name = First_name
        self.Last_name = Last_name
        self.Email_address = Email_address
        self.Course_id = Course_id
        self.grades = grades
        self.Marks = Marks

    def display(self):
        print(f"{self.First_name} {self.Last_name} | Email: {self.Email_address} | "
              f"Course: {self.Course_id} | grades: {self.grades} | Marks: {self.Marks}")

    def update(self, First_name=None, Last_name=None, Course_id=None, grades=None, Marks=None):
        if First_name:
            self.First_name = First_name
        if Last_name:
            self.Last_name = Last_name
        if Course_id:
            self.Course_id = Course_id
        if grades:
            self.grades = grades
        if Marks is not None:
            self.Marks = Marks

    def to_dict(self):
        return {
            "Email_address": self.Email_address,
            "First_name": self.First_name,
            "Last_name": self.Last_name,
            "Course.id": self.Course_id,
            "grades": self.grades,
            "Marks": self.Marks
        }

class Course:
    # Only three fields: Course_id, Course_name, Description.
    def __init__(self, Course_id, Course_name, Description):
        self.Course_id = Course_id
        self.Course_name = Course_name
        self.Description = Description

    def display(self):
        print(f"Course ID: {self.Course_id} | Name: {self.Course_name} | {self.Description}")

    def to_dict(self):
        return {
            "Course_id": self.Course_id,
            "Course_name": self.Course_name,
            "Description": self.Description
        }

class Professor:
    def __init__(self, Professor_id, Professor_Name, Rank, Course_id):
        self.Professor_id = Professor_id
        self.Professor_Name = Professor_Name
        self.Rank = Rank
        self.Course_id = Course_id

    def display(self):
        print(f"Professor ID: {self.Professor_id} | Name: {self.Professor_Name} | "
              f"Rank: {self.Rank} | Course: {self.Course_id}")

    def to_dict(self):
        return {
            "Professor_id": self.Professor_id,
            "Professor Name": self.Professor_Name,
            "Rank": self.Rank,
            "Course.id": self.Course_id
        }

class Grades:
    def __init__(self, Grade_id, Grade, Marks_range):
        self.Grade_id = Grade_id
        self.Grade = Grade
        self.Marks_range = Marks_range

    def display_grade_report(self):
        print(f"Grade ID: {self.Grade_id} | Grade: {self.Grade} | Marks Range: {self.Marks_range}")

    def modify_grade(self, Grade=None, Marks_range=None):
        if Grade:
            self.Grade = Grade
        if Marks_range:
            self.Marks_range = Marks_range

    def to_dict(self):
        return {
            "Grade_id": self.Grade_id,
            "Grade": self.Grade,
            "Marks_range": self.Marks_range
        }

class LoginUser:
    def __init__(self, User_id, Password, Role):
        self.User_id = User_id
        self.Role = Role
        if User_id == "micheal@mycsu.edu" and Password == "AQ10134" and Role == "professor":
            self.Password = Password
        else:
            self.Password = self.encrypt_password(Password)

    def encrypt_password(self, plain_password):
        encoded_bytes = base64.b64encode(plain_password.encode('utf-8'))
        return encoded_bytes.decode('utf-8')

    def decrypt_password(self):
        if self.User_id == "micheal@mycsu.edu" and self.Password == "AQ10134" and self.Role == "professor":
            return self.Password
        decoded_bytes = base64.b64decode(self.Password.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    
    def to_dict(self):
        return {
            "User_id": self.User_id,
            "Password": self.Password,
            "Role": self.Role
        }


# Main Application Class (CRUD, Searching, Sorting, Statistics & Reports)
# ============================================================
class CheckMyGradeApp:
    def __init__(self):
        initialize_csv_if_empty()  # Write sample rows if no data exists.

        self.students = []      # List of Student objects.
        self.courses = []       # List of Course objects.
        self.professors = []    # List of Professor objects.
        self.grades_list = []   # List of Grades objects.
        self.login_users = []   # List of LoginUser objects.

        self.load_data()

    def load_data(self):
        # Load Student records.
        student_headers = ["Email_address", "First_name", "Last_name", "Course.id", "grades", "Marks"]
        student_data = load_csv(STUDENT_FILE, student_headers)
        for row in student_data:
            st = Student(row["First_name"], row["Last_name"], row["Email_address"],
                         row["Course.id"], row["grades"], row["Marks"])
            self.students.append(st)
        
        # Load Course records.
        course_headers = ["Course_id", "Course_name", "Description"]
        course_data = load_csv(COURSE_FILE, course_headers)
        for row in course_data:
            co = Course(row["Course_id"], row["Course_name"], row["Description"])
            self.courses.append(co)
        
        # Load Professor records.
        prof_headers = ["Professor_id", "Professor Name", "Rank", "Course.id"]
        prof_data = load_csv(PROFESSOR_FILE, prof_headers)
        for row in prof_data:
            pr = Professor(row["Professor_id"], row["Professor Name"], row["Rank"], row["Course.id"])
            self.professors.append(pr)
        
        # Load Login Users.
        login_headers = ["User_id", "Password", "Role"]
        login_data = load_csv(LOGIN_FILE, login_headers)
        for row in login_data:
            user = LoginUser(row["User_id"], row["Password"], row["Role"])
            self.login_users.append(user)
        
        # Load Grades records.
        grades_headers = ["Grade_id", "Grade", "Marks_range"]
        grades_data = load_csv(GRADES_FILE, grades_headers)
        for row in grades_data:
            gr = Grades(row["Grade_id"], row["Grade"], row["Marks_range"])
            self.grades_list.append(gr)
    
    def save_data(self):
        # Save Student records.
        student_headers = ["Email_address", "First_name", "Last_name", "Course.id", "grades", "Marks"]
        student_data = [s.to_dict() for s in self.students]
        save_csv(STUDENT_FILE, student_data, student_headers)
        
        # Save Course records.
        course_headers = ["Course_id", "Course_name", "Description"]
        course_data = [c.to_dict() for c in self.courses]
        save_csv(COURSE_FILE, course_data, course_headers)
        
        # Save Professor records.
        prof_headers = ["Professor_id", "Professor Name", "Rank", "Course.id"]
        prof_data = [p.to_dict() for p in self.professors]
        save_csv(PROFESSOR_FILE, prof_data, prof_headers)
        
        # Save Login Users.
        login_headers = ["User_id", "Password", "Role"]
        login_data = [u.to_dict() for u in self.login_users]
        save_csv(LOGIN_FILE, login_data, login_headers)
        
        # Save Grades records.
        grades_headers = ["Grade_id", "Grade", "Marks_range"]
        grades_data = [g.to_dict() for g in self.grades_list]
        save_csv(GRADES_FILE, grades_data, grades_headers)
    
    
    # Student CRUD & Functions
    # ----------------------
    def add_student(self, first_name, last_name, email_address, course_id, grade, marks):
        if any(s.Email_address == email_address for s in self.students):
            print("A student with this email already exists.")
            return
        st = Student(first_name, last_name, email_address, course_id, grade, marks)
        self.students.append(st)
        self.save_data()
        print("Student added successfully.")

    def delete_student(self, email_address):
        init_len = len(self.students)
        self.students = [s for s in self.students if s.Email_address != email_address]
        if len(self.students) < init_len:
            self.save_data()
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def update_student(self, email_address, **kwargs):
        found = False
        for s in self.students:
            if s.Email_address == email_address:
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
        results = [s for s in self.students if (
            search_term.lower() in s.Email_address.lower() or 
            search_term.lower() in s.First_name.lower() or 
            search_term.lower() in s.Last_name.lower()
        )]
        end_time = time.time()
        print(f"Search completed in {end_time - start_time:.4f} seconds")
        return results

    def sort_students_by_marks(self, reverse=False):
        start_time = time.time()
        sorted_students = sorted(self.students, key=lambda s: float(s.Marks), reverse=reverse)
        end_time = time.time()
        print(f"Sorting completed in {end_time - start_time:.4f} seconds")
        return sorted_students
    
    def display_all_students(self):
        print("\n--- Student Records ---")
        for s in self.students:
            s.display()
    
    
    # Course CRUD & Functions
    # ----------------------
    def add_course(self, course_id, course_name, description):
        if any(c.Course_id == course_id for c in self.courses):
            print("A course with this ID already exists.")
            return
        co = Course(course_id, course_name, description)
        self.courses.append(co)
        self.save_data()
        print("Course added successfully.")

    def delete_course(self, course_id):
        init_len = len(self.courses)
        self.courses = [c for c in self.courses if c.Course_id != course_id]
        if len(self.courses) < init_len:
            self.save_data()
            print("Course deleted successfully.")
        else:
            print("Course not found.")

    def update_course(self, course_id, **kwargs):
        found = False
        for c in self.courses:
            if c.Course_id == course_id:
                if 'Course_name' in kwargs:
                    c.Course_name = kwargs['Course_name']
                if 'description' in kwargs:
                    c.Description = kwargs['description']  # Update the proper attribute.
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
    
    
    # Professor CRUD & Functions
    # ----------------------
    def add_professor(self, professor_id, Professor_Name, Rank, course_id):
        if any(p.Professor_id == professor_id for p in self.professors):
            print("A professor with this ID already exists.")
            return
        pr = Professor(professor_id, Professor_Name, Rank, course_id)
        self.professors.append(pr)
        self.save_data()
        print("Professor added successfully.")

    def delete_professor(self, professor_id):
        init_len = len(self.professors)
        self.professors = [p for p in self.professors if p.Professor_id != professor_id]
        if len(self.professors) < init_len:
            self.save_data()
            print("Professor deleted successfully.")
        else:
            print("Professor not found.")

    def update_professor(self, professor_id, **kwargs):
        found = False
        for p in self.professors:
            if p.Professor_id == professor_id:
                if 'Professor_Name' in kwargs:
                    p.Professor_Name = kwargs['Professor_Name']
                if 'Rank' in kwargs:
                    p.Rank = kwargs['Rank']
                if 'course_id' in kwargs:
                    p.Course_id = kwargs['course_id']
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
    
    
    # Grades CRUD & Functions
    # ----------------------
    def add_grade(self, Grade_id, Grade, Marks_range):
        if any(g.Grade_id == Grade_id for g in self.grades_list):
            print("A grade with this ID already exists.")
            return
        g = Grades(Grade_id, Grade, Marks_range)
        self.grades_list.append(g)
        self.save_data()
        print("Grade added successfully.")

    def delete_grade(self, Grade_id):
        init_len = len(self.grades_list)
        self.grades_list = [g for g in self.grades_list if g.Grade_id != Grade_id]
        if len(self.grades_list) < init_len:
            self.save_data()
            print("Grade deleted successfully.")
        else:
            print("Grade not found.")

    def modify_grade(self, Grade_id, Grade=None, Marks_range=None):
        found = False
        for g in self.grades_list:
            if g.Grade_id == Grade_id:
                g.modify_grade(Grade, Marks_range)
                found = True
                break
        if found:
            self.save_data()
            print("Grade updated successfully.")
        else:
            print("Grade not found.")

    def display_all_grades(self):
        print("\n--- Grades Records ---")
        for g in self.grades_list:
            g.display_grade_report()
    
    
    # Login CRUD & Functions
    # ----------------------
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

    
    # Statistics Functions & Grouped Reports
    # ========================================================
    def calculate_course_statistics(self, course_id):
        """Calculates and returns the average and median marks for students in a given course."""
        marks_list = [float(s.Marks) for s in self.students if s.Course_id == course_id]
        if not marks_list:
            print(f"No students found for course {course_id}.")
            return None, None
        avg = sum(marks_list) / len(marks_list)
        med = statistics.median(marks_list)
        return avg, med

    def report_by_course(self):
        """Prints a report of each course with the list of enrolled students and course statistics."""
        print("\n--- Course-wise Report ---")
        for course in self.courses:
            print(f"\nCourse: {course.Course_id} - {course.Course_name}")
            enrolled = [s for s in self.students if s.Course_id == course.Course_id]
            if enrolled:
                for s in enrolled:
                    print(f"   {s.First_name} {s.Last_name} | Marks: {s.Marks} | Grade: {s.grades}")
                avg, med = self.calculate_course_statistics(course.Course_id)
                print(f"   >> Average Marks: {avg:.2f} | Median Marks: {med:.2f}")
            else:
                print("   No students enrolled.")

    def report_by_professor(self):
        """Prints a report for each professor showing the course they teach and the students enrolled."""
        print("\n--- Professor-wise Report ---")
        for prof in self.professors:
            print(f"\nProfessor: {prof.Professor_id} - {prof.Professor_Name} ({prof.Rank})")
            course = next((c for c in self.courses if c.Course_id == prof.Course_id), None)
            if course:
                print(f"   Teaches Course: {course.Course_id} - {course.Course_name}")
                enrolled = [s for s in self.students if s.Course_id == course.Course_id]
                if enrolled:
                    for s in enrolled:
                        print(f"      {s.First_name} {s.Last_name} | Marks: {s.Marks} | Grade: {s.grades}")
                else:
                    print("      No students enrolled.")
            else:
                print("   No course found for this professor.")

    def report_by_student(self):
        """Prints each student's record."""
        print("\n--- Student-wise Report ---")
        for s in self.students:
            s.display()
    
    
    # (Additional reports can be added as needed.)
    # -------------------------------------------------------

# ============================================================
# Unit Tests
# ============================================================
class TestCheckMyGradeApp(unittest.TestCase):
    def setUp(self):
        self.app = CheckMyGradeApp()
        # Clear in-memory lists for fresh tests:
        self.app.students = []
        self.app.courses = []
        self.app.professors = []
        self.app.grades_list = []
        self.app.login_users = []

    def test_add_and_search_student(self):
        print("\n=== Running test_add_and_search_student ===")
        self.app.add_student("Alice", "Smith", "alice@example.com", "CS101", "A", "90")
        results = self.app.search_students("alice")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].Email_address, "alice@example.com")

    def test_update_student(self):
        print("\n=== Running test_update_student ===")
        self.app.add_student("David", "Evans", "david@example.com", "CS101", "B", "80")
        self.app.update_student("david@example.com", First_name="Dave", Marks="88")
        results = self.app.search_students("david")
        self.assertEqual(results[0].First_name, "Dave")
        self.assertEqual(results[0].Marks, "88")

    def test_sort_students_by_marks(self):
        print("\n=== Running test_sort_students_by_marks ===")
        self.app.add_student("Bob", "Brown", "bob@example.com", "CS101", "B", "85")
        self.app.add_student("Charlie", "Davis", "charlie@example.com", "CS101", "A", "95")
        sorted_students = self.app.sort_students_by_marks(reverse=False)
        self.assertEqual(sorted_students[0].Email_address, "bob@example.com")
        self.assertEqual(sorted_students[1].Email_address, "charlie@example.com")

    def test_large_number_of_students_and_search_timing(self):
        print("\n=== Running test_large_number_of_students_and_search_timing ===")
        self.app.students = []
        # Use 100 dummy records for easier timing display.
        for i in range(100):
            self.app.add_student(f"First{i}", f"Last{i}", f"student{i}@example.com", "CS101", "A", str(70 + (i % 30)))
        print("Finished adding 100 dummy student records.")
        start_time = time.time()
        results = self.app.search_students("student")
        end_time = time.time()
        total_search_time = end_time - start_time
        print(f"Total time taken for searching 100 records: {total_search_time:.4f} seconds")
        self.assertTrue(len(results) >= 100)

    def test_sorting_timing(self):
        print("\n=== Running test_sorting_timing ===")
        self.app.students = []
        for i in range(100):
            self.app.add_student(f"First{i}", f"Last{i}", f"student{i}@example.com", "CS101", "A", str(70 + i))
        start_time = time.time()
        sorted_students_asc = self.app.sort_students_by_marks(reverse=False)
        asc_time = time.time() - start_time
        print(f"Sorting (ascending) 100 records took: {asc_time:.4f} seconds")
        start_time = time.time()
        sorted_students_desc = self.app.sort_students_by_marks(reverse=True)
        desc_time = time.time() - start_time
        print(f"Sorting (descending) 100 records took: {desc_time:.4f} seconds")
        self.assertEqual(sorted_students_asc[0].Marks, "70")

    def test_course_crud(self):
        print("\n=== Running test_course_crud ===")
        self.app.courses = []
        # 1) Add a course.
        self.app.add_course("TEST101", "Intro to Testing", "Just a test course")
        self.assertEqual(len(self.app.courses), 1)
        self.assertEqual(self.app.courses[0].Course_id, "TEST101")
        # 2) Update the course (modify).
        self.app.update_course("TEST101", Course_name="Intro to Testing Updated", description="New desc")
        self.assertEqual(self.app.courses[0].Course_name, "Intro to Testing Updated")
        self.assertEqual(self.app.courses[0].Description, "New desc")
        # 3) Delete the course.
        self.app.delete_course("TEST101")
        self.assertEqual(len(self.app.courses), 0)

    def test_professor_crud(self):
        print("\n=== Running test_professor_crud ===")
        self.app.professors = []
        self.app.add_professor("prof@example.com", "Dr. Smith", "Senior", "CS101")
        self.assertEqual(len(self.app.professors), 1)
        self.app.update_professor("prof@example.com", Professor_Name="Dr. John Smith", Rank="Chief")
        self.assertEqual(self.app.professors[0].Professor_Name, "Dr. John Smith")
        self.assertEqual(self.app.professors[0].Rank, "Chief")
        self.app.delete_professor("prof@example.com")
        self.assertEqual(len(self.app.professors), 0)

    def test_add_and_modify_grade(self):
        print("\n=== Running test_add_and_modify_grade ===")
        self.app.add_grade("G1", "A", "90-100")
        self.app.modify_grade("G1", Grade="A+", Marks_range="95-100")
        grade_record = [g for g in self.app.grades_list if g.Grade_id == "G1"]
        self.assertEqual(len(grade_record), 1)
        self.assertEqual(grade_record[0].Grade, "A+")
        self.assertEqual(grade_record[0].Marks_range, "95-100")

    def test_course_statistics(self):
        print("\n=== Running test_course_statistics ===")
        self.app.students = []
        self.app.add_student("Johnny", "Smith", "johnny@example.com", "CS101", "B", "80")
        self.app.add_student("Jane", "e", "jane@example.com", "CS101", "A", "90")
        self.app.add_student("Jim", "Beam", "jim@example.com", "CS101", "C", "70")
        avg, med = self.app.calculate_course_statistics("CS101")
        self.assertAlmostEqual(avg, (80+90+70)/3)
        self.assertEqual(med, 80)

    def test_report_by_course(self):
        print("\n=== Running test_report_by_course ===")
        self.app.students = []
        self.app.courses = []
        self.app.add_course("CS101", "Intro to CS", "Basic CS course")
        self.app.add_student("Alice", "Smith", "alice@example.com", "CS101", "A", "95")
        self.app.add_student("Bob", "Brown", "bob@example.com", "CS101", "B", "85")
        self.app.report_by_course()

    def test_report_by_professor(self):
        print("\n=== Running test_report_by_professor ===")
        self.app.professors = []
        self.app.courses = []
        self.app.students = []
        self.app.add_course("CS101", "Intro to CS", "Basic CS course")
        self.app.add_professor("prof@example.com", "Dr. Smith", "Senior", "CS101")
        self.app.add_student("Alice", "Smith", "alice@example.com", "CS101", "A", "95")
        self.app.report_by_professor()


# Demo & Main Execution Block
# ============================================================
def run_tests_and_demo():
    print("Running unit tests...\n")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckMyGradeApp)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    print("\nUnit tests completed.\n")
    
    # Minimal Demo: display records, search/sort timings, and print reports.
    app = CheckMyGradeApp()
    print("\n--- Displaying All Student Records ---")
    app.display_all_students()
    print("\n--- Displaying All Course Records ---")
    app.display_all_courses()
    print("\n--- Displaying All Professor Records ---")
    app.display_all_professors()
    print("\n--- Searching for 'Sam' ---")
    results = app.search_students("Sam")
    for s in results:
        s.display()
    print("\n--- Sorting Students by Marks Ascending ---")
    sorted_list = app.sort_students_by_marks(reverse=False)
    for s in sorted_list:
        s.display()
    print("\n--- Course-wise Report ---")
    app.report_by_course()
    print("\n--- Professor-wise Report ---")
    app.report_by_professor()

def run_cli():
    # Create an instance of the application.
    app = CheckMyGradeApp()
    while True:
        # Display the main menu.
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
        print("17. Display All Login Users")
        print("18. Report by Course")
        print("19. Report by Professor")
        print("0. Exit")
        
        # Prompt for user input.
        choice = input("Enter your choice: ").strip()
        
        # Process user input:
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
            grade = input("New Grade: ")
            marks = input("New Marks: ")
            kwargs = {}
            if first_name:
                kwargs['First_name'] = first_name
            if last_name:
                kwargs['Last_name'] = last_name
            if course_id:
                kwargs['Course_id'] = course_id
            if grade:
                kwargs['grades'] = grade
            if marks:
                kwargs['Marks'] = marks
            app.update_student(email_address, **kwargs)
        elif choice == "4":
            app.display_all_students()
        elif choice == "5":
            term = input("Enter search term (name or email): ")
            results = app.search_students(term)
            for student in results:
                student.display()
        elif choice == "6":
            order = input("Sort in descending order? (yes/no): ").strip().lower()
            rev = True if order == "yes" else False
            sorted_students = app.sort_students_by_marks(reverse=rev)
            for student in sorted_students:
                student.display()
        elif choice == "7":
            course_id = input("Course ID: ")
            course_name = input("Course Name: ")
            description = input("Description: ")
            app.add_course(course_id, course_name, description)
        elif choice == "8":
            app.display_all_courses()
        elif choice == "9":
            professor_id = input("Professor ID (Email): ")
            Professor_Name = input("Name: ")
            Rank = input("Rank: ")
            course_id = input("Course ID: ")
            app.add_professor(professor_id, Professor_Name, Rank, course_id)
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
            Grade_id = input("Grade ID: ")
            Grade = input("Grade: ")
            Marks_range = input("Marks Range (e.g., 90-100): ")
            app.add_grade(Grade_id, Grade, Marks_range)
        elif choice == "15":
            Grade_id = input("Grade ID to update: ")
            new_grade = input("New Grade (leave empty if no change): ")
            new_marks_range = input("New Marks Range (leave empty if no change): ")
            app.modify_grade(Grade_id, Grade=new_grade if new_grade else None, Marks_range=new_marks_range if new_marks_range else None)
        elif choice == "16":
            Grade_id = input("Grade ID to delete: ")
            app.delete_grade(Grade_id)
        elif choice == "17":
            print("\n--- All Login Users ---")
            for u in app.login_users:
                print(f"{u.User_id} | Role: {u.Role} | Encrypted Password: {u.Password}")
        elif choice == "18":
            app.report_by_course()
        elif choice == "19":
            app.report_by_professor()
        elif choice == "0":
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")


# Main Execution Block
# ============================================================
if __name__ == "__main__":
    # To run unit tests and demo first, uncomment the next line and comment out run_cli().
    run_tests_and_demo()
    
    # Pre-populate the student file with 100 dummy records (if not already present).
    app_instance = CheckMyGradeApp()
    populate_dummy_students(app_instance)
    
    # Run the interactive CLI.
    run_cli()
