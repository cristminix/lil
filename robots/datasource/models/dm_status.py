from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class DMStatus(Base):
	__tablename__ = 'dm_status'

	id=Column(Integer,primary_key=True)
	courseId=Column(Integer)
	vIndex=Column(String)
	metaStatus=Column(Integer)
	videoStatus=Column(Integer)
	captionStatus=Column(Integer)
	dtMetaStart=Column(String)
	dtVideoStart=Column(String)
	dtCaptionStart=Column(String)
	dtMetaEnd=Column(String)
	dtVideoEnd=Column(String)
	dtCaptionEnd=Column(String)
	dlMetaRetryCount=Column(Integer)
	dlCaptionRetryCount=Column(Integer)
	dlVideoRetryCount=Column(Integer)
	videoSz=Column(Integer)
	captionSz=Column(Integer)
	finished=Column(Integer)
	interupted=Column(Integer)

	def __repr__(self):
		return f"<DMStatus(courseId={self.courseId},vIndex={self.vIndex},metaStatus={self.metaStatus},videoStatus={self.videoStatus},captionStatus={self.captionStatus},dtMetaStart={self.dtMetaStart},dtVideoStart={self.dtVideoStart},dtCaptionStart={self.dtCaptionStart},dtMetaEnd={self.dtMetaEnd},dtVideoEnd={self.dtVideoEnd},dtCaptionEnd={self.dtCaptionEnd},dlMetaRetryCount={self.dlMetaRetryCount},dlCaptionRetryCount={self.dlCaptionRetryCount},dlVideoRetryCount={self.dlVideoRetryCount},videoSz={self.videoSz},captionSz={self.captionSz},finished={self.finished},interupted={self.interupted},)>"
