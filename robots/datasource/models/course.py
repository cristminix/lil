from sqlalchemy import Column, Integer, String, text
from robots.datasource.models import Base, author_course_association
from sqlalchemy.orm import relationship

class Course(Base):
	__tablename__ = 'course'

	id=Column(Integer,primary_key=True)
	title=Column(String)
	slug=Column(String)
	duration=Column(String)
	sourceCodeRepository=Column(String)
	description=Column(String)
	urn=Column(String)
	authors = relationship('Author', secondary=author_course_association, back_populates='courses')


	def __repr__(self):
		return f"<Course(title={self.title},slug={self.slug},duration={self.duration},sourceCodeRepository={self.sourceCodeRepository},description={self.description},urn={self.urn})>"

class MCourse:
	ds=None
	def __init__(self, ds):
		self.ds = ds
    
	def getAvailableStreamFmt(self,courseId):
		t = text(f"""SELECT
					stream_location.fmt fmt
					FROM
					course
					JOIN section
					ON course.id = section.courseId 
					JOIN toc
					ON section.id = toc.sectionId 
					JOIN stream_location
					ON toc.id = stream_location.tocId
					WHERE
					course.id={courseId}
					GROUP BY
					fmt""")
		result = self.ds.conn.execute(t).fetchall()
		return [item[0] for item in result]
	
	def getAvailableTransLang(self,courseId):
		t = text(f"""SELECT
					
					LOWER(transcript.country) AS lang
					FROM
					course
					JOIN section
					ON course.id = section.courseId 
					JOIN toc
					ON section.id = toc.sectionId 
					JOIN transcript
					ON toc.id = transcript.tocId
					WHERE
					course.id={courseId}
					GROUP BY
					lang""")
		result = self.ds.conn.execute(t).fetchall()
		return [item[0] for item in result]
	
	def get(self,id):
		row = self.ds.session.query(Course).filter_by(id=id).first()
		return row
	
	def getBySlug(self,slug):
		row = self.ds.session.query(Course).filter_by(slug=slug).first()
		return row
	def getList(self):
		rows = self.ds.session.query(Course).all()
		return rows
	def addAuthor(self,course, author):
		course.authors.append(author)
		self.ds.session.commit()
	def getLastSlug(self,keys=[]):
		pass
	
	def setLastSlug(self):
		pass
	
	def addAuthorId(self):
		pass
	
	def getCoursePageData(self):
		pass
	
	def getCourseSecsTocs(self):
		pass
	
	def create(self, title, slug, duration, sourceCodeRepository, description, urn,update=False):
		course = self.getBySlug(slug)
		if course:
			if update:
				course.title = title
				course.slug = slug
				course.duration = duration
				course.sourceCodeRepository = sourceCodeRepository
				course.description = description
				course.urn = urn
				self.ds.session.commit()

			return course
		course = Course(title=title, slug=slug, duration=duration, sourceCodeRepository=sourceCodeRepository, description=description, urn=urn)
		self.ds.session.add(course)
		self.ds.session.commit()
		
		return course
	
	def update(self,id,row):
		pass