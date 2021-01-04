from sqlalchemy import MetaData, Table, create_engine, Column, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os

engine = create_engine(os.environ.get('DATABASE_URL'))
print(engine.table_names())
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Student(Base):
    __table__ = Table('student', Base.metadata,
                    autoload=True, autoload_with=engine)
    courses = relationship('Course', secondary='signup')

    def __repr__(self):
        return '{}, {}, {}, {}, {}, {}\n'.format(self.id, self.gender, self.username, self.email, self.password, self.courses)

class Course(Base):
	__table__ = Table('course', Base.metadata,
                    autoload=True, autoload_with=engine)
	students = relationship('Student', secondary='signup')
	deadlines = relationship('Deadline', backref='course_in', lazy=True)

	def __repr__(self):
		return self.course_name

class Signup(Base):
	__table__ = Table('signup', Base.metadata,
                    autoload=True, autoload_with=engine)
	

	def __repr__(self):
		return 'C:{}, S:{}\n'.format(self.course_id, self.student_id)

class Deadline(Base):
	__table__ = Table('deadline', Base.metadata,
                    autoload=True, autoload_with=engine)

	def __repr__(self):
		work_list = ['Other', 'Quiz', 'Test', 'Submission', 'Project', 'Viva']
		deadline_str = "\n{0}\nDate: {1}\nTime: {2}\nBrief Details: {3}\n".format(work_list[int(self.work_type)], self.submit_date.strftime("%d %b, %Y. %A"),
																			self.submit_time.strftime("%H:%M"), self.brief_desc)
		return deadline_str