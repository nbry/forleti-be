from flask import jsonify
from project import create_app

app = create_app("development.cfg")


@app.route('/test')
def hello_world():
    return jsonify({"message": "hello world"})

# # IF RUNNING ON PYCHARM:
# if __name__ == '__main__':
#     app.run()
