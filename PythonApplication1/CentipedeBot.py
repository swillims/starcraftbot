import sc2
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer, Human
from sc2.constants import *
import random

class CentipedeBotAI(BotAI):


    def __init__(self):
        self.TechShield = False
        self.TechStim = False
        self.RallyPoint = None
        # I don't know how this works. I borrowed the concept from Sam. I believe it is a global variable
        # I believe there is a better way to do it with can_cast ability then reference the upgrade_blank ability but it goes beyond the amount of time available and is less efficient.

    async def on_step(self, iteration):
        """Early Game"""
        if self.time <= 240:
            if iteration % 5 == 0:
                await self.Ebuildorder()
            if iteration % 6 == 3:
                await self.Esupplydepotup()
                await self.Esupplydepotdown()
            if iteration % 6 == 0:
                await self.distribute_workers()
            if iteration % 10 == 0:
                await self.EBarracks()
            if iteration % 10 == 5:
                await self.EFactory()
                await self.EOrbitalCommand()
            if iteration % 150 == 0:
                await self.EEarlyDefend()

        """Mid Game"""
        if self.time <= 480 and self.time > 240:
            if iteration % 5 == 0:
                await self.Esupplydepotup()
            if iteration % 10 == 0:
                await self.MBarracks()
                await self.MFactory()
                await self.MStarport()
            if iteration & 15 == 0:
                await self.MManageSupply()
                await self.MCommandCenter()
                await self.MOrbitalCommand()
            if iteration % 20 == 0:
                await self.Esupplydepotdown()
                await self.distribute_workers()
                await self.MReaperScout()
            if iteration % 20 == 10:
                await self.MMarineProximity()
                await self.MMARAUDERProximity()
            if iteration % 25 == 0:
                await self.MSiegedTankProximity()
                await self.MSiegeTankProximity()
                await self.MLandIdleBuildings()
                await self.MDefend()
            if iteration % 30 == 0:
                await self.MReplaceExpand()
                await self.MRefineryBuild()
            if iteration % 50 == 25:
                await self.MRavenProximity()
            if iteration % 100 == 0:
                await self.MBTechlab()
                await self.LEngineeringBay() # code recycling travels the wrong way here because it used to be late game only
                await self.MMedivacProximity()
            if iteration % 300 == 0:
                await self.MRally()

        """Late Game"""
        if self.time > 480:
            if iteration % 10 == 0:
                await self.MMarineProximity()
                await self.MMARAUDERProximity()
            if iteration % 15 == 0:
                await self.MSiegeTankProximity()
                await self.MRavenProximity()
            if iteration % 20 == 0:
                await self.MBarracks()
                await self.MFactory()
                await self.MStarport()
                await self.MLandIdleBuildings()
                await self.LReplaceExpand()
            if iteration % 40 == 0:
                await self.MSiegedTankProximity()
                await self.MDefend()
            if iteration % 60 == 0:
                await self.MManageSupply()
            if iteration % 75 == 0:
                await self.MRefineryBuild()
            if iteration % 100 == 0:
                await self.LAttackInitiation()
                await self.MMedivacProximity()
            if iteration % 125 == 0:
                await self.MReaperScout()
                await self.LOrbitalCommand()
                await self.MBTechlab()
                await self.LEngineeringBay()
            if iteration % 200 == 0:
                await self.distribute_workers()
                await self.MCommandCenter()
            if iteration % 250 == 0:
                await self.LScanNearArmy()
            if iteration % 500 == 0:
                await self.MRally()
                await self.Esupplydepotdown()


    """Methods"""
    async def MMarineProximity(self):
        for m in self.units(MARINE):
            threat = self.known_enemy_units.not_structure.closer_than(9, m.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                print("M_ATTACK")
                if await self.can_cast(m, EFFECT_STIM_MARINE) and m.health_percentage > 7/8:
                    await self.do(m(EFFECT_STIM_MARINE))
                    print("STIM")
                await self.do(m.attack(threat.closest_to(m.position).position))

    async def MMARAUDERProximity(self):
        for m in self.units(MARAUDER):
            threat = self.known_enemy_units.not_structure.not_flying.closer_than(9, m.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                print("M_ATTACK")
                if await self.can_cast(m, EFFECT_STIM_MARAUDER) and m.health_percentage > 9.5/10:
                    await self.do(m(EFFECT_STIM_MARAUDER))
                    print("STIM")
                await self.do(m.attack(threat.closest_to(m.position).position))

    async def MSiegeTankProximity(self):
        for s in self.units(SIEGETANK):
            threat = self.known_enemy_units.closer_than(15, s).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                await self.do(s(SIEGEMODE_SIEGEMODE))
                print("SIEGE")

    async def MSiegedTankProximity(self):
        for s in self.units(SIEGETANKSIEGED):
            threat = self.known_enemy_units.closer_than(20, s).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if not threat.exists:
                await self.do(s(UNSIEGE_UNSIEGE))
                print("UNSIEGE")

    async def MMedivacProximity(self):
        m = self.units(MARINE) | self.units(MARAUDER)
        if m.exists:
            p = m.furthest_to(self.start_location).position.towards(self.start_location, 3)
            for medivac in self.units(MEDIVAC):
                await self.do(medivac.attack(p))
        if self.units(MEDIVAC).exists and False: # "and False" added to not create unknown bugs. This is future code and is not implemented
            sacrifice = self.units(MEDIVAC).random
            threat = self.known_enemy_units.not_structure.closer_than(9, sacrifice.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            r = self.units(RAVEN).closer_than(6, sacrifice.position)
            if threat.amount > 10 and r.amount > 1:
                p = threat.random.position
                print("LOADING MEDIVAC CANNON!!!")
                if await self.can_cast(m, EFFECT_MEDIVACIGNITEAFTERBURNERS):
                    await self.do(m, EFFECT_MEDIVACIGNITEAFTERBURNERS)
                    await self.do(m.move(p))
                    print("MARU BLAST!!!")
                    for rr in r:
                        if rr.energy > 75:
                            if await self.can_casr(rr, EFFECT_ANTIARMORMISSILE, sacrifice):
                                await self.do(rr, EFFECT_ANTIARMORMISSILE, sacrifice)


    async def MRavenIdle(self): # code is no long in use... It has been removed
        for r in self.units(RAVEN).idle:
            e = self.known_enemy_units.not_structure.closer_than(11, r.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if e.exists:
                if r.energy > 75:
                    # ea = e.closest_to(r.position) # changed do to opinion
                    ea = e.random
                    if ea.is_mechanical and await self.can_cast(r, EFFECT_INTERFERENCEMATRIX, ea):
                        await self.do(r(EFFECT_INTERFERENCEMATRIX, ea))
                        print("INTERENCE MATRIX")
                    elif await self.can_cast(r, EFFECT_ANTIARMORMISSILE, ea):
                        await self.do(r(EFFECT_ANTIARMORMISSILE, ea))
                        print("ORANGE ATTACK")
                else:
                    await self.do(r.move(r.position.towards(self.start_location, 5)))
            else:
                s = self.units(SIEGETANK) | self.units(SIEGETANKSIEGED)
                if s.exists:
                    p = s.furthest_to(self.start_location).position.towards(self.start_location, 5)
                    await self.do(r.attack(p))
    # ^^^ Code is retired ^^^

    async def MRavenProximity(self):
        for r in self.units(RAVEN):
            e = self.known_enemy_units.not_structure.closer_than(11, r.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE).exclude_type(OVERSEER).exclude_type(PROBE).exclude_type(SCV).exclude_type(DRONE)
            if e.exists and r.energy > 75:
                eMechPriority = e(SIEGETANKSIEGED) | e(VIKINGFIGHTER) | e(BATTLECRUISER) | e(THOR) | e(CARRIER) | e(VOIDRAY) | e(CARRIER) | e(COLOSSUS) | e(MOTHERSHIP) | e(TEMPEST)
                if eMechPriority.exists:
                    ea = eMechPriority.random
                    if await self.can_cast(r, EFFECT_INTERFERENCEMATRIX, ea):
                        await self.do(r(EFFECT_INTERFERENCEMATRIX, ea))
                        print("INTERENCE MATRIX")
                else:
                    ea = e.random
                    if r.position.distance_to(ea.position) > 6:
                        if await self.can_cast(r, EFFECT_ANTIARMORMISSILE, ea):
                            await self.do(r(EFFECT_ANTIARMORMISSILE, ea))
                            print("ORANGE!!!")
                    elif await self.can_cast(r, RAVENBUILD_AUTOTURRET, r.position):
                        await self.do(r, RAVENBUILD_AUTOTURRET, r.position)
            elif e.exists:
                ea = e.closest_to(r.position)
                p = ea.position.towards(r.position, 13)
                await self.do(r.move(p))
            else:
                a = self.units(MARINE) | self.units(MARAUDER) | self.units(SIEGETANK) | self.units(SIEGETANKSIEGED)
                p = a.furthest_to(self.start_location).position.towards(self.start_location, 2)
                await self.do(r.move(p))

    async def MReaperScout(self):
        for r in self.units(REAPER).idle:
            m = self.state.mineral_field.closer_than((self.supply_used*4), self.start_location).random.position
            await self.do(r.attack(m))
            print("SCOUT")

    async def LAttackInitiation(self):
        a = self.units(SIEGETANK) | self.units(MARINE) | self.units(MARAUDER)
        e = self.known_enemy_units.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
        if a.amount > 40 and e.amount > 10:
            ep = e.closest_to(a.furthest_to(self.start_location).position).position.towards(self.game_info.map_center, -10)
            for aa in a:
                await self.do(aa.attack(ep))
                print("MARCH")
        elif self.known_enemy_structures.amount > 0 and self.supply_used >= 195:
            ep = e.closest_to(self.start_location).position
            for aa in a:
                await self.do(aa.attack(ep))
                print("ATTACK")

    async def MRally(self):
        building = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED) | self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        if self.known_enemy_structures.exists and building.exists:
            self.RallyPoint = building.closest_to(self.known_enemy_structures.random.position).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        for a in self.units.idle.not_structure:
            if a.distance_to(self.RallyPoint) > 15:
                await self.do(a.attack(self.RallyPoint))

    async def MDefend(self):
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        for c in cc:
            threat = self.known_enemy_units.closer_than(25, c.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                army = self.units.exclude_type(SCV).exclude_type(RAVEN).exclude_type(MEDIVAC).not_structure.closer_than(50, c.position)
                # improve code to include scv attacks
                p = threat.random.position
                for a in army:
                    await self.do(a.attack(p))
                print("Threat Detected")
                print(c.position)
            else:
                print("No Threat Detected")
                print(c.position)

    async def EEarlyDefend(self):

        threat = self.known_enemy_units.closer_than(16, self.start_location)
        if threat.exists:
            army = self.units.not_structure
            for a in army:
                await self.do(a.attack(threat.random))
                print("*Relatively Not Safe*")
        else:
            print("*Relatively Safe*")

    async def MLandIdleBuildings(self):
        b = self.units(BARRACKSFLYING).idle
        f = self.units(FACTORYFLYING).idle
        s = self.units(STARPORTFLYING).idle
        if b.exists:
            if not self.units(BARRACKSTECHLAB).exists and not self.units(TECHLAB).exists:
                b1 = b.random
                p = b1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                await self.do(b1.move(p))
                if self.can_afford(BARRACKSTECHLAB):
                    await self.do(b1.build(BARRACKSTECHLAB, p))
                    print("LAND B_TECHLAB")
            elif not self.units(REACTOR).exists:
                for b2 in b:
                    p = b2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    await self.do(b2.move(p))
                    if self.can_afford(BARRACKSREACTOR):
                        await self.do(b2.build(BARRACKSREACTOR, p))
                        print("LAND B_TECHLAB")

        if f.exists:
            if not self.units(TECHLAB).exists:
                for f2 in f:
                    p = f2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    await self.do(f2.move(p))
                    if self.can_afford(FACTORYTECHLAB):
                        await self.do(f2.build(FACTORYTECHLAB, p))
                        print("LAND F_TECHLAB")

        if s.exists:
            if not self.units(STARPORTREACTOR).exists and not self.units(REACTOR).exists:
                s1 = s.random
                p = s1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                await self.do(s1.move(p))
                if self.can_afford(STARPORTREACTOR):
                    await self.do(s1.build(STARPORTREACTOR, p))
                    print("LAND S_REACTORLAB")
            else:
                for s2 in s:
                    p = s2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    await self.do(s2.move(p))
                    if self.can_afford(STARPORTTECHLAB):
                        await self.do(s2.build(STARPORTTECHLAB, p))
                        print("LAND S_TECHLAB")

    async def MCommandCenter(self):
        cc = self.units(COMMANDCENTER)
        oc = self.units(ORBITALCOMMAND)
        for c in cc.ready.noqueue:
            if self.can_afford(ORBITALCOMMAND) and cc.not_ready.exists:
                print("CC_OC")
                await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
            elif self.can_afford(SCV) and self.units(SCV).amount < (cc.amount*20) + (oc.amount*15) + 15 and self.units(SCV).amount < 70:
                print("CC_SCV")
                await self.do(c.train(SCV))
                # coded this way to deal with a bug with expandnow()

    async def LScanNearArmy(self):
        oc = self.units(ORBITALCOMMAND).random
        if oc.energy > 50 and self.supply_used > 100 and self.known_enemy_units.amount > 0:
            e = self.known_enemy_units
            if e.exists:
                e2 = e.closest_to(self.start_location).position
                p = self.units.closest_to(e2).position
                await self.do(oc(SCANNERSWEEP_SCAN, p.towards(e2, 16)))
                ea = self.known_enemy_units.closer_than(18, p).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
                # radius is 15 because a wiki said so
                if ea.exists:
                    p = ea.random.position
                    army = self.units(SIEGETANK) | self.units(MARINE) | self.units(MARAUDER)
                    armynear = army.closer_than(40, p)
                    for a in armynear:
                        await self.do(a.attack(p))

    async def LOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        for o in oc.ready.noqueue:
            if self.can_afford(SCV) and self.units(SCV).amount < 55:
                print("OC_SCV")
                await self.do(o.train(SCV))
        for o in oc.ready:
            if o.energy == 200:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    await self.do(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")
                elif self.known_enemy_structures.amount == 0:
                    await self.do(o(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))
                    await self.do(o(SCANNERSWEEP_SCAN, self.state.mineral_field.random.position))

    async def MOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        for o in oc.ready.noqueue:
            if self.can_afford(SCV) and self.units(SCV).amount < 50:
                print("OC_SCV")
                await self.do(o.train(SCV))
        for o in oc.ready:
            if o.energy >= 150:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    await self.do(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")
            elif o.energy > 100 and self.known_enemy_structures.amount == 0:
                await self.do(o(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))
                await self.do(o(SCANNERSWEEP_SCAN, self.state.mineral_field.random.position))
                print("SCAN SEARCH")

    async def EOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        for o in oc.ready.noqueue:
            if self.can_afford(SCV) and self.units(SCV).amount < 50:
                print("OC_SCV")
                await self.do(o.train(SCV))
        for o in oc.ready:
            if o.energy >= 50:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    await self.do(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")

    async def MManageSupply(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND)
        s = self.units(SCV)
        if cc.exists and s.exists and self.supply_used + self.supply_left < 200:
            if self.supply_left < self.supply_used/16 + 4 and not self.already_pending(SUPPLYDEPOT) and self.can_afford(SUPPLYDEPOT):
                sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
                if sd.exists:
                    await self.build(SUPPLYDEPOT, near=sd.random)
                    print("SUPPLYDEPOT")
                else:
                    await self.build(SUPPLYDEPOT, near=cc.random)
                    print("CC_SUPPLYDEPOT")
                if self.can_afford(SUPPLYDEPOT) and sd.exists:
                    await self.build(SUPPLYDEPOT, near=sd.random)
                    print("SUPPLYDEPOT")
            elif self.supply_left < 0 and self.can_afford(SUPPLYDEPOT):
                await self.build(SUPPLYDEPOT, near=cc.random)
                """most code here is untested"""

    async def LReplaceExpand(self):
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        f = self.units(FACTORY) | self.units(FACTORYFLYING)
        s = self.units(STARPORT) | self.units(STARPORTFLYING)
        a = b.flying | f.flying | s.flying
        t = self.units(TECHLAB)
        r = self.units(REACTOR)
        e = self.units(ENGINEERINGBAY)
        ar = self.units(ARMORY)

        if sd.ready.exists and not b.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(BARRACKS, p)

        elif b.ready.exists and not f.exists and not self.already_pending(FACTORY) and self.can_afford(FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(FACTORY, p)

        elif f.ready.exists and not s.exists and not self.already_pending(STARPORT) and self.can_afford(STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(STARPORT, p)

        elif not e.exists and not self.already_pending(ENGINEERINGBAY) and self.can_afford(ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(ENGINEERINGBAY, p)

        elif s.ready.exists and not ar.exists and not self.already_pending(ARMORY) and self.can_afford(ARMORY):
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(ARMORY, p)

        elif t.exists and a.exists:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f.flying | s.flying
            if b.flying.exists and self.units(BARRACKSREACTOR).exists:
                bf = b.flying.first
                await self.do(bf(LAND, p))
            elif a2.exists:
                af = a2.first
                p = t.first.add_on_land_position
                await self.do(af(LAND, p))

        elif r.exists and (b.flying.exists or s.flying.exists):
            print("REPLACE REACTOR SPOT TRY DO")
            if not self.units(STARPORTREACTOR).exists and s.flying.exists:
                p = r.first.add_on_land_position
                sf = s.flying.first
                await self.do(sf(LAND, p))

            elif b.flying.exists:
                p = r.first.add_on_land_position
                bf = b.flying.first
                await self.do(bf(LAND, p))

        elif b.amount < cc.amount and not self.already_pending(BARRACKS) and self.can_afford(FACTORY):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(BARRACKS, p)

        elif f.amount < 2 and not self.already_pending(FACTORY) and self.can_afford(FACTORY):
            print("NOT ENOUGH FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(FACTORY, p)

        elif s.amount < 2 and not self.already_pending(STARPORT) and self.can_afford(STARPORT):
            print("NOT ENOUGH FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(STARPORT, p)


    async def MReplaceExpand(self):
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        f = self.units(FACTORY) | self.units(FACTORYFLYING)
        s = self.units(STARPORT) | self.units(STARPORTFLYING)
        e = self.units(ENGINEERINGBAY)
        a = b.flying | f.flying | s.flying
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if sd.ready.exists and not b.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(BARRACKS, p)

        elif b.ready.exists and not f.exists and not self.already_pending(FACTORY) and self.can_afford(FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(FACTORY, p)

        elif f.ready.exists and not s.exists and not self.already_pending(STARPORT) and self.can_afford(STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(STARPORT, p)

        elif not e.exists and not self.already_pending(ENGINEERINGBAY) and self.can_afford(ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(ENGINEERINGBAY, p)

        elif t.exists and a.exists:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f.flying | s.flying
            if b.flying.exists and self.units(BARRACKSREACTOR).exists:
                bf = b.flying.first
                await self.do(bf(LAND, p))
            elif a2.exists:
                af = a2.first
                p = t.first.add_on_land_position
                await self.do(af(LAND, p))

        elif r.exists and (b.flying.exists or s.flying.exists):
            print("REPLACE REACTOR SPOT TRY DO")
            if not self.units(STARPORTREACTOR).exists and s.flying.exists:
                p = r.first.add_on_land_position
                sf = s.flying.first
                await self.do(sf(LAND, p))

            elif b.flying.exists:
                p = r.first.add_on_land_position
                bf = b.flying.first
                await self.do(bf(LAND, p))

        elif b.amount == 1 and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(BARRACKS, p)

        elif self.minerals > 500:
            print("expand")
            await self.expand_now()

        elif f.amount == 1 and not self.already_pending(FACTORY) and cc.amount > 2 and self.can_afford(FACTORY):
            print("NOT ENOUGH FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(FACTORY, p)

        elif s.amount == 1 and not self.already_pending(STARPORT) and cc.amount > 2 and self.can_afford(STARPORT):
            print("NOT ENOUGH STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(6, 10))
                await self.build(STARPORT, p)

    async def Ebuildorder(self):
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER)
        oc = self.units(ORBITALCOMMAND)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)

        if cc.ready.exists or oc.ready.exists:
            cci = cc.ready.noqueue | oc.ready.noqueue
            if cc.not_ready.exists and cc.ready.noqueue.exists and self.can_afford(ORBITALCOMMAND) and b.ready.exists:
                c = cc.noqueue.ready.random
                await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
            elif cci.exists and self.can_afford(SCV):
                for c in cci:
                    if self.can_afford(SCV):
                        """this is not a redundancy"""
                        await self.do(c.train(SCV))

            if scv.exists and not sd.exists and not self.already_pending(SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(SUPPLYDEPOT):

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
                    await self.do(s.build(SUPPLYDEPOT, p))
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                s = scv.furthest_to(self.start_location)
                if not b.exists and not self.already_pending(BARRACKS):
                    if self.can_afford(BARRACKS):
                        p = self.main_base_ramp.barracks_correct_placement.position
                        await self.do(s.build(BARRACKS, p))
                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print("BARRACKS1")
                        if self.can_afford(BARRACKS):
                            p = self.main_base_ramp.barracks_correct_placement.offset((0, -2))
                            await self.do(s.build(BARRACKS, p))
                            print("placement problem")

                if b.exists:
                    if self.can_afford(REFINERY) and not self.units(REFINERY).exists:
                        await self.ERefineryBuild()
                    else:
                        if oc.amount + cc.amount == 1 and self.can_afford(COMMANDCENTER):
                            await self.expand_now()
                            print("EXPAND")
                        elif cc.amount == 2 and self.can_afford(ORBITALCOMMAND):
                            if cc.noqueue.ready.exists:
                                c == cc.noqueue
                                await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
                                print("UPGRADE ORBITAL")
                        elif oc.exists or self.already_pending(ORBITALCOMMAND) or self.units(BARRACKSREACTOR).exists:
                            if sd.amount == 1 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
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

                                await self.build(SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT2")
                            elif sd.amount <= 2:
                                if b.amount < 2 and self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
                                    print("BARRACKS2")
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
                                    await self.build(BARRACKS, p)
                                elif b.amount == 2:
                                    if self.units(REFINERY).amount == 1 and not self.already_pending(REFINERY):
                                        await self.ERefineryBuild()
                                    elif self.units(FACTORY).amount == 0 and self.can_afford(FACTORY) and not self.already_pending(FACTORY):
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
                                        await self.build(FACTORY, p)
                                        print("FACTORY")
                                        """change later"""
                                    elif self.units(FACTORY).exists:
                                        if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
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
                                            await self.build(SUPPLYDEPOT, p)
                                            print("SUPPLYDEPOT3")

    async def MRefineryBuild(self):
        if self.units(REFINERY).amount < (self.units(COMMANDCENTER).amount * 2) + (self.units(ORBITALCOMMAND).amount * 2):
            for cc in self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND):
                v = self.state.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(REFINERY) and not self.already_pending(REFINERY):
                        #observation from E method is still valid.
                            if not self.units(REFINERY).closer_than(1, ve).exists:
                                worker = self.select_build_worker(ve.position)
                                if worker is None:
                                    break
                                await self.do(worker.build(REFINERY, ve))
                                print("REFINERY")
                            # copy pasted from E method because I might want it to be slightly different than the other method
                            # it currently has a larger amount of refineries because I plan on doing a vespene gas heavy army

    async def ERefineryBuild(self):
        if self.units(REFINERY).amount < self.units(COMMANDCENTER).amount + (self.units(ORBITALCOMMAND).amount * 2):
            for cc in self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND):
                v = self.state.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(REFINERY) and not self.already_pending(REFINERY):
                        """ 
                        Observation: The code was learned from  the youtube tutorial. It is not optimally coded.
                        It in theory, only allows one refinery construction at a time. Loop -> Loop -> Check
                        If the check was done before the loop, there wouldn't be needless cycles.
                        Code left unchanged because of time constraint and not wanting to break the project.
                        """
                        if not self.units(REFINERY).closer_than(1, ve).exists:
                            worker = self.select_build_worker(ve.position)
                            if worker is None:
                                break
                            await self.do(worker.build(REFINERY, ve))
                            print("REFINERY")
                            # recycled code that works for early game
                            # logic doesn't fit code because I didn't need to change the code to accomplish what I wanted it to accomplish

    async def LEngineeringBay(self):
        for e in self.units(ENGINEERINGBAY).idle.noqueue:
            if await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1):
                await self.do(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2):
                await self.do(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3):
                await self.do(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1):
                await self.do(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2):
                await self.do(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3):
                await self.do(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3))

    async def MBTechlab(self):
        bt = self.units(BARRACKSTECHLAB).ready.noqueue
        if bt.exists:
            bt1 = bt.first
            if self.can_afford(RESEARCH_COMBATSHIELD) and not self.TechShield:
                await self.do(bt1(RESEARCH_COMBATSHIELD))
                self.TechShield = True
                print("UPGRADE_SHIELD")
            elif self.can_afford(BARRACKSTECHLABRESEARCH_STIMPACK) and not self.TechStim:
                await self.do(bt1(BARRACKSTECHLABRESEARCH_STIMPACK))
                self.TechStim = True
                print("UPGRADE_STIM")

    async def MBarracks(self):
        for b in self.units(BARRACKS).ready.noqueue:
            if b.add_on_tag == 0:
                #code changed
                """if self.units(REACTOR).exists and not self.units(BARRACKSREACTOR).exists:
                    await self.do(b(LIFT))
                    print("FLY!!!")
                elif self.units(TECHLAB).exists:
                    await self.do(b(LIFT))
                    print("FLY!!!")
                elif self.can_afford(BARRACKSREACTOR) and not self.units(BARRACKSREACTOR).exists:
                    await self.do(b.build(BARRACKSREACTOR))
                    print("B_REACTOR")
                elif self.can_afford(BARRACKSTECHLAB):
                    await self.do(b.build(BARRACKSTECHLAB))
                    print("B_TECHLAB")"""
                await self.do(b(LIFT))
                print("FLY!!!")
            elif self.units(BARRACKSTECHLAB).exists and self.supply_left > 1:
                id = self.units(BARRACKSTECHLAB).random.tag
                if b.add_on_tag == id:
                    if self.can_afford(MARAUDER) and self.supply_left > 1:
                        await self.do(b.train(MARAUDER))

                elif self.supply_left > 1:
                    if self.can_afford(REAPER) and not self.units(REAPER).exists and self.units(MARINE).amount >= 10:
                        await self.do(b.train(REAPER))
                        print("B_R1")
                        if self.can_afford(REAPER):
                            await self.do(b.train(REAPER))
                            print("B_R2")
                    elif self.can_afford(MARINE):
                        await self.do(b.train(MARINE))
                        print("B_R1")
                        if self.can_afford(MARINE):
                            await self.do(b.train(MARINE))
                            print("B_R2")

            elif self.supply_left > 1:
                if self.can_afford(REAPER) and not self.units(REAPER).exists and self.units(MARINE).amount >= 10:
                    await self.do(b.train(REAPER))
                    print("B_R1")
                    if self.can_afford(REAPER):
                        await self.do(b.train(REAPER))
                        print("B_R2")
                elif self.can_afford(MARINE):
                    await self.do(b.train(MARINE))
                    print("B_R1")
                    if self.can_afford(MARINE):
                        await self.do(b.train(MARINE))
                        print("B_R2")

    async def EBarracks(self):
        for b in self.units(BARRACKS).ready.noqueue:
            if self.units(BARRACKSREACTOR).exists and self.supply_used < 198:
                id = self.units(BARRACKSREACTOR).random.tag
                if b.add_on_tag == id:
                    if self.can_afford(REAPER) and not self.units(REAPER).exists and self.units(MARINE).amount >= 10:
                        await self.do(b.train(REAPER))
                        print("B_R1")
                        if self.can_afford(REAPER):
                            await self.do(b.train(REAPER))
                            print("B_R2")
                    else:
                        if self.can_afford(MARINE):
                            await self.do(b.train(MARINE))
                            print("B_M1")
                        if self.can_afford(MARINE):
                            await self.do(b.train(MARINE))
                            print("B_M2")
                elif b.add_on_tag == 0:
                    if self.can_afford(BARRACKSTECHLAB):
                        await self.do(b.build(BARRACKSTECHLAB))
                        print("B_TECHLAB")
                else:
                    if self.can_afford(MARAUDER):
                        await self.do(b.train(MARAUDER))
                        print("B_MARAUDER")
            elif self.can_afford(REAPER):
                await self.do(b.build(BARRACKSREACTOR))
                print("B_REACTOR")

    async def MFactory(self):
        for f in self.units(FACTORY).ready.noqueue:
            if not self.units(FACTORYREACTOR).exists and self.supply_left > 2:
                """assumption is that there will be no factory reactor and it is coded not to crash if it exists*"""
                if f.add_on_tag == 0:
                    await self.do(f(LIFT))
                    print("FLY!!!")
                    """if self.units(TECHLAB).exists:
                        await self.do(f(LIFT))
                        print("FLY!!!")
                    elif self.can_afford(FACTORYTECHLAB):
                        await self.do(f.build(FACTORYTECHLAB))
                        print("F_TECHLAB")"""
                else:
                    if self.can_afford(SIEGETANK):
                        await self.do(f.train(SIEGETANK))
                        print("F_SIEGETANK")
            elif self.units(FACTORYREACTOR).exists:
                await self.do(f(LIFT))
                print("FLY!!!")

    async def EFactory(self):
        for f in self.units(FACTORY).ready.noqueue:
            if not self.units(FACTORYREACTOR).exists and self.supply_used <= 197:
                """assumption is that there will be no factory reactor and it is coded not to crash if it exists*"""
                if f.add_on_tag == 0:
                    if self.can_afford(FACTORYTECHLAB):
                        await self.do(f.build(FACTORYTECHLAB))
                        print("F_TECHLAB")
                else:
                    if self.can_afford(SIEGETANK):
                        await self.do(f.train(SIEGETANK))
                        print("F_SIEGETANK")

    async def MStarport(self):
        for s in self.units(STARPORT).ready.noqueue:
            if s.add_on_tag == 0:
                await self.do(s(LIFT))

            elif self.units(STARPORTREACTOR).exists:
                id = self.units(STARPORTREACTOR).random.tag
                if s.add_on_tag == id and self.supply_left > 4:
                    if self.can_afford(MEDIVAC) and self.units(MEDIVAC).amount <= 12:
                        await self.do(s.train(MEDIVAC))
                        if self.can_afford(MEDIVAC):
                            await self.do(s.train(MEDIVAC)) #replacement code
                    """if self.units(MEDIVAC).amount + 2 < self.units(VIKINGFIGHTER).amount:
                        if self.can_afford(MEDIVAC):
                            await self.do(s.train(MEDIVAC))
                            if self.can_afford(MEDIVAC):
                                await self.do(s.train(MEDIVAC))
                    else:
                        if self.minerals > 350 and self.vespene > 200:
                            await self.do(s.train(VIKING))
                            await self.do(s.train(VIKING))""" # tried a couple things to make this code work but gave up for future sprint
                elif self.supply_left > 2:
                    if self.can_afford(RAVEN):
                        await self.do(s.train(RAVEN))

            else:
                if self.can_afford(RAVEN):
                    await self.do(s.train(RAVEN))

    async def Esupplydepotdown(self):
        for sd in self.units(SUPPLYDEPOT).ready:
            e = self.known_enemy_units.closer_than(6, sd.position)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                await self.do(sd(MORPH_SUPPLYDEPOT_LOWER))

    async def Esupplydepotup(self):
        for sd in self.units(SUPPLYDEPOTLOWERED).ready:
            e = self.known_enemy_units.closer_than(8, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists:
                await self.do(sd(MORPH_SUPPLYDEPOT_RAISE))
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