from flask_wtf import FlaskForm
import wtforms
#from wtforms import StringField, TextField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class InputData(FlaskForm):
    """ INPUTS: u
    user type, location, household size, 
    monthly energy used, desired percentage renewable """ 

    user_type = wtforms.SelectField("User Type: ", choices=[("Government","Government"),("Resident","Resident")])
    location = wtforms.StringField("City/Town: ", [DataRequired()])
    monthly_eng = wtforms.StringField("Energy usage (monthly): ", [DataRequired()])
    renewable = wtforms.StringField("Energy Percentage Renewables: ", [DataRequired()])
    api_key = wtforms.StringField("API Key: ", [DataRequired()])
    #recaptcha = RecaptchaField()
    submit = wtforms.SubmitField("Submit")