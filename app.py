from flask import Flask, request, jsonify, make_response
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__) #define app using Flask
app.config['JSON_SORT_KEYS'] = False

SWAGGER_URL = '/kuis3'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Belajar API Flask"
    }
)


app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

languages = [{'name' : 'JavaScript'}, {'name' : 'Python'}, {'name' : 'Ruby'}]


@app.route('/', methods=['GET'])
def test():
	return jsonify({'message' : 'It works!'})


@app.route('/lang', methods=['GET'])
def returnAll():
	return jsonify({'languages' : languages})

# #GET

@app.route('/lang/<string:name>', methods=['GET'])
def returnOne(name):
    langs = [language for language in languages if language['name'] == name]
    return jsonify({'language' : langs[0]})

# #POST

@app.route('/lang', methods=['POST'])
def addOne():
    text=request.form.get('text')
    language = {'name' : text}
    languages.append(language)
    return jsonify({'languages' : languages})

# #PUT

@app.route('/lang/<string:name>', methods=['PUT'])
def editOne(name):
    langs = [language for language in languages if language['name'] == name]
    langs[0]['name'] = request.form.get('text')
    return jsonify({'language' : langs[0]})

# #DEL

@app.route('/lang/<string:name>', methods=['DELETE'])
def removeOne(name):
    lang = [language for language in languages if language['name'] == name]
    languages.remove(lang[0])
    return jsonify({'languages' : languages})

@app.errorhandler(400)
def handle_400_error(_error):
    "Return a http 400 error to client"
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@app.errorhandler(401)
def handle_401_error(_error):
    "Return a http 401 error to client"
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@app.errorhandler(404)
def handle_404_error(_error):
    "Return a http 404 error to client"
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    "Return a http 500 error to client"
    return make_response(jsonify({'error': 'Server error'}), 500)

if __name__ == '__main__':
	app.run()
