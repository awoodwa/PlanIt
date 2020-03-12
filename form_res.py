from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Length


class InputData_res(FlaskForm):
    """ INPUTS: u
    user type, location, household size,
    monthly energy used, desired percentage renewable """

    
    location = wtforms.StringField("*City/Town: ", [DataRequired()])
    state_abbrev = ["AL", "AK",
        "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    state = wtforms.SelectField("*State: ",
     choices=[(state, state) for state in state_abbrev])
    household = wtforms.StringField("*Household Size: ", [DataRequired()])
    monthly_eng = wtforms.StringField(
        "*Monthly Energy Usage (kWh): ", [DataRequired()])
    renewable = wtforms.StringField(
        "Goal Percentage of Energy from Renewables: ")
    api_key = wtforms.StringField("*API Key: ", [DataRequired()])
    submit = wtforms.SubmitField("Submit")
