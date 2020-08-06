from ..base import Base

from ..errors import NotCompatible, NotSupported

from .txt import mk_txt


class Call(Base):
    
    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        args = self.args
        if args:
            args = [value(variables) for value in args]

        kwargs = self.kwargs
        if kwargs:
            kwargs = {key: value(variables) for key, value in kwargs.items()}

        obj = self.objet(variables)

        try:
            try: call__ = obj['call__']
            except TypeError:
                call__ = obj.call__

        except (KeyError, AttributeError):
            raise NotSupported(obj, 'call__')

        else:
            return call__(variables, args, kwargs)

    def end__(self, cont):

        self.objet, args = self.value

        self.args = args.list__
        self.kwargs = args.dict__


class Attachement(Base):
    
    def __call__(self, variables):

        variables.action_ligne__ = self.ligne__

        obj = self.objet(variables)


        for attache in self.attaches:

            attache = attache(variables)

            if attache.__class__.__name__ != 'Table':
                raise NotCompatible(self, attache, self.ligne__)


            args = attache.list__
            if args:
                args = [value(variables) for value in args]

            kwargs = attache.dict__
            if kwargs:
                kwargs = {key: value(variables) for key, value in kwargs.items()}


            try:
                try: call__ = obj['call__']
                except TypeError:
                    call__ = obj.call__

            except (KeyError, AttributeError):
                raise NotSupported(obj, 'call__')

            else:
                obj = call__(variables, args, kwargs)


        return obj

    def end__(self, cont):

        self.objet, *self.attaches = self.value

        for attache in [self.objet] + self.attaches:
            if attache.__class__.__name__ not in [
                    'Var', 'RedirecPoint', 'Prio', 'Typ'
                ]:
                raise NotCompatible(self, self.attache, self.ligne__)