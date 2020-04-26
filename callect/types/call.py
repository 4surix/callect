from ..base import Base

from ..errors import NotCompatible, NotSupported

from .txt import mk_txt


class Call(Base):
    
    def __call__(self, variables):

        args = []
        add = args.append

        for value in self.args:
            value = value(variables)
            value.ligne__ = self.ligne__
            add(value)


        kwargs = {}

        for key, value in self.kwargs:
            value = value(variables)
            value.ligne__ = self.ligne__
            kwargs[key(variables)] = value


        obj = self.objet(variables)

        try:
            call = obj['call__']

        except (KeyError, AttributeError):
            raise NotSupported(obj, 'call__')

        except TypeError:
            call = obj.call__


        return call(variables, args, kwargs)

    def end__(self, cont):

        self.objet, args = self.value

        self.args = args.list__
        self.kwargs = args.dict__.items()


class Attachement(Base):
    
    def __call__(self, variables):

        attache = self.attache(variables)

        if attache.__class__.__name__ != 'Table':
            raise NotCompatible(self, attache, self.ligne__)


        args = []
        add = args.append

        for value in attache.list__:
            add(value(variables))


        kwargs = {}

        for key, value in attache.dict__.items():
            kwargs[key(variables)] = value(variables)


        obj = self.objet(variables)

        try:
            call = obj['call__']

        except (KeyError, AttributeError):
            raise NotSupported(obj, 'call__')

        except TypeError:
            call = obj.call__


        return call(variables, args, kwargs)

    def end__(self, cont):

        self.objet, self.attache = self.value

        if self.attache.__class__.__name__ not in ['Var', 'RedirecItem', 'RedirecPoint', 'Prio']:
            raise NotCompatible(self, self.attache, self.ligne__)