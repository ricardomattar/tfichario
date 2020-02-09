#!/usr/bin/env python
# -*- coding: latin1 -*-

import Tkinter
import tkMessageBox
import StringIO
import copy
import datetime
import time
import os
import sys
import socket
import struct
import threading
import hashlib
import zlib
import pickle

from tkhelper import TkString
from tkhelper import TkOption

import post
    
class App:
    def __init__(self, master):
        self.master = master
        self.master.title('Usuarios')
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = ''
        self.server_timedelta = datetime.datetime.now() - datetime.datetime.now()
        self.encryptionkey = '*' * 32
        self.current_user = None
        self.current_user_edited = False
        self.user_dispatch_list = []
        
        frame = Tkinter.Frame(master, borderwidth=2)
        frame.pack()
        
        form_frame = Tkinter.LabelFrame(frame, text = 'User')
        rec_frame = Tkinter.LabelFrame(form_frame, text = '')
        search_frame = Tkinter.LabelFrame(frame, text = 'Procura')
        server_frame = Tkinter.LabelFrame(frame, text = 'Server')
        
        form_frame.grid(row = 0, column = 5, sticky = Tkinter.N)
        rec_frame.grid(row = 28, column = 0, sticky = Tkinter.N)
        
        search_frame.grid(row = 0, column = 0, sticky = Tkinter.N)
        server_frame.grid(row = 1, column = 0, sticky = Tkinter.N+Tkinter.W)
        
        #usuario_id              = Column(UUID       , primary_key = True)
        #cadastro_data           = Column(DateTime   , nullable = False, default=datetime.datetime.utcnow)
        #last_login              = Column(DateTime   , nullable = False, default=datetime.datetime.utcnow)
        #email                   = Column(String(70))
        #status                  = Column(String(1)  , nullable = False, default = '1')
        #nome                    = Column(String(70) , nullable = False)
        #password                = Column(String(32) , nullable = False)
        
        #user frame
        status_list = ("Ativo", "Inativo")
        self.usuario_id    = TkString(form_frame, u'UUID',            0, 0, 1, 0, 45)
        self.nome          = TkString(form_frame, u'Nome',            0, 1, 1, 1, 45)
        self.status        = TkOption(form_frame, u'Situação',        0, 2, 1, 2, 45, status_list)
        self.classe        = TkString(form_frame, u'Classe',          0, 3, 1, 3, 45)
        self.email         = TkString(form_frame, u'E-Mail',          0, 4, 1, 4, 45)
        self.last_login    = TkString(form_frame, u'Ultimo login',    0, 5, 1, 5, 45)
        self.data_cadastro = TkString(form_frame, u'Data cadastro',   0, 6, 1, 6, 45)
        self.senha         = TkString(form_frame, u'Senha',           0, 7, 1, 7, 45)
        
        
        self.button_save = Tkinter.Button(rec_frame, text="Save", command=self.save)
        self.button_save.grid(row = 1, column = 0, sticky = Tkinter.W)
        
        self.button_new = Tkinter.Button(rec_frame, text="New ID", command=self.new)
        self.button_new.grid(row = 0, column = 0, sticky = Tkinter.W)
        self.v_new_id = Tkinter.StringVar()
        self.newid = Tkinter.Entry(rec_frame, width = 11, textvariable = self.v_new_id)
        self.newid.grid(row = 0, column = 1, sticky = Tkinter.W)
        self.newid.bind( "<KeyRelease-Return>", self.new )
        
        #twserver frame
        Tkinter.Label(server_frame, text="Select twserver:").grid(columnspan=2, column = 7, row=0, sticky=Tkinter.W)
        self.servervar = Tkinter.StringVar()
        self.servervar.set (' '.join(['root@li61-58.members.linode.com:/home/secvoice/',
                                      'root@li15-205.members.linode.com:/home/teste/',
                                      'root@li15-205.members.linode.com:/home/ricardo/']))
        
        self.serverlist = Tkinter.Listbox(server_frame, listvariable = self.servervar, \
            selectmode = Tkinter.SINGLE, width = 50, height = 3)
        self.serverlist.grid(row=0, column=8, sticky = Tkinter.W)
        
        #self.v_server.set(servers_option_list[0])
        
        Tkinter.Label(server_frame, text="Key hash sequence").grid(columnspan=2, column = 7, row=2, sticky=Tkinter.W)
        self.v_sequence        = Tkinter.StringVar()
        self.v_sequence.set('0001')
        self.sequence          = Tkinter.Entry(server_frame, width = 5, textvariable = self.v_sequence)
        self.sequence          .grid(column = 8, row = 2, sticky = Tkinter.W)
        self.button_export_server = Tkinter.Button(server_frame, text="Export to twserver", command=self.export_server)
        self.button_export_server.grid(row = 3, column = 7)
        self.v_message = Tkinter.StringVar()
        self.v_message.set('----')
        Tkinter.Label(server_frame, textvariable = self.v_message).grid(column = 8, row=3, sticky=Tkinter.W)
        
        #user search frame
#        self.button_get_online = Tkinter.Button(search_frame, text="Get online users", command=self.get_online)
#        self.button_get_online.grid(row = 1, column = 2, sticky = Tkinter.W)
#        self.button_get_talking = Tkinter.Button(search_frame, text="Get talking users", command=self.get_talking)
#        self.button_get_talking.grid(row = 2, column = 2, sticky = Tkinter.W)
        
        self.yScroll  =  Tkinter.Scrollbar ( search_frame, orient=Tkinter.VERTICAL )
        self.yScroll.grid ( row=0, column=1, rowspan=20, sticky=Tkinter.N+Tkinter.S )
        
        self.uservar = Tkinter.StringVar()
        self.userlist = Tkinter.Listbox(search_frame, listvariable = self.uservar, \
            selectmode = Tkinter.SINGLE, yscrollcommand=self.yScroll.set, height = 20)
        self.userlist.grid(row=0, column=0, rowspan=20, sticky = Tkinter.W)
        self.uservar.set('')
        self.yScroll["command"]  =  self.userlist.yview
        
        self.userlist.bind ( "<ButtonRelease-1>", self.userlist_click )
        
        Tkinter.Label(search_frame, text="Procurar").grid(column = 0, row=29, sticky=Tkinter.W)
        self.text_search = Tkinter.Entry(search_frame, width = 40)
        self.text_search.grid(row = 30, column = 0)
        self.text_search.bind( "<KeyRelease-Return>", self.search )
        
        lth = threading.Thread(target = self.listenner, args = ())
        lth.setDaemon(True)
        lth.start()
        
    def server_timestamp(self):
        dt = datetime.datetime.now() + self.server_timedelta
        return struct.pack('d', time.mktime(dt.timetuple()))
        
    def listenner(self):
        while True:
            try:
                incoming_data, addr = self.sock.recvfrom(16384)
                msg = Message(incoming_data)
                #HDR_ADM_MESSAGE        = 'ADMN'
                #COMMAND_SET_USER       = 'SETU'
                #COMMAND_GET_USER       = 'GETU'
                #COMMAND_EXPORT_USERS   = 'EXPU'
                #COMMAND_GET_ONLINE     = 'GETO'
                #COMMAND_GET_TALKING    = 'GETT'
                if msg.header == HDR_ADM_MESSAGE:
                    adm_msg = AdmMessage(key = self.encryptionkey, packet = msg.encrypted)
                    if adm_msg.command == COMMAND_GET_TIMESTAMP:
                        server_timestamp = struct.unpack('d', msg.timestamp)[0]
                        self.server_timedelta = datetime.datetime.fromtimestamp(server_timestamp) - datetime.datetime.now()
                        continue
                        
                    if adm_msg.command == COMMAND_SET_USER:
                        self.user_dispatch_list.remove(adm_msg.user_id)
                        continue
                        
                    if adm_msg.command == COMMAND_GET_ONLINE:
                        data = zlib.decompress(adm_msg.data)
                        user_list = pickle.loads(data)
                        s_list = [ uuid_form(user) for user in user_list ]
                        user_list_string = ' '.join(s_list)
                        self.uservar.set(user_list_string)
                        continue
                        
                    if adm_msg.command == COMMAND_GET_TALKING:
                        data = zlib.decompress(adm_msg.data)
                        user_list = pickle.loads(data)
                        s_list = [ uuid_form(user) for user in user_list ]
                        user_list_string = ' '.join(s_list)
                        self.uservar.set(user_list_string)
                        continue
                        
            except:
                print sys.exc_info()[0]
                print sys.exc_info()[1]
                
    def save(self):
        uuid = self.v_uuid.get()
        edituser = copy.deepcopy(keyring.user[uuid])
        
        if not self.v_OS.get() in ['wmob', 'linx', 'wind']:
            tkMessageBox.showerror("Error", "Please select a target OS")
            return
            
        try:
            expire_date = datetime.date(*time.strptime(self.v_expire_date.get(), '%Y-%m-%d')[:3])
        except:
            #msg = self.v_expire_date.get()
            #msg = msg + ' INCORRECT EXPIRE DATE FORMAT'
            self.expire_date.select_range(0, Tkinter.END)
            tkMessageBox.showerror("Error", "Incorrect date format")
            return
            
        edituser.OS            = self.v_OS             .get()
        edituser.expire_date   = expire_date
        edituser.Name          = self.v_Name           .get()
        edituser.Company_Name  = self.v_Company_Name   .get()
        edituser.Address       = self.v_Address        .get()
        edituser.Address2      = self.v_Address2       .get()
        edituser.Phone         = self.v_Phone          .get()
        edituser.City          = self.v_City           .get()
        edituser.State         = self.v_State          .get()
        edituser.Country       = self.v_Country        .get()
        edituser.Postal_Code   = self.v_Postal_Code    .get()
        edituser.Email_Address = self.v_Email_Address  .get()
        edituser.Machine_id    = self.v_Machine_id     .get()
        if self.v_active.get().strip() == '1' or self.v_active.get().strip() == 'True':
            edituser.active = True
        else:
            tkMessageBox.showwarning('Warning', 'User id is DEACTIVATED')
            edituser.active = False
            
        keyring.user[uuid] = copy.deepcopy(edituser)
        keyring.save()
        
    def new(self, *a):
        uuid = uuid_form(self.v_new_id.get())
        keyring.new(uuid)
        self.showuser(uuid)
        
    def export_server(self):
        self.button_export_server.flash()
        key_hash_sequence = self.v_sequence.get()
        if len(key_hash_sequence) == 4 and int(key_hash_sequence) >= 1:
            user_dict = keyring.export_server_dict(key_hash_sequence)
            self.user_dispatch_list = user_dict.keys()
            self.user_dispatch_list.sort()
            while len(self.user_dispatch_list) > 0:
                local_user_dispatch_list = copy.copy(self.user_dispatch_list)
                for user_id in local_user_dispatch_list:
                    msg = Message()
                    msg.header = HDR_ADM_MESSAGE
                    adm_msg = AdmMessage(key = self.encryptionkey, packet = None)
                    adm_msg.command = COMMAND_SET_USER
                    adm_msg.user_id = user_id
                    adm_msg.data = pickle.dumps(user_dict[user_id])
                    msg.timestamp = self.server_timestamp()
                    msg.encrypted = adm_msg.packet()
                    msg.integrity = hashlib.sha256(msg.integrity_data() + self.encryptionkey).digest()[:4]
                    print self.server
                    self.sock.sendto(msg.packet(), (self.server, 9001))
                    # limit to 100 packets/sec
                    time.sleep(.01)
                    self.v_message.set(str(len(self.user_dispatch_list)))
                    print len(self.user_dispatch_list)
                # wait before retransmit
                time.sleep(2)
                print len(self.user_dispatch_list)
                    
    def search(self, *a):
        userlist = ''
        u_list = []
        result = StringIO.StringIO(keyring.search(self.text_search.get()))
        for line in result.readlines():
            u_list.append(line.split()[0])
            
        u_list.sort()
        userlist = ' '.join(u_list)
        
        self.uservar.set(userlist)
        
    def clear_screen(self):
        self.v_uuid          .set('')
        self.v_OS            .set('')
        self.v_expire_date   .set('')
        self.v_Name          .set('')
        self.v_Company_Name  .set('')
        self.v_Address       .set('')
        self.v_Address2      .set('')
        self.v_Phone         .set('')
        self.v_City          .set('')
        self.v_State         .set('')
        self.v_Country       .set('')
        self.v_Postal_Code   .set('')
        self.v_Email_Address .set('')
        self.v_Machine_id    .set('')
        self.v_active        .set('')
        self.v_hashes        .set('')
        
    def userlist_click(self, event):
        user_id = self.userlist.get(self.userlist.curselection()[0])
        self.showuser(user_id)
                
    def get_timestamp(self):
        msg = Message()
        msg.header = HDR_ADM_MESSAGE
        adm_msg = AdmMessage(key = self.encryptionkey, packet = None)
        adm_msg.command = COMMAND_GET_TIMESTAMP
        adm_msg.data = ''
        msg.timestamp = EMPTY_TIMESTAMP
        msg.encrypted = adm_msg.packet()
        msg.integrity = hashlib.sha256(msg.integrity_data() + self.encryptionkey).digest()[:4]
        self.sock.sendto(msg.packet(), (self.server, 9001))
        
    def get_online(self):
        msg = Message()
        msg.header = HDR_ADM_MESSAGE
        adm_msg = AdmMessage(key = self.encryptionkey, packet = None)
        adm_msg.command = COMMAND_GET_ONLINE
        adm_msg.data = ''
        msg.encrypted = adm_msg.packet()
        msg.timestamp = self.server_timestamp()
        msg.integrity = hashlib.sha256(msg.integrity_data() + self.encryptionkey).digest()[:4]
        self.sock.sendto(msg.packet(), (self.server, 9001))
        
    def get_talking(self):
        msg = Message()
        msg.header = HDR_ADM_MESSAGE
        adm_msg = AdmMessage(key = self.encryptionkey, packet = None)
        adm_msg.command = COMMAND_GET_TALKING
        msg.encrypted = adm_msg.packet()
        msg.timestamp = self.server_timestamp()
        msg.integrity = hashlib.sha256(msg.integrity_data() + self.encryptionkey).digest()[:4]
        self.sock.sendto(msg.packet(), (self.server, 9001))
        
    def showuser(self, user_id):
        self.clear_screen()
        user = keyring.user[user_id]
        
        self.current_user = copy.deepcopy(user)
        self.current_user_edited = False
        
        self.v_uuid          .set(user_id)
        self.v_OS            .set(user.OS)
        self.v_expire_date   .set(user.expire_date)
        self.v_Name          .set(user.Name)
        self.v_Company_Name  .set(user.Company_Name)
        self.v_Address       .set(user.Address)
        self.v_Address2      .set(user.Address2)
        self.v_Phone         .set(user.Phone)
        self.v_City          .set(user.City)
        self.v_State         .set(user.State)
        self.v_Country       .set(user.Country)
        self.v_Postal_Code   .set(user.Postal_Code)
        self.v_Email_Address .set(user.Email_Address)
        self.v_Machine_id    .set(user.Machine_id)
        self.v_active        .set(user.active)
        
        rnd, integrity = keyring.get(user_id)
        if rnd != None:
            self.v_hashes.set(rnd[:6] + ' ' + rnd[6:12] + ' ' + rnd[12:18] + ' ' + rnd[18:24] + ' ' + rnd[24:30] + ' ' + integrity[:6])
        
root = Tkinter.Tk()
app = App(root)
root.mainloop()
sys.exit(0)

