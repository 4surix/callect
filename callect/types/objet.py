from ..base import Base, Return

from ..errors import NotItem

from .txt import Txt, mk_txt
from .table import Table, mk_table
from .bloc import Bloc


class CallObjetWithParent:

    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

    def __call__(self, variables, args=[], kwargs={}):
        return self.value(variables, args, kwargs, mk_table(_dict=self.parent.__dict__))

    def __setitem__(self, item, value):
        self.value[item] = value

    def __getitem__(self, item):
        if item == 'call__':
            return self

        return self.value[item]


class Inst:

    def __init__(self):
        self.call__ = lambda *args: self

    def __str__(self):
        return '<Objet %s>' % self.__class__.__name__

    def __repr__(self):
        return '<Objet %s>' % self.__class__.__name__

    def __call__(self, *args):
        return self


    def __getitem__(self, item):
        try:
            value = self.__dict__[item]
        except:
            raise NotItem(self, item, item.ligne__)

        if isinstance(value, Objet):
            return CallObjetWithParent(value, self)

        return value

    def __setitem__(self, item, value):
        self.__dict__[mk_txt(item)] = value


    def __iter__(self):
        for key, value in self.__dict__.items():
            if key[-2:] != '__':
                yield key, value


class Objet(Base):

    def __call__(*args):

        if len(args) == 2:
            self, variables = args

            if self.__name__:
                variables.set(self.__name__, self)

            return self
            
        else:
            return Objet.call__(*args)

    def __getitem__(self, item):
        try:
            return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __str__(self):
        return '<Objet %s>' % self.__name__

    def __repr__(self):
        return '<Objet %s>' % self.__name__
    
    def call__(self, variables, args, kwargs={}, parent=None):

        inst = None

        if self.self:
            inst = self.__inst()
            arguments = inst.__dict__
            arguments[self.self] = inst

            if parent and self.parent:
                arguments[self.parent] = parent

        else:
            arguments = {}


        for key, value in self.kwargs:
            arguments[key(variables)] = value(variables)

        for key, value in kwargs.items():
            arguments[key] = value


        variables = variables.add(arguments)


        for key, value in zip(self.args, args):
            key(variables, setvar=value, local=True)


        try:
            for element in self.bloc.value:
                element(variables)
        except Return as r:
            return r.value(variables)


        if inst is None:

            inst = self.__inst()

            dict__ = inst.__dict__

            for key, value in arguments.items():
                dict__[key] = value

            if parent and self.parent:
                inst[self.parent] = parent


        inst.ligne__ = self.ligne__

        return inst

    def end__(self, cont):

        self.__name__ = ''

        self.self = None
        self.parent = None

        self.args = []
        self.kwargs = {}.items()

        self.bloc = None

        self.callable_without_call = True


        for value in self.value:

            name_type_value = value.__class__.__name__

            if name_type_value == 'Var':
                if self.parent:
                    raise
                elif self.self:
                    self.parent = mk_txt(value)
                else:
                    self.self = mk_txt(value)

            elif isinstance(value, Txt):
                self.__name__ = value

            elif isinstance(value, Table):
                self.args = value.list__
                self.kwargs = value.dict__.items()
                self.callable_without_call = False

            elif isinstance(value, Bloc):
                self.bloc = value


        class inst(Inst):
            pass
        
        if self.__name__:
            inst.__name__ = str(self.__name__)

        self.__inst = inst