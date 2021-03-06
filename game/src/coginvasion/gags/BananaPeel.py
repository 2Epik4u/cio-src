"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file BananaPeel.py
@author Maverick Liberty
@date July 26, 2015

"""

from src.coginvasion.gags.ActivateTrapGag import ActivateTrapGag
from src.coginvasion.gags import GagGlobals
from direct.interval.IntervalGlobal import Parallel, Sequence, Wait, LerpPosInterval, LerpScaleInterval, ActorInterval, SoundInterval
from panda3d.core import Point3

class BananaPeel(ActivateTrapGag):
        
    name = GagGlobals.BananaPeel
    model = 'phase_5/models/props/banana-peel-mod.bam'
    hitSfxPath = GagGlobals.BANANA_SFX
    activateSfxPath = GagGlobals.FALL_SFX
    anim = 'phase_5/models/props/banana-peel-chan.bam'
    doesAutoRelease = True
    collRadius = 2.0

    def __init__(self):
        ActivateTrapGag.__init__(self)
        self.slipSfx = None
        self.setImage('phase_3.5/maps/banana-peel.png')

        if metadata.PROCESS == 'client':
            self.slipSfx = base.audio3d.loadSfx(GagGlobals.PIE_WOOSH_SFX)

    def onActivate(self, entity, suit):
        slidePos = entity.getPos(render)
        slidePos.setY(slidePos.getY() - 5.1)
        moveTrack = Sequence(Wait(0.1), LerpPosInterval(self.gag, 0.1, slidePos))
        animTrack = Sequence(ActorInterval(self.gag, 'banana', startTime=3.1), Wait(1.1), LerpScaleInterval(self.gag, 1,
                                        Point3(0.01, 0.01, 0.01)))
        suitTrack = ActorInterval(suit, 'slip-backward')
        soundTrack = Sequence(SoundInterval(self.slipSfx, duration=0.55, node=suit), SoundInterval(self.activateSfx, node=suit))
        Parallel(moveTrack, animTrack, suitTrack, soundTrack).start()
        ActivateTrapGag.onActivate(self, entity, suit)

    def equip(self):
        ActivateTrapGag.equip(self)
        self.build()
        self.gag.reparentTo(self.handJoint)
