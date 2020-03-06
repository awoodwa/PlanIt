from flask import Flask, request, url_for, render_template, redirect
from form import InputData


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
    #user_type = request.form["user_type"]
    if request.method == "POST":
        collected_data = request.form.get("user_type")
        return redirect(url_for("results", collected_data=collected_data))
    return render_template("form.html", form=form)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)