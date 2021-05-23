from datetime import datetime
from app import db


class Customer(db.Model):
    cid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cname = db.Column(db.String(250), nullable=False)
    cmail = db.Column(db.String(250), unique=True, nullable=False)
    cmobile = db.Column(db.Integer, unique=True, nullable=False)
    caddress = db.Column(db.String(250), nullable=False)
    cpassword = db.Column(db.String(250), nullable=False)

    # def __init__(self, cid, cname, cmail,cmobile,cpassword):
    # self.cid = cid
    # self.cname = cname
    # self.cmail = cmail
    # self.cmobile = cmobile
    # self.cpassword = cpassword
    
    # def __repr__(self):
    #     return "customer('{self.cid}')"


class Restadmin(db.Model):
    rid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rname = db.Column(db.String(250), nullable=False)
    rmail = db.Column(db.String(250), unique=True, nullable=False)
    rmobile = db.Column(db.Integer,unique=True, nullable=False)
    raddress = db.Column(db.String(250), nullable=False)
    rpassword = db.Column(db.String(250), nullable=False)

class Ws(db.Model):
    wid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wname = db.Column(db.String(250), nullable=False)
    wmail = db.Column(db.String(250), unique=True, nullable=False)
    wmobile = db.Column(db.Integer,unique=True, nullable=False)
    waddress = db.Column(db.String(250), nullable=False)
    wpassword = db.Column(db.String(250), nullable=False)
    

class admin(db.Model):
    amail = db.Column(db.String(250), primary_key=True) 
    apassword = db.Column(db.String(250), nullable=False)
    

class Items(db.Model):
    iid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iname = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    iprice = db.Column(db.Integer, nullable=False)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    #rname = db.Column(db.String(250),db.ForeignKey('restadmin.rname'),nullable=False)

class Wsitems(db.Model):
    wiid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    winame = db.Column(db.String(250), nullable=False)
    wicategory = db.Column(db.String(250), nullable=False)
    wiprice = db.Column(db.Integer, nullable=False)
    wid = db.Column(db.Integer, db.ForeignKey('ws.wid'), nullable=False)

class Orders(db.Model):
    ohash = db.Column(db.Integer,primary_key=True, autoincrement=True)
    cid = db.Column(db.Integer, db.ForeignKey('customer.cid'), nullable=False)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    items = db.Column(db.String(250), nullable=False)
    tprice=db.Column(db.Integer, nullable=False)
    ostatus = db.Column(db.String(20), nullable=False)
    iname = db.Column(db.String(20), nullable=True)
    inumber = db.Column(db.Integer, nullable=True)
    idate = db.Column(db.String(20), nullable=True)
    odate = db.Column(db.String(20), nullable=True)
    otime = db.Column(db.String(20), nullable=True)
    ofeedback = db.Column(db.String(250), nullable=True)

class Wsorders(db.Model):
    wohash = db.Column(db.Integer,primary_key=True, autoincrement=True)
    rid = db.Column(db.Integer, db.ForeignKey('restadmin.rid'), nullable=False)
    wid = db.Column(db.Integer, db.ForeignKey('ws.wid'), nullable=False)
    witems = db.Column(db.String(250), nullable=False)
    wtprice=db.Column(db.Integer, nullable=False)
    wostatus = db.Column(db.String(20), nullable=False)
    winame = db.Column(db.String(20), nullable=True)
    winumber = db.Column(db.Integer, nullable=True)
    widate = db.Column(db.String(20), nullable=True)
    

db.create_all()
