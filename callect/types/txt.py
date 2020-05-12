from ..base import Base, methode_py_to_cl, fonction_py_to_cl

from ..errors import NotCompatible, NotItem


def mk_txt(obj, variables=None, *, return_str=False, ligne__=''):
    
    if getattr(obj, 'txt__', None):
        try:
            txt = obj['txt__']
        except:
            txt = obj.txt__

        txt = txt(variables)
        return str(txt) if return_str else txt

    elif return_str:
        return str(obj)

    else:
        txt = Txt(str(obj))
        txt._methodes()

        try:
            txt.ligne__ = obj.ligne__
        except:
            txt.ligne__ = ligne__

        return txt


class Txt(Base):

    def _methodes(self):

        self.upper = fonction_py_to_cl(lambda: mk_txt(self.value.upper()))
        self.lower = fonction_py_to_cl(lambda: mk_txt(self.value.lower()))

        self.split = fonction_py_to_cl(lambda sep: mk_txt(self.value.split(str(sep))))

    def __call__(self, variables):

        txt = Txt(self.value)
        txt.ligne__ = self.ligne__
        return txt

    def __eq__(self, obj):
        return self.value == obj

    def __ne__(self, obj):
        return self.value != obj


    def __iter__(self):
        for value in self.value:
            yield Txt(value)

    def __str__(self, *args):
        return '%s' % self.value

    def __repr__(self):
        return '"%s"' % self.value


    def __getitem__(self, item):

        name_type = item.__class__.__name__

        if name_type == 'Pos' or name_type == 'Neg':
            txt = mk_txt(self.value[item.value])
            txt.ligne__ = item.ligne__
            return txt

        elif name_type == 'Intervalle':
            txt = mk_txt(self.value[slice(item.debut, item.fin, item.step)])
            txt.ligne__ = item.ligne__
            return txt

        if name_type == 'slice':
            txt = mk_txt(self.value[item])
            txt.ligne__ = self.ligne__
            return txt

        try:
            return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __setitem__(self, item, value):

        self.__dict__[item] = value


    def __hash__(self):
        return hash(self.value)


    @methode_py_to_cl
    def in__(variables, self, obj):
        return obj.value in self.value


    @methode_py_to_cl
    def ega__(variables, self, obj):
        return self.value == obj.value


    @methode_py_to_cl
    def add__(variables, self, obj):
        if obj.__class__ != Txt:
            raise NotCompatible(self, obj, self.ligne__)
        return mk_txt(self.value + obj.value)

    @methode_py_to_cl
    def mul__(variables, self, obj):
        if obj.__class__.__name__ != 'Pos':
            raise NotCompatible(self, obj, self.ligne__)
        return mk_txt(self.value * obj.value)


    def call__(*args):

        if len(args) == 2:
            return args[0]

        else:
            return mk_txt(args[1][0], args[0])


    def end__(self, cont):

        self.value = ''.join(map(str, self.value))

        self._methodes()

        self.ligne__ = str(cont.ligne)