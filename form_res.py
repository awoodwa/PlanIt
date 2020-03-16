from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired


class InputData_res(FlaskForm):
    """
    This class builds the form for residential users
    INPUTS:
        state: users will select their state from the list provided
        location: users will input their city or town
            (first letter of city/town should be uppercase)
        household size: users should record the
            number of members living at their address
        energy_bill: optional field allowing users to record the
            energy reported from previous energy bills (units of kWh)
        goal_percentage_renewable: optional field allowing users
            to decide how much energy should be from renewable sources
        api_key: this is required for the user to
            access the database for calculations
    """
    location = wtforms.StringField("*City/Town: ", [DataRequired()])
    state_abbrev = ["AL", "AK",
                    "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    state = wtforms.SelectField("*State: ", choices=[
        (state, state) for state in state_abbrev])
    household = wtforms.StringField("*Household Size: ", [DataRequired()])
    energy_bill = wtforms.StringField("Monthly Energy Bill (kWh): ")
    goal_renewable = wtforms.StringField("Goal Renewable Energy (%): ")
    api_key = wtforms.StringField("*API Key: ", [DataRequired()])
    submit = wtforms.SubmitField("Submit")
