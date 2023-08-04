from sqlalchemy import Column, Integer, String,MetaData, Table

from robots.datasource.models import Base
from sqlalchemy import text
class Prx(Base):
	__tablename__ = 'prx_cache'

	id=Column(Integer,primary_key=True)
	page_name=Column(String)
	content=Column(String)

	def __repr__(self):
		return f"<StreamLocation(page_name={self.page_name})>"

class MPrx:
	ds=None
	def __init__(self, ds):
		self.ds = ds
	
	def getByPageName(self, page_name):
		row = self.ds.session.query(Prx).filter_by(page_name=page_name).first()
		return row
	def deleteByPageName(self, page_name):
		row = self.ds.session.query(Prx).filter_by(page_name=page_name).first()
		if row:
			self.ds.session.delete(row)
			self.ds.session.commit()
	def clear(self):
		rows = self.ds.session.query(Prx).all()
		for row in rows:
			self.ds.session.delete(row)
		# self.ds.conn.execute(text("COMMIT"))
		self.ds.conn.execute(text("VACUUM"))
		self.ds.session.commit()


	def getSize(self):
		table_name="prx_cache"
		t = text(f"pragma page_count('{table_name}')")
		result = self.ds.conn.execute(t).fetchall()
		page_count= [item[0] for item in result][0]
		# print(page_count)
		t = text(f"pragma page_size")
		result = self.ds.conn.execute(t).fetchall()
		page_size= [item[0] for item in result][0]
		# print(page_size)
		table_size_bytes = page_count * page_size
		return table_size_bytes

	def create(self, page_name, content):
		existing = self.getByPageName(page_name)
		if existing:
			self.ds.session.delete(existing)

		rec = Prx(page_name=page_name, content=content)
		self.ds.session.add(rec)
		self.ds.session.commit()
		return rec
