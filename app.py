from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
    # app.run(host='0.0.0.0', port=7658) 