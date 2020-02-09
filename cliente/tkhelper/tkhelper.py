# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 07:00:36 2015

@author: ricardo

"""
import Tkinter
import tktable

def show_modal(master, cls):
       window = Tkinter.Toplevel()
       window.focus_set()
       window.grab_set()
       window.transient(master)
       
       l = cls(window)
       window.wait_window(window)
    
class PasswordDialog(Tkinter.Toplevel):
    def __init__(self, username, password):
        Tkinter.Toplevel.__init__(self)
        self.username = username
        self.password = password
        self.entry = Tkinter.Entry(self, show='*')
        self.entry.bind("<KeyRelease-Return>", self.StorePassEvent)
        self.entry.pack()
        self.button = Tkinter.Button(self)
        self.button["text"] = "Submit"
        self.button["command"] = self.StorePass
        self.button.pack()

    def StorePassEvent(self, event):
        self.StorePass()

    def StorePass(self):
        self.password = self.entry.get()
        self.destroy()
        #print '1: Password was', self.parent.password
    
class TkWidget(object):
    def get(self):
        return self.data.get()
        
    def set(self, value):
        self.data.set(value)

        
class TkString(TkWidget):
    def __init__(self,
                 parent = None,
                 label = '',
                 label_col = 0,
                 label_row = 0,
                 wid_col = 0,
                 wid_row = 0,
                 wid_width = 50,
                 command=None
                 ):
                 
        self.data = Tkinter.StringVar()
        self.parent = parent
        self.command = command
        self.label = Tkinter.Label(self.parent, text=label).grid(column = label_col, row=label_row, sticky=Tkinter.W)
        self.widget = Tkinter.Entry(self.parent, width = wid_width, textvariable = self.data)
        self.widget.grid(column = wid_col, row = wid_row, sticky = Tkinter.W)
        if self.command:
            self.widget.bind( "<KeyRelease-Return>", self.command )
            
    def get(self):
        return self.widget.get()
        

class TkText(object):
    def __init__(self,
                 parent = None,
                 label = '',
                 label_col = 0,
                 label_row = 0,
                 wid_col = 0,
                 wid_row = 0,
                 wid_width = 50,
                 wid_height=1
                 ):
                 
        self.parent = parent
        self.label = Tkinter.Label(self.parent, text=label).grid(column = label_col, row=label_row, sticky=Tkinter.W)
        self.widget = Tkinter.Text(self.parent, width = wid_width, height=wid_height)
        self.widget.grid(column = wid_col, row = wid_row, sticky = Tkinter.W)
            
    def get(self):
        return self.widget.get(1.0, Tkinter.END)
        
    def set(self, value):
        try:
            self.widget.delete(1.0, Tkinter.END)
            
        finally:
            self.widget.insert(Tkinter.END, value)
                

class TkPassword(TkWidget):
    def __init__(self,
                 parent = None,
                 label = '',
                 label_col = 0,
                 label_row = 0,
                 wid_col = 0,
                 wid_row = 0,
                 wid_width = 50,
                 command=None
                 ):
                 
        self.data = Tkinter.StringVar()
        self.parent = parent
        self.command = command
        self.label = Tkinter.Label(self.parent, text=label).grid(column = label_col, row=label_row, sticky=Tkinter.W)
        self.widget = Tkinter.Entry(self.parent, width = wid_width, textvariable = self.data, show="#")
        self.widget.grid(column = wid_col, row = wid_row, sticky = Tkinter.W)
        if self.command:
            self.widget.bind( "<KeyRelease-Return>", self.command )
            
    def get(self):
        return self.widget.get()




class TkOption(TkWidget):
    def __init__(self,
                 parent = None,
                 label = '',
                 label_col = 0,
                 label_row = 0,
                 wid_col = 0,
                 wid_row = 0,
                 wid_width = 50,
                 options = ()
                 ):
                 
        self.data = Tkinter.StringVar()
        self.parent = parent
        self.label = Tkinter.Label(self.parent, text=label).grid(column = label_col, row=label_row, sticky=Tkinter.W)
        self.widget = Tkinter.OptionMenu(self.parent, self.data, *options)
        self.widget.grid(column = wid_col, row = wid_row, sticky = Tkinter.W)

class TkButton(TkWidget):
    def __init__(self,
                 parent = None,
                 label = '',
                 col = 0,
                 row = 0,
                 command=None
               ):
        self.parent = parent
        self.command = command
        self.button = Tkinter.Button(self.parent, text=label, command=self.command)
        self.button.grid(row = row, column = col, sticky = Tkinter.W)


class TkSearch(object):
    def __init__(self,
                 parent=None,
                 col=0,
                 row=0,
                 rowspan=30,
                 width=40,
                 command_search=None,
                 command_listclick=None
                 ):
        self.col=col
        self.row=row
        self.rowspan = rowspan
        self.width = width
        self.command_search = command_search
        self.command_listclick = command_listclick
        
        self.search_frame = Tkinter.LabelFrame(parent, text = 'Pesquisa')
        self.search_frame.grid(row = self.row, column = self.col, sticky = Tkinter.N)
        self.yScroll  =  Tkinter.Scrollbar ( self.search_frame, orient=Tkinter.VERTICAL )
        self.yScroll.grid ( row=0, column=1, rowspan=self.rowspan, sticky=Tkinter.N+Tkinter.S )
        
        self.recordvar = Tkinter.StringVar()
        self.record_list = Tkinter.Listbox(self.search_frame, listvariable = self.recordvar, \
            selectmode = Tkinter.SINGLE, yscrollcommand=self.yScroll.set, height = self.rowspan)
        self.record_list.config(width=self.width)
        self.record_list.grid(row=0, column=0, rowspan=self.rowspan, sticky = Tkinter.W)
        self.recordvar.set('')
        self.yScroll["command"]  =  self.record_list.yview
        
        self.record_list.bind ( "<ButtonRelease-1>", self.record_list_click )
        
        Tkinter.Label(self.search_frame, text="Procurar").grid(column = 0, row=self.rowspan, sticky=Tkinter.W)
        self.search_text = TkString(self.search_frame, u'Procurar',   0, self.rowspan, 0, self.rowspan+1, self.width, command=self.search)
        
    def set_list(self, lst):
        self.record_list.delete(0, Tkinter.END)
        sl = sorted(lst, key=lambda s: s.lower())
        for item in sl:
            self.record_list.insert(Tkinter.END, item )
        
    def record_list_click(self, event):
        record = self.record_list.get(self.record_list.curselection()[0])
        self.command_listclick(record)
        
    def search(self, event):
        search_text = self.search_text.get()
        self.command_search(search_text)
        
class Search(object):
    def __init__(self,
                 parent=None,
                 col=0,
                 row=0,
                 rowspan=30,
                 width=40,
                 command_search=None,
                 command_listclick=None,
                 header = ['']
                 ):
        
        self.col=col
        self.row=row
        self.rowspan = rowspan
        self.width = width
        self.command_search = command_search
        self.command_listclick = command_listclick
        self.header = header
        self.cols = len(self.header)
        self.search_frame = Tkinter.LabelFrame(parent, text = 'Pesquisa')
        self.search_frame.grid(row = self.row, column = self.col, sticky = Tkinter.N)
        
        self.recordvar = tktable.ArrayVar()
        self.record_list = tktable.Table(self.search_frame,
                                         rows=1,
                                         cols=self.cols,
                                         state='disabled',
                                         width=6,
                                         height=self.rowspan,
                                         titlerows=1,
                                         titlecols=0,
                                         roworigin=-1,
                                         colorigin=0,
                                         selectmode='browse',
                                         selecttype='row',
                                         rowstretch='unset',
                                         colstretch='last',
                                         justify=Tkinter.LEFT,
                                         #browsecmd=self.browsecmd,
                                         flashmode='on',
                                         variable=self.recordvar,
                                         usecommand=0,
                                         command=self.test_cmd)
        
        self.record_list.config(width=self.width)
        self.record_list.grid(row=0, column=0, rowspan=self.rowspan, sticky = Tkinter.W)

        self.yScroll  =  Tkinter.Scrollbar ( self.search_frame,
                                            orient=Tkinter.VERTICAL,
                                            command=self.record_list.yview_scroll)
        self.yScroll.grid ( row=0, column=1, rowspan=self.rowspan, sticky=Tkinter.N+Tkinter.S )

        self.record_list.config(yscrollcommand=self.yScroll.set)
        
        self.record_list.bind ( "<ButtonRelease-1>", self.record_list_click )
        self.record_list.bind( "<KeyRelease-Return>", self.record_list_click )        
        
        Tkinter.Label(self.search_frame, text="Procurar").grid(column = 0, row=self.rowspan, sticky=Tkinter.W)
        self.search_text = TkString(self.search_frame, u'Procurar',   0, self.rowspan, 0, self.rowspan+1, self.width, command=self.search)
        
        self.reset_table(0)

    def reset_table(self, rowcount):
        self.record_list.clear_all()
        self.record_list.tag_configure('left', anchor='w')
        self.record_list.tag_col('left', 0, 1, 2 ,3)
        for key, value in self.header.iteritems():
            col, title, width = value
            self.set_cel(col, -1, title)
            self.record_list.set_column_width(col, width)
            self.record_list.tag_configure('alignment', justify='left' )
        
    def set_cel(self, col, row, value):
        index = '%i,%i' % (row, col)
        self.recordvar[index] = value
        
    def get_cel(self, col, row):
        index = '%i,%i' % (row, col)
        value = self.record_list.get(index)
        return value
        
    def set_list(self, lst):
        rowcount = len(lst) + 1
        rowspan = rowcount
        if rowcount > self.rowspan:
            rowspan = self.rowspan
            
        self.record_list.config(state='normal', rows=rowcount, height=rowspan )
        self.reset_table(len(lst))
        
        row = 0        
        for record in lst:
            for key, value in self.header.iteritems():
                c, t, w = value
                self.set_cel(c, row, record[key])
                self.record_list.reread()
            row = row + 1
        self.record_list.config(state='disabled')        
        
    def record_list_click(self, event):
        line = self.record_list.curselection()
        record = {}
        for index in line:
            value = self.record_list.get(index)
            col = index.split(',')[-1]
            for k, v in self.header.iteritems():
                c, l, w = v
                if int(col) == int(c):
                    record[k] = value
                    break
                
        self.command_listclick(record)
        
    def search(self, event):
        search_text = self.search_text.get()
        self.command_search(search_text)
        
    def selcmd(self, event):
        print 'pfff'
        
    def browsecmd(self, event):
        print("event:", event.__dict__)
        print("curselection:", self.record_list.curselection())
        print("active cell index:", self.record_list.index('active'))
        print("active:", self.record_list.index('active', 'row'))
        print("anchor:", self.record_list.index('anchor', 'row'))
        line = self.record_list.curselection()
        record = {}
        for index in line:
            value = self.record_list.get(index)
            col = index.split(',')[-1]
            for k, v in self.header.iteritems():
                c, l, w = v
                if int(col) == int(c):
                    record[k] = value
                    break
                
        self.command_listclick(record)
        
        
    def test_cmd(self, event):
        if event.i == 0:
            return '%i, %i' % (event.r, event.c)
        else:
            return 'set'
        