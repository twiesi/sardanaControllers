import numpy as np

from sardana.pool.controller import PseudoMotorController
from sardana.pool.controller import Type, Description, DefaultValue, Access, FGet, FSet, DataAccess, Memorize, Memorized


class powerPseudoMotorController(PseudoMotorController):
    """A Slit pseudo motor controller for handling gap and offset pseudo 
       motors. The system uses to real motors sl2t (top slit) and sl2b (bottom
       slit)."""
        
    axis_attributes  = {'offset': {Type: float, Description: 'offset', DefaultValue: 0, Memorized: Memorize},
                       'period': {Type: float, Description: 'period', DefaultValue: 1, Memorized: Memorize},
                       'P0': {Type: float, Description: 'P0', DefaultValue: 0, Memorized: Memorize},
                       'Pm': {Type: float, Description: 'Pm', DefaultValue: 1, Memorized: Memorize},
                       }
    
    
    pseudo_motor_roles = ("OutputMotor",)
    motor_roles = ("InputMotor",)
        
    def __init__(self, inst, props):  
        PseudoMotorController.__init__(self, inst, props)
    
    def CalcPhysical(self, axis, pseudo_pos, curr_physical_pos):
        power = pseudo_pos[axis-1]
        return np.degrees(np.arcsin(np.sqrt((power-self.P0)/self.Pm)))/2/self.period + self.offset
    
    def CalcPseudo(self, axis, physical_pos, curr_pseudo_pos):
        wp = physical_pos[axis-1]
        return self.Pm*(np.sin(np.radians(wp-self.offset)*2*self.period)**2)+self.P0
    
    def GetAxisExtraPar(self, axis, name):
        """ Get Smaract axis particular parameters.
        @param axis to get the parameter
        @param name of the parameter to retrive
        @return the value of the parameter
        """
        name = name.lower()
        
        if name == 'offset':
            result = self.offset
        elif name == 'period':
            result = self.period
        elif name == 'p0':
            result = self.P0
        elif name == 'pm':
            result = self.Pm
        else:
            raise ValueError('There is not %s attribute' % name)
        return result

    def SetAxisExtraPar(self, axis, name, value):
        """ Set Smaract axis particular parameters.
        @param axis to set the parameter
        @param name of the parameter
        @param value to be set
        """
        name = name.lower()
        if name == 'offset':
            self.offset = value
        elif name == 'period':
            self.period = value
        elif name == 'p0':
            self.P0 = value
        elif name == 'pm':
            self.Pm = value
        else:
            raise ValueError('There is not %s attribute' % name)
        