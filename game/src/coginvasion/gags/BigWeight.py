"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file BigWeight.py
@author Maverick Liberty
@date August 30, 2015

"""

from src.coginvasion.gags.DropGag import DropGag
from src.coginvasion.gags import GagGlobals
from src.coginvasion.globals import CIGlobals
from direct.interval.IntervalGlobal import Sequence, LerpPosInterval, LerpScaleInterval, Func, Wait, Parallel
from direct.showutil import Effects
from panda3d.core import OmniBoundingVolume, Point3

class BigWeight(DropGag):
      
    name = GagGlobals.BigWeight
    model = 'phase_5/models/props/weight-mod.bam'
    anim = 'phase_5/models/props/weight-chan.bam'
    hitSfxPath = GagGlobals.WEIGHT_DROP_SFX
    missSfxPath = GagGlobals.WEIGHT_MISS_SFX

    def __init__(self):
        DropGag.__init__(self)
        self.setImage('phase_3.5/maps/big-weight.png')
        self.colliderRadius = 2

    def startDrop(self, entity):
        if entity and self.dropLoc:
            endPos = self.dropLoc
            startPos = Point3(endPos.getX(), endPos.getY(), endPos.getZ() + 20)
            dropMdl = entity.find('**/DropMdl')
            entity.setPos(startPos.getX(), startPos.getY() + 2, startPos.getZ())
            dropMdl.setScale(dropMdl.getScale() * 0.75)
            entity.node().setBounds(OmniBoundingVolume())
            entity.node().setFinal(1)
            entity.headsUp(self.avatar)
            self.buildCollisions(entity)
            objectTrack = Sequence()
            animProp = LerpPosInterval(entity, self.fallDuration, endPos, startPos = startPos)
            bounceProp = Effects.createZBounce(entity, 2, endPos, 0.5, 1.5)
            objAnimShrink = Sequence(Wait(0.5), Func(entity.reparentTo, render), animProp, bounceProp)
            objectTrack.append(objAnimShrink)
            dropShadow = CIGlobals.makeDropShadow(1.0)
            dropShadow.reparentTo(hidden)
            dropShadow.setPos(endPos)
            shadowTrack = Sequence(Func(dropShadow.reparentTo, render), LerpScaleInterval(dropShadow, self.fallDuration + 0.1, (1, 1, 1),
                                startScale=Point3(0.01, 0.01, 0.01)), Wait(0.8), Func(dropShadow.removeNode))
            Parallel(Sequence(Wait(self.fallDuration), Func(self.completeDrop), Wait(4), Func(self.clearEntity, entity)), objectTrack, shadowTrack).start()
            self.dropLoc = None
