
from ..base import Base, methode_py_to_cl, fonction_py_to_cl
from ..errors import NotCompatible, NotItem

from .table import mk_table
from .nbr import mk_nbr
from .bool import True__, False__


def mk_txt(obj, variables=None, *, return_str=False, ligne__=''):

    try: txt__ = obj['txt__']
    except (KeyError, AttributeError, TypeError):

        if return_str:
            return str(obj)

        else:
            txt = Txt(str(obj))
            txt.methodes__()

            try: txt.ligne__ = obj.ligne__
            except:
                txt.ligne__ = ligne__

            return txt

    else:
        txt = txt__(variables)
        return str(txt) if return_str else txt


class Txt(Base):

    def methodes__(self):

        self.upper = fonction_py_to_cl(self.upper)
        self.lower = fonction_py_to_cl(self.lower)

        self.join = fonction_py_to_cl(self.join)

        self.split = fonction_py_to_cl(self.split)

        self.replace = fonction_py_to_cl(self.replace)

    def upper(self):

        return mk_txt(self.value.upper(), ligne__=self.ligne__)

    def lower(self):

        return mk_txt(self.value.lower(), ligne__=self.ligne__)

    def join(self, obj):

        return mk_txt(
            self.value.join(
                mk_txt(v, return_str=True) 
                for index, v in obj
            ), 
            ligne__=self.ligne__
        )

    def split(self, obj):

        return mk_table(
            _list=[
                mk_txt(v) 
                for v in self.value.split(
                    mk_txt(obj, return_str=True)
                )
            ],
            ligne__=self.split.variables.action_ligne__
        )

    def replace(self, obj_1, obj_2):

        return mk_txt(
            self.value.replace(
                mk_txt(obj_1, return_str=True), 
                mk_txt(obj_2, return_str=True)
            ),
            ligne__=self.replace.variables.action_ligne__
        )

    def __call__(self, variables):

        txt = Txt(self.value)
        txt.ligne__ = self.ligne__
        txt.methodes__()
        return txt


    def __eq__(self, obj):
        return self.value == obj

    def __ne__(self, obj):
        return self.value != obj


    def __iter__(self):

        nbr = 0
        for value in self.value:
            nbr += 1
            yield mk_nbr(nbr), Txt(value)

    def __str__(self, *args):
        return '%s' % self.value

    def __repr__(self):
        return repr(self.value)


    def __getitem__(self, item):

        name_type = item.__class__.__name__

        if name_type == 'Pos':
            return mk_txt(self.value[item.value-1], ligne__=self.ligne__)

        elif name_type == 'Neg':
            return mk_txt(self.value[item.value], ligne__=self.ligne__)

        elif name_type == 'Intervalle':
            return mk_txt(
                self.value[slice(item.debut, item.fin, item.step)], 
                ligne__=self.ligne__
            )

        elif name_type == 'slice':
            return mk_txt(self.value[item], ligne__=self.ligne__)

        try: return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __setitem__(self, item, value):
        self.__dict__[item] = value


    def __hash__(self):
        return hash(self.value)


    def __len__(self):
        return len(self.value)


    def __bool__(self):
        return True

    def bool__(self, variables):
        return True__


    @methode_py_to_cl
    def in__(variables, self, obj):
        if obj.__class__ != Txt:
            raise NotCompatible(self, obj, variables.action_ligne__)
        return obj.value in self.value


    @methode_py_to_cl
    def ega__(variables, self, obj):
        return self.value == obj.value


    @methode_py_to_cl
    def add__(variables, self, obj):
        if obj.__class__ != Txt:
            raise NotCompatible(self, obj, variables.action_ligne__)
        return mk_txt(self.value + obj.value)

    @methode_py_to_cl
    def mul__(variables, self, obj):
        if obj.__class__.__name__ != 'Pos':
            raise NotCompatible(self, obj, variables.action_ligne__)
        return mk_txt(self.value * obj.value)


    def call__(*args):

        if len(args) == 3:
            return mk_txt(args[1][0], args[0])

        else:
            return args[0]


    def end__(self, cont):

        self.value = ''.join(map(str, self.value))

        self.methodes__()

        self.ligne__ = str(cont.ligne)