from models import Session, Student, Course, Signup, Deadline
import yagmail

session = Session()

yag = yagmail.SMTP(user='coppermind.harmony@gmail.com', password='HeroOfAges')

def make_mail(student):
		courses = session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==student.id).order_by(Signup.course_id).all()
		contents = 'Here are your upcoming deadlines:\n\n'
		for course in courses:
			contents += course.course_name + '\n'
			for work in course.deadlines:
				contents += work.__repr__()
			contents += '____________________\n'

		return contents

print(session.query(Student).all())
print(session.query(Deadline).all())

for student in session.query(Student).all():
	contents = make_mail(student)
	try:
	    # yag.send(to=student.email, subject='A Message from Sazed', contents=contents)
	    print(contents)
	    print("Email sent successfully")
	except:
	    print("Error, email was not sent")