from sqlalchemy import Column, Integer, String
from robots.datasource.models import Base
from cryptography.fernet import Fernet
import json

def generateKey():
    return Fernet.generate_key()

def encrypt(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt(encrypted_message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message).decode()
    return decrypted_message

class Config(Base):
	__tablename__ = 'config'

	id=Column(Integer,primary_key=True)
	key=Column(String)
	value=Column(String)

	def __repr__(self):
		return f"<Config(key={self.key},value={self.value})>"

class MConfig:
	encryption_key=None
	encrypted_config_keys=["email","password","library_id","card_number","pin"]

	def __init__(self, session):
		self.session = session
		encryption_setting_key = 'encryption_key'
		encryption_key = self.get(encryption_setting_key)
		if not encryption_key:
			encryption_key=generateKey()
			encryption_key=encryption_key.decode()
			self.set(encryption_setting_key, encryption_key)
		
		self.encryption_key = encryption_key.encode()
    
	def get(self,key,serialize=True):
		row = self.session.query(Config).filter_by(key=key).first()
		if row:
			if serialize:
				if key in self.encrypted_config_keys:
					encrypted_value = json.loads(row.value)
					decrypted_value = decrypt(encrypted_value, self.encryption_key)
					return decrypted_value

				return json.loads(row.value)
		return row
	
	def getData(self,keys=[]):
		data={}
		for key in keys:
			data[key] = self.get(key)
		return data
	
	def set(self,key,value):
		config = self.get(key,serialize=False)

		if key in self.encrypted_config_keys:
			encrypted_value = encrypt(value, self.encryption_key).decode()
			value = json.dumps(encrypted_value)
		else:
			value = json.dumps(value)
		
		if config:
			config.value = value
		else:
			config = Config(key=key,value=value)
			self.session.add(config)
		
		self.session.commit()
