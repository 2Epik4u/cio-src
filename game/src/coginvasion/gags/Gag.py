"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file Gag.py
@author Maverick Liberty
@date July 07, 2015

"""

from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.distributed import DelayDelete
from direct.interval.IntervalGlobal import Parallel, ParallelEndTogether, ActorInterval, Sequence, \
    LerpScaleInterval, SoundInterval, Wait, Func

from src.coginvasion.attack.BaseAttack import BaseAttack
from src.coginvasion.gags.GagState import GagState
from src.coginvasion.gags.GagType import GagType
from src.coginvasion.gags import GagGlobals
from src.coginvasion.globals import CIGlobals
from src.coginvasion.gui.Crosshair import CrosshairData
from src.coginvasion.base.Precache import precacheActor, precacheModel, precacheSound

from panda3d.core import Point3
from abc import ABCMeta
import abc

class Gag(BaseAttack, DirectObject):
    
    model = None
    anim = None
    scale = 1
    hitSfxPath = None
    name = "Gag"
    gagType = None
    multiUse = False

    def __init__(self):
        __metaclass__ = ABCMeta
        DirectObject.__init__(self)
        BaseAttack.__init__(self)
        self.avatar = None
        self.gag = None
        self.target = None
        self.splat = None
        self.splatPos = None
        self.state = GagState.LOADED
        self.woosh = None
        self.handJoint = None
        self.equipped = False
        self.index = None
        self.id = GagGlobals.getIDByName(self.name)
        self.timeout = 5
        self.animTrack = None
        self.holdGag = True

        # Handles the new recharging for certain gags.

        # The time it takes (in seconds) to recharge this gag.
        self.rechargeTime = 0

        # The elapsed time of the current recharge. Should be a float
        self.rechargeElapsedTime = 0

        if metadata.PROCESS == 'client':
            if self.gagType == GagType.THROW:
                self.woosh = base.audio3d.loadSfx(GagGlobals.PIE_WOOSH_SFX)
            self.hitSfx = base.audio3d.loadSfx(self.hitSfxPath)
            self.drawSfx = base.audio3d.loadSfx(GagGlobals.DEFAULT_DRAW_SFX)
            
    @classmethod
    def doPrecache(cls):
        if cls.anim:
            precacheActor([cls.model, {'chan' : cls.anim, 'zero' : cls.model}])
        elif cls.model:
            precacheModel(cls.model)
        if cls.hitSfxPath:
            precacheSound(cls.hitSfxPath)
    
    def setRechargeTime(self, time):
        self.rechargeTime = time

    def getRechargeTime(self):
        return self.rechargeTime

    def setRechargeElapsedTime(self, time):
        self.rechargeElapsedTime = time

    def getRechargeElapsedTime(self):
        return self.rechargeElapsedTime
        
    def handleRechargeComplete(self):
        pass

    def __doRecharge(self, task):
        task.delayTime = 0.1
        self.rechargeElapsedTime += 0.1
        messenger.send('%s-Recharge-Tick' % (str(self.getID())))

        if self.rechargeElapsedTime >= self.rechargeTime:
            if self.equipped:
                self.handleRechargeComplete()
            self.state = GagState.LOADED
            return task.done
        return task.again

    def startTimeout(self):
        base.localAvatar.gagsTimedOut = True
        base.taskMgr.doMethodLater(self.timeout, self.__timeoutDone, self.avatar.uniqueName('timeoutDone'))

    def __timeoutDone(self, task):
        base.localAvatar.gagsTimedOut = False
        equippedAGag = False
        if base.localAvatar.needsToSwitchToGag != None:
            if base.localAvatar.needsToSwitchToGag != self.getID() and base.localAvatar.needsToSwitchToGag != 'unequip':
                base.localAvatar.b_setCurrentGag(base.localAvatar.needsToSwitchToGag)
                equippedAGag = True
            elif base.localAvatar.needsToSwitchToGag == 'unequip':
                base.localAvatar.b_setCurrentGag(-1)
        if self.equipped and base.localAvatar.backpack.getSupply(self.id) > 0 and not equippedAGag:
            base.localAvatar.b_setCurrentGag(self.id)
        if base.localAvatar.avatarMovementEnabled:
            base.localAvatar.enableGagKeys()
        return task.done

    def stopTimeout(self):
        base.taskMgr.remove(self.avatar.uniqueName('timeoutDone'))

    @abc.abstractmethod
    def primaryFirePress(self):
        if not self.avatar:
            return
        if self.avatar.getBackpack().getSupply(self.getID()) == 0 or self.state == GagState.RECHARGING:
            return
        try:
            base.audio3d.detachSound(self.woosh)
            self.track.pause()
            self.cleanupGag()
        except: pass
        self.state = GagState.START
        self.avatar.getBackpack().setActiveGag(self.getID())

    @abc.abstractmethod
    def reset(self):
        if not self.state == GagState.RECHARGING:
            self.state = GagState.LOADED
        self.target = None
        if self.avatar:
            backpack = self.avatar.getBackpack()
            if backpack.getActiveGag():
                if backpack.getActiveGag() == self:
                    backpack.setActiveGag(None)

                    if self.rechargeTime > 0 and self.isLocal():
                        self.state = GagState.RECHARGING
                        self.setRechargeElapsedTime(0)
                        messenger.send('%s-Recharge-Tick' % (str(self.getID())))
                        taskMgr.doMethodLater(0.5, self.__doRecharge, '%s-Recharge' % (str(self.getID())))
                        base.localAvatar.b_setCurrentGag(-1)

    @abc.abstractmethod
    def primaryFireRelease(self):
        if self.multiUse:
            if self.isLocal():
                base.localAvatar.enableGagKeys()

            self.state = GagState.LOADED

    @abc.abstractmethod
    def release(self):
        self.state = GagState.RELEASED
        return

    @abc.abstractmethod
    def buildCollisions(self):
        return

    @abc.abstractmethod
    def onCollision(self):
        pass

    def setAvatar(self, avatar):
        self.avatar = avatar
        if CIGlobals.isNodePathOk(self.avatar):
            base.audio3d.attachSoundToObject(self.drawSfx, self.avatar)
            if self.hitSfx:
                base.audio3d.attachSoundToObject(self.hitSfx, self.avatar)

    def getAvatar(self):
        return self.avatar

    def setState(self, paramState):
        self.state = paramState

    def getState(self):
        return self.state

    def setTarget(self, target):
        self.target = target

    def getTarget(self):
        return self.target

    def getType(self):
        return self.gagType

    def maybeBuild(self):
        if not self.gag:
            self.build()

    def build(self):
        if self.anim:
            self.gag = Actor(self.model, {'chan' : self.anim, 'zero' : self.model})
        else:
            self.gag = loader.loadModel(self.model)
        self.setHandJoint()
        self.gag.setScale(self.scale)
        self.gag.setName(self.getName())
        return self.gag

    def setHandJoint(self):
        if self.avatar:
            self.handJoint = self.avatar.find('**/def_joint_right_hold')

    def getSingularAnimTrack(self, anim):
        return Sequence(Func(self.avatar.setForcedTorsoAnim, anim), self.getAnimationTrack(anim), Func(self.avatar.clearForcedTorsoAnim))

    def setupViewModel(self):

        if self.gag:
            cam = base.localAvatar.getFPSCam()
            cam.setVMGag(self.gag)
        if base.localAvatar.isFirstPerson():
            base.localAvatar.getViewModel().show()

    def equip(self):
        if not self.avatar or not self.avatar.getBackpack() or self.avatar.getBackpack() and self.avatar.getBackpack().getSupply(self.getID()) == 0 or self.state == GagState.RECHARGING:
            return
        self.setHandJoint()
        
        entity = self.gag
        
        if not entity:
            entity = self.build()
        if self.holdGag:
            entity.show()
            entity.reparentTo(self.handJoint)
        self.equipped = True

        if self.isLocal():
            self.setupViewModel()

        self.avatar.getBackpack().setActiveGag(self.getID())

    @abc.abstractmethod
    def unEquip(self):
        if metadata.PROCESS != 'client':
            return
        if self.equipped and self.handJoint:
            inHand = self.handJoint.getChildren()
            for item in inHand:
                if(item.getName() == self.getName()):
                    item.removeNode()
            self.reset()
            
        self.equipped = False

        self.avatar.getBackpack().setActiveGag(None)

        self.clearAnimTrack()
        self.avatar.clearForcedTorsoAnim()

        if self.isLocal():
            base.localAvatar.getFPSCam().clearVMGag()
            base.localAvatar.getFPSCam().clearVMAnimTrack()
            base.localAvatar.getViewModel().hide()

    def setHealth(self, health):
        self.health = health

    def getHealth(self):
        return self.health

    def setImage(self, image):
        self.image = image

    def getImage(self):
        return self.image

    def getDamage(self):
        return self.damage

    def getName(self):
        return self.name

    def delete(self):
        self.unEquip()
        self.handJoint = None
        self.avatar = None
        self.state = None
        self.drawSfx = None
        self.cleanupGag()
        self.cleanupSplat()
        if self.woosh:
            self.woosh.stop()
            self.woosh = None
        if self.hitSfx:
            self.hitSfx.stop()
            self.hitSfx = None

    def cleanupGag(self):
        try:
            self.track.pause()
        except: pass
        if self.gag and not self.state in [GagState.RELEASED, GagState.START]:
            name = self.gag.getName()
            if isinstance(self.gag, Actor):
                self.gag.cleanup()
            if self.avatar:
                copies = self.avatar.findAllMatches('**/%s' % name)
                for copy in copies:
                    copy.removeNode()
            if self.gag and not self.gag.isEmpty():
                self.gag.removeNode()
            self.gag = None

    def getGag(self):
        return self.gag

    def placeProp(self, handJoint, prop, pos = None, hpr = None, scale = None):
        prop.reparentTo(handJoint)
        if pos:
            prop.setPos(pos)
        if hpr:
            prop.setHpr(hpr)
        if scale:
            prop.setScale(scale)

    def getScaleTrack(self, props, duration, startScale, endScale):
        track = Parallel()
        if not isinstance(props, list):
            props = [props]
        for prop in props:
            track.append(LerpScaleInterval(prop, duration, endScale, startScale = startScale))
        return track

    def getSoundTrack(self, delay, node, duration = None):
        base.audio3d.attachSoundToObject(self.hitSfx, node)
        soundTrack = Sequence()
        soundTrack.append(Wait(delay))
        if duration:
            soundTrack.append(SoundInterval(self.hitSfx, duration = duration))
        else:
            soundTrack.append(SoundInterval(self.hitSfx))
        return soundTrack

    def getScaleIntervals(self, props, duration, startScale, endScale):
        tracks = Parallel()
        if not isinstance(props, list):
            props = [props]
        for prop in props:
            tracks.append(LerpScaleInterval(prop, duration, endScale, startScale=startScale))
        return tracks

    def getScaleBlendIntervals(self, props, duration, startScale, endScale, blendType):
        tracks = Parallel()
        if not isinstance(props, list):
            props = [props]
        for prop in props:
            tracks.append(LerpScaleInterval(prop, duration, endScale, startScale=startScale, blendType=blendType))
        return tracks

    def buildSplat(self, scale, color):
        self.cleanupSplat()
        self.splat = Actor(GagGlobals.SPLAT_MDL, {'chan' : GagGlobals.SPLAT_CHAN})
        self.splat.setScale(scale)
        self.splat.setColor(color)
        self.splat.setBillboardPointEye()
        self.splat.play('chan')
        return self.splat

    def setSplatPos(self, x, y, z):
        self.cleanupGag()
        self.splatPos = Point3(x, y, z)
        self.handleSplat()

    def cleanupSplat(self):
        if self.splat:
            self.splat.cleanup()
            self.splat

    def setEndPos(self, x, y, z):
        pass

    def handleSplat(self):
        pass

    def delSplat(self, task):
        self.cleanupSplat()
        return task.done

    def getAudio3D(self):
        return base.audio3d

    def doesAutoRelease(self):
        return self.autoRelease
