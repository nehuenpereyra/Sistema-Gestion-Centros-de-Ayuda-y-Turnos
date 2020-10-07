from app import create_app

if __name__ == "__main__":
    environment.env="testing"
    app = create_app()
    app.run()
