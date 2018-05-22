import numpy as np

from sardana import pool
from sardana.pool import PoolUtil
from sardana.pool.controller import PseudoMotorController


class powerPseudoMotorController(PseudoMotorController):
    """A Slit pseudo motor controller for handling gap and offset pseudo 
       motors. The system uses to real motors sl2t (top slit) and sl2b (bottom
       slit)."""
    
    pseudo_motor_roles = ("OutputMotor",)
    motor_roles = ("InputMotor",)
    
    attOffset = 0
    attPeriod = 1
    P0 = 0
    Pm = 1
    
    def __init__(self, inst, props):  
        PseudoMotorController.__init__(self, inst, props)
    
    def CalcPhysical(self, axis, pseudo_pos, curr_physical_pos):
        power = pseudo_pos[axis-1]
        return np.degrees(np.arcsin(np.sqrt((power-self.P0)/self.Pm)))/2/self.attPeriod + self.attOffset
    
    def CalcPseudo(self, axis, physical_pos, curr_pseudo_pos):
        wp = physical_pos[axis-1]
        return self.Pm*(np.sin(np.radians(wp-self.attOffset)*2*self.attPeriod)**2)+self.P0