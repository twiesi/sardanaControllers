##############################################################################
##
# This file is part of Sardana
##
# http://www.sardana-controls.org/
##
# Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
##
# Sardana is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
##
# Sardana is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
##
# You should have received a copy of the GNU Lesser General Public License
# along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""This file contains the code for an hypothetical Springfield motor controller
used in documentation"""

from zaber.serial import BinarySerial, BinaryCommand    # Import der Binary Libary von Zaber
import time # denke ein Python interner Befehl für die Zeit?
from sardana import State # 
from sardana.pool.controller import MotorController # Import von Sardana einer Controller Klasse --> MotorController
from sardana.pool.controller import Type, Description, DefaultValue # Import von sardana Konstanten


class ZaberTMMController(MotorController): # Steuerung wird der MotorController Klasse zugewiesen
    ctrl_properties = {'port': {Type: str,
                                Description: 'The port of the rs232 device', #Port des Controllers
                                DefaultValue: '/dev/ttyZaber'}}
    axis_attributes = {
    "Homing" : {
            Type         : bool,
            Description  : "(de)activates the motor homing algorithm", #warum "Homing# und 'port'
            DefaultValue : False,
        },
    }
    
    MaxDevice = 2
    
    def __init__(self, inst, props, *args, **kwargs):
        super(ZaberTMMController, self).__init__(
            inst, props, *args, **kwargs)

        # initialize hardware communication
        self.con = BinarySerial(self.port, timeout=5)
        
        print('Zaber TMM Controller Initialization ...'),
        print('SUCCESS on port %s' % self.port)
        # do some initialization
        self._motors = {}

    def AddDevice(self, axis):
        self._motors[axis] = True
        # change setting of devices, because they are non-volatile
        # disable auto-reply 1*2^0
        # enable backlash correction 1*2^1
        command_number = 40 # set device mode # muss man hier nicht noch die dezimalzahl angeben? also je nachdem was du disable/enable willst?
        command = BinaryCommand(axis, command_number, 3) # ok das passiert hier
        self.con.write(command)

    def DeleteDevice(self, axis):
        del self._motors[axis]

    StateMap = {
        1: State.On,
        2: State.Moving,
        3: State.Fault,
    }

    def StateOne(self, axis):
        limit_switches = MotorController.NoLimitSwitch     
        command_number = 54 # return status
        command = BinaryCommand(axis, command_number)
        self.con.write(command)
        reply = self.con.read()
        
        while (reply.command_number != command_number) & (reply.device_number != axis):
            self.con.write(command)
            reply = self.con.read()
            time.sleep(0.2)
            
        if reply.data == 0: # idle
            return self.StateMap[1], 'Zaber is idle', limit_switches
        elif (reply.data >= 1) & (reply.data <=23):
            return self.StateMap[2], 'Zaber is moving', limit_switches
        else:
            return self.StateMap[3], 'Zaber is faulty', limit_switches      

    def ReadOne(self, axis):
        command_number = 60 # return current position
        command = BinaryCommand(axis, command_number)
        self.con.write(command)
        reply = self.con.read()
        
        while (reply.command_number != command_number) & (reply.device_number != axis):
            self.con.write(command)
            reply = self.con.read()
            time.sleep(0.2)
        
        return int(reply.data)
        
    def StartOne(self, axis, position):
        command_number = 20 # move absolute
        command = BinaryCommand(axis, command_number, int(position))
        self.con.write(command)

    def StopOne(self, axis):
        command_number = 23 # move absolute
        command = BinaryCommand(axis, command_number)
        self.con.write(command)

    def AbortOne(self, axis):
        command_number = 23 # move absolute
        command = BinaryCommand(axis, command_number)
        self.con.write(command)

    def setHoming(self, axis, value):
        """Homing for given axis"""
        if value:       
            command_number = 1 # homing
            command = BinaryCommand(axis, command_number)
            self.con.write(command)
    
    def getHoming(self, axis):
        """Homing for given axis"""       
        return False
