"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file CogOfficeInterior.py
@author Brian Lach
@date December 17, 2015

"""

from direct.fsm import ClassicFSM, State

from src.coginvasion.globals import CIGlobals
from src.coginvasion.hood.Place import Place

class CogOfficeInterior(Place):

    def __init__(self, loader, parentFSM, doneEvent):
        self.parentFSM = parentFSM
        Place.__init__(self, loader, doneEvent)
        self.interior = True
        self.fsm = ClassicFSM.ClassicFSM('CogOfficeInterior', [State.State('start', self.enterStart, self.exitStart, ['stop', 'walk']),
         State.State('walk', self.enterWalk, self.exitWalk, ['stop', 'teleportOut', 'died']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['stop', 'final']),
         State.State('stop', self.enterStop, self.exitStop, ['final', 'walk', 'teleportOut']),
         State.State('died', self.enterDied, self.exitDied, ['final']),
         State.State('shtickerBook', self.enterShtickerBook, self.exitShtickerBook,
                    ['teleportOut', 'walk']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut,
                    ['stop', 'final']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')

    def enter(self, requestStatus):
        Place.enter(self)
        self.fsm.enterInitialState()

    def load(self):
        Place.load(self)
        self.parentFSM.getStateNamed('suitInterior').addChild(self.fsm)

    def unload(self):
        self.parentFSM.getStateNamed('suitInterior').removeChild(self.fsm)
        del self.fsm
        del self.parentFSM
        self.ignoreAll()
        Place.unload(self)
        return
