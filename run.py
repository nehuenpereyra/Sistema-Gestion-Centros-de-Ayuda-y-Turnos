from app import create_app
from smallthon import sm_list

sm_list()

if __name__ == "__main__":
    app = create_app()
    app.run()
