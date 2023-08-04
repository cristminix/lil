from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class DMSetup(Base):
	__tablename__ = 'dm_setup'

	id=Column(Integer,primary_key=True)
	courseId=Column(Integer)
	status=Column(Integer)
	finished=Column(Integer)
	availableFmt=Column(String)
	selectedFmt=Column(String)
	exerciseFile=Column(String)
	sourceRepo=Column(String)

	def __repr__(self):
		return f"<DMSetup(courseId={self.courseId},status={self.status},finished={self.finished},availableFmt={self.availableFmt},selectedFmt={self.selectedFmt},exerciseFile={self.exerciseFile},sourceRepo={self.sourceRepo},)>"
