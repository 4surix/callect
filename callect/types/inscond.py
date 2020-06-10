from ..base import Base
from ..errors import SyntaxIncorrect
from .bool import False__, True__


# Instruction conditionnel

class InsCond(Base):
    
    def __call__(self, variables):

        for condition, bloc in self.insconds:
            if condition(variables):
                return bloc(variables)

        return False__

    def end__(self, cont):

        if len(self.value) == 3:
            inscond, condition, bloc = self.value

            if inscond is None:
                """
                if 1 []
                """
                insconds = []

            elif inscond.__class__.__name__ == 'Try':
                """
                try 1 + 1
                else []
                """
                raise SyntaxIncorrect(self.ligne__)

            elif inscond.__class__.__name__ == 'Except':
                """
                try 1 + 1
                except []
                else []
                """
                insconds = [(inscond, lambda vars: None)]

            else:
                """
                elif 1 []
                else []
                """
                insconds = inscond.insconds

            self.insconds = insconds + [(condition, bloc)]

        else:
            raise SyntaxIncorrect(self.ligne__)