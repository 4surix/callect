from ..base import Base


class InsCond(Base):
    
    def __call__(self, variables):

        if self.prioCond and self.prioCond(variables):
            return True

        if self.conditions(variables):
            self.bloc(variables)
            return True

        return False

    def end__(self, cont):

        if len(self.value) == 2:
            self.prioCond = None
            self.conditions, self.bloc = self.value

        else:
            self.prioCond, self.conditions, self.bloc = self.value