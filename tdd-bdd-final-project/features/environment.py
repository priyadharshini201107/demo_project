from service import create_app, db


def before_scenario(context, scenario):
    context.app = create_app({"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    context.client = context.app.test_client()
    context.app_context = context.app.app_context()
    context.app_context.push()
    db.create_all()


def after_scenario(context, scenario):
    db.session.remove()
    db.drop_all()
    context.app_context.pop()
