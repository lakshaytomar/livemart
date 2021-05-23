CREATE TABLE customer (
	cid integer PRIMARY KEY AUTOINCREMENT,
	cname varchar,
	cmail varchar,
	cmobile integer,
	caddress varchar,
	cpassword varchar
);

CREATE TABLE restadmin (
	rid integer PRIMARY KEY AUTOINCREMENT,
	rname varchar,	
	rmail varchar,
	rmobile integer,
	raddress varchar,
	rpassword varchar
);

CREATE TABLE ws (
	wid integer PRIMARY KEY AUTOINCREMENT,
	wname varchar,	
	wmail varchar,
	wmobile integer,
	waddress varchar,
	wpassword varchar
);

CREATE TABLE admin (
	amail varchar,
	apassword varchar
);

CREATE TABLE items (
	iid integer,
	iname varchar,
	iprice integer,
	rid integer,
	category varchar
	
);

CREATE TABLE wsitems (
	wiid integer,
	winame varchar,
	wiprice integer,
	wid integer,
	wcategory varchar
	
);

CREATE TABLE orders (
	oid integer,
	cid integer,
	rid integer,
	iid integer,
	ostatus text,
	iname text,
	inumber integer,
	idate text,
	odate text,
	otime text,
	ofeedback text
);

CREATE TABLE wsorders (
	woid integer,
	rid integer,
	wid integer,
	wiid integer,
	wostatus text,
	winame text,
	winumber integer,
	widate text
);

