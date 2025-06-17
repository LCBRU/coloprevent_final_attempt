from lbrc_flask.database import db
from lbrc_flask.security import Role, User
from lbrc_flask.admin import AdminCustomView, init_admin as flask_init_admin

from coloprevent.model import PackType



class UserView(AdminCustomView):
    column_list = ["username", "first_name", "last_name", "active", "roles"]
    form_columns = ["username", "email", "roles", "active"]

    # form_args and form_overrides required to allow roles to be sets.
    form_args = {
        'roles': {
            'query_factory': lambda: db.session.query(Role)
        },
    }


class PackTypeView(AdminCustomView):
    column_list = ["packtype_name"]
    form_columns = ["packtype_name"]



def init_admin(app, title):
    flask_init_admin(
        app,
        title,
        [
            UserView(User, db.session),
            PackTypeView(PackType, db.session),
        ]
    )
