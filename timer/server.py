from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

import json
import os

#https://medium.com/@dtkatz/3-ways-to-fix-the-cors-error-and-how-access-control-allow-origin-works-d97d55946d9

app = Flask('Website Timer')
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#make a dictionary of dictionaries
#d[name][website] = [time1, time2, ...]

d = {}

@app.route('/')
def hello_world():
    return render_template('popup.html')


#get -> return data to extension
#post -> get data from extension
@app.route('/test', methods = ['GET'])
def testfunc():

    print("testfunc")
    message = {'flask': 'Hello World'}
    print('sending hello world to extension')
    return jsonify(message)




@app.route('/saveTime', methods=['POST'])
@cross_origin()
def saveTime():

    print('saving time')
    data = request.get_json()
    print(data)
    if data == {}:
        return jsonify({'flask': 'nothing received'})

    name = data['username']
    time = data['time']
    website = data['website']
    print(name, time, website)
    print(d)
    if name in d.keys():
        if website in d[name].keys():
            d[name][website].append(time)
        else:
            d[name][website] = [time]
    else:
        d[name] = {}
        d[name][website] = [time]


    #save_file()
    with open("data.json", "w") as f:
        json.dump(d, f)
    message = {'flask': 'Time Saved!'}
    print(d)
    return jsonify(message)

@app.route('/delTime', methods=['POST'])
@cross_origin()
def deleteTime():
    print('saving time')
    data = request.get_json()
    print(data)
    if data == {}:
        return jsonify({'flask': 'nothing received'})

    name = data['username']
    website = data['website']
    print(name, website)
    print(d)
    if name in d.keys():
        if website in d[name].keys():
            del d[name][website]

    #save_file()
    with open("data.json", "w") as f:
        json.dump(d, f)
    message = {'flask': 'Time Deleted!'}
    print(d)
    return jsonify(message)

@app.route('/showTime', methods=['GET', 'POST'])
@cross_origin()
def showTime():
    print("sending Times")
    data = request.get_json()
    print(data)
    if data == {}:
        return jsonify({'flask': 'nothing received'})
    name = data['username']
    website = data['website']
    print(name, website)
    print(d)
    try:
        temp = sorted(d[name][website])[:10]
    except KeyError:
        return jsonify({'flask': 'nothing received'})

    print(temp)
    return jsonify({"time": temp})




if __name__ == '__main__':
    #open file
    if os.stat('data.json').st_size != 0:#check if file exists and is not empty
        try:
            with open('data.json') as f:
                d = json.load(f)
        except FileNotFoundError:
            pass

    print(d)
    app.run(debug = True)