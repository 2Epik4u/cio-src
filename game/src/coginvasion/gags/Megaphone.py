"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file Megaphone.py
@author Brian Lach
@date July 23, 2015

"""

from src.coginvasion.gags.ToonUpGag import ToonUpGag
from src.coginvasion.gags import GagGlobals
from src.coginvasion.globals import CIGlobals
from direct.interval.IntervalGlobal import Sequence, Wait, Func, Parallel, ActorInterval

import random

class Megaphone(ToonUpGag):
    
    name = GagGlobals.Megaphone
    model = 'phase_5/models/props/megaphone.bam'
    minHeal = 10
    maxHeal = 20
    efficiency = 100
    hitSfxPath = GagGlobals.TELLJOKE_SFX
    
    def __init__(self):
        ToonUpGag.__init__(self)
        self.setImage('phase_3.5/maps/megaphone.png')
        self.track = None
        self.soundInterval = None
        self.timeout = 5.0

    def start(self):
        super(Megaphone, self).start()
        if not self.gag:
            self.build()
        if self.avatar == base.localAvatar:
            question, answer = random.choice(GagGlobals.ToonHealJokes)
        self.setupHandJoints()
        self.placeProp(self.handJoint, self.gag)
        self.soundInterval = self.getSoundTrack(self.avatar.getDuration('shout', fromFrame = 0, toFrame = 18), self.gag, 5.5)
        propInterval = Sequence()
        propInterval.append(Wait(self.avatar.getDuration('shout', fromFrame = 0, toFrame = 25)))
        if self.avatar == base.localAvatar:
            propInterval.append(Func(base.localAvatar.b_setChat, question))
        propInterval.append(Wait(self.avatar.getDuration('shout', fromFrame = 26, toFrame = 75)))
        if self.avatar == base.localAvatar:
            propInterval.append(Func(base.localAvatar.b_setChat, answer))
        propInterval.append(Wait(self.avatar.getDuration('shout', fromFrame = 76, toFrame = 118)))
        if self.avatar == base.localAvatar:
            propInterval.append(Func(self.setHealAmount))
            propInterval.append(Func(self.healNearbyAvatars, 20))
        propInterval.append(Wait(self.avatar.getDuration('shout', fromFrame = 118)))
        propInterval.append(Func(self.cleanupGag))
        propInterval.append(Func(self.reset))
        self.track = Parallel(propInterval, ActorInterval(self.avatar, 'shout'), self.soundInterval)
        self.track.start()

    def equip(self):
        super(Megaphone, self).equip()
        self.build()

    def unEquip(self):
        if self.track:
            self.track.finish()
            self.track = None
            self.soundInterval = None
        self.cleanupGag()
        self.reset()

    def cleanupGag(self):
        if self.gag:
            self.gag.removeNode()
            self.gag = None
