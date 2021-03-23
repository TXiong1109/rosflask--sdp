#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from flask_msgs.msg import *
from flask import Flask, render_template, session, redirect, request, flash, url_for
import os
import json
from threading import Thread, Event
import signal, sys
from functools import wraps
flash_msgs = ''
msgs = flaskMsg()
app = Flask(__name__)
app.config['SECRET_KEY']='aldjfkadq37oaisdfo'
basedir = os.path.dirname(os.path.abspath(__file__))

json_names = ['output-floor1','output-floor2']
#Publisher
GOToReceptionpub = rospy.Publisher('GOToReception', String, queue_size=10)
GoToBoothpub = rospy.Publisher('GoToBooth', String, queue_size=10)
GoToExitpub = rospy.Publisher('GoToExit', String, queue_size=10)
GoToChargingpub = rospy.Publisher('GoToCharging', String, queue_size=10)
GoToDropOffpub = rospy.Publisher('GoToDropOff', String, queue_size=10)
Haltpub = rospy.Publisher('Halt', String, queue_size=10)
Resumepub = rospy.Publisher('Resume', String, queue_size=10)
HelpCompleteContinuepub = rospy.Publisher('HelpCompleteContinue', String, queue_size=10)
HelpCompleteRestartpub = rospy.Publisher('HelpCompleteRestart', String, queue_size=10)
def jcallback(data):
    #transform string to json
    global msgs
    msgs = data
    str = data.json
    jname = data.jname
    filename = jname + '.json'
    jsonfile = os.path.join(basedir, 'data', filename)
    newjson = json.loads(str)
    with open(jsonfile, 'w') as f:
        json.dump(newjson, f)
def scallback(data):
    global flash_msgs
    flash_msgs = data.data
def rosappnode():
    rospy.init_node('app_node',disable_signals=True)
    #Subscriber
    rospy.Subscriber("app_json", flaskMsg, jcallback)
    rospy.Subscriber("flash_msgs", String, scallback)

    rospy.spin()

def login_check(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not session.get('username'):
            global flash_msgs
            flash(flash_msgs)
            #flash('Please login firstly!')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return inner


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        accounts_file = os.path.join(basedir, 'data/accounts.json')
        with open(accounts_file, 'r') as f:
            accounts = json.load(f)
            if username in accounts['accounts'] and password == accounts['accounts'][username]:
                session['username'] = username
                return redirect(url_for("index"))
            else:
                global flash_msgs
                flash(flash_msgs)
                #flash('Username and password not matched!')
                return redirect(url_for("login"))
    return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        accounts = None
        global flash_msgs
        if password != password2:
            flash(flash_msgs)
            #flash('Password not matched, please retry!')
            return render_template('register.html')
        accounts_file = os.path.join(basedir, 'data/accounts.json')
        with open(accounts_file, 'r') as f:
            accounts = json.load(f)
            if username in accounts['accounts']:
                flash(flash_msgs)
                #flash('User already exists, pls check!')
                return render_template('register.html')
            accounts['accounts'][username] = password
        if accounts:
            with open(accounts_file, 'w') as f:
                json.dump(accounts, f)
                session['username'] = username
                flash(flash_msgs)
                #flash('Register successfully!')
                return render_template('index.html')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route('/')
@login_check
def index():
    jname=""
    return render_template('index.html', json_names = json_names, jname=jname)


@app.route('/json', methods=['GET'])
@login_check
def read_json():
    jname = request.args.get('jname')
    #filename = jname + '.json'
    robots = []
    robot  = {}
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        if robots:
            robot = robots[0]
        return render_template('index.html', json_names = json_names, jname=jname, robots = robots, robot=robot, robotid=0)

    # print('filepath: --- {}'.format(os.path.join(basedir, 'data' , filename)))
    # with open(os.path.join(basedir, 'data' , filename)) as f:
    #     jsonstr = json.load(f)
    #     robots = jsonstr.get('Robots')
    #     # print(robots)
    #     if robots:
    #         robot = robots[0]
    #     return render_template('index.html', json_names = json_names, jname=jname, robots = robots, robot=robot, robotid=0)

@app.route('/<jname>/robot/<id>/GOToReception', methods=['GET'])
@login_check
def GOToReception(jname,id):
    #send GOToReception message
    str = id + '_overrideReception'
    GOToReceptionpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names = json_names, jname=jname, robots = robots, robot=robot, location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/GoToBooth', methods=['GET'])
@login_check
def GoToBooth(jname,id):
    #send GOToReception message
    str = id + '_overrideBooth'
    GoToBoothpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/GoToExit', methods=['GET'])
@login_check
def GoToExit(jname,id):
    #send GOToReception message
    str = id + '_overrideExit'
    GoToExitpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/GoToCharging', methods=['GET'])
@login_check
def GoToCharging(jname,id):
    #send GOToReception message
    str = id + '_overrideCharging'
    GoToChargingpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)

@app.route('/<jname>/robot/<id>/GoToDropOff', methods=['GET'])
@login_check
def GoToDropOff(jname,id):
    #send GOToReception message
    str = id + '_overrideDropOff'
    GoToDropOffpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/Halt', methods=['GET'])
@login_check
def Halt(jname,id):
    #send GOToReception message
    str = id + '_overrideHalt'
    Haltpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/Resume', methods=['GET'])
@login_check
def Resume(jname,id):
    #send GOToReception message
    str = id + '_overrideResume'
    Resumepub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/HelpCompleteContinue', methods=['GET'])
@login_check
def HelpCompleteContinue(jname,id):
    #send GOToReception message
    str = id + '_HelpCompleteContinue'
    HelpCompleteContinuepub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<id>/HelpCompleteRestart', methods=['GET'])
@login_check
def HelpCompleteRestart(jname,id):
    #send GOToReception message
    str = id + '_HelpCompleteRestart'
    HelpCompleteRestartpub.publish(str)
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        # print(robots)
        i = 0
        for robot in robots:
            i = i+1
            print(robot['ID'])
            if robot['ID'] == id :
                robotid = i
                state = robot["State"]["State"]
                destination = robot["State"]["Destination"]
                location = get_location(state, destination)
                return render_template('index.html', json_names=json_names, jname=jname, robots=robots, robot=robot,
                                   location=location, robotid=robotid)
@app.route('/<jname>/robot/<int:id>', methods=['GET'])
@login_check
def robot(jname, id):
    # filename = jname + '.json'
    # robots = []
    # robot  = {}
    global msgs
    if msgs.jname == jname:
        jsonstr = json.loads(msgs.json)
        robots = jsonstr.get('Robots')
        if robots:
            robot = robots[id]
            state = robot["State"]["State"]
            destination = robot["State"]["Destination"]
            location = get_location(state, destination)
            print('locaiton: {}'.format(location))
        return render_template('index.html', json_names = json_names, jname=jname, robots = robots, robot=robot, location=location, robotid=id)

def get_location(state, destination):
    print('state: {}, destination: {}'.format(state, destination))
    location = 'Reception'
    if state == "WaitingAtReception":
        if destination == "N/A":
            location = "Reception"
    elif state == "ReadyForMovement":
        if destination == "Booth":
            location = "Ready to move to Booth"
        if destination == "Reception":
            location = "Ready to move to Reception"
        if destination == "Exit":
            location = "Ready to move to Exit"
        if destination == "Drop off":
            location = "Ready to move to Dropoff"
    elif state == "Charging":
        if destination == "N/A":
            location = "Charging Center"
    elif state == "Movement":
        if destination == "Booth":
            location = "Way to Booth"
        if destination == "Reception":
            location = "Way to Reception"
        if destination == "Exit":
            location = "Way to Exit"
        if destination == "DropOff":
            location = "Way to Dropoff"
    elif state == "AtExit":
        if destination == "N/A":
            location = "Exit"
    elif state == "AtDropOff":
        if destination == "N/A":
            location = "Dropoff"
    elif state == "WaitingForAssistance":
        if destination == "N/A":
            location = "Booth"
    return location



if __name__ == '__main__':
    Thread(target=rosappnode).start()
    app.run(debug=True, port=5050)

