from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField,DateField,IntegerField,form
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired,Email,Length,EqualTo,ValidationError

bed_list=[' General ward', 'semi sharing', 'single room']
state_list=[' Maharashtra ', 'Karnataka', 'TamilNadu']
city_list=['Mumbai','Nagpur','Pune','Belgaon','Banglore','Hubali','Chennai','Madurai','Salem']

class Create_patient(FlaskForm):
     pat_ssn_id = StringField("Patient SSN ID:", validators=[DataRequired()])
     pat_name = StringField("Patient Name", validators=[DataRequired()])
     pat_age = IntegerField("Patient Age", validators=[DataRequired()])
     date_of_amdn = DateField("Date of Admission",format='%Y-%m-%d')
     bed_type = SelectField(label='Type of Bed', choices=[(bed,bed) for bed in bed_list]) 
     address = StringField("Address", validators=[DataRequired()])
     state = SelectField("State", choices=[(state,state) for state in state_list])
     city = SelectField("City", choices=[(city,city) for city in city_list])
     submit = SubmitField("SUBMIT")
     reset = SubmitField("RESET")

class Update_patient(FlaskForm):
     pat_name = StringField("Patient Name")
     pat_age = IntegerField("Patient Age" )
     date_of_amdn = DateField("Date of Admission",format='%Y-%m-%d')
     bed_type = SelectField(label='Type of Bed',choices=[(row,row) for row in bed_list]) 
     address = StringField("Address")
     state = SelectField("State",choices=[(row,row) for row in state_list])
     city = SelectField("City",choices=[(row,row) for row in city_list])
     submit=SubmitField("SUBMIT")
     


class Get_id(FlaskForm):
     pat_id=IntegerField("Patient ID",validators=[DataRequired()])
     get=SubmitField("Get")

class Search_patient(FlaskForm):
     pat_ssn_id=IntegerField("SSN ID",validators=[DataRequired()])
     pat_name = StringField("Patient Name")
     pat_age = StringField("Patient Age" )
     date_of_amdn = DateField("Date of Admission")
     bed_type = StringField('Type of Bed') 
     address = StringField("Address")
     state = StringField("State")
     city = StringField("City")


class Delete_patient(FlaskForm):
     pat_name = StringField("Patient Name")
     pat_age = StringField("Patient Age" )
     date_of_amdn = StringField("Date of Admission")
     bed_type = StringField('Type of Bed') 
     address = StringField("Address")
     state = StringField("State")
     city = StringField("City")
     submit=SubmitField("Delete")

class Medicine_issued(FlaskForm):
     ssn_id=StringField("SSN ID",validators=[DataRequired()])
     medicine=SelectField("Medicine")
     quantity=StringField("Quantity",validators=[DataRequired()])
     submit=SubmitField("Submit")

class Add_Medicine(FlaskForm):
     med_id=StringField("Medicine Id",validators=[DataRequired()])
     med_name=StringField("medicine Name",validators=[DataRequired()])
     quantity=StringField("Quantity",validators=[DataRequired()])
     rate=StringField("Rate",validators=[DataRequired()])
     submit=SubmitField("Submit")