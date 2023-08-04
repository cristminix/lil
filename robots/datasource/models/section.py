from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base
import json
class Section(Base):
	__tablename__ = 'section'

	id=Column(Integer,primary_key=True)
	courseId=Column(Integer)
	slug=Column(String)
	title=Column(String)
	tocIds=Column(String)
	item_stars=Column(String)

	def __repr__(self):
		return f"<Section(courseId={self.courseId},slug={self.slug},title={self.title},tocIds={self.tocIds},item_stars={self.item_stars})>"

class MSection:
	ds=None
	def __init__(self, ds):
		self.ds = ds
	def get(self, id):
		row = self.ds.session.query(Section).filter_by(id=id).first()
		# if row:
		# 	row.tocIds=json.loads(row.tocIds)
		# 	row.item_stars=json.loads(row.item_stars)
		return row
	def getBySlug(self, slug, courseId):
		row = self.ds.session.query(Section).filter_by(slug=slug,courseId=courseId).first()
		# if row:
		# 	row.tocIds=json.loads(row.tocIds)
		# 	row.item_stars=json.loads(row.item_stars)
		return row
	def getListCourseId(self, courseId):
		rows = self.ds.session.query(Section).filter_by(courseId=courseId).all()
		# for row in rows:
			# row.tocIds=json.loads(row.tocIds)
			# row.item_stars=json.loads(row.item_stars)
		return rows
	
	def create(self, courseId, slug, title, tocIds, item_stars):
		existing = self.getBySlug(slug,courseId)
		if existing:
			return existing
		tocIds=json.dumps(tocIds)
		item_stars=json.dumps(item_stars)

		rec = Section(courseId=courseId,slug=slug,title=title,tocIds=tocIds,item_stars=item_stars)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec