from scrap import Scraper
import telephon



import logging

logging.basicConfig(filename='error.log',
                    format='[%(asctime)s] => %(message)s',
                    level=logging.ERROR)

from flask import Flask, request, jsonify

app = Flask('__name__')
clients = {}


@app.route('/login', methods=['POST'])
async def login():

    if request.is_json:
        if phone:=dict(request.json).get('phone'):


            clients[phone] = (client := telephon.Client(phone))

            await client.login()

            if qr := client.qr_link:
                return jsonify(qr_link_url=qr)
            else:
                return jsonify(qr_link_url=None)
            ...
    return jsonify({'error': 'error data'})

@app.route('/check/login', methods=['GET'])
async def check():

    if phone:=request.args.get('phone'):
        if phone not in clients:
            clients[phone] = await telephon.Client(phone).login()
        return jsonify(status=clients[phone].state)


    return jsonify({'error': 'error data'})


@app.route('/message', methods=['GET'])
async def message_get():

    if (phone:=request.args.get('phone')) and (uname:=request.args.get('uname')):
        if phone  in clients:

            return jsonify(await clients[phone].get_message(uname))
        else:
            return jsonify({'error': 'login error'})

    else:
        return jsonify({'error': 'error data'})


@app.route('/message', methods=['POST'])
def message_post():
    if request.is_json:
        req=dict(request.json)
        if (text:=req.get('message_text')) and (phone:=req.get('from_phone')) and (uname:=req.get('username')):
            if phone in clients:

                return jsonify(status=clients[phone].send_message(uname, text))
            else:
                return jsonify({'error': 'login error'})
        else:
            return jsonify({'error': 'error data'})


@app.route('/scraper', methods=['POST'])  # четвертое задание: точка входа scraper параметры джейсона wild
def scraper():
    if request.is_json:
        if r:=dict(request.json).get('wild'):
            return jsonify(Scraper().get_item(r))

    return jsonify({'error':'no data'})
# @app.errorhandler(TypeError)
# def type(error):
#     print(error)
#     return 'bad param' , 500

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8888,debug=False,load_dotenv=True)
