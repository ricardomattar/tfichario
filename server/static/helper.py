from browser import document, ajax, window, load, aio
from hashlib import sha1
import time
import json

default_timeout = 2

def get_timestamp():
    return str(int(time.time()) + window.timestamp_diff).strip()


def timeout_func():
    pass


async def set_timestamp_diff():
    req = ajax.Ajax()
    req.open('GET', '/timestamp', False)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    req.set_timeout(default_timeout, timeout_func)
    req.send()
    status = req.status
    data = req.text
    window.timestamp_diff = int(time.time() - int(data))


def post_server(username, pw, pr):
    req = ajax.Ajax()
    timestamp = get_timestamp()
    password_hash = sha1(bytes(pw.strip())).hexdigest()
    hash = sha1(bytes(timestamp + json.dumps(pr) + password_hash)).hexdigest()
    req.open('POST', '/brv1', False)
    req.set_timeout(default_timeout, timeout_func)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    post = dict()
    post['timestamp'] = get_timestamp()
    post['username'] = username.strip()
    post['hmac'] = hash
    post['params'] = pr
    req.send(json.dumps(post))

    status = req.status
    data = req.text

    document["srv_message_1"].value = status
    if status != 200:
        document["srv_message_2"].value = data
    else:
        document["srv_message_2"].value = 'OK'

    return (status, data)


def user_logoff(*args, **kwargs):
    window.glb_UserName = ''
    window.glb_Password = ''
    document['logged_user'].text = 'Fazer login'


def user_login(*args, **kwargs):
    params = dict()
    params['method'] = 'usuarios.rpc_authenticate'
    status, data = post_server(document["login_username"].value,
               document["login_password"].value,
               params)
    document["srv_message_1"].text = status
    document["srv_message_2"].text = data

    if (data == "true"):
        window.glb_UserName = document["login_username"].value
        window.glb_Password = document["login_password"].value
        document["logged_user"].text = window.glb_UserName
        document["login_username"].text = ""
        document["login_password"].text = ""

    else:
        window.glb_UserName = ""
        window.glb_UserName = ""
        document["login_username"].text = ""
        document["login_password"].text = ""
        document["logged_user"].text = "Fazer login"
        document["login_username"].focus()
