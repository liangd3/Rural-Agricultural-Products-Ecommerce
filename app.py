from flask import Flask
from datetime import datetime


from blueprints.manager import manager_bp
from blueprints.staff import staff_bp
from blueprints.admin import admin_bp
from blueprints.customer import customer_bp
from blueprints.user.user import user_bp
from blueprints.common import common_bp
from blueprints.internal import internal_bp
# Initializing Flask application
app = Flask(__name__)


app.secret_key = 'arproject2'
app.register_blueprint(manager_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(customer_bp)
app.register_blueprint(user_bp)
app.register_blueprint(common_bp)
app.register_blueprint(internal_bp)

def nzdatetime(d):
     d =  datetime.strptime(str(d),"%Y-%m-%d %H:%M:%S")
     d = d.strftime("%d-%m-%Y %H:%M:%S")
     return d
app.add_template_filter(nzdatetime)

def nzdate(d):
     d =  datetime.strptime(str(d),"%Y-%m-%d")
     d = d.strftime("%d-%m-%Y")
     return d
app.add_template_filter(nzdate)


def htmldatetime(d):
     d =  datetime.strptime(str(d),"%Y-%m-%d %H:%M:%S")
     d = d.strftime("%Y-%m-%dT%H:%M:%S")
     return d
app.add_template_filter(htmldatetime)

@app.template_filter()
def numberFormat(value):
    return format("%.2f" % round(value, 2))
app.add_template_filter(numberFormat)


if __name__ == '__main__':
    app.run(debug=True)