from sardana.pool.controller import PseudoCounterController
import PyTango

class pseudoCounterAltOn(PseudoCounterController):
    """ A simple pseudo counter which receives two counter values (I and I0)
        and returns I/I0"""

    counter_roles        = ('I1', 'I2', 'I3', 'I4', 'I5', 'I6',  'I7',  'I8', )
    pseudo_counter_roles = ('O1', 'O2', 'O3', 'O4', 'O5', 'O6',  'O7',  'O8',)
    value = [0,0,0,0,0,0,0,0]
    field = 0
    
    def __init__(self, inst, props):  
        PseudoCounterController.__init__(self, inst, props)
        self.magnet = PyTango.DeviceProxy("motor/caenfastpsctrl/0")
        
    def Calc(self, axis, counters):
        counter = counters[axis-1]
        
        if axis == 1:
            self.field = self.magnet.position
      
        if self.field < 0:
            self.value[axis-1] = counter        

        return self.value[axis-1]