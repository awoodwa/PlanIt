from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Length


class InputData(FlaskForm):
    """ INPUTS: 
    user type, location, household size,
    monthly energy used, desired percentage renewable """

    user_type = wtforms.SelectField("*User Type:    ",
    choices=[("Government", "Government"), ("Resident", "Resident")])
    submit = wtforms.SubmitField("Submit")
