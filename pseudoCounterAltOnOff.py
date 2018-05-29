from sardana.pool.controller import PseudoCounterController

class minusFieldCounter(PseudoCounterController):
    """ A simple pseudo counter which receives two counter values (I and I0)
        and returns I/I0"""

    counter_roles = "counter", "magfield"

    flip = 0

    def Calc(self, axis, counter_values):
        counter, magfield = counter_values
               
        self.flip += 1
        return self.flip
        
#        if self.flip == -1:
#            self.flip = 1
#            return -1
#        else:
#            self.flip = -1
#            return 1
    
class plusFieldCounter(PseudoCounterController):
    """ A simple pseudo counter which receives two counter values (I and I0)
        and returns I/I0"""

    counter_roles = "counter",

    def Calc(self, axis, counter_values):
#        counter = counter_values
        
        return 1
