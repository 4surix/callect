
from ..base import Base, SigneAction, fonction_py_to_cl, methode_py_to_cl
from ..errors import NotItem, NotIndex, NotValue, ConvertionImpossible, NotCompatible
from ..assignement import Asi

from .nbr import Pos, Neg, Nul, mk_nbr
from .bool import True__, False__


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

            if obj.__class__.__name__ not in ('Pos', 'Neg', 'Txt', 'Table', 'Intervalle'):
                raise ConvertionImpossible(obj, Table, obj.ligne__)


            nbr = 1
            add = table.list__.append

            for i, element in obj:
                if nbr == i:
                    add(element)
                    nbr += 1

                else:
                    table.dict__[i] = element
                    nbr = None

            table.ligne__ = obj.ligne__

        else:
            table.ligne__ = ''

        table.next_index_list = len(table.list__) + 1

        table.methodes__()


    return table


class Table(Base):

    def __call__(self, variables):

        new_table = Table()

        new_table.list__ = [
            e(variables)
            for e in self.list__
        ]
        new_table.dict__ = {
            k(variables): v(variables) 
            for k, v in self.dict__.items()
        }

        new_table.next_index_list = len(new_table.list__) + 1

        new_table.ligne__ = self.ligne__

        new_table.methodes__()

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

        if item.__class__ == Neg and item.value > -self.next_index_list:
            return self.list__[item.value]

        if item.__class__.__name__ == 'Intervalle':
            return mk_table(_list=self.list__[slice(item.debut, item.fin, item.step)])

        value = self.dict__.get(item)
        if value is not None:
            return value

        try:
            return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __setitem__(self, item, value):

        type_name = item.__class__.__name__

        if type_name == 'Pos':

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

        elif type_name == 'Intervalle':
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

        nbr = 0
        for value in self.list__:
            nbr += 1
            yield mk_nbr(nbr), value

        for index, value in self.dict__.items():
            yield index, value

    def __len__(self):

        return self.next_index_list - 1 + len(self.dict__)

    def __eq__(self, obj):

        if obj.__class__ != Table:
            return False

        return obj.list__ == self.list__ and obj.dict__ == self.dict__


    def __bool__(self):
        return True

    def bool__(self, variables):
        return True__


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

        if obj.__class__ != Table:
            return False

        return obj.list__ == self.list__ and obj.dict__ == self.dict__


    @methode_py_to_cl
    def mul__(variables, self, obj):

        if obj.__class__.__name__ != 'Pos':
            raise NotCompatible(self, obj, self.ligne__)

        return mk_table(_list=self.list__ * obj.value, _dict={**self.dict__})


    ### Methodes

    def methodes__(self):

        self.add = fonction_py_to_cl(self.add)
        self.rem = fonction_py_to_cl(self.rem)
        self.remall = fonction_py_to_cl(self.remall)

        self.insert = fonction_py_to_cl(self.insert)

        self.pop = fonction_py_to_cl(self.pop)

        self.index = fonction_py_to_cl(self.index)
        self.value = fonction_py_to_cl(self.func__value)
        self.indexs = fonction_py_to_cl(self.indexs)
        self.values = fonction_py_to_cl(self.values)

    def insert(self, item, value):

        type_name = type(item).__name__

        if item.__class__ == Pos:

            item = item.value
        
            if item <= self.next_index_list:

                self.list__.insert(item-1, value)
                
                self.next_index_list = i = self.next_index_list + 1

                while True:
                    i = Pos(i)
                    value = self.dict__.get(i)

                    if value is None:
                        return self

                    del self.dict__[i]
                    self.list__.append(value)

                    self.next_index_list = i = self.next_index_list + 1

        self.dict__[item] = value

        return self

    def add(self, obj):

        self[Pos(self.next_index_list)] = obj
        return self

    def pop(self, item=Pos(0)):

        if (
            self.list__ # Si la liste est vide cela ne sert à rien de chercher dedans
            and item.__class__ == Pos 
            and item.value < self.next_index_list
        ):
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

            for index, value in self.dict__.items():
                if value == obj:
                    del self.dict__[index]
                    return self

        raise NotValue(self, obj, obj.ligne__)

    def remall(self, value):

        self.list__ = [v for v in self.list__ if v != value]
        self.dict__ = {k: v for k, v in self.dict__.items() if v != value}

        self.next_index_list = len(self.list__) + 1

        return self

    def index(self, obj):

        try:
            return Pos(self.list__.index(obj) + 1)

        except:
            for index, value in self.dict__.items():
                if obj == value:
                    return index

        raise NotIndex(self, obj, obj.ligne__)

    def func__value(self, obj):

        try:
            return self.list__[obj]

        except:

            try:
                return self.dict__[obj]

            except:
                pass

        raise NotValue(self, obj, obj.ligne__)

    def indexs(self):

        return mk_table(_list=[*[mk_nbr(v) for v in range(1, self.next_index_list)], *self.dict__])

    def values(self):

        return mk_table(_list=[*self.list__, *self.dict__.values()])


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

        self.value__ = self.value

        self.list__ = []
        self.dict__ = {}
        self.next_index_list = 1

        self.ligne__ = str(cont.ligne)

        for value in self.value:

            if isinstance(value, Asi):

                keys = [v for v in value.elements if v != SigneAction]
                value = value.objet

                for key in keys:

                    if key.__class__ == Pos:

                        if key.value < self.next_index_list:
                            self.next_index_list += 1
                            self.list__[key.value-1] = value
                            continue

                        elif key.value == self.next_index_list:
                            self.next_index_list += 1
                            self.list__.append(value)
                            continue
                    
                    self.dict__[key] = value

            elif type(value).__name__ == 'Objet' and value.__name__:

                self.dict__[value.__name__] = value

            else:
                self.list__.append(value)


        self.methodes__()