from sardana.pool.controller import PseudoCounterController
import PyTango

class pseudoCounterAltOn(PseudoCounterController):
    """ A simple pseudo counter which receives two counter values (I and I0)
        and returns I/I0"""

    counter_roles        = ('Pumped', 'PumpedErr', 'Unpumped','UnpumpedErr', 'Rel', 'duration', 'numTriggers')
    pseudo_counter_roles = ('PumpedM','PumpedErrM', 'UnpumpedM','UnpumpedErrM', 'RelM', 'durationM', 'numTriggersM')
    value = [0]*7

    def Calc(self, axis, counters):
        counter = counters[axis-1]
        
        kepco = PyTango.DeviceProxy("motor/kepcoctrl/0")
        field = kepco.position
      
        if field < 0:
            self.value[axis-1] = counter        

        return self.value[axis-1]