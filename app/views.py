from flask import render_template
from sqlalchemy import and_
from sqlalchemy import or_
from flask import url_for, redirect, request, make_response,flash
# Importing Session Object to use Sessions
from flask import session
from flask_mail import Mail
from flask import g
from app.models import Customer, Restadmin, Items, Wsitems, Orders, Wsorders, admin, Ws
from app import app, db
import random

app.config.update(
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 465,
	MAIL_USE_SSL = True,
	MAIL_USERNAME = 'lakshaytomar4@gmail.com',
	MAIL_PASSWORD = ''
)
mail = Mail(app)

# ohash=0;

@app.route('/')
@app.route('/index')
def index():
	
	#db.session.add(items)
	# db.session.commit()
#	name='Fruits'
#	items = Items.query.filter_by(iname=name).all()

	'''
	itemname=Items.query.get(iid).iname
	rnames=[]
	for item in items:
		rest=Restadmin.query.filter_by(rid=item.rid).first()
		rnames.append(rest.rname)
	
	
	print("restraunts")
	print(rnames)
	'''
	#cname='Dairy'
	#items = Items.query.filter_by(category=cname).distinct()
	#items=[item.iname for item in items]
	'''
	items=Items.query.filter().all()
	Categories=[]
	for item in items:
		if item.category not in Categories:
			Categories.append(item.category)
	'''
	Categories=['Vegetables','Fruits','Dairy','Packaged']
	return render_template('index.html',categories = Categories)
	#return render_template('index.html',categories = Restadmin.query.all())

@app.route('/restindex')
def restindex():
	
	'''
	items=Wsitems.query.filter().all()
	Categories=[]
	for item in items:
		if item.category not in Categories:
			Categories.append(item.category)
	'''
	Categories=['Vegetables','Fruits','Dairy','Packaged']
	return render_template('restindex.html',categories = Categories)


@app.route('/indexmenu', methods = ['GET','POST'])
def indexmenu():


	if request.method == "GET":
		restid = request.args.get("restid")
		
	elif request.method == "POST":
		restid = request.form['restid']
		print(restid)

	items = Items.query.filter(Items.rid == restid).all()
	restad = Restadmin.query.filter(Restadmin.rid == restid).first()
	return render_template('indexmenu.html',restad=restad, restadmin=items)

@app.route('/items', methods = ['GET','POST'])
def items():
	if request.method == "GET":
		categoryid= request.args.get("categoryid")

	elif request.method == "POST":
		categoryid = request.form['categoryid']
	categoryid=int(categoryid)
	'''
	items=Items.query.filter().all()
	Categories=[]
	for item in items:
		if item.category not in Categories:
			Categories.append(item.category)
	print(Categories)
	'''
	Categories=['Vegetables','Fruits','Dairy','Packaged']
	cname=Categories[categoryid]
	items = Items.query.filter_by(category=cname).distinct()
	unitems=[]
	itemnames=[]
	for item in items:
		if(item.iname not in itemnames):
			unitems.append(item)
			itemnames.append(item.iname)

	return render_template('items.html',items=unitems,category=cname)


@app.route('/grocers', methods = ['GET','POST'])
def grocers():

	if request.method == "GET":
		itemid = request.args.get("itemid")
	
		
	elif request.method == "POST":
		itemid = int(request.form['itemid'])
		session['itemselected']=itemid
	
	

	itemname=Items.query.get(itemid).iname
	items=Items.query.filter_by(iname=itemname).all()

	grocers=[]
	for item in items:
		grocer=Restadmin.query.filter_by(rid=item.rid).first()
		grocers.append(grocer)

	print(grocers)
	return render_template('grocers.html',grocers=grocers,items=items)

@app.route('/restgrocers', methods = ['GET','POST'])
def restgrocers():

	if request.method == "GET":
		itemid = request.args.get("itemid")
	
		
	elif request.method == "POST":
		itemid = int(request.form['itemid'])
		session['wsitemselected']=itemid
	
	

	itemname=Wsitems.query.get(itemid).winame
	items=Wsitems.query.filter_by(winame=itemname).all()

	grocers=[]
	for item in items:
		grocer=Ws.query.filter_by(wid=item.wid).first()
		grocers.append(grocer)

	return render_template('restgrocers.html',grocers=grocers,items=items)

# customerregister.html
@app.route('/register')
def register():
	return render_template('userregister.html')

# customerregisterNext.py
@app.route('/registerNext', methods = ['GET','POST'])
def registerNext():

	if request.method == "GET":
		cmail = request.args.get("cmail")
		cpassword = request.args.get("cpassword")

	elif request.method == "POST":
		cmail = request.form['cmail']
		cpassword = request.form['cpassword']


		customercheck = Customer.query.filter(and_(Customer.cmail == cmail, Customer.cpassword == cpassword)).first()

		# return(str(customer))
		if customercheck :

			return render_template('userregister.html',cmsg="Registration Failed, \n User Already Registered..!")

		else:
		
			customer = Customer(cname=request.form["cname"], cmail=request.form["cmail"], cmobile=request.form["cmobile"], caddress=request.form["caddress"], cpassword=request.form['cpassword'])
					
			db.session.add(customer)
			db.session.commit()

				# 	session['cmail'] = request.form['cmail']
			# return redirect(url_for('login'))
			return render_template('userlogin.html',cusmsg="Registered Succcessfully...! \n Please Login To Continue")

				# return redirect(url_for('adminHome1'))

	
# customerlogin.html
@app.route('/login')
def login():
	return render_template('userlogin.html')

	
# customerloginNext.html
@app.route('/loginNext',methods=['GET','POST'])
def loginNext():
	# if not session.get('cmail'):
	# 	return redirect(request.url_root)

	if request.method == "GET":
		cmail = request.args.get("cmail")
		cpassword = request.args.get("cpassword")
	
	elif request.method == "POST":
		cmail = request.form['cmail']
		cpassword = request.form['cpassword']

		
		customer  = Customer.query.filter(and_(Customer.cmail == cmail, Customer.cpassword == cpassword)).first()


		if customer :
			session['cmail'] = request.form['cmail']

			otp = random.randrange(100000,999999)

			mail.send_message("OTP to login on Live MART", 
			sender = "lakshaytomar4@gmail.com", 
			recipients=[cmail],
			body = "Your OTP to login on Live MART is " + str(otp) + "\n" + "Thanks for choosing us." + "\n" + "Live MART")			

			return render_template('otpverify.html', otp=otp, error = '')

			# return render_template('userhome.html',cusname=customer.cname,restadmin = Restadmin.query.all())
			# return render_template('userhome.html',restadmin = Restadmin.query.all())
			
		return render_template('userlogin.html',cusname="Login failed...\n Please enter valid username and password!")

@app.route('/otpverification',methods=['GET','POST'])
def otpverification():
	# if not session.get('cmail'):
	# 	return redirect(request.url_root)

	if request.method == "GET":
		otp = request.args.get("otp")
		otpenter = request.args.get("otpenter")
	
	elif request.method == "POST":
		otp = request.form['otp']
		otpenter = request.form['otpenter']			

		if otpenter == otp:
			return redirect(url_for('userhome1'))
			# return render_template('userhome.html',cusname=customer.cname,restadmin = Restadmin.query.all())
			# return render_template('userhome.html',restadmin = Restadmin.query.all())
			
		return render_template('otpverify.html', otp=otp, error = "The OTP you entered is invalid. Please enter the correct OTP")

@app.route('/otpverificationR',methods=['GET','POST'])
def otpverificationR():
	# if not session.get('cmail'):
	# 	return redirect(request.url_root)

	if request.method == "GET":
		otp = request.args.get("otp")
		otpenter = request.args.get("otpenter")
	
	elif request.method == "POST":
		otp = request.form['otp']
		otpenter = request.form['otpenter']			

		if otpenter == otp:
			return redirect(url_for('resthome1'))
			# return render_template('userhome.html',cusname=customer.cname,restadmin = Restadmin.query.all())
			# return render_template('userhome.html',restadmin = Restadmin.query.all())
			
		return render_template('otpverifyR.html', otp=otp, error = "The OTP you entered is invalid. Please enter the correct OTP")

@app.route('/otpverificationW',methods=['GET','POST'])
def otpverificationW():
	# if not session.get('cmail'):
	# 	return redirect(request.url_root)

	if request.method == "GET":
		otp = request.args.get("otp")
		otpenter = request.args.get("otpenter")
	
	elif request.method == "POST":
		otp = request.form['otp']
		otpenter = request.form['otpenter']			

		if otpenter == otp:
			return redirect(url_for('wshome1'))
			# return render_template('userhome.html',cusname=customer.cname,restadmin = Restadmin.query.all())
			# return render_template('userhome.html',restadmin = Restadmin.query.all())
			
		return render_template('otpverifyW.html', otp=otp, error = "The OTP you entered is invalid. Please enter the correct OTP")

@app.route('/userhome1',methods=['GET','POST'])
def userhome1():
	if not session.get('cmail'):
		return redirect(request.url_root)
	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()
	#print(Items.query.all())
	'''
	items=Items.query.filter().all()
	Categories=[]
	for item in items:
		if item.category not in Categories:
			Categories.append(item.category)
	print(Categories)
	'''
	Categories=['Vegetables','Fruits','Dairy','Packaged']
	return render_template('userhome.html',cusname=customer.cname,categories = Categories)

@app.route('/useritems',methods=['GET','POST'])
def useritems():
	if not session.get('cmail'):
		return redirect(request.url_root)

	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()
	
	if request.method == "GET":
		categoryid= request.args.get("categoryid")

	elif request.method == "POST":
		categoryid = request.form['categoryid']
	categoryid=int(categoryid)
	'''
	items=Items.query.filter().all()
	Categories=[]
	for item in items:
		if item.category not in Categories:
			Categories.append(item.category)
	print(Categories)
	'''
	Categories=['Vegetables','Fruits','Dairy','Packaged']
	cname=Categories[categoryid]
	items = Items.query.filter_by(category=cname).distinct()
	unitems=[]
	itemnames=[]
	for item in items:
		if(item.iname not in itemnames):
			unitems.append(item)
			itemnames.append(item.iname)

	return render_template('useritems.html', items=unitems,category=cname)
	
	#return render_template('userhome.html',cusname=customer.cname,categories = Categories)

@app.route('/restitems',methods=['GET','POST'])
def restitems():
	if not session.get('rmail'):
		return redirect(request.url_root)

	cmail=session['rmail']
	customer  = Restadmin.query.filter(Restadmin.rmail == cmail).first()
	
	if request.method == "GET":
		categoryid= request.args.get("categoryid")

	elif request.method == "POST":
		categoryid = request.form['categoryid']
	categoryid=int(categoryid)
	'''
	items=Items.query.filter().all()
	Categories=[]
	for item in items:
		if item.category not in Categories:
			Categories.append(item.category)
	print(Categories)
	'''
	Categories=['Vegetables','Fruits','Dairy','Packaged']
	cname=Categories[categoryid]
	items = Wsitems.query.filter_by(wicategory=cname).distinct()
	unitems=[]
	itemnames=[]
	for item in items:
		if(item.winame not in itemnames):
			unitems.append(item)
			itemnames.append(item.winame)

	return render_template('restitems.html', items=unitems,category=cname)

@app.route('/userorders',methods=['GET','POST'])
def userorders():
	if not session.get('cmail'):
		return redirect(request.url_root)
	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()
	cid=customer.cid
	myorders = Orders.query.filter(and_(Orders.cid == cid, Orders.odate == None))

	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)
	# iuour = orders.query.join(items, orders.iid==items.iid).add_columns(users.userId, users.name, users.email, friends.userId, friendId).filter(users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
		
	return render_template('userorders.html',cusname=customer.cname,restadmin = customer.query.all(), myorders=myorders)

@app.route('/userordersoffline',methods=['GET','POST'])
def userordersoffline():
	if not session.get('cmail'):
		return redirect(request.url_root)
	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()
	cid=customer.cid
	myorders = Orders.query.filter(and_(Orders.cid == cid, Orders.odate != None))

	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)
	# iuour = orders.query.join(items, orders.iid==items.iid).add_columns(users.userId, users.name, users.email, friends.userId, friendId).filter(users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
		
	return render_template('userordersoffline.html',cusname=customer.cname,restadmin = customer.query.all(), myorders=myorders)



@app.route('/restorders',methods=['GET','POST'])
def restorders():
	print("restorders")
	if not session.get('rmail'):
		return redirect(request.url_root)
	cmail=session['rmail']
	customer  = Restadmin.query.filter(Restadmin.rmail == cmail).first()
	cid=customer.rid
	myorders = Wsorders.query.filter(Wsorders.rid == cid)

	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)
	# iuour = orders.query.join(items, orders.iid==items.iid).add_columns(users.userId, users.name, users.email, friends.userId, friendId).filter(users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
		
	return render_template('restorders.html',cusname=customer.rname,restadmin = customer.query.all(), myorders=myorders)

@app.route('/showuserprofile', methods = ['GET','POST'])
def showuserprofile():
	if not session.get('cmail'):
		return redirect(request.url_root)
	cmail=session['cmail']

	customer=Customer.query.filter(Customer.cmail==cmail).first()
	# customer.cpassword=cpassword
	# db.session.commit()
	return render_template('showuserprofile.html',cusname=customer.cname,cusinfo = customer)



@app.route('/updateuserprofile',methods = ['GET','POST'])
def updateuserprofile():
	if not session.get('cmail'):
		return redirect(request.url_root)
	return render_template('updateuserprofile.html')


@app.route('/updateuserprofileNext', methods = ['GET','POST'])
def updateuserprofileNext():
	if not session.get('cmail'):
		return redirect(request.url_root)
	cmail=session['cmail']

	cpassword = request.form['cpassword']
	
	customer=Customer.query.filter(Customer.cmail==cmail).first()
	customer.cpassword=cpassword
	db.session.commit()
	return render_template('updateuserprofile.html', cmsg="Passsword Updated Succcessfully...!")


# customerlogout.html
@app.route('/logout')
def logout():
	session.pop('cmail',None)
	return redirect(url_for('index'))



@app.route('/restmenu', methods = ['GET','POST'])
def restmenu():
	if not session.get('cmail'):
		return redirect(url_for('login'))

	if request.method == "GET":
		restid = request.args.get("restid")
	
	elif request.method == "POST":
		restid = request.form['restid']

	itemid=session['itemselected']
	item=Items.query.get(itemid)
	items = Items.query.filter(Items.rid == restid).all()
	restad = Restadmin.query.filter(Restadmin.rid == restid).first()
	return render_template('restmenu.html',restad=restad, restadmin=items,item=item)

@app.route('/wsmenu', methods = ['GET','POST'])
def wsmenu():
	if not session.get('rmail'):
		return redirect(url_for('restlogin'))

	if request.method == "GET":
		restid = request.args.get("restid")
	
	elif request.method == "POST":
		restid = request.form['restid']

	itemid=session.get('wsitemselected')
	item=Wsitems.query.get(itemid)
	items = Wsitems.query.filter(Wsitems.wid == restid).all()
	restad = Ws.query.filter(Ws.wid == restid).first()
	return render_template('wsmenu.html',restad=restad, restadmin=items,item=item)
# restadmin login
@app.route('/restlogin')
def restlogin():
	return render_template('restlogin.html')

@app.route('/wslogin')
def wslogin():
	return render_template('wslogin.html')

@app.route('/restsignup')
def restsignup():
	return render_template('restsignup.html')

@app.route('/wssignup')
def wssignup():
	return render_template('wssignup.html')

@app.route('/restregisterNext', methods = ['GET','POST'])
def restregisterNext():

	if request.method == "GET":
		rmail = request.args.get("rmail")
		rpassword = request.args.get("rpassword")

	elif request.method == "POST":
		rmail = request.form['rmail']
		rpassword = request.form['rpassword']


		customercheck = Restadmin.query.filter(and_(Restadmin.rmail == rmail, Restadmin.rpassword == rpassword)).first()

		# return(str(customer))
		if customercheck :

			return render_template('restsignup.html',cmsg="Registration Failed, \n User Already Registered..!")

		else:
		
			restadmin = Restadmin(rname=request.form["rname"], rmail=request.form["rmail"], rmobile=request.form["rmobile"], raddress=request.form["raddress"], rpassword=request.form['rpassword'])
					
			db.session.add(restadmin)
			db.session.commit()

				# 	session['cmail'] = request.form['cmail']
			# return redirect(url_for('login'))
			return render_template('restlogin.html',cusmsg="Registered Succcessfully...! \n Please Login To Continue")

				# return redirect(url_for('adminHome1'))

@app.route('/wsregisterNext', methods = ['GET','POST'])
def wsregisterNext():

	if request.method == "GET":
		rmail = request.args.get("rmail")
		rpassword = request.args.get("rpassword")

	elif request.method == "POST":
		rmail = request.form['rmail']
		rpassword = request.form['rpassword']


		customercheck = Restadmin.query.filter(and_(Ws.wmail == rmail, Ws.wpassword == rpassword)).first()

		# return(str(customer))
		if customercheck :

			return render_template('wssignup.html',cmsg="Registration Failed, \n User Already Registered..!")

		else:
		
			restadmin =Ws(wname=request.form["rname"], wmail=request.form["rmail"], wmobile=request.form["rmobile"], waddress=request.form["raddress"], wpassword=request.form['rpassword'])
					
			db.session.add(restadmin)
			db.session.commit()

				# 	session['cmail'] = request.form['cmail']
			# return redirect(url_for('login'))
			return render_template('wslogin.html',cusmsg="Registered Succcessfully...! \n Please Login To Continue")

				# return redirect(url_for('adminHome1'))

	
# restadminloginNext.html
@app.route('/restloginNext',methods=['GET','POST'])
def restloginNext():
	# To find out the method of request, use 'request.method'

	if request.method == "GET":
		rmail = request.args.get("rmail")
		rpassword = request.args.get("rpassword")
	
	elif request.method == "POST":
		rmail = request.form['rmail']
		rpassword = request.form['rpassword']

		
		restadmin  = Restadmin.query.filter(and_(Restadmin.rmail == rmail, Restadmin.rpassword == rpassword)).first()


		if restadmin :
			session['rmail'] = request.form['rmail']

			otp = random.randrange(100000,999999)

			mail.send_message("OTP to login on Live MART", 
			sender = "lakshaytomar4@gmail.com", 
			recipients=[rmail],
			body = "Your OTP to login on Live MART is " + str(otp) + "\n" + "Thanks for choosing us." + "\n" + "Live MART")			

			return render_template('otpverifyR.html', otp=otp, error = '')

			# return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all())
			# return render_template('resthome.html',restadmin = Restadmin.query.all())
			
		return render_template('restlogin.html',rusname="Login failed...\n Please enter valid username and password!")

@app.route('/wsloginNext',methods=['GET','POST'])
def wsloginNext():
	# To find out the method of request, use 'request.method'

	if request.method == "GET":
		rmail = request.args.get("rmail")
		rpassword = request.args.get("rpassword")
	
	elif request.method == "POST":
		rmail = request.form['rmail']
		rpassword = request.form['rpassword']

		
		restadmin  = Ws.query.filter(and_(Ws.wmail == rmail, Ws.wpassword == rpassword)).first()


		if restadmin :
			session['wmail'] = request.form['rmail']

			otp = random.randrange(100000,999999)

			mail.send_message("OTP to login on Live MART", 
			sender = "lakshaytomar4@gmail.com", 
			recipients=[rmail],
			body = "Your OTP to login on Live MART is " + str(otp) + "\n" + "Thanks for choosing us." + "\n" + "Live MART")			

			return render_template('otpverifyW.html', otp=otp, error = '')
			# return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all())
			# return render_template('resthome.html',restadmin = Restadmin.query.all())
			
		return render_template('wslogin.html',rusname="Login failed...\n Please enter valid username and password!")

@app.route('/resthome1',methods=['GET','POST'])
def resthome1():
	if not session.get('rmail'):
		return redirect(request.url_root)
	rmail=session['rmail']
	restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	rid=restadmin.rid
	# myorders = Orders.query.filter(Orders.rid == rid)
	myorders = Orders.query.filter(and_(Orders.rid == rid, Orders.odate == None, or_(Orders.ostatus=='Order Placed', Orders.ostatus=='Order Dispatched', Orders.ostatus=='In Transit')))
	return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all(), myorders=myorders)

@app.route('/wshome1',methods=['GET','POST'])
def wshome1():
	if not session.get('wmail'):
		return redirect(request.url_root)
	rmail=session['wmail']
	restadmin  = Ws.query.filter(Ws.wmail == rmail).first()
	rid=restadmin.wid
	# myorders = Orders.query.filter(Orders.rid == rid)
	myorders = Wsorders.query.filter(and_(Wsorders.wid == rid, or_(Wsorders.wostatus=='Order Placed', Wsorders.wostatus=='Order Dispatched', Wsorders.wostatus=='In Transit')))
	return render_template('wshome.html',rusname=restadmin.wname,restadmin = Ws.query.all(), myorders=myorders)

# ////////////////////////////////////////
	# q = Orders.query.join(Restadmin, Orders.rid==Restadmin.rid).join(Customer, Orders.cid==Customer.cid).join(Items, Restadmin.rid==Items.rid).add_columns(Orders.ohash, Orders.rid,Restadmin.rname,Customer.cname,Customer.cid,Items.iid,Orders.ostatus,Orders.tprice).filter(and_(Orders.rid == rid, Orders.cid==Customer.cid,Items.rid==Restadmin.rid, Orders.ostatus=='pending')).distinct()
	
	# db.session.query(
	#    Class.Orders,
	#    Class.Customer,
	#    Class.Restadmin,
	#    func.group_concat(Orders..distinct()),
	#    func.group_concat(Course.course_name.distinct())
	#    ).filter(Class.courses, User.classes).group_by(Class.class_id)


	# return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all(), myorders=q)
	# return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all())


# ///////////////////////////////////////

	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)
	


# //////////////////////////////////
@app.route('/acceptorreject',methods=['GET','POST'])
def acceptorreject():
	if not session.get('rmail'):
		return redirect(request.url_root)
	rmail=session['rmail']

	ohash = request.form['ohash']
	cid = request.form['cid']
	acceptreject=	request.form['acceptreject']

	customer=Customer.query.filter(Customer.cid==cid).first()
	
	# myorders = Orders.query.filter(Orders.ohash == ohash)


	if acceptreject=="dispatched":
		orders=Orders.query.filter(Orders.ohash==ohash).first()
		orders.ostatus="Order Dispatched"
		db.session.commit()

	if acceptreject=="inTransit":
		orders=Orders.query.filter(Orders.ohash==ohash).first()
		orders.ostatus="In Transit"
		db.session.commit()
	
	if acceptreject=="delivered":
		orders=Orders.query.filter(Orders.ohash==ohash).first()
		orders.ostatus="Order Delivered"
		db.session.commit()

		mail.send_message("Please give your valuable feedback for order no." + ohash, 
		sender = "lakshaytomar4@gmail.com", 
		recipients=[customer.cmail],
		body = "Please reply to this mail with your feedback for the product and your delivery experience" + "\n"
		"Thanks for choosing us." + "\n" + "Live MART")		
		
	
	if acceptreject=="reject":
		Orders.query.filter(Orders.ohash == ohash).delete()
		db.session.commit()
		

	restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	rid=restadmin.rid

	myorders = Orders.query.filter(Orders.rid == rid)
	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)

	return redirect(url_for('resthome1'))
	# return render_template('resthome.html',rusname=restadmin.rname,restadmin = Restadmin.query.all(), myorders=myorders)

@app.route('/wsacceptorreject',methods=['GET','POST'])
def wsacceptorreject():
	if not session.get('wmail'):
		return redirect(request.url_root)
	rmail=session['wmail']

	ohash = request.form['ohash']
	acceptreject=	request.form['acceptreject']

	# myorders = Orders.query.filter(Orders.ohash == ohash)


	if acceptreject=="dispatched":
		orders=Wsorders.query.filter(Wsorders.wohash==ohash).first()
		orders.wostatus="Order Dispatched"
		db.session.commit()

	if acceptreject=="inTransit":
		orders=Wsorders.query.filter(Wsorders.wohash==ohash).first()
		orders.wostatus="In Transit"
		db.session.commit()
	
	if acceptreject=="delivered":
		orders=Wsorders.query.filter(Wsorders.wohash==ohash).first()
		orders.wostatus="Order Delivered"
		db.session.commit()
		
	
	if acceptreject=="reject":
		Wsorders.query.filter(Wsorders.wohash == ohash).delete()
		db.session.commit()
		

	restadmin  = Ws.query.filter(Ws.wmail == rmail).first()
	rid=restadmin.wid

	myorders = Wsorders.query.filter(Wsorders.wid == rid)
	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)

	return redirect(url_for('wshome1'))


@app.route('/adddelivery',methods = ['GET','POST'])
def adddelivery():
	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		ohash = request.args.get("ohash")
		cid = request.args.get("cid")
		iname = request.args.get("iname")
		inumber = request.args.get("inumber")
		idate = request.args.get("idate")
	
	elif request.method == "POST":
		ohash = request.form['ohash']
		cid = request.form['cid']
		iname = request.form['iname']
		inumber = request.form['inumber']
		idate = request.form['idate']

	orders=Orders.query.filter(Orders.ohash==ohash).first()
	orders.iname=iname
	orders.inumber=inumber
	orders.idate=idate
	db.session.commit()

	customer=Customer.query.filter(Customer.cid==cid).first()

	mail.send_message("Details of Order No. " + ohash, 
	sender = "lakshaytomar4@gmail.com", 
	recipients=[customer.cmail],
	body = "Your order will be delivered by " + iname + "\n" +
	"Mobile Number: " + inumber + "\n" + "Tentative delivery date is " + idate + "\n"
	"Thanks for choosing us." + "\n" + "Live MART")

	return redirect(url_for('resthome1'))

# ////////////////////////////////

@app.route('/wsadddelivery',methods = ['GET','POST'])
def wsadddelivery():
	if not session.get('wmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		ohash = request.args.get("ohash")
		cid = request.args.get("cid")
		iname = request.args.get("iname")
		inumber = request.args.get("inumber")
		idate = request.args.get("idate")
	
	elif request.method == "POST":
		ohash = request.form['ohash']
		cid = request.form['cid']
		iname = request.form['iname']
		inumber = request.form['inumber']
		idate = request.form['idate']

	orders=Wsorders.query.filter(Wsorders.wohash==ohash).first()
	orders.winame=iname
	orders.winumber=inumber
	orders.widate=idate
	db.session.commit()

	customer=Restadmin.query.filter(Restadmin.rid==cid).first()

	mail.send_message("Details of Order No. " + ohash, 
	sender = "lakshaytomar4@gmail.com", 
	recipients=[customer.rmail],
	body = "Your order will be delivered by " + iname + "\n" +
	"Mobile Number: " + inumber + "\n" + "Tentative delivery date is " + idate + "\n"
	"Thanks for choosing us." + "\n" + "Lakshay" + "\n" + "Live MART")

	return redirect(url_for('wshome1'))

@app.route('/restacceptedorders',methods=['GET','POST'])
def restacceptedorders():
	if not session.get('rmail'):
		return redirect(request.url_root)
	rmail=session['rmail']
	restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	rid=restadmin.rid
	myorders = Orders.query.filter(and_(Orders.rid == rid, Orders.ostatus=='Order Delivered'))
	restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()

	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)
	
	return render_template('restacceptedorders.html',rusname=restadmin.rname,restadmin = Restadmin.query.all(), myorders=myorders)


@app.route('/restacceptedordersoffline',methods=['GET','POST'])
def restacceptedordersoffline():
	if not session.get('rmail'):
		return redirect(request.url_root)
	rmail=session['rmail']
	restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	rid=restadmin.rid
	myorders = Orders.query.filter(and_(Orders.rid == rid, Orders.odate != None))
	restadmin  = Restadmin.query.filter(Restadmin.rmail == rmail).first()

	# mycustomer=Customer.query.filter(Customer.cid==myorders.cid)
	
	return render_template('restacceptedordersoffline.html',rusname=restadmin.rname,restadmin = Restadmin.query.all(), myorders=myorders)


# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

@app.route('/showmyrestmenu',methods=['GET','POST'])
def showmyrestmenu():
	if not session.get('rmail'):
		return redirect(request.url_root)
	rmail=session['rmail']
	restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	restid=restad.rid
	items = Items.query.filter(Items.rid == restid).all()


	return render_template('showmymenu.html',restad=restad, restadmin=items)

@app.route('/showmywsmenu',methods=['GET','POST'])
def showmywsmenu():
	if not session.get('wmail'):
		return redirect(request.url_root)
	rmail=session['wmail']
	restad  = Ws.query.filter(Ws.wmail == rmail).first()
	restid=restad.wid
	items = Wsitems.query.filter(Wsitems.wid == restid).all()
	print(items)

	return render_template('showmywsmenu.html',restad=restad, restadmin=items)

@app.route('/additem')
def additem():
	
	if not session.get('rmail'):
		return redirect(request.url_root)
	return render_template('additem.html')

@app.route('/wsadditem')
def wsadditem():
	
	if not session.get('wmail'):
		return redirect(request.url_root)
	return render_template('wsadditem.html')


@app.route('/additemNext',methods = ['GET','POST'])
def additemNext():

	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		# iid = request.args.get("iid")
		iname = request.args.get("iname")
		iprice = request.args.get("iprice")
		category= request.args.get("category")
		# rid = request.args.get("rid")
	
	elif request.method == "POST":
		# iid = request.form['iid']
		iname = request.form['iname']
		iprice = request.form['iprice']
		category = request.form['category']
		# rid = request.form['rid']

	
	rmail=session['rmail']
	restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	restid=restad.rid

	items = Items(iname=request.form["iname"], iprice=request.form["iprice"], category=request.form["category"], rid=restid)
	db.session.add(items)
	db.session.commit()
	
	return redirect(url_for('showmyrestmenu'))

@app.route('/wsadditemNext',methods = ['GET','POST'])
def wsadditemNext():
	if not session.get('wmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		# iid = request.args.get("iid")
		iname = request.args.get("winame")
		iprice = request.args.get("wiprice")
		wicategory= request.args.get("wcategory")
		# rid = request.args.get("rid")
	
	elif request.method == "POST":
		# iid = request.form['iid']
		winame = request.form['iname']
		wiprice = request.form['iprice']
		wicategory = request.form['category']
		# rid = request.form['rid']

	
	rmail=session['wmail']
	restad  = Ws.query.filter(Ws.wmail == rmail).first()
	restid=restad.wid

	items = Wsitems(winame=request.form["iname"], wiprice=request.form["iprice"], wicategory=request.form["category"], wid=restid)
	db.session.add(items)
	db.session.commit()
	
	return redirect(url_for('showmywsmenu'))


@app.route('/updateitem',methods = ['GET','POST'])
def updateitem():
	if not session.get('rmail'):
		return redirect(request.url_root)
	return render_template('updateitem.html')


@app.route('/updateitemNext',methods = ['GET','POST'])
def updateitemNext():
	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		iid = request.args.get("iid")
		iname = request.args.get("iname")
		iprice = request.args.get("iprice")
	
	elif request.method == "POST":
		iid = request.form['iid']
		iname = request.form['iname']
		iprice = request.form['iprice']

	
	rmail=session['rmail']
	restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	restid=restad.rid

	item = Items.query.filter(and_(Items.iid ==iid,Items.rid==restid)).first()
	if item :
		item.iname=iname
		item.iprice=iprice

		db.session.commit()
		return redirect(url_for('showmyrestmenu'))
	else :
		# return redirect(url_for('updateitem'))		
		return render_template('updateitem.html',imsg="Error! Item id does not belong to you..! ")



@app.route('/deleteitem',methods = ['GET','POST'])
def deleteitem():
	if not session.get('rmail'):
		return redirect(request.url_root)
	return render_template('removeitem.html')	

@app.route('/wsdeleteitem',methods = ['GET','POST'])
def wsdeleteitem():
	if not session.get('wmail'):
		return redirect(request.url_root)
	return render_template('wsremoveitem.html')


@app.route('/deleteitemNext',methods = ['GET','POST'])
def deleteitemNext():
	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		iid = request.args.get("iid")
	
	elif request.method == "POST":
		iid = request.form['iid']
	
	rmail=session['rmail']
	restad  = Restadmin.query.filter(Restadmin.rmail == rmail).first()
	restid=restad.rid

	item = Items.query.filter(and_(Items.iid ==iid,Items.rid==restid)).first()
	if item :
		
		db.session.delete(item)
		db.session.commit()
		return redirect(url_for('showmyrestmenu'))
	else :
		# return redirect(url_for('updateitem'))
		return render_template('removeitem.html',imsg="Error! Item id does not belong to you..! ")

@app.route('/wsdeleteitemNext',methods = ['GET','POST'])
def wsdeleteitemNext():
	if not session.get('wmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		iid = request.args.get("iid")
	
	elif request.method == "POST":
		iid = request.form['iid']
	
	rmail=session['wmail']
	restad  = Ws.query.filter(Ws.wmail == rmail).first()
	restid=restad.wid
	item = Wsitems.query.filter(and_(Wsitems.wiid ==iid,Wsitems.wid==restid)).first()
	if item :
		
		db.session.delete(item)
		db.session.commit()
		return redirect(url_for('showmywsmenu'))
	else :
		# return redirect(url_for('updateitem'))
		return render_template('wsremoveitem.html',imsg="Error! Item id does not belong to you..! ")

@app.route('/showrestprofile', methods = ['GET','POST'])
def showrestprofile():
	if not session.get('rmail'):
		return redirect(request.url_root)
	
	rmail=session['rmail']

	restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
	# customer.cpassword=cpassword
	# db.session.commit()
	return render_template('showrestprofile.html',resinfo = restadmin)		


@app.route('/updaterestprofile',methods = ['GET','POST'])
def updaterestprofile():
	if not session.get('rmail'):
		return redirect(request.url_root)
	return render_template('updaterestprofile.html')


@app.route('/updaterestprofileNext', methods = ['GET','POST'])
def updaterestprofileNext():
	if not session.get('rmail'):
		return redirect(request.url_root)
	
	rmail=session['rmail']

	rpassword = request.form['rpassword']
	
	restadmin=Restadmin.query.filter(Restadmin.rmail==rmail).first()
	restadmin.rpassword=rpassword
	db.session.commit()
	return render_template('updaterestprofile.html', rmsg="Passsword Updated Succcessfully...!")



@app.route('/restlogout')
def restlogout():
	# Remove the session variable if present
	session.pop('rmail',None)
	return redirect(url_for('index'))

@app.route('/wslogout')
def wslogout():
	# Remove the session variable if present
	session.pop('wmail',None)
	return redirect(url_for('index'))


@app.route('/paymentOnline', methods = ['GET','POST'])
def paymentOnline():
	if not session.get('cmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("total")
		items = request.args.get("items")
		rid=request.args.get("restid")
		
	
	elif request.method == "POST":
		tprice=request.form['total']
		items=request.form["items"]
		rid=request.form['restid']

	#//////////////////////////////////////////////////////////////////////////////////////// 
	if(tprice=="0"):
	# return (str(tprice=="0"))
		return render_template('errorzero.html')	
		# return redirect(url_for('restmenu'))
		#////////////////////////////////////////////////////////////////////////////////////

	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()
	# cusid=Customer.cid

	restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
	rname=restadmin.rname

	ostatus="Order Placed"

	return render_template('paymentOnline.html', tprice=tprice, rname=rname ,items=items, rid=rid)

@app.route('/restpaymentOnline', methods = ['GET','POST'])
def restpaymentOnline():
	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("total")
		items = request.args.get("items")
		rid=request.args.get("restid")
		
	
	elif request.method == "POST":
		tprice=request.form['total']
		items=request.form["items"]
		rid=request.form['restid']

	#//////////////////////////////////////////////////////////////////////////////////////// 
	if(tprice=="0"):
	# return (str(tprice=="0"))
		return render_template('errorzero.html')	
		# return redirect(url_for('restmenu'))
		#////////////////////////////////////////////////////////////////////////////////////

	cmail=session['rmail']
	customer  = Restadmin.query.filter(Restadmin.rmail == cmail).first()
	# cusid=Customer.cid

	restadmin  = Ws.query.filter(Ws.wid == rid).first()
	rname=restadmin.wname

	ostatus="Order Placed"

	return render_template('restpaymentOnline.html', tprice=tprice, rname=rname ,items=items, rid=rid)

@app.route('/paymentOffline', methods = ['GET','POST'])
def paymentOffline():
	if not session.get('cmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("total")
		items = request.args.get("items")
		rid=request.args.get("restid")
		
	
	elif request.method == "POST":
		tprice=request.form['total']
		items=request.form["items"]
		rid=request.form['restid']

	#//////////////////////////////////////////////////////////////////////////////////////// 
	if(tprice=="0"):
	# return (str(tprice=="0"))
		return render_template('errorzero.html')	
		# return redirect(url_for('restmenu'))
		#////////////////////////////////////////////////////////////////////////////////////

	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()
	# cusid=Customer.cid

	restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
	rname=restadmin.rname

	ostatus="Order Placed"

	return render_template('paymentOffline.html', tprice=tprice, rname=rname ,items=items, rid=rid)

@app.route('/restpaymentOffline', methods = ['GET','POST'])
def restpaymentOffline():
	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("total")
		items = request.args.get("items")
		rid=request.args.get("restid")
		
	
	elif request.method == "POST":
		tprice=request.form['total']
		items=request.form["items"]
		rid=request.form['restid']
	print(rid)
	#//////////////////////////////////////////////////////////////////////////////////////// 
	if(tprice=="0"):
	# return (str(tprice=="0"))
		return render_template('errorzero.html')	
		# return redirect(url_for('restmenu'))
		#////////////////////////////////////////////////////////////////////////////////////

	cmail=session['rmail']
	customer  = Restadmin.query.filter(Restadmin.rmail == cmail).first()
	# cusid=Customer.cid

	restadmin  = Ws.query.filter(Ws.wid == rid).first()
	rname=restadmin.wname

	ostatus="Order Placed"

	return render_template('restpaymentOffline.html', tprice=tprice, rname=rname ,items=items, rid=rid)

@app.route('/submitorder', methods = ['GET','POST'])
def submitorder():
	if not session.get('cmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("tprice")
		items = request.args.get("items")
		rid=request.args.get("rid")
		
	
	elif request.method == "POST":
		tprice=request.form['tprice']
		items=request.form["items"]
		rid=request.form['rid']
		

	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()

	restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
	rid=restadmin.rid

	ostatus="Order Placed"

	

	
	orders = Orders(cid=customer.cid, rid=rid, items=items,tprice=tprice,ostatus=ostatus)
	if orders :

		db.session.add(orders)
		db.session.commit()

		# return redirect(url_for('userorders'))
		return render_template('lastpage.html')


	return render_template('paymentOnline.html')


@app.route('/submitorderOffline', methods = ['GET','POST'])
def submitorderOffline():
	if not session.get('cmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("tprice")
		items = request.args.get("items")
		rid=request.args.get("rid")
		odate=request.args.get("odate")
		otime=request.args.get("otime")
		
	
	elif request.method == "POST":
		tprice=request.form['tprice']
		items=request.form["items"]
		rid=request.form['rid']
		odate=request.form['odate']
		otime=request.form['otime']
		

	cmail=session['cmail']
	customer  = Customer.query.filter(Customer.cmail == cmail).first()

	restadmin  = Restadmin.query.filter(Restadmin.rid == rid).first()
	rid=restadmin.rid

	ostatus="Order Placed"

	

	
	orders = Orders(cid=customer.cid, rid=rid, items=items,tprice=tprice,ostatus=ostatus,odate=odate,otime=otime)
	if orders :

		db.session.add(orders)
		db.session.commit()

		# return redirect(url_for('userorders'))
		return render_template('lastpage.html')


	return render_template('paymentOffline.html')



@app.route('/restsubmitorder', methods = ['GET','POST'])
def restsubmitorder():
	if not session.get('rmail'):
		return redirect(request.url_root)
	if request.method == "GET":
		tprice = request.args.get("tprice")
		items = request.args.get("items")
		rid=request.args.get("rid")
		
	
	elif request.method == "POST":
		tprice=request.form['tprice']
		items=request.form["items"]
		rid=request.form['rid']
		

	cmail=session['rmail']
	customer  = Restadmin.query.filter(Restadmin.rmail == cmail).first()

	restadmin  = Ws.query.filter(Ws.wid == rid).first()
	rid=restadmin.wid

	ostatus="Order Placed"

	

	
	orders = Wsorders(rid=customer.rid, wid=rid, witems=items,wtprice=tprice,wostatus=ostatus)
	if orders :

		db.session.add(orders)
		db.session.commit()

		# return redirect(url_for('userorders'))
		return render_template('restlastpage.html')


	return render_template('restpaymentOnline.html')



# Admin login
@app.route('/adminlogin')
def adminlogin():

	return render_template('adminlogin.html')

@app.route('/adminsignup')
def adminsignup():
	return render_template('adminsignup.html')

@app.route('/adminregister',methods = ['GET','POST'])
def adminregister():
	if not session.get('amail'):
		return render_template('index.html',admmsg="Only Logged in Admins can Register New Admins")	
		#return redirect(request.url_root,admmsg="Only Logged in Admins can Register New Admins")	
	if request.method == "GET":
		amail = request.args.get("amail")

	elif request.method == "POST":
		amail = request.form['amail']

	
	# restadmin=Restadmin.query.all()

	Admin = admin.query.filter(or_(admin.amail == amail)).first()

	if Admin:
		# return redirect(url_for('adminHome1'))
		print("registration failed")		
		return render_template('adminhome.html', admsg="Admin Already Registered...!")

	else:
		newadmin = admin(amail=request.form["amail"], apassword=request.form['apassword'])
	
		db.session.add(newadmin)
		db.session.commit()

		# return redirect(url_for('adminHome1'))	
		print("admin registered successfully")
		return render_template('adminlogin.html', ssmsg="Admin Registered Succcessfully...!")

@app.route('/adminloginNext',methods=['GET','POST'])
def adminloginNext():
	
	if request.method == "GET":
		amail = request.args.get("amail")
		apassword = request.args.get("apassword")

	elif request.method == "POST":
		amail = request.form['amail']
		apassword = request.form['apassword']


		Admin  = admin.query.filter(and_(admin.amail == amail, admin.apassword == apassword)).first()


		if Admin :
			session['amail'] = request.form['amail']
			return redirect(url_for('adminHome1'))

		return render_template('adminlogin.html',admmsg="Login failed...\n Please enter valid username and password!")



@app.route('/adminHome1',methods=['GET','POST'])
def adminHome1():
	if not session.get('amail'):
		return redirect(request.url_root)
	amail=session['amail']
	Admin  = admin.query.filter(admin.amail == amail).first()

	return render_template('adminhome.html')
	# return ("login success")

@app.route('/restregisterbyadmin', methods = ['GET','POST'])
def restregisterbyadmin():
	if not session.get('amail'):
		return redirect(request.url_root)	
	if request.method == "GET":
		rmail = request.args.get("rmail")
		rmobile = request.args.get("rmobile")

	elif request.method == "POST":
		rmail = request.form['rmail']
		rmobile = request.form['rmobile']

	
	# restadmin=Restadmin.query.all()

	restadmin = Restadmin.query.filter(or_(Restadmin.rmail == rmail, Restadmin.rmobile == rmobile)).first()

	if restadmin:
		# return redirect(url_for('adminHome1'))		
		return render_template('adminhome.html', admsg="Restaurant Already Registered...!")

	else:
		newrest = Restadmin(rname=request.form["rname"], rmail=request.form["rmail"], rmobile=request.form["rmobile"], raddress=request.form["raddress"], rpassword=request.form['rpassword'])
	
		db.session.add(newrest)
		db.session.commit()

		# return redirect(url_for('adminHome1'))	
		return render_template('adminhome.html', ssmsg="Restaurant Registered Succcessfully...!")


@app.route('/adminshowrest')
def adminshowrest():
	if not session.get('amail'):
		return redirect(request.url_root)	
	# items = admin(amail='admin@gmail.com', apassword='admin123')
	
	# db.session.add(items)
	# db.session.commit()
	return render_template('adminshowrest.html',restadmin = Restadmin.query.all())


@app.route('/adminrestmenu', methods = ['GET','POST'])
def adminrestmenu():
	if not session.get('amail'):
		return redirect(request.url_root)

	if request.method == "GET":
		restid = request.args.get("restid")
	
	elif request.method == "POST":
		restid = request.form['restid']

	items = Items.query.filter(Items.rid == restid).all()
	restad = Restadmin.query.filter(Restadmin.rid == restid).first()
	return render_template('adminrestmenu.html',restad=restad, restadmin=items)	


@app.route('/adminlogout')
def adminlogout():
	# Remove the session variable if present
	session.pop('amail',None)
	return redirect(url_for('index'))	


