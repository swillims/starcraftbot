import sc2
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.main import run_game
from sc2.player import Bot, Computer
from sc2.position import Point2
from sc2.unit import Unit
from sc2.units import Units
import random

class CentipedeBotAI(BotAI):


    def __init__(self):
        self.TechShield = False
        self.TechStim = False
        self.RallyPoint = None
        # I don't know how this works. I borrowed the concept from Sam. I believe it is a global variable
        ## I'm redoing old bots with a different iteration of the api. I don't know if it's nessary
        # I believe there is a better way to do it with can_cast ability then reference the upgrade_blank ability but it goes beyond the amount of time available and is less efficient.

    async def on_step(self, iteration):
        """Early Game"""
        if self.time <= 240:
            if iteration % 2 == 0:
                await self.Ebuildorder()
            if iteration % 2 == 1:
                await self.Esupplydepotup()
                await self.Esupplydepotdown()
            if iteration % 4 == 0:
                await self.distribute_workers()
            if iteration % 4 == 1:
                await self.EBarracks()
            if iteration % 4 == 2:
                await self.EFactory()
            if iteration % 4 == 3:
                await self.EOrbitalCommand()
            if iteration % 10 == 0:
                await self.EEarlyDefend()

        """Mid Game"""
        if self.time <= 480 and self.time > 240:
            if iteration % 3 == 0:
                await self.Esupplydepotup()
            if iteration % 3 == 1:
                await self.MMarineProximity()
                await self.MMARAUDERProximity()
            if iteration % 10 == 0:
                await self.MBarracks()
                await self.MFactory()
                await self.MStarport()
            if iteration & 10 == 1:
                await self.MManageSupply()
                await self.MCommandCenter()
                await self.MOrbitalCommand()
            if iteration % 10 == 2:
                await self.Esupplydepotdown()
                await self.distribute_workers()
                await self.MReaperScout()
            if iteration % 24 == 0:
                await self.MSiegedTankProximity()
                await self.MSiegeTankProximity()
                await self.MLandIdleBuildings()
                await self.MDefend()
            if iteration % 30 == 0:
                await self.MReplaceExpand()
                await self.MRefineryBuild()
            if iteration % 30 == 10:
                await self.MRavenProximity()
            if iteration % 30 == 20:
                await self.MBTechlab()
                await self.LEngineeringBay() # code recycling travels the wrong way here because it used to be late game only
                await self.MMedivacProximity()
            if iteration % 100 == 0:
                await self.MRally()

        """Late Game"""
        if self.time > 480:
            if iteration % 3 == 1:
                await self.MMarineProximity()
                await self.MMARAUDERProximity()
            if iteration % 20 == 0:
                await self.MSiegeTankProximity()
                await self.MRavenProximity()
            if iteration % 20 == 1:
                await self.MBarracks()
                await self.MFactory()
                await self.MStarport()
                await self.MLandIdleBuildings()
                await self.LReplaceExpand()
            if iteration % 24 == 0:
                await self.MSiegedTankProximity()
                await self.MDefend()
            if iteration % 24 == 2:
                await self.MManageSupply()
            if iteration % 48 == 3:
                await self.MRefineryBuild()
            if iteration % 48 == 7:
                await self.LAttackInitiation()
                await self.MMedivacProximity()
            if iteration % 52 == 0:
                await self.MReaperScout()
                await self.LOrbitalCommand()
                await self.MBTechlab()
                await self.LEngineeringBay()
            if iteration % 52 == 2:
                await self.distribute_workers()
                await self.MCommandCenter()
            if iteration % 103 == 0:
                await self.LScanNearArmy()
            if iteration % 107 == 0:
                await self.MRally()
                await self.Esupplydepotdown()


    """Methods"""
    async def MMarineProximity(self):
        for m in self.units(UnitTypeId.MARINE):
            threat = self.enemy_units.not_structure.closer_than(9, m.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                if await self.can_cast(m, AbilityId.EFFECT_STIM_MARINE) and m.health_percentage > 7/8:
                    m(AbilityId.EFFECT_STIM_MARINE)
                m.attack(threat.closest_to(m.position).position)

    async def MMARAUDERProximity(self):
        for m in self.units(UnitTypeId.MARAUDER):
            threat = self.enemy_units.not_structure.not_flying.closer_than(9, m.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                if await self.can_cast(m, AbilityId.EFFECT_STIM_MARAUDER) and m.health_percentage > 9.5/10:
                    m(AbilityId.EFFECT_STIM_MARAUDER)
                m.attack(threat.closest_to(m.position).position)

    async def MSiegeTankProximity(self):
        for s in self.units(UnitTypeId.SIEGETANK):
            threat = self.enemy_units.closer_than(15, s).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                s(AbilityId.SIEGEMODE_SIEGEMODE)

    async def MSiegedTankProximity(self):
        for s in self.units(UnitTypeId.SIEGETANKSIEGED):
            threat = self.enemy_units.closer_than(20, s).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if not threat.exists:
                s(AbilityId.UNSIEGE_UNSIEGE)

    async def MMedivacProximity(self):
        m = self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER)
        if m.exists:
            p = m.furthest_to(self.start_location).position.towards(self.start_location, 3)
            for medivac in self.units(UnitTypeId.MEDIVAC):
                medivac.attack(p)
        if self.units(UnitTypeId.MEDIVAC).exists and False: # "and False" added to not create unknown bugs. This is future code and is not implemented
            sacrifice = self.units(UnitTypeId.MEDIVAC).random
            threat = self.enemy_units.not_structure.closer_than(9, sacrifice.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            r = self.units(UnitTypeId.RAVEN).closer_than(6, sacrifice.position)
            if threat.amount > 10 and r.amount > 1:
                p = threat.random.position
                print("LOADING MEDIVAC CANNON!!!")
                if await self.can_cast(m, EFFECT_MEDIVACIGNITEAFTERBURNERS):
                    m(EFFECT_MEDIVACIGNITEAFTERBURNERS)
                    m.move(p)
                    for rr in r:
                        if rr.energy > 75:
                            if await self.can_casr(rr, EFFECT_ANTIARMORMISSILE, sacrifice):
                                rr(EFFECT_ANTIARMORMISSILE, sacrifice)


    async def MRavenIdle(self): # code is no long in use... It has been removed
        for r in self.units(UnitTypeId.RAVEN).idle:
            e = self.enemy_units.not_structure.closer_than(11, r.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if e.exists:
                if r.energy > 75:
                    # ea = e.closest_to(r.position) # changed do to opinion
                    ea = e.random
                    if ea.is_mechanical and await self.can_cast(r, AbilityId.EFFECT_INTERFERENCEMATRIX, ea):
                        r(AbilityId.EFFECT_INTERFERENCEMATRIX, ea)
                        print("INTERENCE MATRIX")
                    elif await self.can_cast(r, AbilityId.EFFECT_ANTIARMORMISSILE, ea):
                        r(AbilityId.EFFECT_ANTIARMORMISSILE, ea)
                        print("ORANGE ATTACK")
                else:
                    r.move(r.position.towards(self.start_location, 5))
            else:
                s = self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.SIEGETANKSIEGED)
                if s.exists:
                    p = s.furthest_to(self.start_location).position.towards(self.start_location, 5)
                    r.attack(p)
    # ^^^ Code is retired ^^^

    async def MRavenProximity(self):
        for r in self.units(UnitTypeId.RAVEN):
            e = self.enemy_units.not_structure.closer_than(11, r.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE).exclude_type(UnitTypeId.OVERSEER).exclude_type(UnitTypeId.PROBE).exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.DRONE)
            if e.exists and r.energy > 75:
                eMechPriority = e(UnitTypeId.SIEGETANKSIEGED) | e(UnitTypeId.VIKINGFIGHTER) | e(UnitTypeId.BATTLECRUISER) | e(UnitTypeId.THOR) | e(UnitTypeId.CARRIER) | e(UnitTypeId.VOIDRAY) | e(UnitTypeId.CARRIER) | e(UnitTypeId.COLOSSUS) | e(UnitTypeId.MOTHERSHIP) | e(UnitTypeId.TEMPEST)
                if eMechPriority.exists:
                    ea = eMechPriority.random
                    if await self.can_cast(r, AbilityId.EFFECT_INTERFERENCEMATRIX, ea):
                        r(AbilityId.EFFECT_INTERFERENCEMATRIX, ea)
                        print("INTERENCE MATRIX")
                else:
                    ea = e.random
                    if r.position.distance_to(ea.position) > 6:
                        if await self.can_cast(r, AbilityId.EFFECT_ANTIARMORMISSILE, ea):
                            r(AbilityId.EFFECT_ANTIARMORMISSILE, ea)
                            print("ORANGE!!!")
                    elif await self.can_cast(r, AbilityId.RAVENBUILD_AUTOTURRET, r.position):
                        r(AbilityId.RAVENBUILD_AUTOTURRET, r.position)
            elif e.exists:
                ea = e.closest_to(r.position)
                p = ea.position.towards(r.position, 13)
                r.move(p)
            else:
                a = self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER) | self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.SIEGETANKSIEGED)
                if a.exists:
                    p = a.furthest_to(self.start_location).position.towards(self.start_location, 2)
                    r.move(p)

    async def MReaperScout(self):
        for r in self.units(UnitTypeId.REAPER).idle:
            m = self.mineral_field.closer_than((self.supply_used*4), self.start_location).random.position
            r.attack(m)
            print("SCOUT")

    async def LAttackInitiation(self):
        a = self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER)
        e = self.enemy_units | self.enemy_structures
        e = e.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
        if a.amount > 40 and e.amount > 10:
            ep = e.closest_to(a.furthest_to(self.start_location).position).position.towards(self.game_info.map_center, -10)
            for aa in a:
                aa.attack(ep)
        elif self.enemy_structures.amount > 0 and self.supply_used >= 195:
            ep = e.closest_to(self.start_location).position
            for aa in a:
                aa.attack(ep)

    async def MRally(self):
        building = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED) | self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        if self.enemy_structures.exists and building.exists:
            self.RallyPoint = building.closest_to(self.enemy_structures.random.position).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        for a in self.units.idle:
            if a.distance_to(self.RallyPoint) > 15:
                a.attack(self.RallyPoint)

    async def MDefend(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        for c in cc:
            threat = self.enemy_units.closer_than(25, c.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                army = self.units.exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.RAVEN).exclude_type(UnitTypeId.MEDIVAC).not_structure.closer_than(50, c.position)
                # improve code to include scv attacks
                p = threat.random.position
                for a in army:
                    a.attack(p)
                print("Threat Detected")
                print(c.position)
            else:
                print("No Threat Detected")
                print(c.position)

    async def EEarlyDefend(self):

        threat = self.enemy_units.closer_than(16, self.start_location)
        if threat.exists:
            army = self.units
            for a in army:
                a.attack(threat.random)
                print("*Relatively Not Safe*")
        else:
            print("*Relatively Safe*")

    async def MLandIdleBuildings(self):
        b = self.structures(UnitTypeId.BARRACKSFLYING).idle
        f = self.structures(UnitTypeId.FACTORYFLYING).idle
        s = self.structures(UnitTypeId.STARPORTFLYING).idle
        if b.exists:
            if not self.structures(UnitTypeId.BARRACKSTECHLAB).exists and not self.structures(UnitTypeId.TECHLAB).exists:
                b1 = b.random
                p = b1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                b1.move(p)
                if self.can_afford(UnitTypeId.BARRACKSTECHLAB):
                    b1.build(UnitTypeId.BARRACKSTECHLAB, p)
                    print("LAND B_TECHLAB")
            elif not self.structures(UnitTypeId.REACTOR).exists:
                for b2 in b:
                    p = b2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    b2.move(p)
                    if self.can_afford(UnitTypeId.BARRACKSREACTOR):
                        b2.build(UnitTypeId.BARRACKSREACTOR, p)
                        print("LAND B_TECHLAB")

        if f.exists:
            if not self.structures(UnitTypeId.TECHLAB).exists:
                for f2 in f:
                    p = f2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    f2.move(p)
                    if self.can_afford(UnitTypeId.FACTORYTECHLAB):
                        f2.build(UnitTypeId.FACTORYTECHLAB, p)
                        print("LAND F_TECHLAB")

        if s.exists:
            if not self.structures(UnitTypeId.STARPORTREACTOR).exists and not self.structures(UnitTypeId.REACTOR).exists:
                s1 = s.random
                p = s1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                s1.move(p)
                if self.can_afford(UnitTypeId.STARPORTREACTOR):
                    s1.build(UnitTypeId.STARPORTREACTOR, p)
                    print("LAND S_REACTORLAB")
            else:
                for s2 in s:
                    p = s2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    s2.move(p)
                    if self.can_afford(UnitTypeId.STARPORTTECHLAB):
                        s2.build(UnitTypeId.STARPORTTECHLAB, p)
                        print("LAND S_TECHLAB")

    async def MCommandCenter(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for c in cc.ready.idle:
            if self.can_afford(UnitTypeId.ORBITALCOMMAND) and cc.not_ready.exists:
                c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
            elif self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < (cc.amount*20) + (oc.amount*15) + 15 and self.units(UnitTypeId.SCV).amount < 70:
                c.train(UnitTypeId.SCV)
                # coded this way to deal with a bug with expandnow()

    async def LScanNearArmy(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND).random
        if oc.energy > 50 and self.supply_used > 100 and self.enemy_units.amount > 0:
            e = self.enemy_units
            if e.exists:
                e2 = e.closest_to(self.start_location).position
                p = self.units.closest_to(e2).position
                oc(AbilityId.SCANNERSWEEP_SCAN, p.towards(e2, 16))
                ea = self.enemy_units.closer_than(18, p).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
                # radius is 15 because a wiki said so
                if ea.exists:
                    p = ea.random.position
                    army = self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER)
                    armynear = army.closer_than(40, p)
                    for a in armynear:
                        a.attack(p)

    async def LOrbitalCommand(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for o in oc.ready.idle:
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 55:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy == 200:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)
                elif self.enemy_structures.amount == 0:
                    o(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])
                    o(AbilityId.SCANNERSWEEP_SCAN, self.mineral_field.random.position)

    async def MOrbitalCommand(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for o in oc.ready.idle:
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 50:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy >= 150:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)
            elif o.energy > 100 and self.enemy_structures.amount == 0:
                o(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])
                o(AbilityId.SCANNERSWEEP_SCAN, self.mineral_field.random.position)
                print("SCAN SEARCH")

    async def EOrbitalCommand(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for o in oc.ready.idle:
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 50:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy >= 50:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)

    async def MManageSupply(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND)
        s = self.units(UnitTypeId.SCV)
        if cc.exists and s.exists and self.supply_used + self.supply_left < 200:
            if self.supply_left < self.supply_used/16 + 4 and not self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.can_afford(UnitTypeId.SUPPLYDEPOT):
                sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
                if sd.exists:
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=sd.random)
                else:
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT) and sd.exists:
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=sd.random)
            elif self.supply_left < 0 and self.can_afford(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)

    async def LReplaceExpand(self):
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORY) | self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORT) | self.structures(UnitTypeId.STARPORTFLYING)
        a = b.flying | f.flying | s.flying
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)
        e = self.structures(UnitTypeId.ENGINEERINGBAY)
        ar = self.structures(UnitTypeId.ARMORY)

        if sd.ready.exists and not b.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.BARRACKS, p)

        elif b.ready.exists and not f.exists and not self.already_pending(UnitTypeId.FACTORY) and self.can_afford(UnitTypeId.FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.FACTORY, p)

        elif f.ready.exists and not s.exists and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.STARPORT, p)

        elif not e.exists and not self.already_pending(UnitTypeId.ENGINEERINGBAY) and self.can_afford(UnitTypeId.ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.ENGINEERINGBAY, p)

        elif s.ready.exists and not ar.exists and not self.already_pending(UnitTypeId.ARMORY) and self.can_afford(UnitTypeId.ARMORY):
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.ARMORY, p)

        elif t.exists and a.exists:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f.flying | s.flying
            if b.flying.exists and self.structures(UnitTypeId.BARRACKSREACTOR).exists:
                bf = b.flying.first
                bf(AbilityId.LAND, p)
            elif a2.exists:
                af = a2.first
                p = t.first.add_on_land_position
                af(AbilityId.LAND, p)

        elif r.exists and (b.flying.exists or s.flying.exists):
            print("REPLACE REACTOR SPOT TRY DO")
            if not self.structures(UnitTypeId.STARPORTREACTOR).exists and s.flying.exists:
                p = r.first.add_on_land_position
                sf = s.flying.first
                sf(AbilityId.LAND, p)

            elif b.flying.exists:
                p = r.first.add_on_land_position
                bf = b.flying.first
                bf(AbilityId.LAND, p)

        elif b.amount < cc.amount and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.FACTORY):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.BARRACKS, p)

        elif f.amount < 2 and not self.already_pending(UnitTypeId.FACTORY) and self.can_afford(UnitTypeId.FACTORY):
            print("NOT ENOUGH FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.FACTORY, p)

        elif s.amount < 2 and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT):
            print("NOT ENOUGH FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.STARPORT, p)


    async def MReplaceExpand(self):
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORY) | self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORT) | self.structures(UnitTypeId.STARPORTFLYING)
        e = self.structures(UnitTypeId.ENGINEERINGBAY)
        a = b.flying | f.flying | s.flying
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)

        if sd.ready.exists and not b.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.BARRACKS, p)

        elif b.ready.exists and not f.exists and not self.already_pending(UnitTypeId.FACTORY) and self.can_afford(UnitTypeId.FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.FACTORY, p)

        elif f.ready.exists and not s.exists and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.STARPORT, p)

        elif not e.exists and not self.already_pending(UnitTypeId.ENGINEERINGBAY) and self.can_afford(UnitTypeId.ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.ENGINEERINGBAY, p)

        elif t.exists and a.exists:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f.flying | s.flying
            if b.flying.exists and self.structures(UnitTypeId.BARRACKSREACTOR).exists:
                bf = b.flying.first
                bf(AbilityId.LAND, p)
            elif a2.exists:
                af = a2.first
                p = t.first.add_on_land_position
                af(AbilityId.LAND, p)

        elif r.exists and (b.flying.exists or s.flying.exists):
            print("REPLACE REACTOR SPOT TRY DO")
            if not self.structures(UnitTypeId.STARPORTREACTOR).exists and s.flying.exists:
                p = r.first.add_on_land_position
                sf = s.flying.first
                sf(AbilityId.LAND, p)

            elif b.flying.exists:
                p = r.first.add_on_land_position
                bf = b.flying.first
                bf(AbilityId.LAND, p)

        elif b.amount == 1 and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.BARRACKS, p)

        elif self.minerals > 500 and not self.already_pending(UnitTypeId.COMMANDCENTER):
            print("expand")
            await self.expand_now()

        elif f.amount == 1 and not self.already_pending(UnitTypeId.FACTORY) and cc.amount > 2 and self.can_afford(UnitTypeId.FACTORY):
            print("NOT ENOUGH FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.FACTORY, p)

        elif s.amount == 1 and not self.already_pending(UnitTypeId.STARPORT) and cc.amount > 2 and self.can_afford(UnitTypeId.STARPORT):
            print("NOT ENOUGH STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(UnitTypeId.STARPORT, p)

    async def Ebuildorder(self):
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)

        if cc.ready.exists or oc.ready.exists:
            cci = cc.ready.idle | oc.ready.idle
            if cc.not_ready.exists and cc.ready.idle.exists and self.can_afford(UnitTypeId.ORBITALCOMMAND) and b.ready.exists:
                c = cc.idle.ready.random
                c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
            elif cci.exists and self.can_afford(UnitTypeId.SCV):
                for c in cci:
                    if self.can_afford(UnitTypeId.SCV):
                        """this is not a redundancy"""
                        c.train(UnitTypeId.SCV)

            if scv.exists and not sd.exists and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):

                    if x < xd:
                        print("x<xd")
                        if y < yd:
                            p = self.main_base_ramp.barracks_correct_placement.offset((0, 2)).position
                            print("y<yd")
                            # south east side darkness sanctuary *PASS*
                            print("NE DOWN RAMP")
                        else:
                            p = self.main_base_ramp.barracks_correct_placement.offset((0, -3)).position
                            print("y>yd")
                            # north side 16bit
                            # south west side darkness sanctuary *SEMI PASS VERY STRONG*
                            print("SE DOWN RAMP")
                    else:
                        print("x>xd")
                        if y < yd:
                            p = self.main_base_ramp.barracks_correct_placement.offset((0, 2)).position
                            print("y<yd")
                            # south side 16bit
                            # north east side darkness sanctuary *SEMI PASS STRONG*
                            print("NW DOWN RAMP")
                        else:
                            p = self.main_base_ramp.barracks_correct_placement.offset((-3, 1)).position
                            print("y>yd")
                            # north west side darkness sanctuary *NO CRASH*
                            print("SW DOWN RAMP")
                    s.build(UnitTypeId.SUPPLYDEPOT, p)
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                s = scv.furthest_to(self.start_location)
                if not b.exists and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):
                        p = self.main_base_ramp.barracks_correct_placement.position
                        s.build(UnitTypeId.BARRACKS, p)
                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print("BARRACKS1")
                        if self.can_afford(UnitTypeId.BARRACKS):
                            p = self.main_base_ramp.barracks_correct_placement.offset((0, -2))
                            s.build(UnitTypeId.BARRACKS, p)
                            print("placement problem")

                if b.exists:
                    if self.can_afford(UnitTypeId.REFINERY) and not self.structures(UnitTypeId.REFINERY).exists:
                        await self.ERefineryBuild()
                    else:
                        if oc.amount + cc.amount == 1 and self.can_afford(UnitTypeId.COMMANDCENTER):
                            await self.expand_now()
                        elif cc.amount == 2 and self.can_afford(UnitTypeId.ORBITALCOMMAND):
                            if cc.idle.ready.exists:
                                c == cc.idle
                                c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
                        elif oc.exists or self.already_pending(UnitTypeId.ORBITALCOMMAND) or self.structures(UnitTypeId.BARRACKSREACTOR).exists:
                            if sd.amount == 1 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                                if x < xd:
                                    if y < yd:
                                        p = b.first.position.offset((5, -1))
                                    else:
                                        p = b.first.position.offset((5, 1))
                                else:
                                    if y < yd:
                                        p = b.first.position.offset((-2, 0))
                                    else:
                                        p = b.first.position.offset((5, -1))

                                await self.build(UnitTypeId.SUPPLYDEPOT, p)
                            elif sd.amount <= 2:
                                if b.amount < 2 and self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
                                    if x < xd:
                                        if y < yd:
                                            p = b.first.position.offset((0, -3))
                                        else:
                                            p = b.first.position.offset((0, 4))
                                    else:
                                        if y < yd:
                                            p = b.first.position.offset((0, -3))
                                        else:
                                            p = b.first.position.offset((0, 3))
                                    await self.build(UnitTypeId.BARRACKS, p)
                                elif b.amount == 2:
                                    if self.structures(UnitTypeId.REFINERY).amount == 1 and not self.already_pending(UnitTypeId.REFINERY):
                                        await self.ERefineryBuild()
                                    elif self.structures(UnitTypeId.FACTORY).amount == 0 and self.can_afford(UnitTypeId.FACTORY) and not self.already_pending(UnitTypeId.FACTORY):
                                        if x < xd:
                                            if y < yd:
                                                p = b.first.position.offset((0, -7))
                                            else:
                                                p = b.first.position.offset((-6, 0))
                                        else:
                                            if y < yd:
                                                p = b.first.position.offset((0, -6))
                                            else:
                                                p = b.first.position.offset((0, 7))
                                        await self.build(UnitTypeId.FACTORY, p)
                                    elif self.structures(UnitTypeId.FACTORY).exists:
                                        if self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                                            if x < xd:
                                                if y < yd:
                                                    p = b.first.position.offset((7, -2))
                                                else:
                                                    p = b.first.position.offset((-5, 3))
                                            else:
                                                if y < yd:
                                                    p = b.first.position.offset((-2, -2))
                                                else:
                                                    p = b.first.position.offset((5, 1))
                                            await self.build(UnitTypeId.SUPPLYDEPOT, p)

    async def MRefineryBuild(self):
        if self.structures(UnitTypeId.REFINERY).amount < (self.structures(UnitTypeId.COMMANDCENTER).amount * 2) + (self.structures(UnitTypeId.ORBITALCOMMAND).amount * 2):
            for cc in self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND):
                v = self.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
                        #observation from E method is still valid.
                            if not self.structures(UnitTypeId.REFINERY).closer_than(1, ve).exists:
                                worker = self.select_build_worker(ve.position)
                                if worker is None:
                                    break
                                worker.build(UnitTypeId.REFINERY, ve)
                            # copy pasted from E method because I might want it to be slightly different than the other method
                            # it currently has a larger amount of refineries because I plan on doing a vespene gas heavy army

    async def ERefineryBuild(self):
        if self.structures(UnitTypeId.REFINERY).amount < self.structures(UnitTypeId.COMMANDCENTER).amount + (self.structures(UnitTypeId.ORBITALCOMMAND).amount * 2):
            for cc in self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND):
                v = self.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
                        """ 
                        Observation: The code was learned from  the youtube tutorial. It is not optimally coded.
                        It in theory, only allows one refinery construction at a time. Loop -> Loop -> Check
                        If the check was done before the loop, there wouldn't be needless cycles.
                        Code left unchanged because of time constraint and not wanting to break the project.
                        """
                        if not self.structures(UnitTypeId.REFINERY).closer_than(1, ve).exists:
                            worker = self.select_build_worker(ve.position)
                            if worker is None:
                                break
                            worker.build(UnitTypeId.REFINERY, ve)
                            # recycled code that works for early game
                            # logic doesn't fit code because I didn't need to change the code to accomplish what I wanted it to accomplish

    async def LEngineeringBay(self):
        for e in self.structures(UnitTypeId.ENGINEERINGBAY).idle.idle:
            if await self.can_cast(e, AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1) and self.can_afford(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1):
                e(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1)
            elif await self.can_cast(e, AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2) and self.can_afford(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2):
                e(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2)
            elif await self.can_cast(e, AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3) and self.can_afford(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3):
                e(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3)
            elif await self.can_cast(e, AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1) and self.can_afford(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1):
                e(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1)
            elif await self.can_cast(e, AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2) and self.can_afford(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2):
                e(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2)
            elif await self.can_cast(e, AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3) and self.can_afford(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3):
                e(AbilityId.ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3)

    async def MBTechlab(self):
        bt = self.structures(UnitTypeId.BARRACKSTECHLAB).ready.idle
        if bt.exists:
            bt1 = bt.first
            if self.can_afford(AbilityId.RESEARCH_COMBATSHIELD) and not self.TechShield:
                bt1(AbilityId.RESEARCH_COMBATSHIELD)
                self.TechShield = True
                print("UPGRADE_SHIELD")
            elif self.can_afford(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK) and not self.TechStim:
                bt1(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK)
                self.TechStim = True
                print("UPGRADE_STIM")

    async def MBarracks(self):
        for b in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if b.add_on_tag == 0:
                b(AbilityId.LIFT)
                print("FLY!!!")
            elif self.structures(UnitTypeId.BARRACKSTECHLAB).exists and self.supply_left > 1:
                id = self.structures(UnitTypeId.BARRACKSTECHLAB).random.tag
                if b.add_on_tag == id:
                    if self.can_afford(UnitTypeId.MARAUDER) and self.supply_left > 1:
                        b.train(UnitTypeId.MARAUDER)

                elif self.supply_left > 1:
                    if self.can_afford(UnitTypeId.REAPER) and not self.units(UnitTypeId.REAPER).exists and self.units(UnitTypeId.MARINE).amount >= 10:
                        b.train(UnitTypeId.REAPER)
                        if self.can_afford(UnitTypeId.REAPER):
                            b.train(UnitTypeId.REAPER)
                    elif self.can_afford(UnitTypeId.MARINE):
                        b.train(UnitTypeId.MARINE)
                        if self.can_afford(UnitTypeId.MARINE):
                            b.train(UnitTypeId.MARINE)

            elif self.supply_left > 1:
                if self.can_afford(UnitTypeId.REAPER) and not self.units(UnitTypeId.REAPER).exists and self.units(UnitTypeId.MARINE).amount >= 10:
                    b.train(UnitTypeId.REAPER)
                    if self.can_afford(UnitTypeId.REAPER):
                        b.train(UnitTypeId.REAPER)
                elif self.can_afford(UnitTypeId.MARINE):
                    b.train(UnitTypeId.MARINE)
                    if self.can_afford(UnitTypeId.MARINE):
                        b.train(UnitTypeId.MARINE)

    async def EBarracks(self):
        for b in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if self.structures(UnitTypeId.BARRACKSREACTOR).exists and self.supply_used < 198:
                id = self.structures(UnitTypeId.BARRACKSREACTOR).random.tag
                if b.add_on_tag == id:
                    if self.can_afford(UnitTypeId.REAPER) and not self.units(UnitTypeId.REAPER).exists and self.units(UnitTypeId.MARINE).amount >= 10:
                        b.train(UnitTypeId.REAPER)
                        if self.can_afford(UnitTypeId.REAPER):
                            b.train(UnitTypeId.REAPER)
                    else:
                        if self.can_afford(UnitTypeId.MARINE):
                            b.train(UnitTypeId.MARINE)
                        if self.can_afford(UnitTypeId.MARINE):
                            b.train(UnitTypeId.MARINE)
                elif b.add_on_tag == 0:
                    if self.can_afford(UnitTypeId.BARRACKSTECHLAB):
                        b.build(UnitTypeId.BARRACKSTECHLAB)
                else:
                    if self.can_afford(UnitTypeId.MARAUDER):
                        b.train(UnitTypeId.MARAUDER)
            elif self.can_afford(UnitTypeId.REAPER):
                b.build(UnitTypeId.BARRACKSREACTOR)

    async def MFactory(self):
        for f in self.structures(UnitTypeId.FACTORY).ready.idle:
            if not self.structures(UnitTypeId.FACTORYREACTOR).exists and self.supply_left > 2:
                """assumption is that there will be no factory reactor and it is coded not to crash if it exists*"""
                if f.add_on_tag == 0:
                    f(AbilityId.LIFT)
                    print("FLY!!!")
                else:
                    if self.can_afford(UnitTypeId.SIEGETANK):
                        f.train(UnitTypeId.SIEGETANK)
            elif self.structures(UnitTypeId.FACTORYREACTOR).exists:
                f(AbilityId.LIFT)
                print("FLY!!!")

    async def EFactory(self):
        for f in self.structures(UnitTypeId.FACTORY).ready.idle:
            if not self.structures(UnitTypeId.FACTORYREACTOR).exists and self.supply_used <= 197:
                """assumption is that there will be no factory reactor and it is coded not to crash if it exists*"""
                if f.add_on_tag == 0:
                    if self.can_afford(UnitTypeId.FACTORYTECHLAB):
                        f.build(UnitTypeId.FACTORYTECHLAB)
                        print("F_TECHLAB")
                else:
                    if self.can_afford(UnitTypeId.SIEGETANK):
                        f.train(UnitTypeId.SIEGETANK)

    async def MStarport(self):
        for s in self.structures(UnitTypeId.STARPORT).ready.idle:
            if s.add_on_tag == 0:
                s(AbilityId.LIFT)

            elif self.structures(UnitTypeId.STARPORTREACTOR).exists:
                id = self.structures(UnitTypeId.STARPORTREACTOR).random.tag
                if s.add_on_tag == id and self.supply_left > 4:
                    if self.can_afford(UnitTypeId.MEDIVAC) and self.units(UnitTypeId.MEDIVAC).amount <= 12:
                        s.train(UnitTypeId.MEDIVAC)
                        if self.can_afford(UnitTypeId.MEDIVAC):
                            s.train(UnitTypeId.MEDIVAC) #replacement code
                elif self.supply_left > 2:
                    if self.can_afford(UnitTypeId.RAVEN):
                        s.train(UnitTypeId.RAVEN)

            else:
                if self.can_afford(UnitTypeId.RAVEN):
                    s.train(UnitTypeId.RAVEN)

    async def Esupplydepotdown(self):
        for sd in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
            e = self.enemy_units.closer_than(6, sd.position)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

    async def Esupplydepotup(self):
        for sd in self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            e = self.enemy_units.closer_than(8, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_RAISE)
"""end class"""

"""TEST SCRIPT BELOW"""
# run_game(maps.get("(2)Dreamcatcher LE"), [
#     Bot(Race.Terran, CentipedeBotAI()),
#     Computer(Race.Random, Difficulty.Hard)
# ], realtime=False)


#run_game(maps.get("(2)Dreamcatcher LE"), [
#   Bot(Race.Terran, CentipedeBotAI()),
#   Computer(Race.Protoss, Difficulty.Hard)
#], realtime=False)

#run_game(maps.get("(2)Dreamcatcher LE"), [
#   Bot(Race.Terran, CentipedeBotAI()),
#   Computer(Race.Zerg, Difficulty.Hard)
#], realtime=False)

#run_game(maps.get("(2)Dreamcatcher LE"), [
#   Bot(Race.Terran, CentipedeBotAI()),
#   Computer(Race.Terran, Difficulty.Hard)
#], realtime=False)

#run_game(maps.get("(4)Darkness Sanctuary LE"), [
#    Bot(Race.Terran, CentipedeBotAI()),
#    Computer(Race.Random, Difficulty.Hard)
#], realtime=False)

#run_game(maps.get("(2)16-Bit LE"), [
#    Bot(Race.Terran, CentipedeBotAI()),
#    Computer(Race.Random, Difficulty.Hard)
#], realtime=True)

#run_game(maps.get("Abyssal Reef LE"), [
#    Bot(Race.Terran, CentipedeBotAI()),
#    Computer(Race.Random, Difficulty.Hard)
#], realtime=True)