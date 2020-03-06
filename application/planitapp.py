from flask import Flask, request, url_for, render_template, redirect
from form import InputData
import numpy as np
import build_hscfg  # functions must be in "application" directory


app = Flask(__name__, instance_relative_config=False)
app.config.from_object("config.Config")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/results/<collected_data>")
def results(collected_data):
    result = collected_data

    return render_template("results.html", result=result)

@app.route("/PlanIt", methods=("GET", "POST"))
def form():
    collected_data = []
    form = InputData()
    
    if request.method == "POST":
        # collect input data to use in functions
        collected_data.append(request.form.get("user_type"))
        collected_data.append(request.form.get("location"))
        collected_data.append(request.form.get("monthly_eng"))
        collected_data.append(request.form.get("renewable"))
        collected_data.append(request.form.get("api_key"))
        # run "build_config.py" to build file for accessing NREL data
        build_hscfg.config_file(collected_data[4])
        message = "config file has been built"
        # variables should preceed functions and those will be returned

        return redirect(url_for("results", collected_data=message))
    return render_template("form.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)