import matplotlib.pyplot as plt
import numpy as np
import os
from flask import request
import json
import jwt
import time


def getChart(train_data, test_data, type):
    epoch = len(train_data)
    # x_data = resolveEpoch(epoch)
    train_ndarray = np.array(train_data)
    test_ndarray = np.array(test_data)
    print(train_ndarray)
    print(test_ndarray)
    # y_data = train_ndarray[x_data]
    # y_data2 = test_ndarray[x_data]
    x_data = [(i+1) for i in range(epoch)]
    ln1, = plt.plot(x_data, train_ndarray, color='red', linewidth=2.0, linestyle='--')
    ln2, = plt.plot(x_data, test_ndarray, color='blue', linewidth=2.0, linestyle='-.')
    plt.title(type)
    plt.legend(handles=[ln1, ln2], labels=['train', 'val'])
    plt.xlabel("epoch")
    plt.ylabel(type)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    # plt.show()
    plt.savefig("/Users/sunfan/PycharmProjects/flaskProject/chart/" + type+".jpg")


def del_file(filepath, i):
    del_list = os.listdir(filepath)
    for f in del_list:
        if f.split(" ")[-1].split(".")[0] == str(i):
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)


def search_file(i, dirpath):
    # sear_file = os.listdir(g_path + g_name+"/results/" + project)
    for f in os.listdir(dirpath):
        index = f.split(".")[0].split(" ")[-1]
        if index == str(i):
            return f
    return "None"


def getData():
    data = request.get_data()
    data = str(data, 'utf8')
    data = json.loads(data)
    return data


def popen3(cmd):
    import warnings
    msg = "os.popen3 is deprecated.  Use the subprocess module."
    warnings.warn(msg, DeprecationWarning, stacklevel=2)

    import subprocess
    popen = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             shell=True,
                             )
    stdout, stderr = popen.communicate()

    return stdout, stderr


def token_encoder(name, role):
    d = {
        'exp': time.time() + 3000,  # (Expiration Time) 此token的过期时间的时间戳
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': 'deepL',  # (Issuer) 指明此token的签发者

        'data': {
            'username': name,
            'timestamp': time.time(),
            'role': role
        }
    }

    jwt_encode = jwt.encode(d, 'deep', algorithm='HS256')

    return jwt_encode


def token_decoder(token):
    print(token)
    jwt_decode = jwt.decode(token, 'deep', issuer='deepL', algorithms=['HS256'])

    return jwt_decode['data']['username'], jwt_decode['data']['role']
    # 打印解密后信息
    # {'exp': 1622604718.6736836, 'iat': 1622601718.6736836, 'iss': 'Issuer', 'data': {'username': 'xjj', 'timestamp': 1622601718.6736836}}


def get_matrix_name(l):
    dic = {"fea": "R_square", "change detection": "precision"}
    for item in l:
        if item in ["ssd", "yolo", "fea", "change detection"]:
            return dic[item]


def delete_dir(name):
    try:
        os.removedirs(name)  # 递归地删除目录。如果子目录成功被删除，则将会成功删除父目录，子目录没成功删除，将抛异常。
        return "success"
    except:
        return "fail"


def apply_ascyn(func, args, callback):
    func(args[0], args[1])
    callback(args[2], args[3])

def makedir(g_name, projectName):
    os.makedirs(g_name+"/params/" + projectName)
    return "ok"

def fileSave(file, dirpath):
    file.save(dirpath)

import paramiko


class SshClass:
    """
    ssh连接对象
    本对象提供了密钥连接、密码连接、命令执行、关闭连接
    """
    ip = ''
    port = 22
    username = ''
    timeout = 0
    ssh = None

    def __init__(self, ip, username, port=22, timeout=30):
        """
        初始化ssh对象
        :param ip: str  主机IP
        :param username: str  登录用户名
        :param port: int  ssh端口
        :param timeout: int  连接超时
        """
        self.ip = ip
        self.username = username
        self.port = port
        self.timeout = timeout
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh = ssh

    def conn_by_pwd(self, pwd):
        """
        密码连接
        :param pwd: str  登录密码
        :return: ssh连接对象
        """
        self.ssh.connect(hostname=self.ip, port=self.port, username=self.username, password=pwd)
        if self.ssh:
            return True
        else:
            self.close()
            return False


    def close(self):
        """
        关闭当前连接
        :return:
        """
        if self.ssh:
            self.ssh.close()
            return True
        else:
            raise Exception("ssh关闭失败，当前对象并没有ssh连接.")
            return False


