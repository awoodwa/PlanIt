from flask import request, url_for, render_template, redirect, flash
#from PlanIt import form, form_gov, form_res, build_hscfg, homepage_map, location_handling, app 
from form import InputData
from form_res import InputData_res
from form_gov import InputData_gov
from app import app, pages, freezer
import build_hscfg  # functions must be in "application" directory
import homepage_map
import location_handling


@app.route("/")
def home():
    homepage_map.states()
    return render_template("home.html")


@app.route("/PlanIt", methods=("GET", "POST"))
def form():
    collected_data = []
    form = InputData()
    if request.method == "POST":
        # collect input data to use in functions
        collected_data.append(request.form.get("user_type"))
        if collected_data[0] == "Government":
            return redirect(url_for("form_gov"))
        else:
            return redirect(url_for("form_res"))
    return render_template("form.html", form=form)

@app.route("/gov", methods=("GET", "POST"))
def form_gov():
    collected_data = []
    form_gov = InputData_gov()
    if request.method == "POST":
        try:
        # collect input data to use in functions
            collected_data.append("Government")
            collected_data.append(request.form.get("state"))
            collected_data.append(request.form.get("location"))
            collected_data.append(request.form.get("monthly_eng"))
            collected_data.append(request.form.get("renewable"))
            collected_data.append(request.form.get("land_ava"))
            collected_data.append(request.form.get("api_key"))
            # run "build_config.py" to build file for accessing NREL data
            build_hscfg.config_file(collected_data[5])

            loc_handling = location_handling.get_loc(
                collected_data[2], collected_data[1])
            #if loc_handling == len(0)
            message = loc_handling  # "config file has been built"
            return redirect(url_for("results_gov", gov_results=message))
        except IndexError:
            flash("ERROR 'City/Town' spelling or try a nearby city")
            #return redirect(url_for("form_res"))
            return render_template("form_gov.html", form_gov=form_gov)
    return render_template("form_gov.html", form_gov=form_gov)

@app.route("/res", methods=("GET", "POST"))
def form_res():
    collected_data = []
    form_res = InputData_res()
    if request.method == "POST":
        try:
            # collect input data to use in functions
            collected_data.append("Resident")
            collected_data.append(request.form.get("state"))
            collected_data.append(request.form.get("location"))
            collected_data.append(request.form.get("household"))
            collected_data.append(request.form.get("monthly_eng"))
            collected_data.append(request.form.get("renewable"))
            collected_data.append(request.form.get("api_key"))
            # run "build_config.py" to build file for accessing NREL data
            build_hscfg.config_file(collected_data[6])
            loc_handling = location_handling.get_loc(
                collected_data[2], collected_data[1])
            message = loc_handling  # "config file has been built"
            return redirect(url_for("results_res", res_results=message))
        except IndexError:
            flash("ERROR 'City/Town' spelling or try a nearby city")
            #return redirect(url_for("form_res"))
            return render_template("form_res.html", form_res=form_res)
    return render_template("form_res.html", form_res=form_res)


@app.route("/results_res/<res_results>")
def results_res(res_results):
    result = res_results
    return render_template("results_res.html", result=result)


@app.route("/results_gov/<gov_results>")
def results_gov(gov_results):
    result = gov_results
    return render_template("results_gov.html", result=result)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)


       
