from flask import Flask, request, url_for, render_template
from flask import redirect, flash, Response
from form import InputData
from form_res import InputData_res
from form_gov import InputData_gov
import build_hscfg
import h5pyd
import wrapper


app = Flask(__name__, instance_relative_config=False)
app.config.from_object("config.Config")


@app.route("/")
def home():
    """
    Directs the user to the homepage of the application
    """
    return render_template("home.html")


@app.route("/PlanIt", methods=("GET", "POST"))
def form():
    """
    Collects the user's selection from the initial form page and
    redirects them to the appropriate form page to collect the relevant data
    """
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
    """
    Collects the data from the government form and
    redirects them to the appropriate results page to report
    the final results
    """
    collected_data = []
    form_gov = InputData_gov()
    if request.method == "POST":
        try:
            collected_data.append("Government")
            collected_data.append(request.form.get("state"))
            collected_data.append(request.form.get("location"))
            collected_data.append(request.form.get("land_ava"))
            collected_data.append(request.form.get("goal_renewable"))
            collected_data.append(request.form.get("api_key"))
            # run "build_config.py" to build file for accessing NREL data
            build_hscfg.config_file(collected_data[5])
            # input data to wrapper function
            wtk = h5pyd.File("/nrel/wtk-us.h5", "r")
            if collected_data[4] == '':
                results = wrapper.wrapper(
                    wtk, collected_data[2], collected_data[1],
                    float(collected_data[3]))
            else:
                results = wrapper.wrapper(
                    wtk, collected_data[2], collected_data[1],
                    float(collected_data[3]), goal=int(collected_data[4]))
            return redirect(url_for("results_gov", gov_results=results))
        except IndexError:
            flash("ERROR: Check spelling of 'City/Town' or try a nearby city")
            return render_template("form_gov.html", form_gov=form_gov)
        except OSError:
            flash("ERROR: API key not accepted")
            return render_template("form_gov.html", form_gov=form_gov)
        except ValueError:
            flash("Error: Land available must be a number")
            return render_template("form_gov.html", form_gov=form_gov)
    return render_template("form_gov.html", form_gov=form_gov)


@app.route("/res", methods=("GET", "POST"))
def form_res():
    """
    Collects the data from the resident form and
    redirects the user to the appropriate page to report
    the final results based off of the provided information
    """
    collected_data = []
    form_res = InputData_res()
    if request.method == "POST":
        try:
            # collect input data to use in functions
            collected_data.append("Resident")
            collected_data.append(request.form.get("state"))
            collected_data.append(request.form.get("location"))
            collected_data.append(request.form.get("household"))
            collected_data.append(request.form.get("energy_bill"))
            collected_data.append(request.form.get("goal_renewable"))
            collected_data.append(request.form.get("api_key"))
            # run "build_config.py" to build file for accessing NREL data
            build_hscfg.config_file(collected_data[6])

            # input data to wrapper function
            wtk = h5pyd.File("/nrel/wtk-us.h5", "r")
            if collected_data[4] == '' and collected_data[5] == '':
                results = wrapper.wrapper(
                    wtk, collected_data[2], collected_data[1],
                    0, residential=True,
                    household_size=int(collected_data[3]))
            elif collected_data[4] == '' and collected_data[5] != '':
                results = wrapper.wrapper(
                    wtk, collected_data[2], collected_data[1],
                    0, goal=int(collected_data[5]), residential=True,
                    household_size=int(collected_data[3]))
            elif collected_data[5] == '' and collected_data[4] != '':
                results = wrapper.wrapper(
                    wtk, collected_data[2], collected_data[1],
                    0, residential=True, energy_bill=float(collected_data[4]),
                    household_size=int(collected_data[3]))
            else:
                results = wrapper.wrapper(
                    wtk, collected_data[2], collected_data[1],
                    0, residential=True,
                    energy_bill=float(collected_data[4]),
                    goal=int(collected_data[5]),
                    household_size=int(collected_data[3]))
            return redirect(url_for("results_res", res_results=results))
        except IndexError:
            flash("ERROR: Check spelling of 'City/Town' or try a nearby city")
            return render_template("form_res.html", form_res=form_res)
        except OSError:
            flash("ERROR: API key not accepted")
            return render_template("form_res.html", form_res=form_res)
    return render_template("form_res.html", form_res=form_res)


@app.route("/results_res/<res_results>")
def results_res(res_results):
    """
    Formats the output from the calculations and
    reports the residents results
    """
    result0 = res_results
    res_results = res_results.replace("[", " ")
    res_results = res_results.replace("]", " ")
    result0 = list(res_results.split(","))
    return render_template("results_res.html", result0=result0)


@app.route("/results_gov/<gov_results>")
def results_gov(gov_results):
    """
    Reports a plot based off of the government input information
    """
    gov_results = gov_results.replace("[", " ")
    gov_results = gov_results.replace("]", " ")
    return render_template("results_gov.html", chart="gov_chart")


@app.route("/results_gov/")
def gov_chart():
    """
    This function allows the resulting plot to be embedded
    into the "results_gov" page
    """
    return render_template("gov_chart.html")


@app.route("/home_map/")
def home_map():
    """
    This function allows the homepage_map plot to be embedded
    into the home page of the application
    """
    return render_template("energy.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run()
