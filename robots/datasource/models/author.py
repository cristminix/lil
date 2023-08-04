from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base, author_course_association
# from robots.datasource.models import MCourse
from sqlalchemy.orm import relationship

class Author(Base):
	__tablename__ = 'author'

	id=Column(Integer,primary_key=True)
	name=Column(String)
	slug=Column(String)
	biography=Column(String)
	shortBiography=Column(String)
	# courseIds=Column(String)
	courses = relationship('Course', secondary=author_course_association, back_populates='authors')

	def __repr__(self):
		return f"<Author(name={self.name},slug={self.slug},biography={self.biography},shortBiography={self.shortBiography})>"

class MAuthor:
	ds=None
	m_course=None
	def __init__(self, ds):
		self.ds = ds
		self.m_course=ds.m_course
	
	def getBySlug(self, slug):
		row = self.ds.session.query(Author).filter_by(slug=slug).first()
		# if row:
		# 	row.tocIds=json.loads(row.tocIds)
		# 	row.item_stars=json.loads(row.item_stars)
		return row
	def addCourse(self,author,course):
		author.courses.append(course)
		self.ds.session.commit()
	
	def create(self, slug, name, biography, shortBiography):
		existing = self.getBySlug(slug)
		if existing:
			return existing
		# tocIds=json.dumps(tocIds)
		# item_stars=json.dumps(item_stars)

		rec = Author(slug=slug,name=name,biography=biography,shortBiography=shortBiography)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec