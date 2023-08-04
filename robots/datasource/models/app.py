from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class App(Base):
	__tablename__ = 'app'

	id=Column(Integer,primary_key=True)
	version=Column(String)
	state=Column(String)
	lastCourseSlug=Column(String)
	nav=Column(String)
	freshInstall=Column(String)

	def __repr__(self):
		return f"<App(version={self.version},state={self.state},lastCourseSlug={self.lastCourseSlug},nav={self.nav},freshInstall={self.freshInstall},)>"
