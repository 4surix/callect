import os

from .base import Return, Commentaire, Prio, SigneAction
from .operations import Rac, Exp, Mul, Div, Mod, Sub, Add
from .assignement import Asi, Typ, Global, Local, IsExist, Del
from .boucle import For, IFor, While, Repeat, Break, Continue
from .redirec import RedirecItem, RedirecPoint
from .errors import Try, Except, Raise
from .conditions import (
    Not, Inf, Sup, InfOrEga, SupOrEga, Ega, EgaObj, In, RemIn, PopIn,
    And, Or, XAnd, XOr
)
from .types.bloc import Bloc, Up, Down
from .types.bool import True__, False__
from .types.call import Call, Attachement
from .types.event import Event, Hidden
from .types.inscond import InsCond
from .types.intervalle import Intervalle
from .types.nbr import Pos, Neg, Nul
from .types.objet import Objet
from .types.table import Table
from .types.txt import Txt
from .types.var import Var


class Ligne:

    def __init__(self, path_file):
        self.value = 1
        self.path_file = path_file

    def __call__(self):
        self.value += 1

    def __str__(self):
        return "[L~%s in file %s]" % (self.value, self.path_file)


class Conteneur:

    def __init__(self, value, last, ligne):

        self.value = value

        self.last = last

        self.ligne = ligne

    def push__(self, value):

        value.ligne__ = str(self.ligne)

        return Conteneur(value, self, self.ligne)

    def rem__(self):

        last = self.last

        ligne__ = self.value.ligne__

        self.value.end__(self)

        self.value.ligne__ = ligne__

        return last

    def action(self, objet, Act, acts=None, *, get_last=True, prio=False):

        cont = self

        cont, objet = end_objet(cont, objet)

        if acts:
            while isinstance(cont.value, acts):
                cont = cont.rem__()

        if not isinstance(cont.value, Act) or prio:
            act = Act()
            
            if get_last:
                act.push__(cont.value.pop__())

            cont.value.push__(act)
            cont = cont.push__(act)

            act.ligne__ = str(self.ligne)

        if get_last:
            cont.value.liée = True

        return None, cont

    def mise_a_niveau(self, acts):

        cont = self

        value_type = type(cont.value)

        while value_type in acts and not cont.value.liée:
            while not isinstance(cont.value, value_type):
                cont = cont.rem__()

            cont = cont.rem__()
            value_type = type(cont.value)

        cont.value.liée = False

        return cont

def action(cont, Act):

    if not isinstance(cont.value, Act):
        act = Act()
        act.push__(cont.value.pop__())

        act.ligne__ = str(cont.ligne)

        cont.value.push__(act)
        cont = cont.push__(act)

    return cont


def end_objet(cont, objet):

    if objet is None:
        return cont, objet


    objet.end__(cont)

    objet.ligne__ = str(cont.ligne)

    value = objet.value


    ### Condition

    if value == 'if':
        cont.value.push__(None)
        objet, cont = cont.action(None, InsCond)    

    elif value == 'elif':
        objet, cont = cont.action(None, InsCond)

    elif value == 'else':
        objet, cont = cont.action(None, InsCond)
        cont.value.push__(True__)


    ### Boucle

    elif value == 'for':
        objet, cont = cont.action(None, For, get_last=False)    

    elif value == 'ifor':
        objet, cont = cont.action(None, IFor, get_last=False)    

    elif value == 'while':
        objet, cont = cont.action(None, While, get_last=False)    

    elif value == 'repeat':
        objet, cont = cont.action(None, Repeat, get_last=False)    

    elif value == 'break':
        cont.value.push__(Break())

    elif value == 'continue':
        cont.value.push__(Continue())


    ### Déplacement

    elif value == 'up':
        # [up]
        objet, cont = cont.action(None, Up, get_last=False) 
        cont.value.liée = True

    elif value == 'down':
        # [down]
        objet, cont = cont.action(None, Down, get_last=False) 
        cont.value.liée = True


    ### Var

    elif value == 'del':
        objet, cont = cont.action(None, Del, get_last=False)    
        cont.value.liée = True

    elif value == 'hide':
        objet, cont = cont.action(None, Hidden, get_last=False)    
        cont.value.liée = True

    elif value == 'local':
        objet, cont = cont.action(None, Local, get_last=False)    
        cont.value.liée = True

    elif value == 'global':
        objet, cont = cont.action(None, Global, get_last=False)    
        cont.value.liée = True

    elif value == 'return':
        objet, cont = cont.action(None, Return, get_last=False)    
        cont.value.liée = True


    ### Cond

    elif value == 'in':
        if not isinstance(cont.value, (For, IFor)):
            objet, cont = cont.action(None, In)
        cont.value.push__(SigneAction)

    elif value == 'remin':
        objet, cont = cont.action(None, RemIn)
        cont.value.push__(SigneAction)

    elif value == 'popin':
        objet, cont = cont.action(None, PopIn)
        cont.value.push__(SigneAction)


    ### Essaies

    elif value == 'raise':
        objet, cont = cont.action(None, Raise, get_last=False)
        cont.value.liée = True

    elif value == 'try':
        objet, cont = cont.action(None, Try, get_last=False)    

    elif value == 'except':
        if isinstance(cont.value, Try):
            cont = cont.rem__()
        objet, cont = cont.action(None, Except)


    ### Event

    elif value == 'event':

        cont = cont.mise_a_niveau((
            RedirecItem, RedirecPoint, Intervalle, Typ, Attachement, Asi, Hidden, Global, Return, IsExist,
            Not, Inf, Sup, InfOrEga, SupOrEga, Ega, In, RemIn, PopIn, Rac, Exp, Mul, Div, Mod, Sub, Add
        ))
        
        while not isinstance(cont.value, Bloc):
            cont = cont.rem__()

        objet, cont = cont.action(None, Event, get_last=False)  


    ### Autre

    else:
        cont.value.push__(objet)

    return cont, None


def decode(data, path_file):

    cont = Conteneur(Bloc(), None, Ligne(path_file))
    cont.value.liée = False

    objet = None


    acts_var = (Asi, Hidden, Global, Local, Return, IsExist, Del, Raise, Up, Down)

    acts_redirec = (RedirecItem, RedirecPoint, Intervalle, Typ, Attachement)

    acts_calcul = (Rac, Exp, Mul, Div, Mod, Sub, Add)

    acts_condition = (Not, Inf, Sup, InfOrEga, SupOrEga, Ega, In, RemIn, PopIn)

    acts_condition_niv_sup = (And, Or, XAnd, XOr)


    index_min = 0

    echappement = False


    for icarac, carac in enumerate(data):

        #print(carac, type(cont.value), cont.value.value)

        carac2 = data[icarac:icarac+2]

        if icarac < index_min:
            continue


        if carac == '\n':
            """
            pomme
            poire
            """
            cont.ligne()
            carac = ' '

        if carac == '\t':
            """
            pomme   poire
            """
            continue


        ### Commentaire

        """
        //
            Bla bla bla
        //
        """

        if isinstance(objet, Commentaire):
            if carac2 == '//':
                index_min = icarac + 2
                objet = None

        elif carac2 == '//':
            index_min = icarac + 2
            objet = Commentaire()


        ### Echappement

        elif carac ==  '\\':

            if echappement:
                # pouet = "abcd\\efgh"
                cont.value.push__('\\')
                echappement = False

            else:
                # pouet = "abcd\efgh"
                echappement = True

        elif echappement:

            if isinstance(objet, Txt):
                add = objet.push__

                if carac == 'n':
                    # piaf = "hiboux\ncailloux"
                    add('\n')

                elif carac == 't':
                    # piaf = "hiboux\tcailloux"
                    add('\t')

                elif carac == 'e':
                    # piaf = "hiboux\ecailloux"
                    add('')

                elif carac == '"':
                    # piaf = "hiboux\"cailloux"
                    add('"')

                elif carac == "'":
                    # piaf = 'hiboux\'cailloux'
                    add("'")

            else:
                add = cont.value.push__

                if carac == 'n':
                    # piaf = "hiboux" + \n
                    add(Txt('\n'))

                elif carac == 't':
                    # piaf = "hiboux" + \t
                    add(Txt('\t'))

            echappement = False


        ### Texte

        elif isinstance(objet, Txt):

            if (   # Balise fermente
                   (carac == '"' and objet._symb == '"') # ""
                or (carac == "'" and objet._symb == "'") # ''
            ):
                cont, objet = end_objet(cont, objet)

            else:
                objet.push__(carac)

        elif carac == '"' or carac == "'":
            # pouf = ""
            # pouf = ''

            cont, objet = end_objet(cont, objet)

            cont = cont.mise_a_niveau(
                acts_redirec + acts_var + acts_condition 
                + acts_calcul + acts_condition_niv_sup
            )

            objet = Txt()
            objet._symb = carac


        ### Redirection

        elif carac == '.':
            # pouet = arbre.branche.feuille

            if isinstance(objet, (Pos, Neg, Nul)):
                objet.push__('.')
                continue

            cont, objet = end_objet(cont, objet)

            cont = action(cont, RedirecPoint)

            cont.value.liée = True

        elif carac == '#':
            # pouet = arbre#'branche'#'feuille'

            cont, objet = end_objet(cont, objet)

            if isinstance(cont.value, RedirecPoint):
                cont = cont.rem__()
                
            cont = action(cont, RedirecItem)

            cont.value.liée = True


        ### Attachement

        elif carac == '~':
            # pouet~piaf

            cont = cont.mise_a_niveau((RedirecPoint, Typ))

            cont, objet = end_objet(cont, objet)

            objet, cont = cont.action(objet, Attachement)

            cont.value.liée = True


        ### Intervalle

        elif carac == ';':
            # cuik = 1;10;2

            cont, objet = end_objet(cont, objet)

            while isinstance(
                    cont.value, 
                    acts_calcul + (RedirecPoint, Typ, Attachement)
                ):
                cont = cont.rem__()

            cont = action(cont, Intervalle)

            cont.value.push__(SigneAction)

            cont.value.liée = True


        ### Calcul
                
        elif carac == '+':
            # pouet = 1 + 1

            cont, objet = end_objet(cont, objet)

            if not isinstance(cont.value.last__(), (RedirecPoint, RedirecItem, Var, Nul, Pos, Neg, Txt, Call, Prio)):

                cont = cont.mise_a_niveau(
                    acts_redirec + acts_var + acts_condition + acts_calcul + acts_condition_niv_sup
                )

                nul = Nul(0)
                nul.ligne__ = str(cont.ligne)
                cont.value.push__(nul)

            objet, cont = cont.action(objet, Add, (Rac, Exp, Mul, Div, Mod, Sub, RedirecItem, RedirecPoint, Typ))

        elif carac == '-':
            # pouet = 1 - 1

            cont, objet = end_objet(cont, objet)

            if not isinstance(cont.value.last__(), (RedirecPoint, RedirecItem, Var, Nul, Pos, Neg, Txt, Call, Prio)):

                cont = cont.mise_a_niveau(
                    acts_redirec + acts_var + acts_condition + acts_calcul + acts_condition_niv_sup
                )

                nul = Nul(0)
                nul.ligne__ = str(cont.ligne)
                cont.value.push__(nul)

            objet, cont = cont.action(objet, Sub, (Rac, Exp, Mul, Div, Mod, Add, RedirecItem, RedirecPoint, Typ))
                
        elif carac == '/':
            # pouet = 1 / 1

            objet, cont = cont.action(objet, Div, (Rac, Exp, Mod, Mul, RedirecItem, RedirecPoint, Typ))
                
        elif carac == '%':
            # pouet = 1 % 1

            objet, cont = cont.action(objet, Mod, (Rac, Exp, Mul, Div, RedirecItem, RedirecPoint, Typ))

        elif carac == '*':
            # pouet = 1 * 1

            objet, cont = cont.action(objet, Mul, (Rac, Exp, Mod, Div, RedirecItem, RedirecPoint, Typ))

        elif carac == '^':
            # pouet = 1 ^ 1

            objet, cont = cont.action(objet, Exp, (Rac, RedirecItem, RedirecPoint, Typ))

        elif data[icarac:icarac+3] == ' V ':

            index_min = icarac + 3

            objet, cont = cont.action(objet, Rac, (Exp, RedirecItem, RedirecPoint, Typ))

        ### Condition

        elif carac == '!':
            # !1 == 0
            # !!1 == 1

            cont = cont.mise_a_niveau(
                acts_redirec + acts_var + acts_condition 
                + acts_calcul + acts_condition_niv_sup
            )

            objet, cont = cont.action(objet, Not, get_last=False, prio=True)    

            cont.value.liée = True

        elif carac2 == '<=':
            # 5 <= 6

            index_min = icarac + 2

            objet, cont = cont.action(objet, InfOrEga, acts_redirec + acts_calcul + (Hidden, IsExist, Not))

            cont.value.push__(SigneAction)

        elif carac2 == '>=':
            # 5 >= 6

            index_min = icarac + 2

            objet, cont = cont.action(objet, SupOrEga, acts_redirec + acts_calcul + (IsExist, Not, Hidden))

            cont.value.push__(SigneAction)

        elif carac == '<':
            # 5 < 6

            objet, cont = cont.action(objet, Inf, acts_redirec + acts_calcul + (IsExist, Not, Hidden))

            cont.value.push__(SigneAction)

        elif carac == '>':
            # 5 > 6

            objet, cont = cont.action(objet, Sup, acts_redirec + acts_calcul + (IsExist, Not, Hidden))

            cont.value.push__(SigneAction)

        elif data[icarac:icarac+3] == '===':
            # 5 === 6

            index_min = icarac + 3

            objet, cont = cont.action(objet, EgaObj, acts_redirec + acts_calcul + (IsExist, Not, Hidden))

            cont.value.push__(SigneAction)

        elif carac2 == '==':
            # 5 == 6

            index_min = icarac + 2

            objet, cont = cont.action(objet, Ega, acts_redirec + acts_calcul + (IsExist, Not, Hidden))

            cont.value.push__(SigneAction)

        elif carac2 == '&&':
            # 5 > 6 && 5 == 5

            index_min = icarac + 2

            objet, cont = cont.action(objet, XAnd, acts_redirec + acts_calcul + acts_condition + (IsExist, Hidden, And, Or, XOr))

            cont.value.push__(SigneAction)

        elif carac == '&':
            # 5 > 6 & 5 == 5

            objet, cont = cont.action(objet, And, acts_redirec + acts_calcul + acts_condition + (IsExist, Hidden, Or))

            cont.value.push__(SigneAction)

        elif carac2 == '||':
            # 5 > 6 || 5 == 5

            index_min = icarac + 2

            objet, cont = cont.action(objet, XOr, acts_redirec + acts_calcul + acts_condition + (IsExist, Hidden, And, Or, XAnd))

            cont.value.push__(SigneAction)

        elif carac == '|':
            # 5 > 6 | 5 == 5

            objet, cont = cont.action(objet, Or, acts_redirec + acts_calcul + acts_condition + (IsExist, Hidden, And))

            cont.value.push__(SigneAction)

        ### Variable

        elif carac == ':':
            # pouet:pos = 1:neg

            objet, cont = cont.action(objet, Typ, (
                RedirecPoint, # pomme.pouet:pos
                Local,        # local pouf:pos
                Global,       # global pouf:pos
                Hidden        # hide pouf:pos
            ))

        elif carac == '=':
            # pouet = 1

            objet, cont = cont.action(
                objet, Asi, (Hidden, Global, Return, Typ) + acts_redirec
            )

            cont.value.push__(SigneAction)

        elif carac == '?':
            # pouet = pouf ? pomme ? 0

            objet, cont = cont.action(objet, IsExist, acts_redirec)

            cont.value.push__(SigneAction)


        ### Priorité

        elif carac == '(':
            # (1 + 1) * 5

            cont.value.liée = False

            objet, cont = cont.action(objet, Prio, get_last=False, prio=True)

        elif carac == ')':

            cont, objet = end_objet(cont, objet)

            while not isinstance(cont.value, Prio):
                cont = cont.rem__()

            cont = cont.rem__()


        ### Bloc de code

        elif carac == '[':

            objet, cont = cont.action(
                objet, 
                Bloc, 
                acts_condition_niv_sup + acts_calcul + acts_condition 
                + acts_redirec + acts_var, 
                get_last=False, prio=True
            )

        elif carac == ']':

            cont, objet = end_objet(cont, objet)

            while not isinstance(cont.value, Bloc):
                cont = cont.rem__()

            cont = cont.rem__()

            if isinstance(cont.value, (
                    Objet,    # @'pouet' [1 + 2]
                    Event,    # event date minute == 60 []
                    InsCond,  # if a < b [] elif a > b [] else []
                    For,      # for a in b []
                    IFor,     # ifor a, b in c []
                    While,    # while a == b []
                    Repeat,   # repeat 20 []
                    Except    # try a = b except []
                )):
                cont = cont.rem__()


        ### Table

        elif carac == '{':

            cont, objet = end_objet(cont, objet)

            if isinstance(cont.value, Typ):
                # pouet:pos{}
                cont = cont.rem__()
                objet, cont = cont.action(objet, Call, (RedirecPoint,))

            elif (
                not isinstance(cont.value, Objet)
                and isinstance(cont.value.last__(), (
                    Var,           # pouet{}
                    RedirecPoint,  # pouf.piaf{}
                    Call,          # piaf{}{}
                    Prio           # (123 + 456){}
            ))):
                objet, cont = cont.action(objet, Call, (RedirecPoint,))

            else:
                cont = cont.mise_a_niveau(
                    acts_redirec + acts_var + acts_calcul 
                    + acts_condition + acts_condition_niv_sup
                )

            objet, cont = cont.action(objet, Table, get_last=False, prio=True)

        elif carac == '}':

            cont, objet = end_objet(cont, objet)

            while not isinstance(cont.value, Table):
                cont = cont.rem__()

            cont = cont.rem__()

            # pouet{}
            if isinstance(cont.value, Call):
                cont = cont.rem__()


        ### Foncion

        elif carac == '@':
            # @'pouet' {a, b}[return a + b]

            cont = cont.mise_a_niveau(
                acts_redirec + acts_var + acts_condition
                + acts_calcul + acts_condition_niv_sup
            )

            cont, objet = end_objet(cont, objet)

            objet, cont = cont.action(objet, Objet, get_last=False)

            if isinstance(cont.last.value, Asi):

                value = cont.last.value.value[0]

                if isinstance(value, Var):
                    cont.value.push__(Txt(value.value))

                elif isinstance(value, RedirecPoint):
                    cont.value.push__(Txt(value.value.split('.')[-1]))

                elif isinstance(value, RedirecItem):
                    cont.value.push__(value.value[-1])


        ### Séparation

        elif carac == ',':
            # pomme, poire, pouf

            # Pour éviter les cas comme `{pomme, {1, 2, 3}}`
            cont.value.push__(SigneAction)


        ### Autre

        elif carac == ' ':

            if objet is None:
                continue

            cont, objet = end_objet(cont, objet)


        elif objet is not None:

            objet.push__(carac)

        else:

            cont = cont.mise_a_niveau(
                acts_redirec + acts_var + acts_condition 
                + acts_calcul + acts_condition_niv_sup
            )

            if carac == '0' and data[icarac+1] != '.':
                # 0

                objet = Nul()
                objet.end__(cont)

            elif carac in list('0123456789'):
                # 0.0, 0.1, 2, 3, 345, 8.9

                objet = Pos()
                objet.push__(carac)
            
            else:
                # pomme, poire, pouet

                objet = Var()
                objet.push__(carac)


    if objet:
        objet.end__(cont)
        cont.value.push__(objet)
        objet = None

    while cont.last:
        cont = cont.rem__()

    cont.value.end__(cont)

    return cont.value