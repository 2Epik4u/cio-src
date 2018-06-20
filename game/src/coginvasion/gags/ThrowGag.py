"""
COG INVASION ONLINE
Copyright (c) CIO Team. All rights reserved.

@file ThrowGag.py
@author Maverick Liberty
@date July 07, 2015

"""

from panda3d.core import CollisionSphere, BitMask32, CollisionNode, NodePath, CollisionHandlerEvent
from panda3d.bullet import BulletSphereShape, BulletGhostNode
from direct.interval.IntervalGlobal import Sequence, Func, Wait, Parallel, ProjectileInterval, ActorInterval
from direct.gui.DirectGui import DirectWaitBar, DGG

from src.coginvasion.minigame.FlightProjectileInterval import FlightProjectileInterval
from src.coginvasion.gags.Gag import Gag
from src.coginvasion.gags.GagType import GagType
from src.coginvasion.globals import CIGlobals
from src.coginvasion.phys import PhysicsUtils, WorldCollider
from direct.actor.Actor import Actor
import GagGlobals

import math

class ThrowGag(Gag):
    
    ReleaseSpeed = 1.0
    ReleasePlayRateMultiplier = 1.0
    BobStartFrame = 30
    BobEndFrame = 40
    BobPlayRateMultiplier = 0.25
    ThrowObjectFrame = 62
    FinalThrowFrame = 90

    def __init__(self, name, model, damage, hitSfx, splatColor, anim = None, scale = 1):
        Gag.__init__(self, name, model, GagType.THROW, hitSfx, anim = anim, scale = scale)
        self.splatScale = GagGlobals.splatSizes[self.name]
        self.splatColor = splatColor
        self.entities = []
        self.timeout = 1.0
        self.power = 50
        self.powerBar = None
        self.tossPieStart = 0
        self.pieSpeed = 0.2
        self.pieExponent = 0.75

    def setAvatar(self, avatar):
        Gag.setAvatar(self, avatar)
        if self.isLocal():
            self.powerBar = DirectWaitBar(range = 150, frameColor = (1, 1, 1, 1),
                         barColor = (0.286, 0.901, 1, 1), relief = DGG.RAISED,
                         borderWidth = (0.04, 0.04), pos = (0, 0, 0.85), scale = 0.2,
                         hpr = (0, 0, 0), parent = aspect2d, frameSize = (-0.85, 0.85, -0.12, 0.12))
            self.powerBar.hide()

    def __getPiePower(self, time):
        elapsed = max(time - self.tossPieStart, 0.0)
        t = elapsed / self.pieSpeed
        t = math.pow(t, self.pieExponent)
        power = int(t * 150) % 300
        if power > 150:
            power = 300 - power
        return power

    def build(self):
        if not self.gag:
            Gag.build(self)
            self.equip()
            if self.anim and self.gag:
                self.gag.loop('chan')
        return self.gag

    def __doDraw(self):
        self.doDrawAndHold('pie', 0, self.BobStartFrame, self.playRate, self.BobStartFrame,
                           self.BobEndFrame, self.playRate * self.BobPlayRateMultiplier)

    def equip(self):
        Gag.equip(self)

        if self.isLocal():
            vmGag = base.localAvatar.getFPSCam().vmGag
            if vmGag:
                vmGag.setPosHpr(0.07, 0.17, -0.01, 0, -100, -10)
                vmGag.setScale(self.gag.getScale() * 0.567)
            vm = base.localAvatar.getViewModel()
            fpsCam = base.localAvatar.getFPSCam()
            fpsCam.setVMAnimTrack(Sequence(ActorInterval(vm, "pie_draw"), Func(vm.loop, "pie_idle")))

        self.__doDraw()

    def start(self):
        Gag.start(self)
        if not self.gag:
            self.build()

        if self.isLocal():
            taskMgr.remove("hidePowerBarTask" + str(hash(self)))
            self.powerBar.show()
            self.startPowerBar()

    def startPowerBar(self):
        self.tossPieStart = globalClock.getFrameTime()
        taskMgr.add(self.__powerBarUpdate, "powerBarUpdate" + str(hash(self)))

    def __powerBarUpdate(self, task):
        if self.powerBar is None:
            return task.done
        self.powerBar['value'] = self.__getPiePower(globalClock.getFrameTime())
        return task.cont

    def stopPowerBar(self):
        taskMgr.remove("powerBarUpdate" + str(hash(self)))
        self.power = self.powerBar['value']

    def __hidePowerBarTask(self, _):
        self.powerBar.hide()

    def throw(self):
        if self.isLocal():
            self.stopPowerBar()
            self.power += 50
            self.power = 250 - self.power
            # Make other toons set the throw power on my gag.
            base.localAvatar.sendUpdate('setThrowPower', [self.id, self.power])
            self.startTimeout()
            taskMgr.doMethodLater(1.5, self.__hidePowerBarTask, "hidePowerBarTask" + str(hash(self)))
        self.clearAnimTrack()
        
        if not self.gag:
            self.build()

        def shouldRelease():
            if self.isLocal():
                base.localAvatar.releaseGag()
                vm = base.localAvatar.getViewModel()
                fpsCam = base.localAvatar.getFPSCam()
                fpsCam.setVMAnimTrack(Sequence(Func(vm.hide), Func(vm.pose, "pie_draw", 0)))
        
        self.setAnimTrack(
            Parallel(
                Sequence(
                    self.getAnimationTrack('pie', startFrame=self.ThrowObjectFrame,
                                           playRate=(self.playRate * self.ReleasePlayRateMultiplier)),
                    Func(self.__doDraw),
                ),
                Sequence(
                    Func(shouldRelease)
                )
            )
        )
        
        self.animTrack.start()

    def setPower(self, power):
        self.power = power

    def release(self):
        Gag.release(self)
        base.audio3d.attachSoundToObject(self.woosh, self.gag)
        base.playSfx(self.woosh, node = self.gag)

        throwRoot = render.attachNewNode('throwRoot')
        throwRoot.setPos(self.avatar.getPos(render))
        throwRoot.setHpr(self.avatar.getHpr(render))
        if self.isLocal() and base.localAvatar.isFirstPerson():
            hitPos = PhysicsUtils.getHitPosFromCamera()
            throwRoot.headsUp(hitPos)
            throwRoot.setP(render, camera.getP(render))
        else:
            throwRoot.setP(self.avatar, self.avatar.getLookPitch())
        throwPath = NodePath('ThrowPath')
        throwPath.reparentTo(throwRoot)
        throwPath.setScale(render, 1)
        throwPath.setPos(0, self.power, -90)
        throwPath.setHpr(0, -90, 0)

        gagRoot = render.attachNewNode('gagRoot')
        gagRoot.setPos(self.handJoint.getPos(render))
        gagRoot.headsUp(throwPath)

        entity = self.gag

        if not entity:
            entity = self.build()

        entity.wrtReparentTo(gagRoot)
        entity.setHpr(render, throwPath.getHpr(render))
        self.gag = None

        if not self.handJoint:
            self.handJoint = self.avatar.find('**/def_joint_right_hold')

        track = FlightProjectileInterval(gagRoot, startPos = self.handJoint.getPos(render), endPos = throwPath.getPos(render), gravityMult = 0.9, duration = 3)
        event = self.avatar.uniqueName('throwIvalDone') + '-' + str(hash(entity))
        track.setDoneEvent(event)
        base.acceptOnce(event, self.__handlePieIvalDone, [entity])
        track.start()
        
        if self.isLocal():
            collider = self.buildCollisions(entity)
            self.entities.append([gagRoot, track, collider])
            base.localAvatar.sendUpdate('usedGag', [self.id])
        else:
            self.entities.append([gagRoot, track, NodePath()])
        self.reset()

        throwPath.removeNode()
        throwRoot.removeNode()

    def __handlePieIvalDone(self, pie):
        if not pie.isEmpty():
            pie.removeNode()

    def handleSplat(self):
        base.audio3d.detachSound(self.woosh)
        if self.woosh:
            self.woosh.stop()

        CIGlobals.makeSplat(self.splatPos, self.splatColor, self.splatScale, self.hitSfx)

        self.cleanupEntity(self.splatPos)
        self.splatPos = None

    def cleanupEntity(self, pos):
        closestPie = None
        trackOfClosestPie = None
        colliderOfClosestPie = None
        pieHash2range = {}
        for entity, track, collider in self.entities:
            if not entity.isEmpty():
                pieHash2range[hash(entity)] = (entity.getPos(render) - pos).length()
        ranges = []
        for distance in pieHash2range.values():
            ranges.append(distance)
        ranges.sort()
        for pieHash in pieHash2range.keys():
            distance = pieHash2range[pieHash]
            if not distance is None and distance == ranges[0]:
                for entity, track, collData in self.entities:
                    if hash(entity) == pieHash:
                        closestPie = entity
                        trackOfClosestPie = track
                        colliderOfClosestPie = collData
                        break
            break
        if closestPie != None and trackOfClosestPie != None and colliderOfClosestPie != None:
            if [closestPie, trackOfClosestPie, colliderOfClosestPie] in self.entities:
                self.entities.remove([closestPie, trackOfClosestPie, colliderOfClosestPie])
            if not colliderOfClosestPie.isEmpty():
                print colliderOfClosestPie, "removing!"
                colliderOfClosestPie.removeNode()
            if not closestPie.isEmpty():
                if isinstance(closestPie, Actor):
                    closestPie.cleanup()
                closestPie.removeNode()

    def onCollision(self, frNp, intoNP):
        print "onCollision:", frNp, "->", intoNP
        avNP = intoNP.getParent()
        fromNP = frNp.getParent()

        if fromNP.isEmpty():
            return

        for key in base.cr.doId2do.keys():
            obj = base.cr.doId2do[key]
            if obj.__class__.__name__ in CIGlobals.SuitClasses:
                if obj.getKey() == avNP.getKey():
                    obj.sendUpdate('hitByGag', [self.getID(), self.avatar.getDistance(obj)])
            elif obj.__class__.__name__ == "DistributedPlayerToon":
                if obj.getKey() == avNP.getKey():
                    if obj.getHealth() < obj.getMaxHealth():
                        if obj != self.avatar:
                            self.avatar.sendUpdate('toonHitByPie', [obj.doId, self.getID()])
                        else:
                            self.avatar.acceptOnce('gagSensor-into', self.onCollision)
                            return
            elif obj.__class__.__name__ == "DistributedPieTurret":
                if obj.getKey() == avNP.getKey():
                    if obj.getHealth() < obj.getMaxHealth():
                        self.avatar.sendUpdate('toonHitByPie', [obj.doId, self.getID()])

        self.splatPos = fromNP.getPos(render)
        self.avatar.sendUpdate('setSplatPos', [self.getID(), self.splatPos.getX(), self.splatPos.getY(), self.splatPos.getZ()])
        self.handleSplat()

    def buildCollisions(self, entity):
        collider = WorldCollider.WorldCollider('gagSensor', 1, 'throwGagCollide', needSelfInArgs = True)
        collider.reparentTo(entity)
        self.avatar.acceptOnce('throwGagCollide', self.onCollision)
        return collider

    def unEquip(self):
        taskMgr.remove("hidePowerBarTask" + str(hash(self)))
        if self.powerBar:
            self.powerBar.hide()
        Gag.unEquip(self)

    def delete(self):
        taskMgr.remove("powerBarUpdate" + str(hash(self)))
        taskMgr.remove("hidePowerBarTask" + str(hash(self)))
        if self.powerBar:
            self.powerBar.destroy()
            self.powerBar = None
        self.clearAnimTrack()
        Gag.delete(self)
