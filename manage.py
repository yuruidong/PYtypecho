import os
from app import create_app
from app.modules import User, Content, Category, Comment, Options
from flask.ext.script import Manager, Shell

app = create_app(os.getenv("FLASK_CONFIG") or "default")
manager = Manager(app)


def make_shell_context():
    return dict(app=app, User=User, Content=Content,
                Category=Category, Comment=Comment, Options=Options)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == "__main__":
    manager.run()
