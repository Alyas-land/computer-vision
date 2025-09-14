from flask.views import View
from flask import render_template

class Main(View):
    def dispatch_request(self):
        return render_template("main.html")