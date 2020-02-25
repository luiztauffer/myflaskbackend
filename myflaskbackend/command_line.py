from myflaskbackend import my_app


def main():
    my_app.app.run(host='127.0.0.1', port=5000, debug=True)
