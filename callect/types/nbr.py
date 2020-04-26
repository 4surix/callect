from ..base import Base, methode_py_to_cl, fonction_py_to_cl

from ..errors import NotSupported, NotCompatible, NotItem, ConvertionImpossible

from .txt import Txt


def mk_nbr(obj, return_value=False, convert=None):
    nbr = str(obj)

    if ',' in nbr:
        nbr = nbr.replace(',', '.')

    try:

        if '.' in nbr:

            if nbr.split('.')[-1] == '0': 
                value = int(nbr.split('.')[0])
            else:
                value = float(nbr)

        else:
            value = int(nbr)

    except ValueError:
        raise ConvertionImpossible(obj, Nbr, obj.ligne__)


    if convert:
        value = convert(value)


    if return_value:
        return value


    if value == 0:
        value = Nul(0)

    elif value < 0:
        value = Neg(value)

    else:
        value = Pos(value)

    try:
        value.ligne__ = obj.ligne__
    except:
        value.ligne__ = ''

    return value


class Nbr:

    def _if_pos_neg_nul(self, obj, silent=False):

        if isinstance(obj, (Neg, Pos, Nul)):
            return obj.value

        elif not silent:
            raise NotCompatible(self, obj, self.ligne__)

        else:
            return obj


    def __lt__(self, obj):
        return self.value < self._if_pos_neg_nul(obj)

    def __le__(self, obj):
        return self.value <= self._if_pos_neg_nul(obj)

    def __eq__(self, obj):
        return self.value == self._if_pos_neg_nul(obj, True)

    def __ne__(self, obj):
        return self.value != self._if_pos_neg_nul(obj, True)

    def __ge__(self, obj):
        return self.value >= self._if_pos_neg_nul(obj)

    def __gt__(self, obj):
        return self.value > self._if_pos_neg_nul(obj)


    def __add__(self, obj):
        return mk_nbr(self.value + self._if_pos_neg_nul(obj))

    def __sub__(self, obj):
        return mk_nbr(self.value - self._if_pos_neg_nul(obj))

    def __mul__(self, obj):
        return mk_nbr(self.value * self._if_pos_neg_nul(obj))

    def __truediv__(self, obj):
        return mk_nbr(self.value / self._if_pos_neg_nul(obj))

    def __floordiv__(self, obj):
        return mk_nbr(self.value // self._if_pos_neg_nul(obj))

    def __mod__(self, obj):
        return mk_nbr(self.value % self._if_pos_neg_nul(obj))

    def __pow__(self, obj):
        return mk_nbr(self.value ** self._if_pos_neg_nul(obj))


    @methode_py_to_cl
    def inf__(variables, self, obj):
        return self.value < self._if_pos_neg_nul(obj)

    @methode_py_to_cl
    def inf_ega__(variables, self, obj):
        return self.value <= self._if_pos_neg_nul(obj)

    @methode_py_to_cl
    def ega__(variables, self, obj):
        return self.value == self._if_pos_neg_nul(obj, True)

    @methode_py_to_cl
    def sup_ega__(variables, self, obj):
        return self.value >= self._if_pos_neg_nul(obj)

    @methode_py_to_cl
    def sup__(variables, self, obj):
        return self.value > self._if_pos_neg_nul(obj)



    def __abs__(self):
        return Pos(abs(self.value))
    
    def __pos__(self):
        if isinstance(self, Pos):
            return self
        return Pos(-self.value)

    def __neg__(self):
        if isinstance(self, Neg):
            return self
        return Neg(-self.value)


    @methode_py_to_cl
    def add__(variables, self, obj):
        return mk_nbr(self.value + self._if_pos_neg_nul(obj))

    @methode_py_to_cl
    def sub__(variables, self, obj):
        return mk_nbr(self.value - self._if_pos_neg_nul(obj))

    @methode_py_to_cl
    def mul__(variables, self, obj):
        return mk_nbr(self.value * self._if_pos_neg_nul(obj))

    @methode_py_to_cl
    def div__(variables, self, obj):
        return mk_nbr(self.value / self._if_pos_neg_nul(obj))

    @methode_py_to_cl
    def mod__(variables, self, obj):
        return mk_nbr(self.value % self._if_pos_neg_nul(obj))

    @methode_py_to_cl
    def exp__(variables, self, obj):
        return mk_nbr(self.value ** self._if_pos_neg_nul(obj))

    @methode_py_to_cl
    def rac__(variables, self, obj):
        return mk_nbr(self.value ** (1 / self._if_pos_neg_nul(obj)))


    def __hash__(self):
        return hash(repr(self))

    def __index__(self):
        return self.value

    def __float__(self):
        self.value = float(self.value)
        return self.value

    def __int__(self):
        self.value = int(self.value)
        return self.value

    def __str__(self):
        return '%s' % self.value

    def __repr__(self):
        return '%s' % self.value


    @methode_py_to_cl
    def obj__(variables, self):
        return self


    def __getitem__(self, item):

        try:
            return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __setitem__(self, item, value):
        setattr(self, str(item), value)


    def call__(*args):

        if len(args) == 3:

            variables, args, kwargs = args

            return mk_nbr(args[0])


class Pos(Base, Nbr):

    def __call__(self, variables):

        pos = Pos(self.value)
        pos.ligne__ = self.ligne__
        return pos

    def __iter__(self):

        for value in range(1, self.value+1):
            yield Pos(value)

    def __bool__(self):
        return True

    def call__(*args):

        if len(args) == 3:

            obj = args[1][0]

            if getattr(obj, 'pos__', None):
                return obj['pos__'](args[0], args[1], {})

            elif isinstance(obj, (Neg, Pos, Nul)):
                return Pos(+abs(obj.value))

            elif isinstance(obj, Txt):
                return Pos(+abs(mk_nbr(obj, return_value=True)))

            else:
                raise NotSupported(obj, 'pos__')

        else:
            self = args[0]
            self.value += args[2][0].value if args[2] else 1
            return self

    def end__(self, cont):

        nbr = ''.join([str(e) for e in self.value])

        if '.' in nbr:
            self.value = 0 + float(nbr)
        else:
            self.value = 0 + int(nbr)

        self.ligne__ = str(cont.ligne)


class Neg(Base, Nbr):

    def __call__(self, variables):

        neg = Neg(self.value)
        neg.ligne__ = self.ligne__
        return neg

    def __iter__(self):

        for value in range(-1, self.value-1, -1):
            yield Neg(value)

    def __bool__(self):
        return True

    def call__(*args):

        if len(args) == 3:

            obj = args[1][0]

            if getattr(obj, 'neg__', None):
                return obj['neg__'](args[0], args[1], {})

            elif isinstance(obj, (Neg, Pos, Nul)):
                return Neg(-abs(obj.value))

            elif isinstance(obj, Txt):
                return Neg(-abs(mk_nbr(obj, return_value=True)))

            else:
                raise NotSupported(obj, 'neg__')

        else:
            self = args[0]
            self.value -= args[2][0].value if args[2] else 1
            return self

    def end__(self, cont):

        nbr = ''.join([str(e) for e in self.value])

        if '.' in nbr:
            self.value = 0 - float(nbr)
        else:
            self.value = 0 - int(nbr)

        self.ligne__ = str(cont.ligne)


class Nul(Base, Nbr):

    def __call__(self, variables):

        nul = Nul(0)
        nul.ligne__ = self.ligne__
        return nul

    def __bool__(self):
        return False

    def call__(*args):

        if len(args) == 3:

            obj = args[1][0]

            if getattr(obj, 'nul__', None):
                obj['nul__'](*args)

            return Nul(0)

        else:
            return args[0]

    def end__(self, cont):

        self.value = 0

        self.ligne__ = str(cont.ligne)