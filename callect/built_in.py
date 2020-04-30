
import os
import sys

import socket

import random

import time
import datetime

from .decode import decode

from .errors import FileNotFound, NotCompatible, ValueIncorrect

from .importation import import_

from .base import fonction_py_to_cl, methode_py_to_cl

from .types.nbr import Nbr, Pos, Neg, Nul, mk_nbr
from .types.txt import Txt, mk_txt
from .types.table import Table, mk_table
from .types.objet import Inst
from .types.bool import True__, False__


@fonction_py_to_cl
def type_(obj):
    return type(obj)


@fonction_py_to_cl
def print_(*args, sep=' ', end='\n'):

    variables = print_.variables

    sys.stdout.write(
        str(sep).join(mk_txt(arg, return_str=True) for arg in args) + str(end)
    )

    return False__


@fonction_py_to_cl
def input_(text):
    return mk_txt(input(str(text)))


@fonction_py_to_cl
def int_(obj):
    return mk_nbr(obj, convert=int)


@fonction_py_to_cl
def float_(obj):
    return mk_nbr(obj, convert=float)


@fonction_py_to_cl
def now():
    return mk_table(_list=[mk_nbr(nbr) for nbr in datetime.datetime.utcnow().strftime("%Y/%m/%d/%H/%M/%S").split("/")])


@fonction_py_to_cl
def stop(secondes):
    if isinstance(secondes, Pos):
        time.sleep(secondes.value)
    return False__


@fonction_py_to_cl
def len_(obj):
    return Pos(len(obj))


### Open file

@fonction_py_to_cl
def open_(chemin, mode='r', *, encoding='utf-8'):

    ligne = chemin.ligne__

    class File(Inst):

        def __init__(self, chemin, mode, encoding):
            self.path = chemin
            self.file = open(str(chemin), {'write':'w','read':'r'}.get(mode), encoding=str(encoding))

            if mode == 'read':
                self.read = fonction_py_to_cl(self.read)
                self.readto = fonction_py_to_cl(self.readto)

            if mode == 'write':
                self.write = fonction_py_to_cl(self.write)

            self.close = fonction_py_to_cl(self.close)

        def __str__(self):
            return '[FILE %s %s]' % (self.path, 'OPEN' if self.file else 'CLOSE')

        def read(self):
            if self.file:
                return mk_txt(self.file.read())
            return False__

        def readto(self, var_data):
            if self.file:
                if var_data.__class__.__name__ != 'Txt':
                    raise NotCompatible(self, var_data, var_data.ligne__)
                self.readto.variables.set(var_data, mk_txt(self.file.read()))
                return self
            return False__

        def write(self, value):
            if self.file:
                self.file.write(str(value))
                return self
            return False__

        def close(self):
            self.file.close()
            self.file = False__
            return False__


    if mode not in ['new', 'write', 'read']:
        raise ValueIncorrect(mode, mode.ligne__)

    if not os.path.exists(str(chemin)):
        if mode == 'new':
            mode = 'write'
            dossier = os.path.dirname(str(chemin))
            if dossier:
                os.makedirs(dossier, exist_ok=True)

        else:
            raise FileNotFound(chemin, ligne)

    return File(chemin, mode, encoding)


### Socket


class SocketClt(Inst):

    def __init__(self, client):
        self.so = client

        self.connect = fonction_py_to_cl(self.connect)

        self.send = fonction_py_to_cl(self.send)
        self.recv = fonction_py_to_cl(self.recv)

        self.close = fonction_py_to_cl(self.close)

        self.is_close = False__

    def connect(self, hote, port):
        if hote.__class__ != Txt:
            raise NotCompatible(self, hote, hote.ligne__)
        if port.__class__ != Pos:
            raise NotCompatible(self, port, port.ligne__)

        if self.is_close:
            return Neg(-1)

        try:
            self.so.connect((str(hote), int(port)))
            return True__
        except socket.timeout:
            return False__

    def send(self, msg):
        if self.is_close:
            return Neg(-1)

        self.so.send(str(msg).encode())
        return True__

    def recv(self, limite=Pos(4096)):
        if limite.__class__ != Pos:
            raise NotCompatible(self, limite, limite.ligne__)

        if self.is_close:
            return Neg(-1)
        
        try:
            value = self.so.recv(int(limite)).decode()
            if value:
                return mk_txt(value)
            self.so.close()
            self.is_close = True__
            return Neg(-1)

        except ConnectionResetError:
            self.so.close()
            self.is_close = True__
            return Neg(-1)

        except socket.timeout:
            return False__

    def settimeout(self, timeout=False__):
        if timeout.__class__ not in [Pos, Nul]:
            raise NotCompatible(self, timeout, timeout.ligne__)

        if self.is_close:
            return Neg(-1)

        self.so.settimeout(int(timeout) if timeout else None)
        return True__

    def close(self, hote, port):
        self.so.close()
        self.is_close = True__
        return False__


@fonction_py_to_cl
def socketclt():

    return SocketClt(socket.socket(socket.AF_INET, socket.SOCK_STREAM))


@fonction_py_to_cl
def socketsrv():
    
    class SocketSrv(Inst):

        def __init__(self):
            self.so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.bind = fonction_py_to_cl(self.bind)
            self.listen = fonction_py_to_cl(self.listen)

            self.accept = fonction_py_to_cl(self.accept)

            self.settimeout = fonction_py_to_cl(self.settimeout)

            self.close = fonction_py_to_cl(self.close)

            self.is_close = False__

        def bind(self, hote, port):
            if hote.__class__ != Txt:
                raise NotCompatible(self, hote, hote.ligne__)
            if port.__class__ != Pos:
                raise NotCompatible(self, port, port.ligne__)

            if self.is_close:
                return Neg(-1)

            self.so.bind((str(hote), int(port)))
            return self

        def listen(self, value=Pos(5)):
            if value.__class__ != Pos:
                raise NotCompatible(self, value, value.ligne__)

            if self.is_close:
                return Neg(-1)

            self.so.listen(int(value))
            return self

        def accept(self):
            if self.is_close:
                return Neg(-1)

            try:
                client, (ip, port) = self.so.accept()
                client.settimeout(self.so.gettimeout())
                return SocketClt(client)

            except socket.timeout:
                return False__

        def settimeout(self, timeout=False__):
            if timeout.__class__ not in [Pos, Nul]:
                raise NotCompatible(self, timeout, timeout.ligne__)

            if self.is_close:
                return Neg(-1)

            self.so.settimeout(int(timeout) if timeout else None)
            return True__

        def close(self, hote, port):
            if self.is_close:
                return Neg(-1)

            self.so.close()
            self.is_close = True__

            return Neg(-1)

    return SocketSrv()


socket_ = mk_table(_dict={
    'clt': socketclt,
    'srv': socketsrv
})


### Random

@fonction_py_to_cl
def random_(debut, fin):
    if debut.__class__ not in [Pos, Neg]:
        raise NotCompatible(random_, debut, debut.ligne__)
    if fin.__class__ not in [Pos, Neg]:
        raise NotCompatible(random_, fin, fin.ligne__)

    return mk_nbr(random.randint(int(debut), int(fin)))


fonctions_intégrées = {
    'import': import_(decode),

    'type': type_,

    'int': int_,
    'float': float_,

    'print': print_,
    'input': input_,

    'now': now,
    'stop': stop,
    'len': len_,
    'open': open_,

    'socket': socket_,

    'random': random_,

    'nbr': Nbr,
    'pos': Pos,
    'neg': Neg,
    'nul': Nul,
    'txt': Txt,
    'tbl': Table
}
