from app import db
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base
from datetime import datetime

class Controler(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	name = db.Column(db.String(64), index=True,unique=True)
	status = db.Column(db.Integer)
	description = db.Column(db.Text)
	elements = db.relationship('Element', backref='controler', lazy='dynamic')
	addedAt = db.Column(db.DateTime)
	def __repr__(self):
		return '<Controler %r>' %(self.name)
	def __init__(self,name,status,description):
		self.name = name
		self.status = status
		self.description = description
		self.addedAt = datetime.now()

class Element(db.Model):

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(64),index=True,unique=True)
	description = db.Column(db.Text())
	status = db.Column(db.Integer)
	lastUpdate = db.Column(db.DateTime)
	addedAt = db.Column(db.DateTime)
	controler_id = db.Column(db.Integer, db.ForeignKey('controler.id'))
	
	def __init__(self,name,status,description):
		self.name = name
		self.status = status
		self.description = description
		self.addedAt = datetime.now()