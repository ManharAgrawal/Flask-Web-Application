from config import db, app, mongo
from flask import  render_template
from user_auth.user import user_blueprint
from fields.fields import fields_blueprint
from navigation.navigation import navigate_blueprint
from group.user_groups import groups_blueprint
from records.records import records_blueprint

app.register_blueprint(user_blueprint, url_prefix='/auth')
app.register_blueprint(navigate_blueprint, url_prefix='/navigate')
app.register_blueprint(groups_blueprint, url_prefix='/users_group')
app.register_blueprint(fields_blueprint, url_prefix='/users_field')
app.register_blueprint(records_blueprint, url_prefix='/users_reocrds')

@app.route('/')
def home():
    return render_template('index/index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)
    with app.app_context():
        db.create_all()