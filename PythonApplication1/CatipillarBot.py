import sc2
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer, Human
from sc2.constants import *
import random
"""
Nameing Conventions for methods
G: General
R: Random -> Random is a Starcraft race that can be referenced at the of start a game even though it turns into a different faction on startup.
T: Terran
Z: Zerg
P: Protoss
-----------
E: Early Game
M: Mid Game
L: Late Game
-----------
Note* A lot of methods are reused. If the naming convention characters don't match, it because it is probably intentionly borrowed from another playstyle
"""
class CatipillarAI(BotAI):
    def on_start(self):
        self.Rally = None
        self.BattleWinningMath = 1.0 # unimplemented feature -> will be used to make good decisions
        self.target = None
        self.STRAT="error"
        self.nextXpansionLocation = self.start_location
        if self.enemy_race == Race.Random:
            self.STRAT = "AntiRandom"
        elif self.enemy_race == Race.Terran:
            self.STRAT = "AntiTerran"
        elif self.enemy_race == Race.Zerg:
            self.STRAT = "AntiZerg"
        elif self.enemy_race == Race.Protoss:
            self.STRAT = "AntiProtoss"
        print("Strat:")
        print(self.STRAT)

    async def on_step(self, iteration):
        if self.STRAT == "AntiRandom":
            """Early Game"""
            if True:# self.time <= 240:
                if iteration % 5 == 0:
                    await self.REBuildOrder()
                    await self.GEReaperScout()
                    await self.GEUnfinshedBuildingCheck()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.RECheckEnemy()
                if iteration % 10 == 0:
                    await self.REBarracks()
                if iteration % 10 == 5:
                    await self.GEFactory()
                    await self.GEOrbitalCommand()
                if iteration % 150 == 0:
                    await self.GEEarlyDefend()

        elif self.STRAT == "AntiTerran":
            if self.time <= 240:
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.TECommandCenter()
                    await self.TEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GEReaperScout()
                    await self.TEBuildOrder()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 10 == 0:
                    await self.GEBarracks()
                    await self.TEInBaseCommandCenter()
                    await self.TMAddonAbductBuilding()
                if iteration % 10 == 5:
                    await self.GEFactory()
                if iteration % 150 == 0:
                    await self.GEEarlyDefend()
            elif self.time > 240 and True:
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.TELandCommandCenter()
                    await self.TECommandCenter()
                    await self.TEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GMReaperScout()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GMManageSupply()
                if iteration % 10 == 0:
                    await self.GMRefineryBuild()
                    await self.GMBarracks()
                    await self.GMFactory()
                    await self.GMStarport()
                    await self.TEInBaseCommandCenter()
                    await self.GMSiegeTankProximity(16)
                if iteration % 10 == 5:
                    await self.TMAddonAbductBuilding()
                    await self.GMLandIdleBuildings()
                    await self.TMReplaceExpand()

                if iteration % 20 == 0:
                    await self.GMSiegedTankProximity(20)
                    await self.GMMarineProximity(10)
                    await self.GMMarauderProximity(10)
                    await self.GMMedivacProximity()
                    await self.GMRavenProximity()
                    await self.GMRefineryBuild()
                    await self.GMRally()
                if iteration % 25 == 0:
                    await self.GMDefend()
                    await self.TMAttackInitiation(20, 25)
                    await self.GMBTechlab()
                    await self.GMEngineeringBay()
                    await self.GMArmoryGround()

        elif self.STRAT == "AntiZerg":
            if self.time <= 240:
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.GEReaperProximity()
                    await self.GEReaperScout()
                    await self.ZEBuildOrder()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 10 == 0:
                    await self.GEBarracks()
                if iteration % 10 == 5:
                    await self.ZEFactory()
                    await self.GEOrbitalCommand()
                if iteration % 150 == 0:
                    await self.GEEarlyDefend()
            if self.time > 240 and True:   # time for late game iteration may or may not be needed
                if iteration % 5 == 0:
                    await self.GEReaperProximity()
                    await self.GEUnfinshedBuildingCheck()
                    await self.GMReaperScout()
                    await self.ZMHellionFollow(10)
                if iteration % 10 == 0:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                    await self.ZMAddonAbductBuilding()
                    await self.GMSiegeTankProximity(15)
                    await self.ZMHellionProximity(10)
                    await self.GMMedivacProximity()
                    await self.GMRavenProximity()
                    await self.GMSiegeTankFollow(3) # code is weird but is meant for following a-moved units
                if iteration % 20 == 0:
                    await self.GMMarineProximity(10)
                    await self.GMMarauderProximity(10)
                    await self.distribute_workers()
                    await self.GMLandIdleBuildings()  # it intentionally doesn't replace reactor for Factory
                    await self.ZMFTechlab()
                    await self.GMEngineeringBay()
                    await self.GMArmoryGround()
                    await self.GMBTechlab()
                    await self.ZMLurkerCheck()
                if iteration % 25 == 0:
                    await self.ZMFactory()
                    await self.GMBarracks()
                    await self.GMStarport()  # redo code for no ravens or raven cap 1?
                    await self.GMManageSupply()
                    await self.ZMAttackInitiation(10, 20) #  Hellion psudo timing attack and max supply push
                if iteration % 50 == 0:
                    await self.ZMHellbatProximity(14)
                    await self.GMCommandCenter()
                    await self.GMOrbitalCommand()
                    await self.GMLandCommandCenter()
                    await self.GMRefineryBuild()
                    await self.ZMReplaceExpand()
                if iteration % 100 == 0:
                    await self.GMSiegedTankProximity(16)
                    await self.GMDefend()
                    await self.GMOrbitalScansAttack()
                if iteration % 200 == 0:
                    await self.GMRallyAlternateMarineMarauder()

        elif self.STRAT == "AntiProtoss":

            if self.time <= 240:
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.TECommandCenter()
                    await self.TEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GEReaperScout()
                    await self.PEBuildOrder()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 10 == 0:
                    await self.GEBarracks()
                    await self.TEInBaseCommandCenter()
                    await self.TMAddonAbductBuilding()
                if iteration % 10 == 5:
                    await self.GEFactory()
                if iteration % 150 == 0:
                    await self.GEEarlyDefend()
            elif self.time > 240 and True:
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.TELandCommandCenter()
                    await self.TECommandCenter()
                    await self.TEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GMReaperScout()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GMManageSupply()
                if iteration % 10 == 0:
                    await self.GMRefineryBuild()
                    await self.GMBarracks()
                    await self.GMFactory()
                    await self.GMStarport()
                    await self.TEInBaseCommandCenter()
                    await self.GMSiegeTankProximity(16)
                if iteration % 10 == 5:
                    await self.TMAddonAbductBuilding()
                    await self.GMLandIdleBuildings()
                    await self.TMReplaceExpand()

                if iteration % 20 == 0:
                    await self.GMSiegedTankProximity(20)
                    await self.GMMarineProximity(10)
                    await self.GMMarauderProximity(10)
                    await self.GMMedivacProximity()
                    await self.GMRavenProximity()
                    await self.GMRefineryBuild()
                    await self.GMRally()
                if iteration % 25 == 0:
                    await self.GMDefend()
                    await self.PMAttackInitiation(30, 30)
                    await self.GMBTechlab()
                    await self.GMEngineeringBay()
                    await self.GMArmoryGround()

    """Methods: GENERAL"""
    async def GMMarineProximity(self, proximity):
        for m in self.units(MARINE):
            threat = self.known_enemy_units.not_structure.closer_than(proximity, m.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists and m.health_percentage > 2/8:
                print("M_ATTACK")
                if await self.can_cast(m, EFFECT_STIM_MARINE) and m.health_percentage > 7/8:
                    await self.do(m(EFFECT_STIM_MARINE))
                    print("STIM")
                await self.do(m.attack(threat.closest_to(m.position).position))
            elif threat.exists:
                e = threat.closest_to(m.position).position
                p = m.position.towards(e, -proximity)

    async def GMMarauderProximity(self, proximity):
        for m in self.units(MARAUDER):
            threat = self.known_enemy_units.not_structure.not_flying.closer_than(proximity, m.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                print("M_ATTACK")
                if await self.can_cast(m, EFFECT_STIM_MARAUDER) and m.health_percentage > 9.5/10:
                    await self.do(m(EFFECT_STIM_MARAUDER))
                    print("STIM")
                await self.do(m.attack(threat.closest_to(m.position).position))

    async def GMSiegeTankProximity(self, proximity):
        for s in self.units(SIEGETANK):
            threat = self.known_enemy_units.closer_than(proximity, s).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                await self.do(s(SIEGEMODE_SIEGEMODE))
                print("SIEGE")

    async def GMSiegedTankProximity(self, proximity):
        for s in self.units(SIEGETANKSIEGED):
            threat = self.known_enemy_units.closer_than(proximity, s).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if not threat.exists:
                await self.do(s(UNSIEGE_UNSIEGE))
                print("UNSIEGE")

    async def GMMedivacProximity(self):
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
                await self.chat_send("LOADING MEDIVAC CANNON!!!")
                if await self.can_cast(m, EFFECT_MEDIVACIGNITEAFTERBURNERS):
                    await self.do(m, EFFECT_MEDIVACIGNITEAFTERBURNERS)
                    await self.do(m.move(p))
                    print("MARU BLAST!!!")
                    await self.chat_send("MARU BLAST!!!") # Maru is a professional starcraft player who used a medivac to extend the range of reaper missiles

                    for rr in r:
                        if rr.energy > 75:
                            if await self.can_casr(rr, EFFECT_ANTIARMORMISSILE, sacrifice):
                                await self.do(rr, EFFECT_ANTIARMORMISSILE, sacrifice)

    async def GMRavenProximity(self):
        for r in self.units(RAVEN):
            e = self.known_enemy_units.not_structure.closer_than(11, r.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE).exclude_type(OVERSEER).exclude_type(PROBE).exclude_type(SCV).exclude_type(DRONE).exclude_type(LARVA).exclude_type(EGG)
            if e.exists and r.energy > 75:
                eMechPriority = e(SIEGETANKSIEGED) | e(VIKINGFIGHTER) | e(BATTLECRUISER) | e(THOR) | e(CARRIER) | e(VOIDRAY) | e(CARRIER) | e(COLOSSUS) | e(MOTHERSHIP) | e(TEMPEST)
                if eMechPriority.exists:
                    ea = eMechPriority.random
                    if await self.can_cast(r, EFFECT_INTERFERENCEMATRIX, ea):
                        await self.do(r(EFFECT_INTERFERENCEMATRIX, ea))
                        print("INTERENCE MATRIX")
                        await self.chat_send("INTERENCE MATRIX!!!")
                else:
                    ea = e.random
                    eap = ea.position
                    e2 = e.closer_than(3, eap)
                    r2 = self.units.closer_than(5, eap)  # arbituary numbers used
                    if r.position.distance_to(ea.position) > 6 and e2.amount > r2.amount + 2 and await self.can_cast(r, EFFECT_ANTIARMORMISSILE, ea):
                        await self.do(r(EFFECT_ANTIARMORMISSILE, ea))
                        print("ORANGE!!!")
                        await self.chat_send("ORANGE!!!")
                    else:
                        print("idk debug this")
                        """
                        if self.can_afford(AUTOTURRET):
                            p = await self.find_placement(AUTOTURRET, near=r.position)
                            if await self.can_cast(r(RAVENBUILD_AUTOTURRET, p)):
                                await self.do(r(RAVENBUILD_AUTOTURRET, r.position))"""
            elif e.exists:
                ea = e.closest_to(r.position)
                p = ea.position.towards(r.position, 13)
                await self.do(r.move(p))
            else:
                a = self.units(MARINE) | self.units(MARAUDER) | self.units(SIEGETANK) | self.units(SIEGETANKSIEGED)
                if a.exists:
                    p = a.furthest_to(self.start_location).position.towards(self.start_location, 2)
                    await self.do(r.move(p))

    async def GEReaperProximity(self):
        for r in self.units(REAPER):
            threat = self.known_enemy_units.closer_than(10, r.position).not_structure.not_flying
            if threat.exists:
                death = threat.closest_to(r.position)
                p = death.position.towards(r.position, 3)
                if p.distance_to(r.position) < 5:
                    if await self.can_cast(r, KD8CHARGE_KD8CHARGE, p):
                        await self.do(r(KD8CHARGE_KD8CHARGE, p))
                        print("GRENADE")
                        print(p)
                        await self.chat_send("GRENADE!!!")
                if r.health_percentage > 5 / 7 and r.weapon_cooldown == 0:
                    await self.do(r.attack(death))

                if death.position.distance_to(r.position) < 5 and not (r.is_attacking or r.is_moving):
                    nodeath = r.position.towards(death.position, -1)
                    await self.do(r.move(nodeath))

                if r.health_percentage < 3 / 7:
                    nodeath = r.position.towards(death.position, -4)
                    await self.do(r.move(nodeath))

    async def GMSiegeTankFollow(self, distance):
        s = self.units(SIEGETANK).idle
        m = self.units(MARINE) | self.units(MARAUDER)
        e = self.known_enemy_units.not_flying
        for s1 in s:
            if m.exists and e.exists:
                mp = m.closest_to(e.closest_to(s1.position).position).position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))
                await self.do(s1.attack(mp))

    async def GMReaperScout(self):
        for r in self.units(REAPER).idle:
            m = self.state.mineral_field.closer_than((self.supply_used*4), self.start_location).random.position
            await self.do(r.attack(m))
            print("SCOUT")
            await self.chat_send("LOOKING FOR ENIMIES!!!")

    async def GEReaperScout(self):
        i = len(self.enemy_start_locations)
        j = random.randint(0, i-1)
        self.target = self.enemy_start_locations[j]
        if self.known_enemy_structures.exists:
            self.target = self.known_enemy_structures.random.position
        m = self.state.mineral_field.closer_than(20, self.target)
        if m.exists:
            self.target = m.random.position
        for r in self.units(REAPER).idle:
            print("Moving")
            print(self.target)
            await self.chat_send("Killing Workers")
            await self.do(r.move(self.target))

    async def GMRally(self):
        building = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED) | self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        if self.known_enemy_structures.exists and building.exists:
            self.RallyPoint = building.closest_to(self.known_enemy_structures.random.position).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        for a in self.units.idle.not_structure.not_flying.exclude_type(HELLION):
            if a.distance_to(self.RallyPoint) > 15:
                await self.do(a.attack(self.RallyPoint))

    async def GMRallyAlternateMarineMarauder(self):  # allows follow tactics
        building = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED) | self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        if self.known_enemy_structures.exists and building.exists:
            self.RallyPoint = building.closest_to(self.known_enemy_structures.random.position).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        alternate = self.units(MARINE).idle | self.units(MARAUDER).idle
        for a in alternate:
            if a.distance_to(self.RallyPoint) > 30:
                await self.do(a.attack(self.RallyPoint))

    async def GMDefend(self):
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        for c in cc:
            threat = self.known_enemy_units.closer_than(25, c.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE).exclude_type(OVERSEER).exclude_type(SCV).exclude_type(DRONE).exclude_type(PROBE)
            if threat.exists:
                army = self.units.exclude_type(SCV).exclude_type(RAVEN).exclude_type(MEDIVAC).not_structure.closer_than(40, c.position)
                # improve code to include scv attacks
                p = threat.random.position
                for a in army:
                    await self.do(a.attack(p))
                await self.chat_send("Threat Detected")

    async def GEEarlyDefend(self):

        threat = self.known_enemy_units.closer_than(10, self.start_location)
        if threat.exists:
            army = self.units.not_structure
            for a in army:
                await self.do(a.attack(threat.random))
                print("*Not Safe*")
                await self.chat_send("GO AWAY")

    async def GEUnfinshedBuildingCheck(self):
        if self.units(SCV).exists:
            for a in self.units.structure.not_ready.exclude_type(REACTOR).exclude_type(BARRACKSREACTOR).exclude_type(FACTORYREACTOR).exclude_type(STARPORTREACTOR).exclude_type(TECHLAB).exclude_type(BARRACKSTECHLAB).exclude_type(FACTORYTECHLAB).exclude_type(STARPORTTECHLAB):

                #print (a.position) # code no work # modified version
                scvclose = self.units(SCV).closer_than(4, a.position)
                buildingcheck = False
                # for s in scvclose: # code no work
                    #print(s.is_constructing_scv)
                    #if s.is_constructing_scv:
                     #   buildingcheck = True
                #if not buildingcheck:
                    #scvfar = self.units(SCV).closest_to(a.position)
                    #await self.do(scvfar(BUILD, a))
                e = self.known_enemy_units.closer_than(6, a.position)
                if a.health_percentage < .3 and e.amount > a.health_percentage * 10:
                    await self.do(a(CANCEL_BUILDINPROGRESS))
                if not scvclose.exists:
                    await self.do(a(CANCEL_BUILDINPROGRESS))

    async def GMLandIdleBuildings(self): # This needs to be reworked
        b = self.units(BARRACKSFLYING).idle
        f = self.units(FACTORYFLYING).idle
        s = self.units(STARPORTFLYING).idle
        if b.exists and self.supply_used < 200:
            if not self.units(BARRACKSTECHLAB).exists and not self.units(TECHLAB).exists:
                b1 = b.random
                p = b1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                await self.do(b1.move(p))
                if self.can_afford(BARRACKSTECHLAB) and self.can_afford(BARRACKS):
                    p = await self.find_placement(BARRACKS, near=b1.position)
                    await self.do(b1.build(BARRACKSTECHLAB, p))
                    print("LAND B_TECHLAB")
            elif not self.units(REACTOR).exists:
                for b2 in b:
                    p = b2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    await self.do(b2.move(p))
                    if self.can_afford(BARRACKSREACTOR) and self.can_afford(BARRACKS):
                        p = await self.find_placement(BARRACKS, near=b2.position)
                        await self.do(b2.build(BARRACKSREACTOR, p))
                        print("LAND B_TECHLAB")

        if f.exists and self.supply_used < 200:
            if not self.units(TECHLAB).exists:  # Zerg does not gain replacement reactors intentionally
                for f2 in f:
                    p = f2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    await self.do(f2.move(p))
                    if self.can_afford(FACTORY):
                        p = await self.find_placement(FACTORY, near=f2.position)
                        await self.do(f2.build(FACTORYTECHLAB, p))
                        print("LAND F_TECHLAB")

        if s.exists and self.supply_used < 200:
            if not self.units(STARPORTREACTOR).exists and not self.units(REACTOR).exists:
                s1 = s.random
                p = s1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                await self.do(s1.move(p))
                if self.can_afford(STARPORT):
                    p = await self.find_placement(STARPORT, near=s1.position)
                    await self.do(s1.build(STARPORTREACTOR, p))
                    print("LAND S_REACTORLAB")
            else:
                for s2 in s:
                    p = s2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    await self.do(s2.move(p))
                    if self.can_afford(STARPORT):
                        p = await self.find_placement(STARPORT, near=s2.position)
                        await self.do(s2.build(STARPORTTECHLAB, p))
                        print("LAND S_TECHLAB")

    async def GMLandCommandCenter(self):
        for cc in self.units(COMMANDCENTERFLYING).idle | self.units(ORBITALCOMMANDFLYING).idle:
            p = await self.get_next_expansion()
            print(p)
            if self.can_afford(COMMANDCENTER):
                p = await self.find_placement(COMMANDCENTER, near=p)
                print(p)
                await self.do(cc(LAND, p))
            else:
                await self.do(cc(MOVE, p))

    async def GMOrbitalScansAttack(self):
        o = self.units(ORBITALCOMMAND)
        if o.exists:
            oo = o.random
            a = self.units.not_structure.further_than(60, oo.position).exclude_type(SCV).exclude_type(REAPER)
            e = self.known_enemy_units
            if oo.energy > 50 and a.exists and e.exists:
                ap = a.furthest_to(oo.position).position.towards(e.closest_to(oo.position).position, 10)
                await self.do(oo(SCANNERSWEEP_SCAN, ap))
                e2 = self.known_enemy_units.closer_than(16, ap)
                if e2.exists:
                    e2p = e2.random.position
                    for aa in a.closer_than(25, ap):
                        await self.do(aa.attack(e2p))

    async def GMCommandCenter(self):
        cc = self.units(COMMANDCENTER)
        oc = self.units(ORBITALCOMMAND)
        for c in cc.noqueue:
            cc2 = cc.further_than(3, c.position).closer_than(12, c.position) | oc.further_than(3, c.position).closer_than(12, c.position)
            if cc2.exists:
                print("wait")
                # await self.do(c(LIFT))
            else:
                if self.can_afford(ORBITALCOMMAND) and cc.not_ready.exists:
                    print("CC_OC")
                    await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
                elif self.can_afford(SCV) and self.units(SCV).amount < (cc.amount*20) + (oc.amount*15) + 15 and self.units(SCV).amount < 70 and self.units(SCV).closer_than(20, c).amount < 24 and self.supply_left > 0:
                    await self.do(c.train(SCV))
                    # coded this way to deal with a bug with expandnow()

    async def GMOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        for o in oc.ready.noqueue:
            scv = self.units(SCV).closer_than(10, o)
            m = self.state.mineral_field.closer_than(15, o)
            if not scv.exists and not m.exists:
                await self.do(o(LIFT))
            if self.can_afford(SCV) and self.units(SCV).amount < 50:
                await self.do(o.train(SCV))
        for o in oc.ready:
            if o.energy >= 120:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    await self.do(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")
            elif o.energy > 100 and self.known_enemy_structures.amount == 0:
                await self.do(o(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))  # can be improved with random
                await self.do(o(SCANNERSWEEP_SCAN, self.state.mineral_field.random.position))
                print("SCAN SEARCH")
            elif o.energy == 200:
                a = self.units.not_structure
                if a.exists:
                    aa = a.furthest_to(o.position).position
                    await self.do(o(SCANNERSWEEP_SCAN, aa.offset((random.randint(-5, 5), random.randint(-5, 5)))))

    async def GEOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        for o in oc.ready.noqueue:
            if self.can_afford(SCV) and self.units(SCV).amount < 50:
                await self.do(o.train(SCV))
        for o in oc.ready:
            if o.energy >= 50:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    await self.do(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")

    async def GEInBaseCommandCenter(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND).ready #  not flying
        if cc.amount > 1:
            cc1 = cc.closest_to(self.start_location)
            cc2 = cc.further_than(2, cc1.position).closer_than(12, cc1.position)
            for c in cc2.idle:
                await self.do(c(LIFT))

    async def GMManageSupply(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND)
        s = self.units(SCV)
        if cc.exists and s.exists and self.supply_used + self.supply_left < 200:
            if self.supply_left < self.supply_used/16 + 4 and not self.already_pending(SUPPLYDEPOT) and self.can_afford(SUPPLYDEPOT):
                sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
                if sd.exists:
                    await self.build(SUPPLYDEPOT, near=sd.random)
                    print("SUPPLYDEPOT")
                    if self.can_afford(SUPPLYDEPOT):
                        await self.build(SUPPLYDEPOT, near=sd.random)
                        print("SUPPLYDEPOT")
                else:
                    await self.build(SUPPLYDEPOT, near=cc.random)
                    print("CC_SUPPLYDEPOT")
                    if self.can_afford(SUPPLYDEPOT):
                        await self.build(SUPPLYDEPOT, near=cc.random)
                        print("CC_SUPPLYDEPOT")
            elif self.supply_left < 0 and self.can_afford(SUPPLYDEPOT):
                await self.build(SUPPLYDEPOT, near=cc.random)
                """most code here is untested"""

    async def GMAddonAbductBuilding(self):
        b = self.units(BARRACKSFLYING)
        f = self.units(FACTORYFLYING)
        s = self.units(STARPORTFLYING)
        a = b|f|s
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if t.exists and a.exists:
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

    async def GMRefineryBuild(self):
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

    async def GERefineryBuild(self):
        for cc in self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND):
            v = self.state.vespene_geyser.closer_than(15.0, cc)
            for ve in v:
                if self.can_afford(REFINERY) and not self.already_pending(REFINERY):
                    """ 
                    Observation: The code was learned from  the youtube tutorial. It is not optimally coded.
                    It in theory, only allows one refinery construction at a time. Loop -> Loop -> Check
                    If the check was done before the loop, there wouldn't be needless cycles.
                    Code left unchanged because of time constraint and not wanting to break the project.
                    ^^^
                    Observation: My previous observation is technically correct but any performance drop created by it
                    is marginal. It doesn't bog down real time False or real time True.
                    """
                    if not self.units(REFINERY).closer_than(1, ve).exists:
                        worker = self.select_build_worker(ve.position)
                        if worker is None:
                            break
                        await self.do(worker.build(REFINERY, ve))
                        print("REFINERY")

    async def GMEngineeringBay(self):
        for e in self.units(ENGINEERINGBAY).ready.idle.noqueue:
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

    async def GMArmoryGround(self):
        for a in self.units(ARMORY).ready.idle.noqueue:
            if await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1):
                await self.do(a(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2):
                await self.do(a(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3):
                await self.do(a(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1):
                await self.do(a(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2):
                await self.do(a(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3):
                await self.do(a(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3))

    async def GMBTechlab(self):
        bt = self.units(BARRACKSTECHLAB).ready.noqueue
        if bt.exists:
            bt1 = bt.first
            if await self.can_cast(bt1, RESEARCH_COMBATSHIELD) and self.can_afford(RESEARCH_COMBATSHIELD):
                await self.do(bt1(RESEARCH_COMBATSHIELD))
                print("UPGRADE_SHIELD")
            elif await self.can_cast(bt1, BARRACKSTECHLABRESEARCH_STIMPACK) and self.can_afford(BARRACKSTECHLABRESEARCH_STIMPACK):
                await self.do(bt1(BARRACKSTECHLABRESEARCH_STIMPACK))
                print("UPGRADE_STIMPACK")

    async def GMBarracks(self):
        for b in self.units(BARRACKS).ready.noqueue:
            if b.add_on_tag == 0:
                await self.do(b(LIFT))
                print("FLY!!!")
            elif self.units(BARRACKSTECHLAB).exists and self.supply_left > 1:
                id = self.units(BARRACKSTECHLAB).random.tag
                if b.add_on_tag == id:
                    if self.can_afford(MARAUDER) and self.supply_left > 1:
                        await self.do(b.train(MARAUDER))

                elif self.supply_left > 1:
                    if self.can_afford(REAPER) and not self.units(REAPER).exists and self.units(MARINE).amount >= 10 and self.known_enemy_structures.amount < 3:
                        await self.do(b.train(REAPER))
                        if self.can_afford(REAPER):
                            await self.do(b.train(REAPER))
                    elif self.can_afford(MARINE):
                        await self.do(b.train(MARINE))
                        if self.can_afford(MARINE):
                            await self.do(b.train(MARINE))

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

    async def GEBarracks(self):
        for b in self.units(BARRACKS).ready.noqueue:
            if self.units(BARRACKSREACTOR).exists and self.supply_used < 198:
                id = self.units(BARRACKSREACTOR).random.tag
                if b.add_on_tag == id:
                    if self.can_afford(REAPER) and not self.units(REAPER).exists and self.units(MARINE).amount >= 10:
                        await self.do(b.train(REAPER))
                        if self.can_afford(REAPER):
                            await self.do(b.train(REAPER))
                    else:
                        if self.can_afford(MARINE):
                            await self.do(b.train(MARINE))
                        if self.can_afford(MARINE):
                            await self.do(b.train(MARINE))
                elif b.add_on_tag == 0:
                    if self.can_afford(BARRACKSTECHLAB):
                        await self.do(b.build(BARRACKSTECHLAB))
                        print("B_TECHLAB")
                else:
                    if self.can_afford(MARAUDER):
                        await self.do(b.train(MARAUDER))
            elif self.can_afford(REAPER):
                await self.do(b.build(BARRACKSREACTOR))
                print("B_REACTOR")

    async def GMFactory(self):
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
            elif self.units(FACTORYREACTOR).exists:
                await self.do(f(LIFT))
                print("FLY!!!")

    async def GEFactory(self):
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

    async def GMStarport(self):
        for s in self.units(STARPORT).ready.noqueue:
            if s.add_on_tag == 0:
                await self.do(s(LIFT))

            elif self.units(STARPORTREACTOR).exists:
                id = self.units(STARPORTREACTOR).random.tag
                if s.add_on_tag == id and self.supply_left > 4:
                    if self.can_afford(MEDIVAC) and self.units(MEDIVAC).amount < 8:
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

    async def GEsupplydepotdown(self):
        for sd in self.units(SUPPLYDEPOT).ready:
            e = self.known_enemy_units.closer_than(8, sd.position).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                await self.do(sd(MORPH_SUPPLYDEPOT_LOWER))

    async def GEsupplydepotup(self):
        for sd in self.units(SUPPLYDEPOTLOWERED).ready:
            e = self.known_enemy_units.closer_than(10, sd.position).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            a = self.units.not_structure.not_flying.closer_than(3, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists and not a.exists:
                await self.do(sd(MORPH_SUPPLYDEPOT_RAISE))

    """Methods: RANDOM"""
    async def REBuildOrder(self):
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
                        await self.do(c.train(SCV))

            if scv.exists and not sd.exists and not self.already_pending(SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(SUPPLYDEPOT):

                    print("Build: AntiRandom")
                    if x < xd:
                        print("x<xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-1.5, .5))
                            print("y<yd")
                            # pass: 3 supply depot 2 racks # 2+ success
                            # shape is ugly but it is functional and is a full wall off
                            print("NE DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((1.5, 1.5))
                            # pass: 3 supply depot 2 racks
                            print("y>yd")
                            print("SE DOWN RAMP")
                    else:
                        print("x>xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-.5, -2.5))
                            # pass: 3 supply depot 2 racks
                            print("y<yd")
                            print("NW DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((2.5, -1.5))
                            # pass: 3 supply depot 2 racks # 2+
                            print("y>yd")
                            print("SW DOWN RAMP")
                    await self.do(s.build(SUPPLYDEPOT, p))
                    print("SUPPLY DEPOT1")

            elif sd.exists and self.can_afford(REFINERY) and not self.units(REFINERY).exists and not self.already_pending(REFINERY):
                await self.GERefineryBuild()
                print("gas")
            elif sd.ready.exists and scv.exists and self.units(REFINERY).exists:
                if not b.exists and not self.already_pending(BARRACKS):
                    if self.can_afford(BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        if x < xd:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((-1.5, -2.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((-3.5, .5))
                                print(p)
                        else:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((2.5, -.5))
                                print (p)
                            else:
                                p = self.main_base_ramp.top_center.offset((1.5, .5))
                        await self.build(BARRACKS, p)
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(REFINERY) and self.units(REFINERY).amount < 2 and not self.already_pending(REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(COMMANDCENTER):
                        await self.expand_now()
                        print("EXPAND")
                    elif oc.exists or self.already_pending(ORBITALCOMMAND) or self.units(BARRACKSREACTOR).exists:
                        if sd.amount == 1 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                            if x < xd:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-3.5, .5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-1.5, -1.5))

                            else:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-.5, -4.5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-.5, 1.5))

                            await self.build(SUPPLYDEPOT, p)
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
                                if x < xd:
                                    if y < yd:
                                        p = b.first.position.offset((0.5, -3.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-2.5, 4.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -3.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((1.5, 3.5))
                                print("BARRACKS2")
                                await self.build(BARRACKS, p)
                        elif self.units(BARRACKS).amount > 1 and sd.amount < 3:
                            if self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((4.5, -1.5))

                                await self.build(SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")

    async def REBarracks(self):
        for b in self.units(BARRACKS).ready.noqueue:
            if self.units(BARRACKSREACTOR).exists:
                if b.add_on_tag == 0:
                    if self.can_afford(MARINE):
                        await self.do(b.train(MARINE))
                elif self.supply_left > 1:
                        if self.can_afford(REAPER) and self.units(REAPER).amount < 2:
                            await self.do(b.train(REAPER))
                            if self.can_afford(REAPER):
                                await self.do(b.train(REAPER))
                            elif self.can_afford(MARINE):
                                await self.do(b.train(MARINE))
                        else:
                            if self.can_afford(MARINE):
                                await self.do(b.train(MARINE))
                            if self.can_afford(MARINE):
                                await self.do(b.train(MARINE))
            else:
                if self.can_afford(BARRACKSREACTOR):
                    await self.do(b.build(BARRACKSREACTOR))
                elif self.can_afford(MARINE):
                    await self.do(b.train(MARINE))

    async def RECheckEnemy(self):
        e = self.known_enemy_units
        if e.exists:
            ea = e.random
            if ea.race == Race.Terran:
                await self.chat_send("ENEMY TERRAN DETECTED")
                print("change to terran")
                self.STRAT = "AntiTerran"
            elif ea.race == Race.Zerg:
                await self.chat_send("ZERG DETECTED")
                print("change to zerg")
                self.STRAT = "AntiZerg"
            elif ea.race == Race.Protoss:
                await self.chat_send("PROTOSS DETECTED")
                print("change to protoss")
                self.STRAT = "AntiProtoss"

    """Methods: TERRAN"""
    async def TMAttackInitiation(self, minwave, bubblesize):
        # Note: Poor letter choosing for variables is because I was too lazy to write a method twice and this mostly copy pasted from the AntiZerg equivelant method.
        M1 = self.units(MARINE)
        M2 = self.units(MARAUDER)
        S = self.units(SIEGETANK)
        A = M1 | M2 | S
        if self.known_enemy_units.exclude_type(SCV).exists:
            p = self.known_enemy_units.exclude_type(SCV).closest_to(self.start_location).position
            if self.supply_used > 190:
                print("Supply Attack")
                await self.chat_send("--------------------")
                await self.chat_send("ENEMY TERRAN SPOTTED")
                await self.chat_send("--------------------")
                await self.chat_send(" ")
                for m in A:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        await self.do(m.attack(p))
        else:
            if self.supply_used > 190:
                for m in A.idle:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        p = self.enemy_start_locations[0]  # p should be usually overwritten but it is intended to be an uncommon method
                        i = self.state.mineral_field
                        if i.exists:
                            p = i.random.position
                        await self.do(m.attack(p))  # speaking of uncommon, this is untested
                        print("IDK")
                        await self.chat_send(":(")

    async def TEBuildOrder(self): # code copy pasted from zerg build order
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        oc = self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)

        if cc.ready.exists or oc.ready.exists:
            cci = cc.ready.noqueue | oc.ready.noqueue
            if cc.ready.noqueue.exists and self.can_afford(ORBITALCOMMAND) and b.ready.exists:
                c = cc.noqueue.ready.random
                await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
            """elif cci.exists and self.can_afford(SCV):
                for c in cci:
                    if self.can_afford(SCV):
                        await self.do(c.train(SCV))"""

            if scv.exists and not sd.exists and not self.already_pending(SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: AntiTerran")
                    if x < xd:
                        print("x<xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-1.5, .5))
                            print("y<yd")
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Functional but extremely boring. Most units won't spawn on slow side and rally fixes
                            print("NE DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((1.5, 1.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Too functional. Not enough obstacles to obstruct my forces.
                            print("y>yd")
                            print("SE DOWN RAMP")
                    else:
                        print("x>xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-.5, -2.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Two rax wall is kinda sketch but it looks cool.
                            print("y<yd")
                            print("NW DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((2.5, -1.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: There is a small gap. Marines can escape it and siege tanks can't fit or spawn in it
                            print("y>yd")
                            print("SW DOWN RAMP")
                    await self.do(s.build(SUPPLYDEPOT, p))
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(BARRACKS):
                    if self.can_afford(BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        if x < xd:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((-1.5, -2.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((-3.5, .5))
                        else:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((2.5, -.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((1.5, .5))
                        await self.build(BARRACKS, p)
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(REFINERY) and self.units(REFINERY).amount < 2 and not self.already_pending(
                            REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(COMMANDCENTER):
                        #  await self.expand_now() # code changed to accommodate getting killed early by common enemy push
                        await self.build(COMMANDCENTER, near=self.start_location)
                        print("New CC")
                    else:
                        if sd.amount == 1 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                            if x < xd:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-3.5, .5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-1.5, -1.5))

                            else:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-.5, -4.5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-.5, 1.5))

                            await self.build(SUPPLYDEPOT, p)
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-1.5, -5.5))

                                    else:
                                        p = self.main_base_ramp.top_center.offset((-2.5, 4.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -3.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((1.5, 3.5))
                                print("BARRACKS2")
                                await self.build(BARRACKS, p)
                        elif (self.units(BARRACKS).amount > 1 and oc.exists) or self.supply_left <= 2:
                            if sd.amount < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((4.5, -1.5))
                                await self.build(SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")
                            elif self.can_afford(FACTORY) and self.units(FACTORY).amount < 1 and not self.already_pending(FACTORY):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-1.5, -8.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-9.5, .5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((6.5, .5))
                                await self.build(FACTORY, p)
                                print("FACTORY")

    async def TECommandCenter(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND)
        ccflying = self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        for c in cc.noqueue:
            m = self.state.mineral_field
            minnear = m.closer_than(15, c.position)
            cc2 = cc.further_than(3, c.position).closer_than(15, c.position)
            if not self.units(SCV).exists and not minnear.exists and not ccflying.exists:
                await self.do(c(LIFT))
                p = await self.get_next_expansion()
                if m.exists:
                    m1 = m.closest_to(p).position
                    print(p)
                    print(m1)
                    p2 = m1.towards(p, 5)
                    print(p2)
                    self.nextXpansionLocation = p2
            elif cc2.exists:
                print("wait")
        for c in cc(COMMANDCENTER):
            if self.units(BARRACKS).ready.exists:
                if self.can_afford(ORBITALCOMMAND):
                    print("CC_OC")
                    await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
                elif self.can_afford(SCV) and self.units(SCV).amount < (cc.amount*20) + 10 and self.units(SCV).amount < 70 and self.units(SCV).closer_than(20, c).amount < 24 and self.supply_left > 0:
                    await self.do(c.train(SCV))
                    # coded this way to deal with a bug with expandnow()

    async def TEOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        flyingcc = self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        for o in oc.ready.noqueue:
            scv = self.units(SCV).closer_than(10, o)
            m = self.state.mineral_field.closer_than(15, o)
            if not scv.exists and not m.exists and not flyingcc.exists:
                await self.do(o(LIFT))
                p = await self.get_next_expansion()
                m = self.state.mineral_field
                if m.exists:
                    m1 = m.closest_to(p).position
                    print(p)
                    print(m1)
                    p2 = m1.towards(p, 5)
                    print(p2)
                    self.nextXpansionLocation = p2
            if self.can_afford(SCV) and self.units(SCV).amount < 65 and self.units(SCV).closer_than(20, o.position).amount < 24:
                await self.do(o.train(SCV))
        for o in oc.ready:
            if o.energy == 200:
                a = self.units.not_structure
                if a.exists:
                    aa = a.furthest_to(o.position).position
                    await self.do(o(SCANNERSWEEP_SCAN, aa.offset((random.randint(-5, 5), random.randint(-5, 5)))))
            elif o.energy > 100 and self.known_enemy_structures.amount == 0:
                await self.do(o(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))  # can be improved with random
                await self.do(o(SCANNERSWEEP_SCAN, self.state.mineral_field.random.position))
                print("SCAN SEARCH")
            elif o.energy >= 50:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 6:
                    await self.do(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")

    async def TELandCommandCenter(self):
        for cc in self.units(COMMANDCENTERFLYING).idle | self.units(ORBITALCOMMANDFLYING).idle:
            #p = await self.get_next_expansion()
            print(await self.get_next_expansion())
            p = self.nextXpansionLocation
            print(p)
            """if await self.can_cast(cc(LAND, self.nextXpansionLocation)):
                p = self.nextXpansionLocation
                await self.do(cc(LAND, p))
            else:
                await self.do(cc(MOVE, p))"""
            p = self.nextXpansionLocation
            await self.do(cc(MOVE, p))
            await self.do(cc(LAND, p))
            p = self.nextXpansionLocation
            m = self.state.mineral_field
            if m.exists:
                m1 = m.closest_to(p).position
                print(p)
                print(m1)
                p2 = p.towards(m1, -.5)
                print(p2)
                self.nextXpansionLocation = p2
                e = self.known_enemy_units.closer_than(15, self.nextXpansionLocation)
                if e.exists:
                    self.nextXpansionLocation = await self.get_next_expansion()
                    p3 = cc.position.towards(e.random.position, -1)
                    await self.do(cc.move(p3))

    async def TEInBaseCommandCenter(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND) #  not flying
        ccflying = self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        if cc.amount > 1:
            cc1 = cc.closest_to(self.start_location)
            cc2 = cc.further_than(2, cc1.position).closer_than(15, cc1.position)
            for c in cc2.idle: # only happens if a cc2 exists*
                await self.do(c(LIFT))
                p = await self.get_next_expansion()
                m = self.state.mineral_field
                if m.exists:
                    m1 = m.closest_to(p).position
                    print(p)
                    print(m1)
                    p2 = m1.towards(p, 5)
                    print(p2)
                    self.nextXpansionLocation = p2

    async def TMAddonAbductBuilding(self):
        b = self.units(BARRACKSFLYING)
        f = self.units(FACTORYFLYING)
        s = self.units(STARPORTFLYING)
        a = b|f|s
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if t.exists and (f.exists or s.exists):
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f | s
            af = a2.first
            p = t.first.add_on_land_position
            await self.do(af(LAND, p))

        elif r.exists and b.exists:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            bf = b.first
            await self.do(bf(LAND, p))

        elif s.exists and r.exists and not self.units(STARPORTREACTOR).exists:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            sf = s.first
            await self.do(sf(LAND, p))

        elif b.exists and t.exists and not self.units(BARRACKSTECHLAB).exists:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            bf = b.first
            await self.do(bf(LAND, p))

    async def TMStarport(self):
        for s in self.units(STARPORT).ready.noqueue:
            if s.add_on_tag == 0:
                await self.do(s(LIFT))

            elif self.units(STARPORTREACTOR).exists:
                id = self.units(STARPORTREACTOR).random.tag
                if s.add_on_tag == id and self.supply_left > 4:
                    if self.can_afford(MEDIVAC) and self.units(MEDIVAC).amount < 8:
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

    async def TMReplaceExpand(self):
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND) | self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        oc = self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        f = self.units(FACTORY) | self.units(FACTORYFLYING)
        s = self.units(STARPORT) | self.units(STARPORTFLYING)
        e = self.units(ENGINEERINGBAY)
        a = b.flying | f.flying | s.flying
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if sd.ready.exists and cc.exists and not b.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

        if b.ready.exists and cc.exists and f.amount < 2 and not self.already_pending(FACTORY) and self.can_afford(FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(FACTORY, near=p)

        if f.ready.exists and cc.exists and not s.exists and not self.already_pending(STARPORT) and self.can_afford(STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(STARPORT, near=p)

        if not e.exists and cc.exists and not self.already_pending(ENGINEERINGBAY) and self.can_afford(ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(ENGINEERINGBAY, near=p)

        if f.ready.exists and cc.exists and not self.units(ARMORY).exists and not self.already_pending(ARMORY) and self.can_afford(ARMORY):
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(ARMORY, near=p)

        if b.amount == 1 and cc.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

        if self.minerals > 200 + (cc.amount * 200) and self.can_afford(COMMANDCENTER) and not cc.flying.exists and cc.amount < 5 and not self.already_pending(COMMANDCENTER):
            print("expand")
            #  await self.expand_now()
            p = self.start_location
            await self.build(COMMANDCENTER, near=p)

        if oc.amount > 1:
            if s.amount == 1 and cc.exists and not self.already_pending(STARPORT) and cc.amount > 2 and self.can_afford(STARPORT):
                print("NOT ENOUGH STARPORT")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(STARPORT, near=p)

        if b.amount < oc.amount * 2 and cc.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

    """Methods: ZERG"""
    async def ZMAttackInitiation(self, minwave, bubblesize):
        M1 = self.units(MARINE)
        M2 = self.units(MARAUDER)
        S = self.units(SIEGETANK) | self.units(SIEGETANKSIEGED)
        H = self.units(HELLION) | self.units(HELLIONTANK)
        A = M1 | M2 | S | H
        if self.known_enemy_structures.exists:
            p = self.known_enemy_structures.closest_to(self.start_location).position
            if self.time > 500 and self.time < 600 and A.amount > 30:
                MM = M1 | M2 | S.exclude_type(SIEGETANKSIEGED)
                print("First Attack")
                await self.chat_send("Medivac Drop Incoming")
                for m in MM:
                    if MM.closer_than(bubblesize, m.position).amount >= minwave:
                        await self.do(m.attack(p))
            elif self.supply_used > 190:
                MM = M1 | M2 | S.exclude_type(SIEGETANKSIEGED)
                print("Supply Attack")
                await self.chat_send("gg")
                for m in MM:
                    if MM.closer_than(bubblesize, m.position).amount >= minwave:
                        await self.do(m.attack(p))
        else:
            if self.supply_used > 190:
                MM = M1 | M2 | S.exclude_type(SIEGETANKSIEGED)
                for m in MM:
                    if MM.closer_than(bubblesize, m.position).amount >= minwave:
                        p = self.enemy_start_locations[0]  # code can be improved with random number but uncommon
                        await self.do(m.attack(p))  # speaking of uncommon, this is untested
                        print("IDK")

    async def ZMHellionFollow(self, distance):
        h = self.units(HELLION).idle
        m = self.units(MARINE) | self.units(MARAUDER)
        e = self.known_enemy_units.not_flying
        for h1 in h:
            if m.exists and e.exists:
                mp = m.closest_to(e.closest_to(h1.position).position).position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))
                await self.do(h1.attack(mp))

    async def ZMHellionProximity(self, proximity):
        if self.units(ARMORY).ready.exists:
            for h in self.units(HELLION):
                if self.known_enemy_units.closer_than(proximity, h.position).not_structure.not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE).exists:
                    await self.do(h(MORPH_HELLBAT))
                    print("MORPH HELLBAT")

    async def ZMHellbatProximity(self, proximity):
        if self.units(ARMORY).ready.exists:
            for h in self.units(HELLIONTANK):
                death = self.known_enemy_units.closer_than(proximity, h.position).not_structure.not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
                if death.exists:
                    await self.do(h.attack(death.random.position))
                    print("BURN")
                else:
                    await self.do(h(MORPH_HELLION))
                    print("MORPH HELLBAT")

    async def ZMLurkerCheck(self):
        o = self.units(ORBITALCOMMAND)
        l = self.known_enemy_units(LURKERMP) | self.known_enemy_units(LURKERMPBURROWED)
        if o.exists and l.exists:
            oo = o.random
            ll = l.random
            if oo.energy > 50:
                ap = ll.position
                await self.do(oo(SCANNERSWEEP_SCAN, ap))

    async def ZEBuildOrder(self):
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
                        await self.do(c.train(SCV))

            if scv.exists and not sd.exists and not self.already_pending(SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: AntiZerg")
                    if x < xd:
                        print("x<xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-1.5, .5))
                            print("y<yd")
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Functional but extremely boring. Most units won't spawn on slow side and rally fixes
                            print("NE DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((1.5, 1.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Too functional. Not enough obstacles to obstruct my forces.
                            print("y>yd")
                            print("SE DOWN RAMP")
                    else:
                        print("x>xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-.5, -2.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Two rax wall is kinda sketch but it looks cool.
                            print("y<yd")
                            print("NW DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((2.5, -1.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: There is a small gap. Marines can escape it and siege tanks can't fit or spawn in it
                            print("y>yd")
                            print("SW DOWN RAMP")
                    await self.do(s.build(SUPPLYDEPOT, p))
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(BARRACKS):
                    if self.can_afford(BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        if x < xd:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((-1.5, -2.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((-3.5, .5))
                        else:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((2.5, -.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((1.5, .5))
                        await self.build(BARRACKS, p)
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(REFINERY) and self.units(REFINERY).amount < 2 and not self.already_pending(
                            REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(COMMANDCENTER):
                        await self.expand_now()
                        print("EXPAND")
                    elif oc.exists or self.already_pending(ORBITALCOMMAND) or self.units(BARRACKSREACTOR).exists:
                        if sd.amount == 1 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                            if x < xd:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-3.5, .5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-1.5, -1.5))

                            else:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-.5, -4.5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-.5, 1.5))

                            await self.build(SUPPLYDEPOT, p)
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-1.5, -5.5))

                                    else:
                                        p = self.main_base_ramp.top_center.offset((-2.5, 4.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -3.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((1.5, 3.5))
                                print("BARRACKS2")
                                await self.build(BARRACKS, p)
                        elif self.units(BARRACKS).amount > 1 and oc.exists:
                            if sd.amount < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((4.5, -1.5))
                                await self.build(SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")
                            elif self.can_afford(FACTORY) and self.units(FACTORY).amount < 1 and not self.already_pending(FACTORY):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-1.5, -8.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-9.5, .5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((6.5, .5))
                                await self.build(FACTORY, p)
                                print("FACTORY")

    async def ZEFactory(self):
        for f in self.units(FACTORY).ready.noqueue:
            if self.supply_left > 2:
                # only allow one reactor
                if f.add_on_tag == 0:
                    if self.can_afford(FACTORYREACTOR):
                        await self.do(f.build(FACTORYREACTOR))
                else:
                    if self.can_afford(HELLION):
                        await self.do(f.train(HELLION))
                    if self.can_afford(HELLION):
                        await self.do(f.train(HELLION))
            elif self.units(FACTORYREACTOR).exists:
                await self.do(f(LIFT))
                print("FLY!!!")

    async def ZMFactory(self):
        for f in self.units(FACTORY).ready.noqueue:
            if f.add_on_tag == 0:
                await self.do(f(LIFT))
                print("FLY!!!")
            elif self.units(SIEGETANK).closer_than(15, f.position).amount > 1 and self.time > 500 and self.time < 600:
                await self.do(f(LIFT))
            elif self.units(SIEGETANK).closer_than(25, f.position).amount > 2 and self.supply_left < 4 and self.time > 700:
                await self.do(f(LIFT))
            elif self.supply_used == 0:
                await self.do(f(LIFT))
            elif self.units(FACTORYREACTOR).exists and self.supply_left > 2:
                id = self.units(FACTORYREACTOR).random.tag
                if self.units(FACTORYREACTOR).amount > 1:
                    await self.do(f(LIFT))
                    print("FLY!!!")
                elif f.add_on_tag == id:
                    if self.can_afford(HELLION):
                        await self.do(f.train(HELLION))
                    if self.can_afford(HELLION):
                        await self.do(f.train(HELLION))
                else:
                    if self.can_afford(SIEGETANK):
                        await self.do(f.train(SIEGETANK))
            else:
                #add on exists no reactor(tech lab only possible)
                if self.can_afford(SIEGETANK):
                    await self.do(f.train(SIEGETANK))

    async def ZMAddonAbductBuilding(self):
        b = self.units(BARRACKSFLYING)
        f = self.units(FACTORYFLYING)
        s = self.units(STARPORTFLYING)
        a = b|f|s
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if t.exists and (f.exists or s.exists) and self.supply_used < 200:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f | s
            af = a2.first
            p = t.first.add_on_land_position
            await self.do(af(LAND, p))

        elif r.exists and b.exists and self.supply_used < 200:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            bf = b.first
            await self.do(bf(LAND, p))

        elif f.exists and r.exists and not self.units(FACTORYREACTOR).exists and self.supply_used < 200:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            ff = f.first
            await self.do(ff(LAND, p))

        elif s.exists and r.exists and not self.units(STARPORTREACTOR).exists and self.supply_used < 200:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            sf = s.first
            await self.do(sf(LAND, p))

        elif b.exists and t.exists and not self.units(BARRACKSTECHLAB).exists and self.supply_used < 200:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            bf = b.first
            await self.do(bf(LAND, p))

    async def ZMReplaceExpand(self):
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND) | self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        oc = self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        f = self.units(FACTORY) | self.units(FACTORYFLYING)
        s = self.units(STARPORT) | self.units(STARPORTFLYING)
        e = self.units(ENGINEERINGBAY)
        a = b.flying | f.flying | s.flying
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if sd.ready.exists and cc.exists and not b.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

        if b.ready.exists and cc.exists and f.amount < 2 and not self.already_pending(FACTORY) and self.can_afford(FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(FACTORY, near=p)

        if f.ready.exists and cc.exists and not s.exists and not self.already_pending(STARPORT) and self.can_afford(STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(STARPORT, near=p)

        if not e.exists and cc.exists and not self.already_pending(ENGINEERINGBAY) and self.can_afford(ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(ENGINEERINGBAY, near=p)

        if f.ready.exists and cc.exists and not self.units(ARMORY).exists and not self.already_pending(ARMORY) and self.can_afford(ARMORY):
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(ARMORY, near=p)

        if b.amount == 1 and cc.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

        if self.minerals > 200 + (cc.amount * 150):
            print("expand")
            await self.expand_now()

        if oc.amount > 1:
            if s.amount == 1 and cc.exists and not self.already_pending(STARPORT) and cc.amount > 2 and self.can_afford(STARPORT):
                print("NOT ENOUGH STARPORT")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(STARPORT, near=p)

        if b.amount < cc.amount and cc.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

    async def ZMFTechlab(self):
        ft = self.units(FACTORYTECHLAB).ready.noqueue
        h = self.units(HELLION) | self.units(HELLIONTANK)
        if ft.exists and h.exists:
            ft1 = ft.first
            if await self.can_cast(ft1, RESEARCH_INFERNALPREIGNITER) and self.can_afford(RESEARCH_INFERNALPREIGNITER):
                await self.do(ft1(RESEARCH_INFERNALPREIGNITER))
                print("UPGRADE_FIRE")
            elif await self.can_cast(ft1, RESEARCH_SMARTSERVOS) and self.can_afford(RESEARCH_SMARTSERVOS):
                await self.do(ft1(RESEARCH_SMARTSERVOS))
                print("UPGRADE_FIRE")

    """Methods: Protoss"""
    async def PMAttackInitiation(self, minwave, bubblesize):
        # Note: Poor letter choosing for variables is because I was too lazy to write a method twice and this mostly copy pasted from the AntiZerg equivelant method.
        M1 = self.units(MARINE)
        M2 = self.units(MARAUDER)
        S = self.units(SIEGETANK)
        A = M1 | M2 | S
        if self.known_enemy_units.exclude_type(SCV).exists:
            p = self.known_enemy_units.exclude_type(SCV).closest_to(self.start_location).position
            if self.supply_used > 190:
                print("Supply Attack")
                await self.chat_send("--------------------")
                await self.chat_send("PROTOSS MARKED FOR DELETION")
                await self.chat_send("--------------------")
                await self.chat_send(" ")
                for m in A:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        await self.do(m.attack(p))
        else:
            if self.supply_used > 190:
                for m in A.idle:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        p = self.enemy_start_locations[0]  # p should be usually overwritten but it is intended to be an uncommon method
                        i = self.state.mineral_field
                        if i.exists:
                            p = i.random.position
                        await self.do(m.attack(p))  # speaking of uncommon, this is untested
                        print("IDK")
                        await self.chat_send(":(")

    async def PEBuildOrder(self): # code copy pasted from terran build order
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        oc = self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)

        if cc.ready.exists or oc.ready.exists:
            cci = cc.ready.noqueue | oc.ready.noqueue
            if cc.ready.noqueue.exists and self.can_afford(ORBITALCOMMAND) and b.ready.exists:
                c = cc.noqueue.ready.random
                await self.do(c(UPGRADETOORBITAL_ORBITALCOMMAND))
            """elif cci.exists and self.can_afford(SCV):
                for c in cci:
                    if self.can_afford(SCV):
                        await self.do(c.train(SCV))"""

            if scv.exists and not sd.exists and not self.already_pending(SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: AntiProtoss")
                    if x < xd:
                        print("x<xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-1.5, .5))
                            print("y<yd")
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Functional but extremely boring. Most units won't spawn on slow side and rally fixes
                            print("NE DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((1.5, 1.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Too functional. Not enough obstacles to obstruct my forces.
                            print("y>yd")
                            print("SE DOWN RAMP")
                    else:
                        print("x>xd")
                        if y < yd:
                            p = self.main_base_ramp.top_center.offset((-.5, -2.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: Two rax wall is kinda sketch but it looks cool.
                            print("y<yd")
                            print("NW DOWN RAMP")
                        else:
                            p = self.main_base_ramp.top_center.offset((2.5, -1.5))
                            # pass: 3 supply depot 2 racks 1 factory
                            # note: There is a small gap. Marines can escape it and siege tanks can't fit or spawn in it
                            print("y>yd")
                            print("SW DOWN RAMP")
                    await self.do(s.build(SUPPLYDEPOT, p))
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(BARRACKS):
                    if self.can_afford(BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        if x < xd:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((-1.5, -2.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((-3.5, .5))
                        else:
                            if y < yd:
                                p = self.main_base_ramp.top_center.offset((2.5, -.5))
                            else:
                                p = self.main_base_ramp.top_center.offset((1.5, .5))
                        await self.build(BARRACKS, p)
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(REFINERY) and self.units(REFINERY).amount < 2 and not self.already_pending(
                            REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(COMMANDCENTER):
                        #  await self.expand_now() # code changed to accommodate getting killed early by common enemy push
                        await self.build(COMMANDCENTER, near=self.start_location)
                        print("New CC")
                    else:
                        if sd.amount == 1 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                            if x < xd:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-3.5, .5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-1.5, -1.5))

                            else:
                                if y < yd:
                                    p = self.main_base_ramp.top_center.offset((-.5, -4.5))

                                else:
                                    p = self.main_base_ramp.top_center.offset((-.5, 1.5))

                            await self.build(SUPPLYDEPOT, p)
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(BARRACKS) and not self.already_pending(BARRACKS):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-1.5, -5.5))

                                    else:
                                        p = self.main_base_ramp.top_center.offset((-2.5, 4.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -3.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((1.5, 3.5))
                                print("BARRACKS2")
                                await self.build(BARRACKS, p)
                        elif (self.units(BARRACKS).amount > 1 and oc.exists) or self.supply_left <= 2:
                            if sd.amount < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(SUPPLYDEPOT):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-3.5, -1.5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((4.5, -1.5))
                                await self.build(SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")
                            elif self.can_afford(FACTORY) and self.units(FACTORY).amount < 1 and not self.already_pending(FACTORY):
                                if x < xd:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((-1.5, -8.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((-9.5, .5))
                                else:
                                    if y < yd:
                                        p = self.main_base_ramp.top_center.offset((1.5, -6.5))
                                    else:
                                        p = self.main_base_ramp.top_center.offset((6.5, .5))
                                await self.build(FACTORY, p)
                                print("FACTORY")