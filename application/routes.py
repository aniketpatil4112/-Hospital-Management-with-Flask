from application import app,mysql
from flask import render_template,request,json,Response,redirect,flash,url_for,session,jsonify
from flask_restx import Resource
from application.form import Create_patient,Update_patient,Get_id,Search_patient,Delete_patient,Add_Medicine,Medicine_issued
from application.form import state_list,bed_list,city_list
import MySQLdb.cursors



@app.route('/')
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM userstore WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        user = cursor.fetchone()
        # If account exists in userstore table in out database
        if user:
            # Create session data, we can access this data in other routes
            conn = mysql.connection
            cursor.execute('''UPDATE userstore SET timestamp = now()''')
            conn.commit()
            session['loggedin'] = True
            session['username'] = user['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/diagnostics',methods=['GET', 'POST'])
def diagnostics():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT testname, charge from diagnosticsmaster''')
    test1 = cursor.fetchall()
    if request.method == 'POST' and 'testname' in request.form and 'charge' in request.form:
            testname = request.form['testname']
            charge = request.form['charge']
            conn = mysql.connection
            cursor.execute('insert into diagnosticsmaster (testname,charge) values (%s,%s)', (testname, charge,))
            conn.commit()
            cursor.execute('''SELECT testname, charge from diagnosticsmaster''')
            test1 = cursor.fetchall()
            return render_template('diagnostics.html', msg = "Test Successfully added ",test1 = test1)
    return render_template('diagnostics.html',test1 = test1)

@app.route('/search', methods=['GET', 'POST'])
def search():
    #id = session.get('id')
        
    if request.method == 'POST' and 'testconduct' in request.form:
        conn = mysql.connection
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        testconduct = request.form['testconduct']
        
        cursor.execute('''SELECT patientID FROM patients  WHERE patientID = %s''',[session.get('id')])
        result=cursor.fetchone()
        #patientid=int(result[0])
        cursor.execute('''SELECT testID FROM diagnosticsmaster  WHERE testname = %s''', [testconduct])
        result1 = cursor.fetchone()
        #testId=int(result[0])                                  
        cursor.execute('''insert into testconducted (patientID,testID) values (%s,%s)''', (result["patientID"], result1["testID"],))
        conn.commit()
        cursor.execute('''SELECT patientID,name,age,address,admitdate,bedtype FROM patients  WHERE patientID = %s''', [session.get('id')])
        patient = cursor.fetchall()
        cursor.execute('''SELECT diagnosticsmaster.testname as name, diagnosticsmaster.charge as charge
FROM diagnosticsmaster
INNER JOIN testconducted
ON diagnosticsmaster.testID=testconducted.testID WHERE testconducted.patientID = %s''', [session.get('id')])
        test = cursor.fetchall()
        cursor.execute('''SELECT testname, charge from diagnosticsmaster''')
        test1 = cursor.fetchall()
        cursor.execute('''SELECT testname from diagnosticsmaster''')
        test2 = cursor.fetchall()
        return render_template('diagnostics.html', patient = patient ,test = test,test1 = test1, test2 = test2)



    if request.method == 'POST':
        id = request.form.get('search1', type=int)
        session['id'] = id
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('''SELECT patientID,name,age,address,admitdate,bedtype FROM patients  WHERE patientID = %s''', [id])
        patient = cursor.fetchall()
        cursor.execute('''SELECT diagnosticsmaster.testname as name, diagnosticsmaster.charge as charge
FROM diagnosticsmaster
INNER JOIN testconducted
ON diagnosticsmaster.testID=testconducted.testID WHERE testconducted.patientID = %s''', [id])
        test = cursor.fetchall()
        cursor.execute('''SELECT testname, charge from diagnosticsmaster''')
        test1 = cursor.fetchall()
        cursor.execute('''SELECT testname from diagnosticsmaster''')
        test2 = cursor.fetchall()
        return render_template('diagnostics.html', patient = patient ,test = test,test1 = test1,test2 = test2)
    else:
        return redirect(url_for('diagnostics'))






@app.route('/pharmacist',methods=['GET', 'POST'])
def pharmacist():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''SELECT medicinename, quantity,rate from medicinemaster''')
    test1 = cursor.fetchall()
    if request.method == 'POST' and 'medicine' in request.form and 'quantity' in request.form and 'rate' in request.form:
            medicine    = request.form['medicine']
            quantity    = request.form['quantity']
            rate        = request.form['rate']
            conn = mysql.connection
            cursor.execute('insert into medicinemaster (medicinename,quantity,rate) values (%s,%s,%s)', (medicine, int(quantity),int(rate),))
            conn.commit()
            # a=0
            # cursor.execute('''delete * from medicinemaster where quantity = %s ''',a)
            # conn.commit()
            cursor.execute('''SELECT medicinename, quantity,rate from medicinemaster''')
            test1 = cursor.fetchall()
            return render_template('pharmacist.html', msg = "Medicine Successfully added ",test1 = test1)
    return render_template('pharmacist.html',test1 = test1)

@app.route('/search2', methods=['GET', 'POST'])
def search2():
    if request.method == 'POST' and 'medicineissue' in request.form:
            conn = mysql.connection
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
            medicineissue = request.form['medicineissue']
            
            cursor.execute('''SELECT patientID FROM patients  WHERE patientID = %s''',[session.get('mid')])
            result=cursor.fetchone()
            #patientid=int(result[0])
            cursor.execute('''SELECT medicineID FROM medicinemaster  WHERE medicinename = %s''', [medicineissue])
            result1 = cursor.fetchone()
            #testId=int(result[0]) 

            issuequatity = int(request.form['issuequatity'])                         
            cursor.execute('''select quantity from medicinemaster where medicinename=%s''',[medicineissue])
            quantity =  cursor.fetchone() 
            if issuequatity > quantity["quantity"]:
                msg="Quantity not available"
                cursor.execute('''SELECT patientID,name,age,address,admitdate,bedtype FROM patients  WHERE patientID = %s''', [session.get('mid')])
                patient = cursor.fetchall()
                cursor.execute('''SELECT medicinemaster.medicinename as name, medicine_issued.quantity as quantity, medicinemaster.rate as rate
                FROM medicinemaster
                INNER JOIN medicine_issued
                ON medicinemaster.medicineID = medicine_issued.medicineID WHERE medicine_issued.patientID = %s''', [session.get('mid')])
                test = cursor.fetchall()
                cursor.execute('''SELECT medicinename, quantity,rate from medicinemaster''')
                test1 = cursor.fetchall()
                cursor.execute('''SELECT medicinename from medicinemaster''')
                test2 = cursor.fetchall()
                return render_template('pharmacist.html',msg = msg, patient = patient ,test = test,test1 = test1, test2 = test2)

            cursor.execute('''insert into medicine_issued (patientID,medicineID,quantity) values (%s,%s,%s)''', (result["patientID"], result1["medicineID"],issuequatity,))
            conn.commit()
            cursor.execute('''SELECT medicineID,quantity FROM medicinemaster  WHERE medicinename = %s''', [medicineissue])
            result1 = cursor.fetchone()
            cursor.execute('''UPDATE medicinemaster SET quantity = %s where medicineID=%s''',(result1["quantity"]-issuequatity,result1["medicineID"]))
            conn.commit()
            cursor.execute('''SELECT patientID,name,age,address,admitdate,bedtype FROM patients  WHERE patientID = %s''', [session.get('mid')])
            patient = cursor.fetchall()
            cursor.execute('''SELECT medicinemaster.medicinename as name, medicine_issued.quantity as quantity, medicinemaster.rate as rate
            FROM medicinemaster
            INNER JOIN medicine_issued
            ON medicinemaster.medicineID = medicine_issued.medicineID WHERE medicine_issued.patientID = %s''', [session.get('mid')])
            test = cursor.fetchall()
            
            cursor.execute('''SELECT medicinename, quantity,rate from medicinemaster''')
            test1 = cursor.fetchall()
            cursor.execute('''SELECT medicinename from medicinemaster''')
            test2 = cursor.fetchall()
            msg= "Medicine Issued to Patient "
            return render_template('pharmacist.html',msg = "msg", patient = patient ,test = test,test1 = test1, test2 = test2)


    if request.method == 'POST'and 'search2' in request.form:
                id = request.form.get('search2', type=int)
                session['mid'] = id
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
                cursor.execute('''SELECT patientID,name,age,address,admitdate,bedtype FROM patients  WHERE patientID = %s''', [id])
                patient = cursor.fetchall()
                cursor.execute('''SELECT medicinemaster.medicinename as name, medicine_issued.quantity as quantity, medicinemaster.rate as rate
                FROM medicinemaster
                INNER JOIN medicine_issued
                ON medicinemaster.medicineID = medicine_issued.medicineID WHERE medicine_issued.patientID = %s''', [id])
                test = cursor.fetchall()
                cursor.execute('''SELECT medicinename, quantity,rate from medicinemaster''')
                test1 = cursor.fetchall()
                
                cursor.execute('''SELECT medicinename from medicinemaster''')
                test2 = cursor.fetchall()
                return render_template('pharmacist.html', patient = patient ,test = test,test1 = test1,test2 = test2)
    else:
                return redirect(url_for('pharmacist'))


@app.route("/create_patient",methods=['GET','POST'])
def create_patient():
    form=Create_patient()
    if form.validate_on_submit():
        ssn=request.form["pat_ssn_id"]
        name=request.form["pat_name"]
        age=request.form["pat_age"]
        date=request.form["date_of_amdn"]
        type_bed=request.form["bed_type"]
        address=request.form["address"]
        state=request.form["state"]
        city=request.form["city"]
        if(len(ssn)==9):
            conn = mysql.connection
            cursor =conn.cursor()
            print (ssn,name,age,date,type_bed,address,state,city)
            
            cursor.execute(""" select patientID from patients where patientID=%s""",[int(ssn)])
            ssn_id=cursor.fetchone()
            if(ssn_id==None):
                cursor.execute(""" select max(patientID) from patients """)
                ids=cursor.fetchone()
            
                cursor.execute("""insert into patients(SSNID,name ,age ,admitdate ,bedtype ,Address ,state ,city ) values(%s,%s,%s,%s,%s,%s,%s,%s)""",([int(ssn)],name,age,date,type_bed,address,state,city))
                conn.commit()
                
                return render_template("create_patient.html" ,form=form,msg="Patient creation initiated sucessfully.")
            else:
                return render_template("create_patient.html" ,form=form,msg="SSN ID already exists.")

        else:
                return render_template("create_patient.html" ,form=form,msg="SSN ID must be 9 digit.")
    return render_template("create_patient.html" ,form=form,msg="")


@app.route("/update_patient",methods=['GET','POST'])
def update_patient():
    
    id_form=Get_id()
    form=Update_patient()
    p_id=None
    #record=None
    if id_form.pat_id.validate(id_form):
        p_id=request.form["pat_id"]    
        conn = mysql.connection
        cursor =conn.cursor()
        cursor.execute(""" select * from patients where patientID=%s """,[p_id])
        record=cursor.fetchone()
        print(record)
        if(record!=None):
            session['record']=record
            session['p_id']=[p_id]
        
            form.bed_type.default=record[4]
            form.process()
        
            form.state.default=record[6]
            form.process()
        
            form.city.default=record[7]
            form.process()
            
            return render_template("update_patient.html",id_form=id_form,form=form,get=True,row=record,p_id=[p_id],msg="")

        else:
            return render_template("update_patient.html",id_form=id_form,form=form,get=True,row=record,p_id=[p_id],msg="Patient not found")
    if form.validate_on_submit():
        conn=mysql.connection
        cursor=conn.cursor()
        pat_id=session['p_id']
        cursor.execute(""" update patients set name=%s where patientID=%s """,(request.form["pat_name"],[p_id]))
        conn.commit()

        cursor.execute(""" update patients set age=%s where patientID=%s """,(request.form["pat_age"],[p_id]))
        conn.commit()

        cursor.execute(""" update patients set admitdate=%s where patientID=%s """,(request.form["date_of_amdn"],[p_id]))
        conn.commit()

        cursor.execute(""" update patients set bedtype=%s where patientID=%s """,(request.form["bed_type"],[p_id]))
        conn.commit()

        cursor.execute(""" update patients set Address=%s where patientID=%s """,(request.form["address"],[p_id]))
        conn.commit()

        cursor.execute(""" update patients set state=%s where patientID=%s """,(request.form["state"],[p_id]))
        conn.commit()

        cursor.execute(""" update patients set city=%s where patientID=%s """,(request.form["city"],[p_id]))
        conn.commit()
       
        
        cursor.execute(""" select * from patients where patientID=%s """,([p_id]))
        record=cursor.fetchone()
    
        return render_template("update_patient.html",id_form=id_form,form=form,get=True,row=record,p_id=[p_id],msg="Patient update initiated successfully")
    return render_template("update_patient.html",id_form=id_form,form=form,get=False,row=None,p_id="",msg="")



@app.route("/search_patient",methods=['GET','POST'])
def search_patient():
    id_form=Get_id()
    form=Search_patient()
    pat_id=None
    #record=None
    if id_form.pat_id.validate(id_form):
        pat_id=int(request.form["pat_id"])     
        conn = mysql.connection
        cursor =conn.cursor()    
        cursor.execute(""" select * from patients where patientID=%s """,([pat_id]))
        record=cursor.fetchall()
        print(record)
        if(record==None):
            return render_template("search_patient.html",id_form=id_form,form=form,get=True,record=record,p_id=pat_id,msg="Patient not found.")    
        
        return render_template("search_patient.html",id_form=id_form,form=form,get=True,record=record,p_id=pat_id,msg="Patient found.")
    return render_template("search_patient.html",id_form=id_form,form=form,get=False,record=None,p_id="",msg="")


@app.route("/view_pat")
def view_pat():
    conn = mysql.connection
    cursor =conn.cursor()   
    cursor.execute(""" select patientID,name,age,admitdate,CONCAT(Address,' ',City,' ',State) as addr,bedtype from patients""")
    record=cursor.fetchall()
    return render_template("view_patient.html",record=record)


@app.route("/delete_pat",methods=['GET','POST'])
def delete_pat():
    id_form=Get_id()
    delete_pat=Delete_patient()
    record=None
    if id_form.pat_id.validate(id_form):
            
            pat_id=int(request.form["pat_id"])
            session['pat_id']=[pat_id]
            conn = mysql.connection
            cursor =conn.cursor()  
            cursor.execute(""" select * from patients where patientID=%s """,([pat_id]))
            record=cursor.fetchone()
            
            if(record!=None):
                session['record']=record
                return render_template("delete_patient.html",get=True,id_form=id_form,form=delete_pat,row=record,msg="")
            else:
                return render_template("delete_patient.html",get=True,id_form=id_form,form=delete_pat,row=record,msg="Patient not found")
    if delete_pat.validate_on_submit():
            [pat_id]=session['pat_id']
            conn = mysql.connection
            cursor =conn.cursor()  
            cursor.execute(""" delete from patients where patientID=%s """,([pat_id]))
            conn.commit()
            session['record']=record 
            return render_template("delete_patient.html",get=True,id_form=id_form,form=delete_pat,row=record,msg="Patient deletion initiated successfully")
    return render_template("delete_patient.html",get=False,id_form=id_form,form=delete_pat,row=record,msg="")

@app.route("/bill",methods=['GET','POST'])
def bill():
    if request.method == 'POST'and 'search3' in request.form:
        id = request.form.get('search3', type=int)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) 
        cursor.execute('''SELECT patientID,name,age,address,admitdate,bedtype FROM patients  WHERE patientID = %s''', [id])
        patient = cursor.fetchall()
        cursor.execute('''SELECT medicinemaster.medicinename as name, medicine_issued.quantity as quantity, medicinemaster.rate as rate
        FROM medicinemaster
        INNER JOIN medicine_issued
        ON medicinemaster.medicineID = medicine_issued.medicineID WHERE medicine_issued.patientID = %s''', [id])
        test = cursor.fetchall()
        sum=0
        for data in test:
            add=data['quantity'] * data['rate']
            sum=sum+add
        medicine = sum
        cursor.execute('''SELECT diagnosticsmaster.testname as name, diagnosticsmaster.charge as charge
        FROM diagnosticsmaster
        INNER JOIN testconducted
        ON diagnosticsmaster.testID=testconducted.testID WHERE testconducted.patientID = %s''', [session.get('id')])
        test1 = cursor.fetchall()
        sum = 0
        for data in test1:
            add=data['charge'] 
            sum=sum+add
        diagnostics = sum
        bed_list=[' General ward', 'semi sharing', 'single room']
        cursor.execute('''SELECT admitdate,bedtype FROM patients  WHERE patientID = %s''', [id])
        livingbill = cursor.fetchone()
        print(livingbill)
        cursor.execute('''select datediff(curdate(),%s) as day''',(livingbill["admitdate"],))
        days= cursor.fetchone()
        print(days)
        if livingbill['bedtype']=="General ward":
            roombill=days['day'] * 2000
        if livingbill['bedtype']=="semi sharing":
            roombill=days['day'] * 4000
        if livingbill['bedtype']=="single room":
            roombill=days['day'] * 8000
        total = medicine + diagnostics + roombill
        return render_template('bill.html',patient = patient ,test = test,test1 = test1,total = total, medicine=medicine,diagnostics= diagnostics,roombill = roombill)
    return render_template('bill.html')
       

       