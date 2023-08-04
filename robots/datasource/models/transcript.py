from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base

class Transcript(Base):
	__tablename__ = 'transcript'

	id=Column(Integer,primary_key=True)
	tocId=Column(Integer)
	lang=Column(String)
	country=Column(String)
	fmt=Column(String)
	url=Column(String)
	autoGenerated=Column(Integer)

	def __repr__(self):
		return f"<Transcript(tocId={self.tocId},lang={self.lang},country={self.country},autoGenerated={self.autoGenerated},)>"

class MTranscript:
	ds=None
	def __init__(self, ds):
		self.ds = ds
	def deleteByTocId(self,tocId):
		ls = self.ds.session.query(Transcript).filter_by(tocId=tocId).all()
		for rec in ls:
			self.ds.session.delete(rec)
		
		self.ds.session.commit()
	def getByTocId(self, tocId):
		recs=None
		ls = self.ds.session.query(Transcript).filter_by(tocId=tocId).all()
		if ls:
			recs={}
			for rec in ls:
				recs[rec.lang]=rec
		return recs	
	def getByLang(self, lang, tocId):
		q = self.ds.session.query(Transcript).filter_by(lang=lang, tocId=tocId)

		return q.first()

	def create(self, tocId, lang, country, fmt, url,autoGenerated):
		existing = self.getByLang(lang, tocId)
		if existing:
			return existing
		
		rec = Transcript(tocId=tocId, lang=lang, country=country, fmt=fmt, url=url, autoGenerated=autoGenerated)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec