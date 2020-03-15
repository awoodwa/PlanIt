from flask import Flask
from flask_frozen import Freezer
from flask_flatpages import FlatPages


app = Flask(__name__, instance_relative_config=False)
app.config.from_object("config.Config")
pages = FlatPages(app)
freezer = Freezer(app)
