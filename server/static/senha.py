from browser import document
import helper

def mudar_senha(*args, **kwargs):
    params = dict()
    params['method'] = 'usuarios.rpc_change_password'
    params['new_password1'] = document['new_password1'].value
    params['new_password2'] = document['new_password2'].value
    params['username'] = document['username'].value

    status, data = helper.post_server(params['username'], document['cp_password'].value, params)


document["btn_salvar_senha"].bind("click", mudar_senha)
