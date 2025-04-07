import json
import uuid
import random

from cryptography.fernet import Fernet

def generate_key():
    KEY = Fernet.generate_key()
    return KEY.decode()

KEY = generate_key() # It is assumed that key is distributed in real life by the instructer in class beforehand

class Instructor:
    def __init__(self):
        self.instructor_id = str(uuid.uuid4())
        self.assignment_id = str(uuid.uuid4())
        self.KEY = KEY
        self.submissions = []

    def publish_assignment_id(self) -> bytes:
        print(f"Instructore is publishing assignment ID: {self.assignment_id}")

        f = Fernet(KEY)
        return f.encrypt(self.assignment_id.encode())
    
    def get_submission(self, submission: bytes):
        f = Fernet(KEY)
        decrypted_submission = json.loads(f.decrypt(submission).decode())
        print(f"Instructor is received the submission of student with signature: {decrypted_submission.get("student_signature", None)}.")
        self.submissions.append(decrypted_submission)

    def grade_assignments(self):
        print("Instructor is grading the assignments.")
        for submission in self.submissions:
            submission["grade"] = random.choice(["A", "B", "C", "D", "F"])
    
    def publish_submissions_with_grades(self):
        print("Instructor is publishing the submissions with grades.")
        return encrypt_message(json.dumps(self.submissions), self.KEY)

class Student:
    def __init__(self, id: int):
        self.student_id = id
        self.signature = str(uuid.uuid4()) # Signature is only known by the student. After the grades are announced, student will use this signature to identify their grade.
        self.KEY = KEY
        self.assignment_id = None

    def get_assignment_id(self, encrypted_assignment_id: bytes):
        print(f"Student {self.student_id} is getting the assignment ID.")
        f = Fernet(KEY)
        self.assignment_id = f.decrypt(encrypted_assignment_id).decode()

    def submit_assignment(self):
        print(f"Student {self.student_id} is submitting the assignment.")
        solution = "2+2=4"
        submission = {
            "solution": solution,
            "assignment_id": self.assignment_id,
            "student_signature": self.signature,
        }
        
        return encrypt_message(json.dumps(submission), self.KEY)
    
    def read_grades(self, encrypted_submissions_with_grades: bytes):
        decrypted_submissions = json.loads(decrypt_message(encrypted_submissions_with_grades, self.KEY))

        for submission in decrypted_submissions:
            if submission["student_signature"] == self.signature:
                print(f"Student {self.student_id} finds his grade as: {submission['grade']}")

def encrypt_message(message, key):
    f = Fernet(key)
    return f.encrypt(message.encode())

def decrypt_message(token, key):
    f = Fernet(key)
    return f.decrypt(token).decode()

def simulation():
    NUM_OF_STUDENTS = 5

    instructor = Instructor()
    students = [Student(i+1) for i in range(NUM_OF_STUDENTS)]

    encrypted_assignment_id = instructor.publish_assignment_id()

    print("*"*20)

    for student in students:
        student.get_assignment_id(encrypted_assignment_id)
        
    print("*"*20)

    for student in students:
        encrypted_submission = student.submit_assignment()
        instructor.get_submission(encrypted_submission)
    
    print("*"*20)

    instructor.grade_assignments()

    print("*"*20)

    encrypted_submissions = instructor.publish_submissions_with_grades()

    print("*"*20)
    
    for student in students:
        student.read_grades(encrypted_submissions)

if __name__ == "__main__":
    simulation()
