# encoding:utf-8
import multiprocessing
import subprocess
import torch.multiprocessing

import torch.multiprocessing as mp
from time import sleep

import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
from flask import Flask, request, send_from_directory, make_response, session
import os
from flask_cors import CORS
import utils
import json
import urllib.parse
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from utils import getData, popen3, token_encoder, token_decoder, apply_ascyn, makedir, fileSave
from RunHelp import RunHelp
import threading
import shutil
import hashlib
import jwt
from multiprocessing import Process
import psutil
import re

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True)
PEOPLE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://DL:DL123.@localhost:3306/DL"
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

g_path = "/home/DL/flask/"
# g_path = "/home/DL/flask/"

g_model = {}
g_progress = {}
g_pause = {}
g_queue = {}
torch.multiprocessing.set_start_method('spawn', force=True)

class user(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(20), )
    password = db.Column(db.String(20), )
    role = db.Column(db.Integer, )
    state = db.Column(db.Integer, )

    def __init__(self, name, password, role, state):
        self.name = name
        self.password = password
        self.role = role
        self.state = state

    def dump(self):
        return {
            "real_id": self.id,
            "name": self.name,
            "role": self.role,
            "state": "启用" if self.state == 0 else "禁用"
        }


class project(db.Model):
    __tablename__ = 'project'
    user = db.Column(db.String(20), primary_key=True)
    project = db.Column(db.String(20), primary_key=True)
    date = db.Column(db.String(20),)
    type = db.Column(db.String(20), primary_key=True)

    def __init__(self, user, project, date, type):
        self.user = user
        self.project = project
        self.date = date
        self.type = type


class roles(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255))
    
    def __init__(self, name):
        self.name = name

    def dump(self):
        return {
            "real_id": self.id,
            "name": self.name
        }


class permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(255))
    user_add = db.Column(db.Integer)
    user_update = db.Column(db.Integer)
    user_delete = db.Column(db.Integer)
    user_search = db.Column(db.Integer)
    role_add = db.Column(db.Integer)
    role_update = db.Column(db.Integer)
    role_delete = db.Column(db.Integer)
    role_search = db.Column(db.Integer)

    def __init__(self, name, user_add, user_update, user_delete, user_search, role_add, role_update, role_delete, role_search):
        self.name = name
        self.user_add = user_add
        self.user_update = user_update
        self.user_delete = user_delete
        self.user_search = user_search
        self.role_add = role_add
        self.role_update = role_update
        self.role_delete = role_delete
        self.role_search = role_search

    def dump(self):
        return {
            "real_id": self.id,
            "name": self.name,
            "user_add": "是" if self.user_add else "否",
            "user_update": "是" if self.user_update else "否",
            "user_delete": "是" if self.user_delete else "否",
            "user_search": "是" if self.user_search else "否",
            "role_add": "是" if self.role_add else "否",
            "role_update": "是" if self.role_update else "否",
            "role_delete": "是" if self.role_delete else "否",
            "role_search": "是" if self.role_search else "否",
        }

    def getPermission(self):
        l = ["user_add", "user_update", "user_delete", "user_search", "role_add", "role_update", "role_delete", "role_search"]
        val_l = [self.user_add, self.user_update, self.user_delete, self.user_search, self.role_add, self.role_update, self.role_delete, self.role_search]
        return [l[i] for i in range(len(l)) if val_l[i]]


def get_permission(token):
    jwt_decode = jwt.decode(token, 'deep', issuer='deepL', algorithms=['HS256'])
    role = jwt_decode['data']['role']
    print(role)
    p = permission.query.filter(permission.id == role).first()
    return p.getPermission()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/login', methods=["post", "get"])
def login():
    # data = request.get_data()
    # data = str(data, 'utf8')
    # data = json.loads(data)
    data = getData()
    name, password = data["name"], data["password"]
    sha1 = hashlib.sha1()
    sha1.update(password.encode("utf-8"))
    u = user.query.filter_by(name=name).first()
    if u is not None and u.password == sha1.hexdigest():
        token = token_encoder(u.name, u.role)
        return {"token": token, "role": u.role}
    return "fail"


@app.route('/gettoken', methods=["post", "get"])
def getToken():
    # data = request.get_data()
    # data = str(data, 'utf8')
    # data = json.loads(data)
    data = getData()
    token = data["token"]
    name, role = token_decoder(token)
    token = token_encoder(name, role)
    return token


@app.route('/register', methods=["post", "get"])
def register():
    # data = request.get_data()
    # data = str(data, 'utf8')
    # data = json.loads(data)
    data = getData()
    name, password = data["name"], data["password"]
    u = user.query.filter_by(name=name).first()
    if u is not None:
        return "exist"
    sha1 = hashlib.sha1()
    sha1.update(password.encode("utf-8"))
    addUser = user(name, sha1.hexdigest(), 0, 0)
    db.session.add(addUser)
    db.session.commit()
    os.makedirs(name)
    os.makedirs(name+"/val")
    os.makedirs(name+"/data")
    os.makedirs(name+"/params")
    os.makedirs(name+"/projects")
    os.makedirs(name+"/projects/visual")
    os.makedirs(name+"/projects/code")
    os.makedirs(name+"/results")
    os.makedirs(name+"/save")
    os.makedirs(name+"/chart")
    return "success"


@app.route('/code/run', methods=["get", "post"])
def run_code():
    data = getData()
    code = data["code"]
    rows = code.split("<br>")
    f_code = ""
    for row in rows:
        f_code = f_code + row + '\n'
    fh = open("save.py", 'w', encoding='utf-8')
    fh.write(f_code)
    fh.close()
    # os.system("python3 /Users/sunfan/PycharmProjects/flaskProject/save.py")
    out, err = popen3("python3 /Users/sunfan/PycharmProjects/flaskProject/save.py")
    print(out)
    print(err)
    if str(err).split("'")[1] == "":
        return {"s": "suc", "d": str(out)}
    return {"s": "err", "d": str(out) + "++++" + str(err)}


@app.route('/debug', methods=["post", "get"])
def debug_code():
    data = getData()
    code = data["code"]
    project = data["project"]
    rows = code.split("<br>")
    f_code = ""
    for row in rows:
        f_code = f_code + row + '\n'
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/save/" + project + ".py"
    fh = open(dirpath, 'w', encoding='utf-8')
    fh.write(f_code)
    fh.close()
    # os.system("gnome-terminal -e 'python3 /Users/sunfan/PycharmProjects/flaskProject/save.py'")
    # os.system("python3 " + dirpath)
    args = 'python3 '+dirpath
    print(args)
    subprocess.Popen(args, shell=True)
    return code


@app.route('/debug/<string:type>/<string:location>', methods=["post"])
def downloadChart(type, location):
    epoch = 0
    train_data = []
    test_data = []
    utils.getChart(epoch, train_data, test_data, type)


@app.route('/visual/run', methods=["post"])
def visualRun():
    data = getData()
    process = data["process"]
    params = data["params"]
    saveP = data["saveP"]
    project_name = data["project"]
    time = data["time"]
    print(process)
    print(params)
    print(saveP)
    runHelp = RunHelp()
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    model, name = runHelp.getmodel(process, params, saveP, g_path, g_name, project_name)
    global g_model
    if g_name not in g_model:
        g_model[g_name] = {}
    g_model[g_name][project_name] = model
    q = multiprocessing.Queue()
    file_name = name.replace(" ", "") + "_" + time.replace("/", "") + ".txt"
    p = mp.Process(target=runHelp.train, args=(process, params, q, os.path.join(g_path, g_name, "logs", file_name)))
    p.start()
    if g_name not in g_progress:
        g_progress[g_name] = {}
    g_progress[g_name][project_name] = p
    if g_name not in g_queue:
        g_queue[g_name] = {}
    g_queue[g_name][project_name] = q
    while p.is_alive():
        str = "do not return"
    # runHelp.train(process, params)
    # path = "/Users/sunfan/PycharmProjects/flaskProject/VOC2012"
    # RunHelp().operation(model, path, pro_l, para_l)
    # if process[0] == "upload":
    #     data_path = g_path + g_name + "/data/" + params[0]["packname"]
    return "success"


@app.route('/visual/pause', methods=["get", "post"])
def visualPause():
    data = getData()
    project_name = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    p = psutil.Process(g_progress[g_name][project_name].pid)
    p.suspend()  # 挂起进程
    if g_name not in g_pause:
        g_pause[g_name] = {}
    g_pause[g_name][project_name] = p
    return "success"
    

@app.route('/visual/continue', methods=["get", "post"])
def visualContinue():
    data = getData()
    project_name = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    p = g_pause[g_name][project_name]
    p.resume()  # 恢复进程
    return "success"


@app.route('/visual/stop', methods=["get", "post"])
def visualStop():
    data = getData()
    project_name = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    p = g_progress[g_name][project_name]
    p.terminate()
    p.join()
    return "success"

@app.route('/visual/getloss', methods=["post"])
def visualGetLoss():
    data = getData()
    project = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    print(g_name, project)
    # model = g_model[g_name][project]
    name = RunHelp().getModelType(g_path, g_name, project)
    print("name:", name)
    # train_loss, train_matrix, val_loss, val_matrix = RunHelp().getLossMatrix(name, model)
    [train_loss, train_matrix, val_loss, val_matrix] = g_queue[g_name][project].get()
    l = data["l"]
    print(l)
    print(train_loss, train_matrix, val_loss, val_matrix)
    print(utils.get_matrix_name(l))
    return {'train_loss': train_loss, 'train_matrix': train_matrix, 'val_loss': val_loss, 'val_matrix': val_matrix, 'matrix': utils.get_matrix_name(l)}


@app.route('/visual/upload/<string:name>', methods=["post","get"])
def upload(name):
    img = request.files["file"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/data/"+name
    if not Path(dirpath).is_dir():
        os.makedirs(dirpath)
    filename = img.filename
    file_path = os.path.join(dirpath, filename)
    print(file_path)
    img.save(file_path)
    # response = make_response(send_from_directory(dirpath, filename, as_attachment=True))
    # response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return "success"

@app.route('/visual/uploaddir/<string:datatype>/<string:packname>', methods=["post","get"])
def uploadDir(datatype, packname):
    file = request.files["file"]
    # dirpath = g_path + g_name + "/data/"+name
    # if not Path(dirpath).is_dir():
    #     os.makedirs(dirpath)
    # filename = img.filename
    # file_path = os.path.join(dirpath, filename)
    # print(file_path)
    # img.save(file_path)
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    if not os.path.exists(g_name+"/data/" + packname):
        os.makedirs(g_name+"/data/" + packname + "/train")
        os.makedirs(g_name+"/data/" + packname + "/val")
    sleep(1)
    dirpath = g_path + g_name + "/data/" + packname + "/" + datatype + "/" + file.filename
    file.save(dirpath)
    # response = make_response(send_from_directory(dirpath, filename, as_attachment=True))
    # response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return "success"


@app.route('/visual/errormessage', methods=["get"])
def getErrorMessage():
    return {"message": None}


@app.route('/visual/lossacc', methods=[""])
def getLossAcc():
    return {"loss": None, "acc": None}


@app.route('/code/errormessage', methods=["get"])
def getCodeErrorMessage():
    return {"message": "message"}


@app.route('/code/lossacc', methods=[""])
def getCodeLossAcc():
    return {"loss": None, "acc": None}


@app.route('/visual/test/<int:i>/<string:param>/<string:project>/<string:conn>', methods=["get", "post"])
def visualTest(i, param, project, conn):
    # dirpath = g_path + g_name+"/projects/visual"
    # for file in os.listdir(dirpath):
    #     s = file.split("-*-")
    #     print(s)
    #     print((file.replace(s[0]+"-*-", "", 1))[:-3])
    #     print(param)
    #     if s[0] == project and (file.replace(s[0], "", 1))[:-3] == param:
    #         print(file) # 参数文件名
    # model_path = g_path + g_name + "/params/" + project + "/" + param
    print(request.headers)
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/val/" + project
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    f = request.files["file"]
    utils.del_file(dirpath, i)
    print(dirpath)
    s = f.filename.split(".")[0]
    filename = s + " " + str(i) + f.filename.replace(s, "")
    # filename = f.filename.split(".png")[0].split(".jpg")[0].split(".jpeg")[0]+" "+str(i)+".jpg"
    file_path = os.path.join(dirpath, filename)
    print(file_path)
    f.save(file_path)
    print(conn)
    model_name = RunHelp().getmodelname(conn.split(","))
    RunHelp().infer(g_path, g_name, param + ".pth.tar", [filename], project, model_name)
    # response = make_response(send_from_directory(dirpath, filename, as_attachment=True))
    # response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return str(i)


@app.route("/visual/download", methods=["post", "get"])
def downloader():
    # data = str(request.get_data()).split("'")[1]
    # data = request.get_data()
    # data = str(data, 'utf8')
    # i = json.loads(data)["i"]
    data = getData()
    i = data["i"]
    project = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path+g_name+"/results/" + project
    name = utils.search_file(i, dirpath)
    print(name)
    response = make_response(send_from_directory(dirpath, name, as_attachment=True))
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return response


@app.route("/visual/downparam", methods=["post", "get"])
def downloadParam():
    # data = request.get_data()
    # data = str(data, 'utf8')
    # name = json.loads(str(request.get_data()).split("'")[1])["name"]
    # name = json.loads(data)["name"]
    data = getData()
    name = data["name"]
    project = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path+g_name+"/params/"+project
    print(name)
    response = make_response(send_from_directory(dirpath, name, as_attachment=True))
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return response


@app.route("/visual/downchart", methods=["post", "get"])
def downChart():
    data = getData()
    type = data["type"]
    project = data["project"]
    l = data["l"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    model = g_model[g_name][project]
    dirpath = g_path + "chart"
    print(type)
    name = RunHelp().getModelType(g_path, g_name, project)
    train_loss, train_matrix, val_loss, val_matrix = RunHelp().getLossMatrix(name, model)
    if type == "loss":
        utils.getChart(train_loss, val_loss, "loss", g_name)
        response = make_response(send_from_directory(dirpath, "loss.jpg", as_attachment=True))
    else:
        matrix = utils.get_matrix_name(l)
        utils.getChart(train_matrix, val_matrix, matrix, g_name)
        response = make_response(send_from_directory(dirpath, matrix + ".jpg", as_attachment=True))
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"

    return response

@app.route("/visual/getpackage", methods=["post","get"])
def getPackage():
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path+g_name+"/data"
    dirs = ""
    for file in os.listdir(dirpath):
        dirs += " "+file
    print(dirs)
    return dirs


@app.route("/visual/save", methods=["post", "get"])
def saveVisualProject():
    # data = request.get_data()
    # data = str(data, 'utf8')
    # print(data)
    # data = json.loads(data)
    data = getData()
    params = data["param"]
    name = data["name"]
    date = data["date"]
    print(params)
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    filename = g_path+g_name+"/projects/visual/"+name+".txt"
    file = open(filename, 'w')
    file.write(str(params))
    file.close()
    p = project.query.filter_by(project=name, user=g_name, type="visual").first()
    print(name)
    if p is None:
        addProject = project(g_name, name, date, "visual")
        db.session.add(addProject)
        db.session.commit()
        os.makedirs(g_path + g_name + "/params/" + name)
        os.makedirs(g_path + g_name + "/results/" + name)
        os.makedirs(g_path + g_name + "/val/" + name)
    return "success"


@app.route("/code/save", methods=["post", "get"])
def saveCodeProject():
    # data = request.get_data()
    # data = str(data, 'utf8')
    # print(data)
    # data = json.loads(data)
    data = getData()
    params = data["code"]
    name = data["name"]
    date = data["date"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    filename = g_path+g_name+"/projects/code/"+name+".py"
    file = open(filename, 'w')
    file.write(params)
    file.close()
    p = project.query.filter_by(project=name, user=g_name, type="code").first()
    if p is None:
        addProject = project(g_name, name, date, "code")
        db.session.add(addProject)
        db.session.commit()
    return "success"


@app.route("/visual/getproject", methods=["post", "get"])
def getVisualProject():
    # data = str(request.get_data(), 'utf8')
    # data = json.loads(data)
    data = getData()
    name = data["name"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    filename = g_path + g_name + "/projects/visual/" + name + ".txt"
    file = open(filename, 'r')
    content = file.readline()
    file.close()
    return content


@app.route("/code/getproject", methods=["post", "get"])
def getCodeProject():
    # data = str(request.get_data(), 'utf8')
    # data = json.loads(data)
    data = getData()
    name = data["name"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    filename = g_path + g_name + "/projects/code/" + name + ".py"
    file = open(filename, 'r')
    content = file.read()
    print(content)
    file.close()
    return content


@app.route("/getproject", methods=["post", "get"])
def getProject():
    code_l = []
    visual_l = []
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    u = project.query.filter_by(user=g_name)
    for item in u:
        if item.type == "code":
            code_l.append({"name": item.project, "date": item.date})
        else:
            visual_l.append({"name": item.project, "date": item.date})
    return {"code": code_l, "visual": visual_l}


@app.route("/visual/delete", methods=["post", "get"])
def deleteVisualProject():
    data = getData()
    name = data["name"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/projects/visual/"+name+".txt"
    os.remove(dirpath)
    l = ["params", "results", "val"]
    for i in l:
        shutil.rmtree(g_path + g_name + "/" + i + "/" + name, ignore_errors=True)
        # os.removedirs(g_path + g_name + "/" + i + "/" + name)
    p = project.query.filter_by(user=g_name, project=name, type="visual").first()
    db.session.delete(p)
    db.session.commit()
    return "success"


@app.route("/code/delete", methods=["post", "get"])
def deleteCodeProject():
    data = getData()
    name = data["name"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/projects/code/"+name+".py"
    os.remove(dirpath)
    p = project.query.filter_by(user=g_name, project=name, type="code").first()
    db.session.delete(p)
    db.session.commit()
    return "success"


# @app.route("/visual/createparam", methods=["post", "get"])
# def createVisualParam():
#     # data = str(request.get_data(), 'utf8')
#     # data = json.loads(data)
#     data = getData()
#     param_name = data["param"]
#     project_name = data["project"]
#     name = project_name+"-*-"+param_name
#     filename = g_path + g_name + "/projects/visual/"+name+".h5"
#     file = open(filename, 'w')
#     file.close()
#     return "success"


@app.route("/visual/gettestparam", methods=["post", "get"])
def getTestParam():
    # data = str(request.get_data(), 'utf8')
    # data = json.loads(data)
    data = getData()
    name = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/params/" + name
    l = []
    for file in os.listdir(dirpath):
        # s = file.split("-*-")
        # if name == s[0]:
        l.append(file.replace(".pth.tar", ""))
    return {"params": l}


@app.route("/visual/changename", methods=["post", "get"])
def changeVisualName():
    # data = str(request.get_data(), 'utf8')
    # data = json.loads(data)
    data = getData()
    name = data["name"]
    oldname = data["oldname"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/projects/visual/"
    for file in os.listdir(dirpath):
        if name == file.split(".txt")[0]:
            return "exist"
    os.rename(dirpath + oldname + ".txt", dirpath + name + ".txt")
    # for file in os.listdir(dirpath):
        # if oldname == file.split(".txt")[0]:
        #     os.rename(os.path.join(dirpath, file), os.path.join(dirpath, file.replace(oldname, name, 1)))
        #     for s_file in os.listdir(dirpath):
        #         f = s_file.split("-*-")[0]
        #         if f == oldname:
        #             os.rename(os.path.join(dirpath, s_file), os.path.join(dirpath, s_file.replace(oldname, name, 1)))
        #     print(oldname)
    l = ['/params/', '/results/', '/val/']
    for i in l:
        dirpath = g_path + g_name + i
        os.rename(dirpath + oldname, dirpath + name)
    p = project.query.filter_by(user=g_name, project=oldname, type="visual").first()
    p.project = name
    db.session.commit()
    return "success"
    # return "fail"


@app.route("/code/changename", methods=["post", "get"])
def changeCodeName():
    # data = str(request.get_data(), 'utf8')
    # data = json.loads(data)
    data = getData()
    name = data["name"]
    oldname = data["oldname"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/projects/code/"
    for file in os.listdir(dirpath):
        if name == file.split(".py")[0]:
            return "exist"
    # for file in os.listdir(dirpath):
    #     if oldname == file.split(".py")[0]:
    os.rename(dirpath + oldname + ".py", dirpath + name + ".py")
    os.rename(g_path + g_name + "/save/" + oldname + ".py", g_path + g_name + "/save/" + name + ".py")
    # os.rename(os.path.join(dirpath, file), os.path.join(dirpath, file.replace(oldname, name, 1)))
    p = project.query.filter_by(user=g_name, project=oldname, type="code").first()
    p.project = name
    db.session.commit()
    return "success"
    # return "fail"


@app.route("/visual/findname", methods=["post", "get"])
def findVisualName():
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/projects/visual"
    maxnum = 0
    for file in os.listdir(dirpath):
        if file.endswith(".txt") and file[0:3] == "未命名":
            s = file.split(".txt")[0].split("未命名")[1]
            n = 0 if s == "" else int(s)
            maxnum = maxnum if maxnum > n else (n + 1)
    s_num = "" if maxnum == 0 else str(maxnum)
    return "未命名"+s_num


@app.route("/code/findname", methods=["post", "get"])
def findCodeName():
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/projects/code"
    maxnum = 0
    for file in os.listdir(dirpath):
        if file.endswith(".py") and file[0:3] == "未命名":
            s = file.split(".py")[0].split("未命名")[1]
            n = 0 if s == "" else int(s)
            maxnum = maxnum if maxnum > n else (n + 1)
    s_num = "" if maxnum == 0 else str(maxnum)
    return "未命名"+s_num


@app.route("/visual/leave", methods=["post", "get"])
def visualLeave():
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    data = getData()
    project = data["project"]
    global g_model
    g_model[g_name].pop(project)
    print(g_model)
    return "success"


@app.route("/visual/gettype", methods=["post", "get"])
def visualGetType():
    data = getData()
    project = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    # path = g_path + g_name + "/projects/visual/" + project + ".txt"
    # with open(path, 'r') as f:
    #     j = f.readline()
    #     j = "\"".join(j.split("'"))
    #     data = eval(j)
    # model = ''
    # for p in data['nodeList']:
    #     if p['name'] in ["fea", "ssd", "yolo"]:
    #         model = p['name']
    # d = {"fea": "csv", "changedetection": "image_2"}
    model = RunHelp().getModelType(g_path, g_name, project)
    return {"limit": 2} if model == "change detection" else {"limit": 1}


@app.route("/test/run", methods=["post", "get"])
def testRun():
    files = request.files
    data = request.values.get("data")
    data = json.loads(data)
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    project = data["project"]
    param = data["param"]
    path = g_path + g_name + "/val/" + project + "/"
    if not os.path.exists(path):
        os.makedirs(path)
    for f in data["files"]:
        file = files.get(f)
        file.save(path + f)
        print(files.get(f).mimetype)
    model = RunHelp().getModelType(g_path, g_name, project)
    RunHelp().infer(g_path, g_name, param+".pth.tar", data["files"], project, model)
    return "csv" if model == "fea" else "image"


@app.route("/test/down", methods=["post", "get"])
def testDown():
    data = getData()
    name = data["name"]
    project = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_path + g_name + "/results/" + project
    response = make_response(send_from_directory(dirpath, name, as_attachment=True))
    response.headers["Access-Control-Expose-Headers"] = "Content-disposition"
    return response

@app.route("/test/figshow", methods=["post", "get"])
def testFigShow():
    import plotly.express as px
    import pandas as pd
    data = getData()
    name = data["name"]
    project = data["project"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    output_path = g_path + g_name + "/results/" + project + "/" + name
    deformation_data = pd.read_csv(output_path, encoding='utf-8')

    available_templates = ['ggplot2', 'seaborn', 'simple_white', 'plotly',
                           'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
                           'ygridoff', 'gridon', 'none']
    fig = px.scatter_3d(deformation_data, x='X', y='Y', z='Z',
                        color='S-Mises', color_continuous_scale='rainbow',
                        title='3D: Stress Plot ', template='none',
                        # range_x=[0,1000],range_y=[0,1000],
                        # range_z=[0,1000],
                        )
    fig.update_layout(
        scene=dict(
            aspectmode='data',
            xaxis=dict(showticklabels=True),
            yaxis=dict(showticklabels=True),
            zaxis=dict(showticklabels=True),
        )
    )
    return fig.to_json()


@app.route("/getuser", methods=["get", "post"])
def getUser():
    p = get_permission(request.headers.get("Authorization"))
    if "user_search" not in p:
        return "no_permission"
    users = user.query.all()
    l = []
    for i in range(len(users)):
        u = users[i].dump()
        u["id"] = i
        print(u["role"])
        u["role"] = roles.query.get(u["role"]).name
        l.append(u)
    return json.dumps(l)


@app.route("/deleteuser", methods=["get", "post"])
def deleteUser():
    p = get_permission(request.headers.get("Authorization"))
    if "user_delete" not in p:
        return "no_permission"
    data = getData()
    ids = data["id"]
    for id in ids:
        print(id)
        u = user.query.filter(user.id == id).first()
        print(u)
        name = u.name
        db.session.delete(u)
        db.session.commit()
        utils.delete_dir(name)
    return "success"


@app.route("/updateuser", methods=["get", "post"])
def updateUser():
    p = get_permission(request.headers.get("Authorization"))
    if "user_update" not in p:
        return "no_permission"
    data = getData()
    id = data["id"]
    name = data["name"]
    role = roles.query.filter(roles.name == data["role"]).first().id
    state = 0 if data["state"] == "启用" else 1
    print(id, name, role, state)
    u = user.query.get(id)
    u.name = name
    u.role = role
    u.state = state
    db.session.commit()
    return "success"


@app.route("/adduser", methods=["get", "post"])
def addUser():
    p = get_permission(request.headers.get("Authorization"))
    if "user_add" not in p:
        return {"state": "no_permission"}
    data = getData()
    name = data['name']
    password = data['password']
    role = permission.query.filter(permission.name == data["role"]).first().id
    state = 0 if data["state"] == "启用" else 1
    print(name, password, role, state)
    u = user.query.filter_by(name=name).first()
    if u is not None:
        return {"state": "exist"}
    sha1 = hashlib.sha1()
    sha1.update(password.encode("utf-8"))
    addUser = user(name, sha1.hexdigest(), role, state)
    db.session.add(addUser)
    db.session.commit()
    os.makedirs(name)
    os.makedirs(name + "/val")
    os.makedirs(name + "/data")
    os.makedirs(name + "/params")
    os.makedirs(name + "/projects")
    os.makedirs(name + "/projects/visual")
    os.makedirs(name + "/projects/code")
    os.makedirs(name + "/results")
    os.makedirs(name + "/save")
    os.makedirs(name + "/chart")
    u = user.query.filter_by(name=name).first()
    return {"state": "success", "id": u.id}


@app.route("/getrole", methods=["get", "post"])
def getRole():
    p = get_permission(request.headers.get("Authorization"))
    if "role_search" not in p:
        return "no_permission"
    roles_data = roles.query.all()
    l = []
    name_l = []
    for r in roles_data:
        role = r.dump()
        name_l.append(r.name)
        l.append(role)
    return {"table": l, "list": name_l}


@app.route("/updaterole", methods=["get", "post"])
def updateRole():
    p = get_permission(request.headers.get("Authorization"))
    if "role_update" not in p:
        return "no_permission"
    data = getData()
    name = data["name"]
    id = data["id"]
    r = roles.query.get(id)
    r.name = name
    db.session.commit()
    return "success"


@app.route("/deleterole", methods=["get", "post"])
def deleteRole():
    p = get_permission(request.headers.get("Authorization"))
    if "role_delete" not in p:
        return "no_permission"
    data = getData()
    ids = data["id"]
    role = data["role"]
    role = role if role != '' else '普通用户'
    role_id = permission.query.filter(permission.name == role).first().id
    for id in ids:
        r = permission.query.filter(permission.id == id).first()
        db.session.delete(r)
        db.session.query(user).filter(user.role == id).update({user.role: role_id})
    try:
        db.session.commit()
        return "success"
    except:
        return "error"


@app.route("/addrole", methods=["get", "post"])
def addRole():
    p = get_permission(request.headers.get("Authorization"))
    if "role_add" not in p:
        return "no_permission"
    data = getData()
    name = data["name"]
    useradd = 1 if data["useradd"] == "是" else 0
    userupdate = 1 if data["userupdate"] == "是" else 0
    userdelete = 1 if data["userdelete"] == "是" else 0
    usersearch = 1 if data["usersearch"] == "是" else 0
    roleadd = 1 if data["roleadd"] == "是" else 0
    roleupdate = 1 if data["roleupdate"] == "是" else 0
    roledelete = 1 if data["roledelete"] == "是" else 0
    rolesearch = 1 if data["rolesearch"] == "是" else 0
    r = roles(name)
    db.session.add(r)
    p = permission(name, useradd, userupdate, userdelete, usersearch, roleadd, roleupdate, roledelete, rolesearch)
    db.session.add(p)
    db.session.commit()
    return "success"


@app.route("/getpermission", methods=["get", "post"])
def getPermission():
    p = get_permission(request.headers.get("Authorization"))
    print(p)
    if "role_search" not in p:
        return "no_permission"
    _, role = token_decoder(request.headers.get("Authorization"))
    if role == 0:
        return "no_permission"
    permission_data = permission.query.all()
    l = []
    for per in permission_data:
        p = per.dump()
        l.append(p)
    return json.dumps(l)


@app.route("/updatepermission", methods=["get", "post"])
def updatePermission():
    p = get_permission(request.headers.get("Authorization"))
    if "role_update" not in p:
        return "no_permission"
    data = getData()
    print(data)
    user_add = 1 if data["useradd"] == "是" else 0
    user_update = 1 if data["userupdate"] == "是" else 0
    user_delete = 1 if data["userdelete"] == "是" else 0
    user_search = 1 if data["usersearch"] == "是" else 0
    role_add = 1 if data["roleadd"] == "是" else 0
    role_update = 1 if data["roleupdate"] == "是" else 0
    role_delete = 1 if data["roledelete"] == "是" else 0
    role_search = 1 if data["rolesearch"] == "是" else 0
    name = data["name"]
    id = data["id"]
    p = permission.query.get(id)
    p.name = name
    p.user_add = user_add
    p.user_update = user_update
    p.user_delete = user_delete
    p.user_search = user_search
    p.role_add = role_add
    p.role_update = role_update
    p.role_delete = role_delete
    p.role_search = role_search
    db.session.commit()
    return "success"


@app.route("/getadmin", methods=["get", "post"])
def getAdmin():
    p = get_permission(request.headers.get("Authorization"))
    print(p)
    return "0" if len(p) == 0 else "1"


@app.route("/visual/uploadparam/<string:projectname>/<string:paramname>/<int:i>", methods=["get", "post"])
def visualUploadParam(projectname, paramname, i):
    file = request.files["file"]
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    dirpath = g_name+"/params/" + projectname + "/" + paramname
    try:
        if not os.path.exists(g_name+"/params/" + projectname):
            apply_ascyn(makedir, (g_name, projectname, file, dirpath), fileSave)
            # os.makedirs(g_name+"/params/" + projectName)
        # sleep(1)
        else:
            file.save(dirpath)
        return {"state": "success", "num": str(i)}
    except:
        return {"state": "error", "num": str(i)}


@app.route("/getgpuinfo", methods=["get", "post"])
def getGPUInfo():
    out, err = popen3("nvidia-smi")

    # 显存
    pattern = re.compile(r'\d+MiB / \d+MiB')  # 查找数字
    gpu_memory = pattern.findall(str(out))

    percent = re.compile(r'\d+%')
    gpu_util = percent.findall(str(out))

    l = []
    for i in range(len(gpu_memory)):
        l.append({"no": i, "memory": gpu_memory[i], "util": gpu_util[i*2+1]})
    return {"gpu_info": l}


@app.route("/getcpuinfo", methods=["get", "post"])
def getCPUInfo():
    out, err = popen3("free -m")
    out = str(out).split(" ")
    nums = []
    for o in out:
        if not (o == '' or "\\x" in o or 'b' in o):
            nums.append(o)
        if "\\n" in o and '\\x' not in o.split("\\n")[0]:
            nums.append(o.split("\\n")[0])

    cpu_state = str(psutil.cpu_percent(0))+"%"
    phymem = psutil.virtual_memory()
    memory_state = "%5s%% %6s/%s"%(
            phymem.percent,
            str(int(phymem.used/1024/1024))+"M",
            str(int(phymem.total/1024/1024))+"M"
            )

    return {"cpu_state": cpu_state, "memory_state": memory_state, "memory": nums[0:6]}


@app.route("/updatepassword", methods=["get", "post"])
def updatePassword():
    data = getData()
    old_pass = data["old"]
    new_pass = data["new"]
    print(old_pass, new_pass)
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    u = user.query.filter_by(name=g_name).first()
    sha1 = hashlib.sha1()
    sha1.update(old_pass.encode("utf-8"))
    if sha1.hexdigest() != u.password:
        return "password error"
    sha1 = hashlib.sha1()
    sha1.update(new_pass.encode("utf-8"))
    u.password = sha1.hexdigest()
    db.session.commit()
    return "success"


@app.route("/saveinfolog", methods=["get", "post"])
def saveInfoLog():
    data = getData()
    date = data["date"]
    op = data["op"]
    time = data["time"]
    log = date + " " + op + " " + time + "\n"
    print(log)
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    f = open(g_name + "/log.txt", 'a')
    f.write(log)
    f.close()
    return "success"


@app.route("/getinfolog", methods=["get", "post"])
def getInfoLog():
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    f = open(g_name + "/log.txt", 'r')
    logs = []
    log = f.readline()
    while log != "":
        logs.append(log.split(" "))
        log = f.readline()
    f.close()
    date = logs[0][0]
    l = []
    infos = []
    for log in logs:
        if log[0] == date:
            infos.append({"op": " ".join(log[1:-1]), "time": log[-1]})
        else:
            l.append({"date": date, "infos": infos})
            date = log[0]
            infos = [{"op": " ".join(log[1:-1]), "time": log[-1]}]
    l.append({"date": date, "infos": infos})
    return {"log": l}


@app.route("/getallrunlog", methods=["get", "post"])
def getAllRunLog():
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    files = os.listdir(os.path.join(g_name, "logs"))
    l = []
    for file in files:
        project = file.split("_")[0]
        day = file.split("_")[1]
        day = day[0:4] + "-" + day[4:6] + "-" + day[6:8]
        time = file.split("_")[-1].replace(".txt", "")
        l.append({"project": project, "day": day, "time": time})
    return {"logs": l}


@app.route("/getrunlog", methods=["get", "post"])
def getRunLog():
    # data = getData()
    g_name, _ = token_decoder(request.headers.get("Authorization"))
    project = "maskrcnn"
    name = "20220820_19:11:51"
    f = open(os.path.join(g_name, "logs", "_".join([project, name]) + ".txt"), 'r')
    logs = []
    log = f.readline()
    while log != "":
        logs.append(log)
        log = f.readline()
    f.close()
    s = "\n".join(logs)
    return {"log": s}

@app.route("/connectserver", methods=["get", "post"])
def connectServer():
    data = getData()
    host = data["host"]
    port = data["port"]
    user = data["user"]
    password = data["password"]
    print(type(int(port)))
    SSH = utils.SshClass(host, user, port=int(port))
    state = SSH.conn_by_pwd(password)
    return {"state": "success" if state else "fail"}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, threaded=True)

