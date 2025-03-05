from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    print(data)
    return jsonify({'you_sent': data})

@app.route('/bibizan', methods=['GET'])
def bibizan():
    return jsonify({'bibizan': 'Dimasik',
                    'photo':'https://yt3.googleusercontent.com/UmuHBjKgIi2TD8HKImnH1ZWo7gkbjPv50mWbEyac2CzB7NzfBrFE1swklzBSAQT5q8rGITelsA=s900-c-k-c0x00ffffff-no-rj'})


if __name__ == '__main__':
    app.run(debug=True)