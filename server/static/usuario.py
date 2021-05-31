from browser import document
import helper
import tableman

def mudar_senha(*args, **kwargs):
    params = dict()
    params['method'] = 'usuarios.rpc_change_password'
    params['new_password1'] = document['new_password1'].value
    params['new_password2'] = document['new_password2'].value
    params['username'] = document['username'].value

    status, data = helper.post_server(params['username'], document['cp_password'].value, params)

document["btn_salvar_senha"].bind("click", mudar_senha)

usuarios = tableman.TableMan()

usuarios.save_method = 'usuarios.rpc_save'
usuarios.new_id_method = 'usuarios.rpc_new_id'
usuarios.get_record_method = 'usuarios.rpc_get'
usuarios.query_method = 'usuarios.rpc_query'

usuarios.div_id_tag = 'div_usuario'
usuarios.uuid_id_tag = 'usuario_id'  # uuid
usuarios.focus_id_tag = 'nome'
usuarios.form_class_tag = 'f_usuario'
usuarios.search_table_cols = [('Nome', 'nome'), ('Classe', 'classe')]
usuarios.table_head_id = 'table_usuarios_head'
usuarios.table_tbody_id = 'table_usuarios_body'
usuarios.table_row_class = 'linhausuario'

usuarios.btn_new_record = 'btn_novousuario'
usuarios.btn_save_record = 'btn_salvar_usuario'
usuarios.input_search = 'pesquisar_usuario'

usuarios.bind_controls()
