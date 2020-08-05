
NotItem = None


def methode_py_to_cl(func):

    def conv(self, variables, args=[], kwargs=None):

        return func(
            variables, 
            self, 
            *args, 
            **({str(k): v for k, v in kwargs.items()} if kwargs else {})
        )

    conv.__name__ = func.__name__

    return conv


class fonction_py_to_cl:

    def __init__(self, func):
        self.func__ = func

    def __call__(self, variables):
        return self

    def __getitem__(self, item):
        return getattr(self, str(item))

    def __setitem__(self, item, value):
        return setattr(self, str(item), value)

    def call__(self, variables, args=[], kwargs=None):

        self.variables = variables

        value = self.func__(
            *args, 
            **({str(k): v for k, v in kwargs.items()} if kwargs else {})
        )

        self.variables = None

        return value


class Base:

    def __init__(self, value=None):

        self.value = [] if value is None else value

        self.liée = False

        self.ligne__ = '[L~None]'

    def __repr__(self):
        #return '%s(%s)' % (self.__class__.__name__, self.value)
        return str(self.value)
    
    def __str__(self):
        #return '%s(%s)' % (self.__class__.__name__, self.value)
        return str(self.value)

    def __getitem__(self, item):

        try: return getattr(self, str(item))
        except:
            raise NotItem(self, item, item.ligne__)

    def __setitem__(self, item, value):
        self.__dict__[item] = value

    def __call__(self, *args, **kwargs):
        return self

    def call__(self, *args, **kwargs):
        return self

    def last__(self):

        if not self.value:
            return None

        return self.value[-1]

    def pop__(self):

        return self.value.pop()

    def push__(self, item):

        self.value.append(item)

    def rem__(self, item):

        self.value.append(item)

    def end__(self, cont):
        pass

    @methode_py_to_cl
    def ega_obj__(variables, self, obj):
        return self is obj


class Return(Base, Exception):

    def __call__(self, *args):

        raise self

    def end__(self, cont):

        self.value = self.value[0]


class Commentaire:
    pass


class Prio(Base):

    def __call__(self, variables, *args, **kwargs):

        return self.value[0](variables, *args, **kwargs)


class SigneAction:
    value = value__ = None