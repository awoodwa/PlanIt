from flask_wtf import FlaskForm
import wtforms


class InputData(FlaskForm):
    """
    This class builds to initial form page identifying the user type
    INPUTS:
        user_type: user will select from a list if they are a
            government entity or a resident
                - this determines which calculation and variables will be considered
    """
    user_type = wtforms.SelectField("User Type:    ", choices=[
        ("Government", "Government"), ("Resident", "Resident")])
    submit = wtforms.SubmitField("Submit")
