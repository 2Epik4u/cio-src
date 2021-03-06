"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file BackpackAI.py
@author Maverick Liberty
@date March 20, 2016

@desc The AI version of the backpack.

"""

from src.coginvasion.gags.backpack.BackpackBase import BackpackBase

class BackpackAI(BackpackBase):

    # Sets the supply on each gag in this backpack to the default max.
    def refillSupply(self):
        for gagId in self.avatar.attacks.keys():
            self.setSupply(gagId, self.getMaxSupply(gagId))
    
    # Sets the supply of a gag in the backpack.
    # Returns true or false if the supply was set.
    def setSupply(self, gagId, supply, updateEnabled=True):
        updatedSupply = BackpackBase.setSupply(self, gagId, supply)
        if updatedSupply and updateEnabled:
            self.updateNetAmmo()
        return updatedSupply
    
    # Update the network ammo.
    def updateNetAmmo(self):
        self.avatar.b_setBackpackAmmo(self.toNetString())
