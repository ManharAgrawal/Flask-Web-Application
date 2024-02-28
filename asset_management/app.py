import pdb
from config import db, app
from flask import  render_template
from asset_features.user_groups import groups_blueprint
from fields.fields import fields_blueprint
from user_auth.user import user_blueprint
from navigation.navigation import navigate_blueprint

app.register_blueprint(groups_blueprint, url_prefix='/users_group')
app.register_blueprint(user_blueprint, url_prefix='/auth')
app.register_blueprint(fields_blueprint, url_prefix='/users_field')
app.register_blueprint(navigate_blueprint, url_prefix='/navigate')

@app.route('/')
def home():
    return render_template('index/index.html')

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        db.create_all()