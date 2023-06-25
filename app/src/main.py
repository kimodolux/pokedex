from app import app

import routes


def run_local():
    app.run(host="localhost")


if __name__ == "__main__":
    run_local()
