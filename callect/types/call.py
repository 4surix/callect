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
            kwargs[key] = value


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
        self.kwargs = args.dict__.items()


class Attachement(Base):
    
    def __call__(self, variables):

        obj = self.objet(variables)


        for attache in self.attaches:

            attache = attache(variables)


            args = []
            add = args.append

            kwargs = {}

            if attache.__class__.__name__ != 'Table':
                raise NotCompatible(self, attache, self.ligne__)

            for value in attache.list__:
                add(value(variables))

            for key, value in attache.dict__.items():
                kwargs[key] = value(variables)


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