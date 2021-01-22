from models import Session, Student, Course, Signup, Deadline
import yagmail
import schedule
import time
import os
from datetime import datetime

def make_mail(student, session):
		courses = session.query(Course).filter(Signup.course_id==Course.id, Signup.student_id==student.id).order_by(Signup.course_id).all()
		contents = 'Here are your upcoming deadlines:\n\n'
		for course in courses:
			contents += course.course_name + '\n'
			for work in course.deadlines:
				contents += work.__repr__()
			contents += '____________________\n'

		return contents

# print(session.query(Student).all())
# print(session.query(Deadline).all())

def send_mails():
	yag = yagmail.SMTP(user='coppermind.harmony@gmail.com', password=os.environ.get('MAILER_PASSWORD'))
	session = Session()
	student_list = session.query(Student).all()
	session.close()
	for student in student_list:
		session = Session()
		contents = make_mail(student, session)
		session.close()
		try:
		    yag.send(to=student.email, subject='Upcoming Deadlines as on {}'.format(datetime.now().strftime('%d/%m')), contents=contents)
		    print(contents)
		    print("Email sent successfully")
		except:
		    print("Error, email was not sent")

	yag.close()
	return None

if __name__ == "__main__":
	schedule.every().day.at("06:30").do(send_mails) #Heroku server at UTC time. This is 12:00 pm IST
	print("I am running")
	while True: 
		schedule.run_pending() 
		time.sleep(1) 