from app import create_app
from flask_script import Manager, Server

flaskapp = create_app('default')
# manager = Manager(flaskapp)
# manager.add_command("server", Server(host="127.0.0.1", port=5000, use_debugger=True))


if __name__ == '__main__':
    flaskapp.run()
