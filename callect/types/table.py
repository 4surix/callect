from ..base import Base, fonction_py_to_cl, methode_py_to_cl

from ..errors import NotItem, NotIndex, NotValue, ConvertionImpossible

from .nbr import Pos, Neg, Nul
from .txt import Txt, mk_txt

from ..assignement import Asi


def mk_table(obj=None, variables=None, *, _list=None, _dict=None):

    if getattr(obj, 'tbl__', None):
        table = obj['tbl__'](variables)

    elif isinstance(obj, Table):
        table = obj(variables)

    else:
        table = Table()

        table.list__ = _list if _list else []

        table.dict__ = _dict if _dict else {}

        if obj is not None:

            if obj.__class__.__name__ not in ('Txt', 'Table', 'Intervalle'):
                raise ConvertionImpossible(obj, Table, obj.ligne__)

            table.list__.extend(obj)
            table.ligne__ = obj.ligne__

        else:
            table.ligne__ = ''

        table.next_index_list = len(table.list__) + 1

        table.methodes()


    return table


class Table(Base):

    def __call__(self, variables):

        new_table = Table()
        new_table.list__ = [e(variables) for e in self.list__]
        new_table.dict__ = {k(variables):v(variables) for k, v in self.dict__.items()}
        new_table.next_index_list = len(new_table.list__) + 1

        new_table.ligne__ = self.ligne__

        new_table.methodes()

        return new_table

    def __str__(self):

        return '{%s}' % ', '.join(
            [repr(e) for e in self.list__] + ['%s=%s' % (repr(k),repr(v)) for k,v in self.dict__.items()]
        )

    def __repr__(self):

        return str(self)

    def __getitem__(self, item):

        if item.__class__ == Pos and item.value < self.next_index_list:
            return self.list__[item.value-1]

        if item.__class__.__name__ == 'Intervalle':
            return mk_table(_list=self.list__[slice(item.debut, item.fin, item.step)])

        value = self.dict__.get(str(item))
        if value is not None:
            return value

        try:
            return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __setitem__(self, item, value):

        type_name = type(item).__name__

        if isinstance(item, Pos):

            item = item.value
        
            if item == self.next_index_list:

                self.list__.append(value)
                
                self.next_index_list = i = self.next_index_list + 1

                while True:
                    i = Pos(i)
                    value = self.dict__.get(i)

                    if value is None:
                        return

                    del self.dict__[i]
                    self.list__.append(value)

                    self.next_index_list = i = self.next_index_list + 1

            elif item < self.next_index_list:
                self.list__[item-1] = value
                return

        elif isinstance(item, Intervalle):
            self.list__[slice(item.debut, item.fin, item.step)] = value

        self.dict__[item] = value

    def __delitem__(self, item):

        if isinstance(item, Pos) and item.value < self.next_index_list:
            del self.list__[item.value-1]
            self.next_index_list -= 1

        else:

            try:
                del self.dict__[item]
            except:
                raise NotItem(self, item, item.ligne__)

    def __iter__(self):

        for value in self.list__:
            yield value

        for value in self.dict__.values():
            yield value

    def __len__(self):

        return self.next_index_list - 1 + len(self.dict__)


    @methode_py_to_cl
    def in__(variables, self, obj):

        for value in self.list__:
            if value == obj:
                return True

        for value in self.dict__.values():
            if value == obj:
                return True

    @methode_py_to_cl
    def popin__(variables, self, obj):

        try:
            self.__class__.pop(self, obj)
            return True

        except NotIndex:
            return False

    @methode_py_to_cl
    def remin__(variables, self, obj):

        try:
            self.__class__.rem(self, obj)
            return True

        except NotValue:
            return False


    @methode_py_to_cl
    def ega__(variables, self, obj):
        return str(self) == str(obj)


    ### Methodes

    def methodes(self):

        self.add = fonction_py_to_cl(self.add)
        self.rem = fonction_py_to_cl(self.rem)
        self.remall = fonction_py_to_cl(self.remall)

        self.pop = fonction_py_to_cl(self.pop)

        self.join = fonction_py_to_cl(self.join)

        self.index = fonction_py_to_cl(self.index)
        self.value = fonction_py_to_cl(self.value)
        self.indexs = fonction_py_to_cl(self.indexs)
        self.values = fonction_py_to_cl(self.values)

    def add(self, obj):

        self.list__.append(obj)
        self.next_index_list += 1
        return self

    def join(self, obj):

        return Txt(mk_txt(obj, return_str=True).join(mk_txt(v, return_str=True) for v in self))

    def pop(self, item=Pos(0)):

        if item.__class__ == Pos and item.value < self.next_index_list:
            value = self.list__.pop(item.value-1)
            self.next_index_list -= 1
            return value

        try:
            return self.dict__.pop(item)
        except:
            raise NotIndex(self, item, item.ligne__)

    def rem(self, obj):

        try:
            self.list__.remove(obj)
            self.next_index_list -= 1
            return self

        except:

            try:
                for index, value in self.dict__.items():
                    if value == obj:
                        del self.dict__[index]
                        break

            except:
                raise NotValue(self, obj, obj.ligne__)

        return self

    def remall(self, value):

        self.list__ = [v for v in self.list__ if v != value]
        self.dict__ = {k:v for k, v in self.dict__.items() if v != value}

        self.next_index_list = len(self.list__) + 1

        return self

    def index(self, obj):

        try:
            return Pos(self.list__.index(obj)+1)

        except:
            for index, value in self.dict__.items():
                if obj == value:
                    return index

        raise NotIndex(self, obj, obj.ligne__)

    def value(self, obj):

        try:
            return self.list__[obj]

        except:

            try:
                return self.dict__[obj]

            except:
                pass

        raise NotValue(self, obj, obj.ligne__)

    def indexs(self):

        return mk_table(_list=[v for v in range(1, self.next_index_list)] + [k for k in self.dict__])

    def values(self):

        return mk_table(_list=self.list__ + list(self.dict__.values()))


    ### Appel de table

    def call__(*args):

        if len(args) == 3:
            return mk_table(args[1][0], args[0])

        else:
            self, variables, args, kwargs = args
            
            self.list__.extend(args)
            self.dict__.update(kwargs)

            self.next_index_list = len(self.list__) + 1

            return self


    ### End decodage

    def end__(self, cont):

        self.list__ = []
        self.dict__ = {}
        self.next_index_list = 1

        self.ligne__ = str(cont.ligne)

        for value in self.value:

            if isinstance(value, Asi):

                keys = value.elements
                value = value.value

                for key in keys:
                    if isinstance(key, Pos) and key.value <= len(self.list__)+1:
                        self.list__[key.value-1] = value
                    else:
                        self.dict__[key] = value

            elif type(value).__name__ == 'Objet' and value.__name__:

                self.dict__[value.__name__] = value

            else:
                self.list__.append(value)


        self.methodes()