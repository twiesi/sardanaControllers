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

from sardana import State
from sardana.pool.controller import CounterTimerController
from sardana.pool import PoolUtil
import sys
import PyTango

class motorPosCounterController(CounterTimerController):
    """The most basic controller intended from demonstration purposes only.
    This is the absolute minimum you have to implement to set a proper counter
    controller able to get a counter value, get a counter state and do an
    acquisition.

    This example is so basic that it is not even directly described in the
    documentation"""
    
    def AddDevice(self, axis):
        pass

    def DeleteDevice(self, axis):
        pass

    def __init__(self, inst, props, *args, **kwargs):
        """Constructor"""
        super(motorPosCounterController,
              self).__init__(inst, props, *args, **kwargs)
                
        #self.dev = 'tango://epics-archiver.hhg.lab:10000/motor/kepcoctrl/1'
        #self.
        #pos = dev_proxy.read_attribute('position').value
        #PoolUtil().get_device(self.inst_name, self.dev)

        #print "Connected to: " + self.dev
        
        self.motor_device = PyTango.DeviceProxy("motor/kepcoctrl/1")
        
    def ReadOne(self, axis):
        """Get the specified counter value"""
        try:            
            return 1#return self.motor_device.position
        except:
            print "Unexpected error:", sys.exc_info()[0]
            return 0#dev.position#self.dev_proxy.position#self.dev_proxy.read_attribute('position').value
    
    def StateOne(self, axis):
        """Get the specified counter state"""
        return State.On, "Counter is stopped"
        
    def StartOne(self, axis, value=None):
        """acquire the specified counter"""
        pass
    
    def StartAll(self):
        pass
    
    def LoadOne(self, axis, value, repetitions):
        pass

    def StopOne(self, axis):
        """Stop the specified counter"""
        pass