import tableman

hospedes = tableman.TableMan()

hospedes.save_method = 'hospedes.rpc_save'
hospedes.new_id_method = 'hospedes.rpc_new_id'
hospedes.get_record_method = 'hospedes.rpc_get'
hospedes.query_method = 'hospedes.rpc_query'

hospedes.div_id_tag = 'div_ficha'
hospedes.uuid_id_tag = 'uuid'  # uuid
hospedes.focus_id_tag = 'nome'
hospedes.form_class_tag = 'f_hospede'
hospedes.search_table_cols = [('Nome', 'nome'), ('CPF', 'cpf'), ('RG', 'rg')]
hospedes.table_head_id = 'table_hospedes_head'
hospedes.table_tbody_id = 'table_hospedes_body'
hospedes.table_row_class = 'linhaficha'

hospedes.btn_new_record = 'btn_novaficha'
hospedes.btn_save_record = 'btn_salvar_ficha'
hospedes.input_search = 'pesquisar'

hospedes.bind_controls()

