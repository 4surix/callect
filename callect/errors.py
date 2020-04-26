from .base import Base


### Capture

class Try(Base):

    def end__(self, cont):

        self.essaie = self.value[0]

        self.value = []


class Except(Base):

    def __call__(self, variables):

        try:
            self.essaie(variables)

        except Exception as erreur:
            name_erreur = erreur.__class__.__name__

            for except_ in self.excepts:
                if not except_.erreur or str(except_.erreur) == name_erreur:
                    except_.bloc(variables)
                    break

    def push__(self, obj):

        if isinstance(obj, Try):
            self.essaie = obj.essaie
            self.excepts = [self]

        elif isinstance(obj, Except):
            self.essaie = obj.essaie
            self.excepts = obj.excepts + [self]

        else:
            self.value.append(obj)

    def end__(self, cont):

        if len(self.value) == 2:
            self.var_erreur = None
            self.erreur, self.bloc = self.value 

        elif len(self.value) == 4:
            self.erreur, as_, self.var_erreur, self.bloc = self.value

        else:
            self.erreur = self.var_erreur = None
            self.bloc = self.value[0]


### Erreurs

class NotSupported(Exception):

    def __init__(self, value, methode):

        self.value = "%s NotSupported: Type '%s' not have '%s' methode." % (value.ligne__, value.__class__.__name__, methode)

    def __str__(self):

        return self.value

class NotDefined(Exception):

    def __init__(self, value, ligne):

        self.value = "%s NotDefined: '%s' is not defined." % (ligne, value)

    def __str__(self):

        return self.value

class NotCompatible(Exception):

    def __init__(self, obj1, obj2, ligne):

        self.value = "%s NotCompatible: Type '%s' is not compatible with type '%s'." % (ligne, obj1.__class__.__name__, obj2.__class__.__name__)

    def __str__(self):

        return self.value

class AllNonexistent(Exception):

    def __init__(self, obj, ligne):

        self.value = "%s AllNonexistent: All verification is nonexistent." % (ligne)

    def __str__(self):

        return self.value

class NotItem(Exception):

    def __init__(self, obj, item, ligne):

        self.value = "%s NotItem: Objet '%s' not have item '%s'." % (ligne, obj.__class__.__name__, item)

    def __str__(self):

        return self.value

class NotIndex(Exception):

    def __init__(self, obj, index, ligne):

        self.value = "%s NotIndex: Objet '%s' not have index '%s'." % (ligne, obj.__class__.__name__, index)

    def __str__(self):

        return self.value

class NotValue(Exception):

    def __init__(self, obj, value, ligne):

        self.value = "%s NotValue: Objet '%s' not have value '%s'." % (ligne, obj.__class__.__name__, value)

    def __str__(self):

        return self.value

class ConvertionImpossible(Exception):

    def __init__(self, obj, conv, ligne):

        self.value = "%s ConvertionImpossible: Type '%s' can not be convert to type '%s'." % (ligne, obj.__class__.__name__, conv.__name__)

    def __str__(self):

        return self.value

class ModuleNotFound(Exception):

    def __init__(self, fichier, ligne=''):

        self.value = "%s ModuleNotFound: Module '%s' not found." % (ligne, fichier)

    def __str__(self):

        return self.value

class FileNotFound(Exception):

    def __init__(self, fichier, ligne=''):

        self.value = "%s FileNotFound: File '%s' not found." % (ligne, fichier)

    def __str__(self):

        return self.value

class ValueIncorrect(Exception):

    def __init__(self, fichier, ligne=''):

        self.value = "%s ValueIncorrect: Value '%s' is incorrect." % (ligne, fichier)

    def __str__(self):

        return self.value

class SyntaxIncorrect(Exception):

    def __init__(self, ligne=''):

        self.value = "%s SyntaxIncorrect: Syntax incorrect." % (ligne)

    def __str__(self):

        return self.value


ALLExcept = (
    NotSupported,
    NotDefined,
    NotCompatible,
    AllNonexistent,
    NotItem,
    NotIndex,
    NotValue,
    ConvertionImpossible,
    ModuleNotFound,
    FileNotFound,
    ValueIncorrect,
    SyntaxIncorrect
)