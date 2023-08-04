from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class ExerciseFile(Base):
	__tablename__ = 'exercise_file'

	id=Column(Integer,primary_key=True)
	courseId=Column(Integer)
	name=Column(String)
	url=Column(String)
	size=Column(Integer)

	def __repr__(self):
		return f"<ExerciseFile(courseId={self.courseId},name={self.name},url={self.url},size={self.size},)>"

class MExerciseFile:
	ds=None
	def __init__(self, ds):
		self.ds = ds
    
	def getByCourseId(self,courseId):
		row = self.ds.session.query(ExerciseFile).filter_by(courseId=courseId).first()
		return row

	def create(self, name,url,size,courseId,update=False):
		rec = self.getByCourseId(courseId)
		if rec:
			if update:
				rec.name = name
				rec.url = url
				rec.size = size
				rec.courseId = courseId
				self.ds.session.commit()
				
			return rec
		
		rec = ExerciseFile(name=name,url=url,size=size,courseId=courseId)
		self.ds.session.add(rec)
		self.ds.session.commit()
