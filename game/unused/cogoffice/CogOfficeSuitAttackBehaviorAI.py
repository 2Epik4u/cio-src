# Filename: CogOfficeSuitAttackBehaviorAIAI.py
# Created by:  blach (17Dec15)

from direct.distributed.ClockDelta import globalClockDelta

from src.coginvasion.cog.SuitAttackBehaviorAI import SuitAttackBehaviorAI
from src.coginvasion.cog import SuitAttacks

import random

class CogOfficeSuitAttackBehaviorAIAI(SuitAttackBehaviorAI):
    
    def __init__(self, suit, target):
        SuitAttackBehaviorAI.__init__(self, suit)
        self.target = target
        self.targetToon = self.suit.air.doId2do.get(target)
        self.maxAttacksPerSession = random.choice([1, 2])
        
    def unload(self):
        del self.targetToon
        SuitAttackBehaviorAI.unload(self)
        
    def startAttacking(self, task = None):
        target = self.targetToon
        self.suit.b_setAnimState('neutral')
        self.suit.headsUp(target)

        # Choose a random attack and start it.
        attack = random.choice(self.suit.suitPlan.getAttacks())
        attackIndex = SuitAttacks.SuitAttackLengths.keys().index(attack)
        timestamp = globalClockDelta.getFrameNetworkTime()
        if self.suit.isDead():
            self.stopAttacking()
            return
        self.suit.sendUpdate('doAttack', [attackIndex, target.doId, timestamp])
        
        self.isAttacking = True
        self.attacksThisSession += 1
        self.attacksDone += 1

        self.ATTACK_COOLDOWN = SuitAttacks.SuitAttackLengths[attack]

        if self.attacksThisSession < self.maxAttacksPerSession:
            taskMgr.doMethodLater(self.ATTACK_COOLDOWN, self.startAttacking, self.suit.uniqueName('attackTask'))
        else:
            taskMgr.doMethodLater(self.ATTACK_COOLDOWN, self.stopAttacking, self.suit.uniqueName('finalAttack'))
        
        if task:
            return task.done
        
