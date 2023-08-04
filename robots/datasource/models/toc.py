from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base
import json
class Toc(Base):
	__tablename__ = 'toc'

	id=Column(Integer,primary_key=True)
	sectionId=Column(Integer)
	title=Column(String)
	slug=Column(String)
	url=Column(String)
	duration=Column(String)
	captionUrl=Column(String)
	captionFmt=Column(String)
	streamLocationIds=Column(String)
	item_star=Column(String)
	v_status_urn=Column(String)

	def __repr__(self):
		return f"<Toc(sectionId={self.sectionId},title={self.title},slug={self.slug},url={self.url},duration={self.duration},captionUrl={self.captionUrl},captionFmt={self.captionFmt},streamLocationIds={self.streamLocationIds},item_star={self.item_star}, v_status_urn={self.v_status_urn})>"

class MToc:
	ds=None
	def __init__(self, ds):
		self.ds = ds
	
	def getListBySectionId(self,sectionId):
		rows = self.ds.session.query(Toc).filter_by(sectionId=sectionId).all()
		return rows

	def getByItemStar(self, item_star):
		q = self.ds.session.query(Toc).filter_by(item_star=item_star)
		# print(q.statement.compile(compile_kwargs={"literal_binds": True}))
		row=q.first()
		return row

	def getBySlug(self, slug, sectionId):
		row = self.ds.session.query(Toc).filter_by(slug=slug,sectionId=sectionId).first()
		return row

	def get(self,id):
		row = self.ds.session.query(Toc).filter_by(id=id).first()
		return row
	
	def update(self, id, row):
		pass
	
	def create(self, title, slug, url, duration, captionUrl, captionFmt, sectionId,item_star,v_status_urn):
		existing = self.getBySlug(slug,sectionId)
		if existing:
			return existing
		streamLocationIds=json.dumps([])

		rec = Toc(title=title, slug=slug, url=url, duration=duration, captionUrl=captionUrl, captionFmt=captionFmt, sectionId=sectionId, streamLocationIds=streamLocationIds,item_star=item_star,v_status_urn=v_status_urn)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec