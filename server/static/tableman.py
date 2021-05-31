from browser import document, window, aio
import json
import helper


class TableMan:
    def __init__(self):
        self.save_method = ''        # hospedes.rpc_save
        self.new_id_method = ''      # hospedes.rpc_new_id
        self.get_record_method = ''  # hospedes.rpc_get
        self.query_method = ''       # hospedes.rpc_query

        self.div_id_tag = ''         # id of the div containg the form
        self.uuid_id_tag = 'uuid'    # id of the primary key / field name in the form
        self.focus_id_tag = ''       # id of the field to focus on insertion
        self.form_class_tag = ''     # class of the form fields
        self.search_table_cols = []  # [('Label1', 'field1'), (Label2, 'field2), ('Etc', 'etc')]
                                     # Table header
        self.table_head_id = ''      # Table header id
        self.table_tbody_id = ''     # Table body id
        self.table_row_class = ''    # Table rows class name

        self.btn_new_record = ''     # New record button id
        self.btn_save_record = ''    # Save record button id
        self.input_search = ''       # Search input field id

    def bind_controls(self):
        document[self.btn_new_record].bind("click", self.new_record)
        document[self.btn_save_record].bind("click", self.save_record)
        document[self.input_search].bind("keypress", self.search_keypress)

    def clear_form(self):
        for field in document.select('.%s' % self.form_class_tag):
            field.value = ""

    def new_record(self, *args, **kwargs):
        params = dict()
        params['method'] = self.new_id_method
        status, data = helper.post_server(window.glb_UserName, window.glb_Password, params)
        self.clear_form()
        rec_uuid = document.select('.%s#%s' % (self.form_class_tag, self.uuid_id_tag))[0]
        rec_uuid.value = json.loads(data)
        document.select('.%s#%s' % (self.form_class_tag, self.focus_id_tag))[0].focus()

    def save_record(self, *args, **kwargs):
        params = dict()
        params['method'] = self.save_method
        fields = document.select('#%s .%s' % (self.div_id_tag, self.form_class_tag))
        for item in fields:
            params[item.id] = item.value
        status, data = helper.post_server(window.glb_UserName, window.glb_Password, params)
        if status == 200:
            aio.run(self.show_record(params[self.uuid_id_tag]))
        else:
            pass
            # todo

    async def show_record(self, uuid):
        params = dict()
        params['method'] = self.get_record_method
        params[self.uuid_id_tag] = uuid
        status, data = helper.post_server(window.glb_UserName, window.glb_Password, params)
        if status == 200:
            record = json.loads(data)
            form_elements = document.select('#%s .%s' % (self.div_id_tag, self.form_class_tag))
            for item in form_elements:
                item.value = record[item.id]

    async def highlight_table_line(self, element):
        rows = document.select("#%s .%s" % (self.table_tbody_id, self.table_row_class))
        for row in rows:
            row.classList.remove("bg-info")
        element.classList.add("bg-info")

    def get_record(self, ev):
        aio.run(self.show_record(ev.currentTarget.id))
        aio.run(self.highlight_table_line(ev.currentTarget))

    def make_table(self, records):
        tbl_head = '<tr>'
        for label, col in self.search_table_cols:
            tbl_head += '<th scope = "col">' + label + '</th>'
        tbl_head += '</tr>'
        document[self.table_head_id].html = tbl_head

        tbl_body = ''
        for record in records:
            tbl_body += '<tr class="%s" id="%s">' % (self.table_row_class, record[self.uuid_id_tag])
            for label, col in self.search_table_cols:
                tbl_body += '<td>' + record[col] + '</td>'
            tbl_body += '</tr>'

        document[self.table_tbody_id].html = tbl_body
        for record in records:
            document["%s" % record[self.uuid_id_tag]].bind("click", self.get_record)

    async def search_records(self, query=None):
        params = dict()
        params['method'] = self.query_method
        params['query'] = query if query else document[self.input_search].value
        status, data = helper.post_server(window.glb_UserName, window.glb_Password, params)
        records = json.loads(data)
        self.make_table(records)

    def search_keypress(self, ev):
        if ev.keyCode == 13:
            aio.run(self.search_records())
