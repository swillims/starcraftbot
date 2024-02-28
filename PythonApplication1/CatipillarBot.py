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
    async def on_start(self):
        self.Rally = None
        self.target = None
        # exists because the api maker decided to make it a set instead of list
        self.cornors = list(self.main_base_ramp.corner_depots) 
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
            #Early Game
            if True:# self.time <= 240:
                if iteration % 2 == 0:
                    await self.REBuildOrder()
                if iteration % 2 == 1:
                    await self.GEsupplydepotup()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 6 == 1:
                    await self.GEReaperScout()
                if iteration % 6 == 1:
                    await self.REBarracks()
                if iteration % 6 == 2:
                    await self.GEFactory()
                if iteration % 6 == 3:
                    await self.GEUnfinshedBuildingCheck()
                if iteration % 6 == 4:
                    await self.RECheckEnemy()
                if iteration % 6 == 5:
                    await self.GEOrbitalCommand()
                    await self.GEsupplydepotdown()
                #if iteration % 150 == 0:
                #    await self.GEEarlyDefend() # removed can't defend against unknown enemy

        elif self.STRAT == "AntiTerran":
            if self.time <= 240:
                if iteration % 2 == 0:
                    await self.TEBuildOrder()
                if iteration % 2 == 1:
                    await self.GEsupplydepotup()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 6 == 1:
                    await self.TEInBaseCommandCenter()
                    await self.TEOrbitalCommand()
                if iteration % 6 == 2:
                    await self.TECommandCenter()
                if iteration % 6 == 3:
                    await self.GEBarracks()
                if iteration % 6 == 4:
                    await self.GEReaperScout()
                    await self.GEReaperProximity()
                if iteration % 6 == 5:
                    await self.GEFactory()
                if iteration % 10 == 0:
                    await self.GEUnfinshedBuildingCheck()
                if iteration % 10 == 0:
                    await self.GEsupplydepotdown()
                if iteration % 10 == 1:
                    await self.TMAddonAbductBuilding()
                if iteration % 10 == 2:
                    await self.GEEarlyDefend()
                    
            elif self.time > 240 and True:
                if iteration % 4 == 0:
                    await self.GEsupplydepotup()
                    await self.distribute_workers()
                    await self.GMDefend()
                if iteration % 4 == 1:
                    await self.TEInBaseCommandCenter()
                if iteration % 4 == 2:
                    await self.GMFactory()
                    await self.GMBarracks()
                    await self.GMStarport()
                if iteration % 4 == 3:
                    await self.GMMarineProximity(10)
                    await self.GMMarauderProximity(10)
                    await self.GEReaperProximity()
                if iteration % 8 == 0:
                    await self.GMManageSupply()
                if iteration % 8 == 1:
                    await self.GEsupplydepotdown()
                if iteration % 8 == 2:
                    await self.GMRefineryBuild()
                if iteration % 8 == 3:
                    await self.GMSiegeTankProximity(16)
                if iteration % 8 == 4:
                    await self.TECommandCenter()
                    await self.TEOrbitalCommand()
                if iteration % 8 == 5:
                    await self.GMLandIdleBuildings()
                if iteration % 8 == 6:
                    await self.TMAddonAbductBuilding()
                if iteration % 8 == 7:
                    await self.GEUnfinshedBuildingCheck()
                    await self.TELandCommandCenter()
                if iteration % 16 == 1:
                    await self.GMReaperScout()
                if iteration % 16 == 6:
                    await self.TMReplaceExpand()
                if iteration % 16 == 11:
                    await self.GMSiegedTankProximity(20)
                    await self.GMMedivacProximity()
                    await self.GMRavenProximity()
                    await self.GMRefineryBuild()
                if iteration % 16 == 15:
                    await self.GMRally()
                    await self.TMAttackInitiation(20, 25)
                    await self.GMBTechlab()
                    await self.GMEngineeringBay()
                    await self.GMArmoryGround()

        elif self.STRAT == "AntiZerg":
            if self.time <= 240:
                if iteration % 2 == 0:
                    await self.ZEBuildOrder()
                if iteration % 2 == 1:
                    await self.GEsupplydepotup()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 6 == 1:
                    await self.GEOrbitalCommand()
                if iteration % 6 == 2:
                    await self.TECommandCenter() # old bot didn't have this probably covered by orbital command in build order
                if iteration % 6 == 3:
                    await self.GEBarracks()
                if iteration % 6 == 4:
                    await self.GEReaperScout()
                    await self.GEReaperProximity()
                if iteration % 6 == 5:
                    await self.ZEFactory()
                if iteration % 10 == 0:
                    await self.GEUnfinshedBuildingCheck()
                if iteration % 10 == 0:
                    await self.GEsupplydepotdown()
                #if iteration % 10 == 1:
                #    await self.TMAddonAbductBuilding() # old bot didn't have this    
                if iteration % 10 == 2:
                    await self.GEEarlyDefend()
                    
                    ### line
            if self.time > 240 and True:   # time for late game iteration may or may not be needed
                if iteration % 4 == 0:
                    await self.GEsupplydepotup()
                    await self.distribute_workers()
                    await self.GMDefend()
                if iteration % 4 == 1:
                    await self.GMMarineProximity(10)
                    await self.GMMarauderProximity(10)
                if iteration % 4 == 2:
                    await self.GMFactory()
                    await self.GMBarracks()
                    await self.GMStarport()
                if iteration % 4 == 3:
                    await self.ZMHellionProximity(10)
                    await self.GEReaperProximity()
                    await self.GMSiegeTankProximity(15)
                if iteration % 8 == 0:
                    await self.ZMLurkerCheck()
                if iteration % 8 == 1:
                    await self.GMCommandCenter()
                    await self.GMOrbitalCommand()
                if iteration % 8 == 2:
                    await self.ZMHellionFollow(10)
                    await self.GMReaperScout()
                    await self.GMSiegeTankFollow(3)
                if iteration % 8 == 3:
                    await self.ZMFactory()
                    await self.GMBarracks()
                    await self.GMStarport()
                if iteration % 8 == 4:
                    await self.GMLandIdleBuildings()  # it intentionally doesn't replace reactor for Factory # 2nd gen, I have no clue why I did this in first gen
                    await self.ZMFTechlab()
                    await self.GMBTechlab()
                    await self.GMEngineeringBay()
                    await self.GMArmoryGround()
                if iteration % 8 == 5:
                    await self.GMMedivacProximity()
                    await self.GMRavenProximity()
                    await self.GMManageSupply()
                if iteration % 8 == 6:
                    await self.GEUnfinshedBuildingCheck()
                    await self.GEsupplydepotdown()
                if iteration % 8 == 7:
                    await self.ZMAddonAbductBuilding()
                if iteration % 16 == 0:
                    await self.ZMAttackInitiation(10, 20)
                if iteration % 16 == 3:
                    await self.ZMHellbatProximity(14)
                    await self.GMLandCommandCenter()
                    await self.GMRefineryBuild()
                    await self.ZMReplaceExpand()
                if iteration % 16 == 6:
                    await self.GMSiegedTankProximity(16)
                    await self.GMDefend()
                    await self.GMOrbitalScansAttack()
                if iteration % 16 == 9:
                    #await self.GMRallyAlternateMarineMarauder()
                    await self.GMRally()

        elif self.STRAT == "AntiProtoss":

            if self.time <= 240:
                if iteration % 2 == 0:
                    await self.PEBuildOrder()
                if iteration % 2 == 1:
                    await self.GEsupplydepotup()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                if iteration % 6 == 1:
                    await self.TEInBaseCommandCenter()
                    await self.TEOrbitalCommand()
                if iteration % 6 == 2:
                    await self.TECommandCenter()
                if iteration % 6 == 3:
                    await self.GEBarracks()
                if iteration % 6 == 4:
                    await self.GEReaperScout()
                    await self.GEReaperProximity()
                if iteration % 6 == 5:
                    await self.GEFactory()
                if iteration % 10 == 0:
                    await self.GEUnfinshedBuildingCheck()
                if iteration % 10 == 0:
                    await self.GEsupplydepotdown()
                if iteration % 10 == 1:
                    await self.TMAddonAbductBuilding()
                if iteration % 10 == 2:
                    await self.GEEarlyDefend()
            elif self.time > 240 and True:
                if iteration % 4 == 0:
                    await self.GEsupplydepotup()
                    await self.distribute_workers()
                    await self.GMDefend()
                if iteration % 4 == 1:
                    await self.TEInBaseCommandCenter()
                if iteration % 4 == 2:
                    await self.GMFactory()
                    await self.GMBarracks()
                    await self.GMStarport()
                if iteration % 4 == 3:
                    await self.GMMarineProximity(10)
                    await self.GMMarauderProximity(10)
                    await self.GEReaperProximity()
                if iteration % 8 == 0:
                    await self.GMManageSupply()
                if iteration % 8 == 1:
                    await self.GEsupplydepotdown()
                if iteration % 8 == 2:
                    await self.GMRefineryBuild()
                if iteration % 8 == 3:
                    await self.GMSiegeTankProximity(16)
                if iteration % 8 == 4:
                    await self.TECommandCenter()
                    await self.TEOrbitalCommand()
                if iteration % 8 == 5:
                    await self.GMLandIdleBuildings()
                if iteration % 8 == 6:
                    await self.TMAddonAbductBuilding()
                if iteration % 8 == 7:
                    await self.GEUnfinshedBuildingCheck()
                    await self.TELandCommandCenter()
                if iteration % 16 == 1:
                    await self.GMReaperScout()
                if iteration % 16 == 6:
                    await self.TMReplaceExpand()
                if iteration % 16 == 11:
                    await self.GMSiegedTankProximity(20)
                    await self.GMMedivacProximity()
                    await self.GMRavenProximity()
                    await self.GMRefineryBuild()
                if iteration % 16 == 15:
                    await self.GMRally()
                    await self.PMAttackInitiation(30, 30)
                    await self.GMBTechlab()
                    await self.GMEngineeringBay()
                    await self.GMArmoryGround()

    #Methods: GENERAL
    async def GMMarineProximity(self, proximity):
        for m in self.units(UnitTypeId.MARINE):
            threat = self.enemy_units.closer_than(proximity, m.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists and m.health_percentage > 2/8:
                if await self.can_cast(m, AbilityId.EFFECT_STIM_MARINE) and m.health_percentage > 7/8:
                    m(AbilityId.EFFECT_STIM_MARINE)
                m.attack(threat.closest_to(m.position).position)
            elif threat.exists:
                e = threat.closest_to(m.position).position
                p = m.position.towards(e, -proximity)

    async def GMMarauderProximity(self, proximity):
        for m in self.units(UnitTypeId.MARAUDER):
            threat = self.enemy_units.not_flying.closer_than(proximity, m.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                if await self.can_cast(m, AbilityId.EFFECT_STIM_MARAUDER) and m.health_percentage > 9.5/10:
                    m(AbilityId.EFFECT_STIM_MARAUDER)
                m.attack(threat.closest_to(m.position).position)

    async def GMSiegeTankProximity(self, proximity):
        for s in self.units(UnitTypeId.SIEGETANK):
            threat = self.enemy_units.closer_than(proximity, s).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                s(AbilityId.SIEGEMODE_SIEGEMODE)
                print("SIEGE")

    async def GMSiegedTankProximity(self, proximity):
        for s in self.units(UnitTypeId.SIEGETANKSIEGED):
            threat = self.enemy_units.closer_than(proximity, s).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if not threat.exists:
                s(AbilityId.UNSIEGE_UNSIEGE)
                print("UNSIEGE")

    async def GMMedivacProximity(self):
        m = self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER)
        if m.exists:
            p = m.furthest_to(self.start_location).position.towards(self.start_location, 3)
            for medivac in self.units(UnitTypeId.MEDIVAC):
                medivac.attack(p)

    async def GMRavenProximity(self):
        for r in self.units(UnitTypeId.RAVEN):
            e = self.enemy_units.not_structure.closer_than(11, r.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if e.exists and r.energy > 75:
                eMechPriority = e(UnitTypeId.SIEGETANKSIEGED) | e(UnitTypeId.VIKINGFIGHTER) | e(UnitTypeId.BATTLECRUISER) | e(UnitTypeId.THOR) | e(UnitTypeId.CARRIER) | e(UnitTypeId.VOIDRAY) | e(UnitTypeId.CARRIER) | e(UnitTypeId.COLOSSUS) | e(UnitTypeId.MOTHERSHIP) | e(UnitTypeId.TEMPEST)
                if eMechPriority.exists:
                    ea = eMechPriority.random
                    if await self.can_cast(r, AbilityId.EFFECT_INTERFERENCEMATRIX, ea):
                        r(AbilityId.EFFECT_INTERFERENCEMATRIX, ea)
                else:
                    ea = e.random
                    eap = ea.position
                    e2 = e.closer_than(3, eap)
                    r2 = self.units.closer_than(5, eap)  # arbituary numbers used
                    if r.position.distance_to(ea.position) > 6 and e2.amount > r2.amount + 2 and await self.can_cast(r, AbilityId.EFFECT_ANTIARMORMISSILE, ea):
                        r(AbilityId.EFFECT_ANTIARMORMISSILE, ea)
            elif e.exists:
                ea = e.closest_to(r.position)
                p = ea.position.towards(r.position, 13)
                r.move(p)
            else:
                a = self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER) | self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.SIEGETANKSIEGED)
                if a.exists:
                    p = a.furthest_to(self.start_location).position.towards(self.start_location, 2)
                    r.move(p)

    async def GEReaperProximity(self):
        for r in self.units(UnitTypeId.REAPER):
            threat = self.enemy_units.closer_than(10, r.position).not_flying
            if threat.exists:
                death = threat.closest_to(r.position)
                p = death.position.towards(r.position, 3)
                if p.distance_to(r.position) < 5:
                    if await self.can_cast(r, AbilityId.KD8CHARGE_KD8CHARGE, p):
                        r(AbilityId.KD8CHARGE_KD8CHARGE, p)
                if r.health_percentage > 5 / 7 and r.weapon_cooldown == 0:
                    r.attack(death)

                if death.position.distance_to(r.position) < 5 and not (r.is_attacking or r.is_moving):
                    nodeath = r.position.towards(death.position, -1)
                    r.move(nodeath)

                if r.health_percentage < 3 / 7:
                    nodeath = r.position.towards(death.position, -4)
                    r.move(nodeath)

    async def GMSiegeTankFollow(self, distance):
        s = self.units(UnitTypeId.SIEGETANK).idle
        m = self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER)
        e = self.enemy_units.not_flying
        for s1 in s:
            if m.exists and e.exists:
                mp = m.closest_to(e.closest_to(s1.position).position).position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))
                s1.attack(mp)

    async def GMReaperScout(self):
        for r in self.units(UnitTypeId.REAPER).idle:
            m = self.mineral_field.closer_than((self.supply_used*4), self.start_location).random.position
            r.attack(m)

    async def GEReaperScout(self):
        i = len(self.enemy_start_locations)
        j = random.randint(0, i-1)
        self.target = self.enemy_start_locations[j]
        if self.enemy_structures.exists:
            self.target = self.enemy_structures.random.position
        m = self.mineral_field.closer_than(20, self.target)
        if m.exists:
            self.target = m.random.position
        for r in self.units(UnitTypeId.REAPER).idle:
            print("Moving")
            print(self.target)
            r.move(self.target)

    async def GMRally(self):
        building = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED) | self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        if self.enemy_structures.exists and building.exists:
            self.RallyPoint = building.closest_to(self.enemy_structures.random.position).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        for a in self.units.idle.not_flying.exclude_type(UnitTypeId.HELLION):
            if a.distance_to(self.RallyPoint) > 10:
                a.attack(self.RallyPoint)

    """async def GMRallyAlternateMarineMarauder(self):  # allows follow tactics
        building = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED) | self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        if self.enemy_structures.exists and building.exists:
            self.RallyPoint = building.closest_to(self.enemy_structures.random.position).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        alternate = self.units(UnitTypeId.MARINE).idle | self.units(UnitTypeId.MARAUDER).idle
        for a in alternate:
            if a.distance_to(self.RallyPoint) > 30:
                a.attack(self.RallyPoint)"""

    async def GMDefend(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND)
        for c in cc:
            threat = self.enemy_units.closer_than(25, c.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE).exclude_type(UnitTypeId.OVERSEER).exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.PROBE)
            if threat.exists:
                army = self.units.exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.RAVEN).exclude_type(UnitTypeId.MEDIVAC).exclude_type(UnitTypeId.MULE).closer_than(40, c.position)
                # improve code to include scv attacks
                p = threat.random.position
                for a in army:
                    a.attack(p)

    async def GEEarlyDefend(self):

        threat = self.enemy_units.closer_than(30, self.start_location)
        if threat.amount > 1:
            army = self.units
            for a in army:
                a.attack(threat.random)
                print("*Not Safe*")
                await self.chat_send("GO AWAY")

    async def GEUnfinshedBuildingCheck(self):
        if self.units(UnitTypeId.SCV).exists:
            for a in self.structures.structure.not_ready.exclude_type(UnitTypeId.REACTOR).exclude_type(UnitTypeId.BARRACKSREACTOR).exclude_type(UnitTypeId.FACTORYREACTOR).exclude_type(UnitTypeId.STARPORTREACTOR).exclude_type(UnitTypeId.TECHLAB).exclude_type(UnitTypeId.BARRACKSTECHLAB).exclude_type(UnitTypeId.FACTORYTECHLAB).exclude_type(UnitTypeId.STARPORTTECHLAB):

                #print (a.position) # code no work # modified version
                scvclose = self.units(UnitTypeId.SCV).closer_than(4, a.position)
                buildingcheck = False
                e = self.enemy_units.closer_than(6, a.position)
                if a.health_percentage < .3 and e.amount > a.health_percentage * 10:
                    a(AbilityId.CANCEL_BUILDINPROGRESS)
                if not scvclose.exists:
                    a(AbilityId.CANCEL_BUILDINPROGRESS)

    async def GMLandIdleBuildings(self): # This needs to be reworked
        b = self.structures(UnitTypeId.BARRACKSFLYING).idle
        f = self.structures(UnitTypeId.FACTORYFLYING).idle
        s = self.structures(UnitTypeId.STARPORTFLYING).idle
        if b.exists and self.supply_used < 200:
            if not self.structures(UnitTypeId.BARRACKSTECHLAB).exists and not self.structures(UnitTypeId.TECHLAB).exists:
                b1 = b.random
                p = b1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                b1.move(p)
                if self.can_afford(UnitTypeId.BARRACKSTECHLAB) and self.can_afford(UnitTypeId.BARRACKS):
                    p = await self.find_placement(UnitTypeId.BARRACKS, near=b1.position)
                    b1.build(UnitTypeId.BARRACKSTECHLAB, p)
                    print("AbilityId.LAND B_TECHLAB")
            elif not self.structures(UnitTypeId.REACTOR).exists:
                for b2 in b:
                    p = b2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    b2.move(p)
                    if self.can_afford(UnitTypeId.BARRACKSREACTOR) and self.can_afford(UnitTypeId.BARRACKS):
                        p = await self.find_placement(UnitTypeId.BARRACKS, near=b2.position)
                        b2.build(UnitTypeId.BARRACKSREACTOR, p)
                        print("AbilityId.LAND B_TECHLAB")

        if f.exists and self.supply_used < 200:
            if not self.structures(UnitTypeId.TECHLAB).exists:  # Zerg does not gain replacement reactors intentionally
                for f2 in f:
                    p = f2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    f2.move(p)
                    if self.can_afford(UnitTypeId.FACTORY):
                        p = await self.find_placement(UnitTypeId.FACTORY, near=f2.position)
                        f2.build(UnitTypeId.FACTORYTECHLAB, p)
                        print("AbilityId.LAND F_TECHLAB")

        if s.exists and self.supply_used < 200:
            if not self.structures(UnitTypeId.STARPORTREACTOR).exists and not self.structures(UnitTypeId.REACTOR).exists:
                s1 = s.random
                p = s1.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                s1.move(p)
                if self.can_afford(UnitTypeId.STARPORT):
                    p = await self.find_placement(UnitTypeId.STARPORT, near=s1.position)
                    s1.build(UnitTypeId.STARPORTREACTOR, p)
                    print("AbilityId.LAND S_REACTORLAB")
            else:
                for s2 in s:
                    p = s2.position.offset((random.randint(-5, 5), random.randint(-5, 5)))
                    s2.move(p)
                    if self.can_afford(UnitTypeId.STARPORT):
                        p = await self.find_placement(UnitTypeId.STARPORT, near=s2.position)
                        s2.build(UnitTypeId.STARPORTTECHLAB, p)
                        print("AbilityId.LAND S_TECHLAB")

    async def GMLandCommandCenter(self):
        for cc in self.structures(UnitTypeId.COMMANDCENTERFLYING).idle | self.structures(UnitTypeId.ORBITALCOMMANDFLYING).idle:
            p = await self.get_next_expansion()
            print(p)
            if self.can_afford(UnitTypeId.COMMANDCENTER):
                p = await self.find_placement(UnitTypeId.COMMANDCENTER, near=p)
                print(p)
                cc(AbilityId.LAND, p)
            else:
                cc(AbilityId.MOVE, p)

    async def GMOrbitalScansAttack(self):
        o = self.structures(UnitTypeId.ORBITALCOMMAND)
        if o.exists:
            oo = o.random
            a = self.units.further_than(60, oo.position).exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.REAPER)
            e = self.enemy_units
            if oo.energy > 50 and a.exists and e.exists:
                ap = a.furthest_to(oo.position).position.towards(e.closest_to(oo.position).position, 10)
                oo(AbilityId.SCANNERSWEEP_SCAN, ap)
                e2 = self.enemy_units.closer_than(16, ap)
                if e2.exists:
                    e2p = e2.random.position
                    for aa in a.closer_than(25, ap):
                        aa.attack(e2p)

    async def GMCommandCenter(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for c in cc.idle:
            cc2 = (cc | oc).further_than(3, c.position).closer_than(12, c.position)
            if cc2.exists:
                if cc2.closest_to(c.position).distance_to(self.start_location) < c.distance_to(self.start_location):
                    (c(AbilityId.LIFT))
            else:
                if self.can_afford(UnitTypeId.ORBITALCOMMAND) and cc.not_ready.exists:
                    c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
                elif self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < (cc.amount*20) + (oc.amount*15) + 15 and self.units(UnitTypeId.SCV).amount < 70 and self.units(UnitTypeId.SCV).closer_than(20, c).amount < 24 and self.supply_left > 0:
                    c.train(UnitTypeId.SCV)
                    # coded this way to deal with a bug with expandnow()

    async def GMOrbitalCommand(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for o in oc.ready.idle:
            scv = self.units(UnitTypeId.SCV).closer_than(10, o)
            m = self.mineral_field.closer_than(10, o)
            if not scv.exists and not m.exists:
                o(AbilityId.LIFT)
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 50:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy >= 120:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)
                    print("mule")
            elif o.energy > 100 and self.enemy_structures.amount == 0:
                o(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])  # can be improved with random
                o(AbilityId.SCANNERSWEEP_SCAN, self.mineral_field.random.position)
                print("SCAN SEARCH")
            elif o.energy == 200:
                a = self.units
                if a.exists:
                    aa = a.furthest_to(o.position).position
                    o(AbilityId.SCANNERSWEEP_SCAN, aa.offset((random.randint(-5, 5), random.randint(-5, 5))))

    async def GEOrbitalCommand(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        for o in oc.ready.idle:
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 50:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy >= 50:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 5:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)
                    print("mule")

    async def GEInBaseCommandCenter(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND).ready #  not flying
        if cc.amount > 1:
            cc1 = cc.closest_to(self.start_location)
            cc2 = cc.further_than(2, cc1.position).closer_than(12, cc1.position)
            for c in cc2.idle:
                c(AbilityId.LIFT)

    async def GMManageSupply(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND)
        s = self.units(UnitTypeId.SCV)
        if cc.exists and s.exists and self.supply_used + self.supply_left < 200:
            if self.supply_left < self.supply_used/16 + 4 and not self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.can_afford(UnitTypeId.SUPPLYDEPOT):
                sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
                if sd.exists:
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=sd.random)
                    print("SUPPLYDEPOT")
                    if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                        await self.build(UnitTypeId.SUPPLYDEPOT, near=sd.random)
                        print("SUPPLYDEPOT")
                else:
                    await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)
                    print("CC_SUPPLYDEPOT")
                    if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                        await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)
                        print("CC_SUPPLYDEPOT")
            elif self.supply_left < 0 and self.can_afford(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)
                """most code here is untested"""

    async def GMAddonAbductBuilding(self):
        b = self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORTFLYING)
        a = b|f|s
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)

        if t.exists and a.exists:
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

    async def GMRefineryBuild(self):
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
                                print("REFINERY")
                            # copy pasted from E method because I might want it to be slightly different than the other method
                            # it currently has a larger amount of refineries because I plan on doing a vespene gas heavy army

    async def GERefineryBuild(self):
        for cc in self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND):
            v = self.vespene_geyser.closer_than(15.0, cc)
            for ve in v:
                if self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
                    """ 
                    Observation: The code was learned from  the youtube tutorial. It is not optimally coded.
                    It in theory, only allows one refinery construction at a time. Loop -> Loop -> Check
                    If the check was done before the loop, there wouldn't be needless cycles.
                    Code left unchanged because of time constraint and not wanting to break the project.
                    ^^^
                    Observation: My previous observation is technically correct but any performance drop created by it
                    is marginal. It doesn't bog down real time False or real time True.
                    """
                    if not self.structures(UnitTypeId.REFINERY).closer_than(1, ve).exists:
                        worker = self.select_build_worker(ve.position)
                        if worker is None:
                            break
                        worker.build(UnitTypeId.REFINERY, ve)
                        print("REFINERY")

    async def GMEngineeringBay(self):
        for e in self.structures(UnitTypeId.ENGINEERINGBAY).ready.idle.idle:
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

    async def GMArmoryGround(self):
        for a in self.structures(UnitTypeId.ARMORY).ready.idle.idle:
            if await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1):
                a(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1)
            elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2):
                a(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2)
            elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3):
                a(AbilityId.ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3)
            elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1):
                a(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1)
            elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2):
                a(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2)
            elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3):
                a(AbilityId.ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3)

    async def GMBTechlab(self):
        bt = self.structures(UnitTypeId.BARRACKSTECHLAB).ready.idle
        if bt.exists:
            bt1 = bt.first
            if await self.can_cast(bt1, AbilityId.RESEARCH_COMBATSHIELD) and self.can_afford(AbilityId.RESEARCH_COMBATSHIELD):
                bt1(AbilityId.RESEARCH_COMBATSHIELD)
                print("UPGRADE_SHIELD")
            elif await self.can_cast(bt1, AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK) and self.can_afford(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK):
                bt1(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK)
                print("UPGRADE_STIMPACK")

    async def GMBarracks(self):
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
                    if self.can_afford(UnitTypeId.REAPER) and not self.units(UnitTypeId.REAPER).exists and self.units(UnitTypeId.MARINE).amount >= 10 and self.enemy_structures.amount < 3:
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

    async def GEBarracks(self):
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
                        print("B_TECHLAB")
                else:
                    if self.can_afford(UnitTypeId.MARAUDER):
                        b.train(UnitTypeId.MARAUDER)
            elif self.can_afford(UnitTypeId.REAPER):
                b.build(UnitTypeId.BARRACKSREACTOR)
                print("B_REACTOR")

    async def GMFactory(self):
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

    async def GEFactory(self):
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

    async def GMStarport(self):
        for s in self.structures(UnitTypeId.STARPORT).ready.idle:
            if s.add_on_tag == 0:
                s(AbilityId.LIFT)

            elif self.structures(UnitTypeId.STARPORTREACTOR).exists:
                id = self.structures(UnitTypeId.STARPORTREACTOR).random.tag
                if s.add_on_tag == id and self.supply_left > 4:
                    if self.can_afford(UnitTypeId.MEDIVAC) and self.units(UnitTypeId.MEDIVAC).amount < 8:
                        s.train(UnitTypeId.MEDIVAC)
                        if self.can_afford(UnitTypeId.MEDIVAC):
                            s.train(UnitTypeId.MEDIVAC) #replacement code

                elif self.supply_left > 2:
                    if self.can_afford(UnitTypeId.RAVEN):
                        s.train(UnitTypeId.RAVEN)

            else:
                if self.can_afford(UnitTypeId.RAVEN):
                    s.train(UnitTypeId.RAVEN)

    async def GEsupplydepotdown(self):
        for sd in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
            e = self.enemy_units.closer_than(8, sd.position).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

    async def GEsupplydepotup(self):
        for sd in self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            e = self.enemy_units.closer_than(10, sd.position).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            a = self.units.not_flying.closer_than(3, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists and not a.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_RAISE)

    #Methods: RANDOM
    async def REBuildOrder(self):
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
                        c.train(UnitTypeId.SCV)

            if scv.exists and not sd.exists and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):

                    print("Build: AntiRandom")
                    await self.SupplyDepot1()
                    print("SUPPLY DEPOT1")

            elif sd.exists and self.can_afford(UnitTypeId.REFINERY) and not self.structures(UnitTypeId.REFINERY).exists and not self.already_pending(UnitTypeId.REFINERY):
                await self.GERefineryBuild()
                print("gas")
            elif sd.ready.exists and scv.exists and self.structures(UnitTypeId.REFINERY).exists:
                if not b.exists and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        await self.Barracks1()
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.REFINERY).amount < 2 and not self.already_pending(UnitTypeId.REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(UnitTypeId.COMMANDCENTER):
                        await self.expand_now()
                        print("EXPAND")
                    elif oc.exists or self.already_pending(UnitTypeId.ORBITALCOMMAND) or self.structures(UnitTypeId.BARRACKSREACTOR).exists:
                        if sd.amount == 1 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                            await self.SupplyDepot2()
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
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
                                await self.build(UnitTypeId.BARRACKS, p)
                        elif self.structures(UnitTypeId.BARRACKS).amount > 1 and sd.amount < 3:
                            if self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
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

                                await self.build(UnitTypeId.SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")

    async def REBarracks(self):
        for b in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if self.structures(UnitTypeId.BARRACKSREACTOR).exists:
                if b.add_on_tag == 0:
                    if self.can_afford(UnitTypeId.MARINE):
                        b.train(UnitTypeId.MARINE)
                elif self.supply_left > 1:
                        if self.can_afford(UnitTypeId.REAPER) and self.units(UnitTypeId.REAPER).amount < 2:
                            b.train(UnitTypeId.REAPER)
                            if self.can_afford(UnitTypeId.REAPER):
                                b.train(UnitTypeId.REAPER)
                            elif self.can_afford(UnitTypeId.MARINE):
                                b.train(UnitTypeId.MARINE)
                        else:
                            if self.can_afford(UnitTypeId.MARINE):
                                b.train(UnitTypeId.MARINE)
                            if self.can_afford(UnitTypeId.MARINE):
                                b.train(UnitTypeId.MARINE)
            else:
                if self.can_afford(UnitTypeId.BARRACKSREACTOR):
                    b.build(UnitTypeId.BARRACKSREACTOR)
                elif self.can_afford(UnitTypeId.MARINE):
                    b.train(UnitTypeId.MARINE)

    async def RECheckEnemy(self):
        e = self.enemy_units
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

    #Methods: TERRAN
    async def TMAttackInitiation(self, minwave, bubblesize):
        # Note: Poor letter choosing for variables is because I was too lazy to write a method twice and this mostly copy pasted from the AntiZerg equivelant method.
        M1 = self.units(UnitTypeId.MARINE)
        M2 = self.units(UnitTypeId.MARAUDER)
        S = self.units(UnitTypeId.SIEGETANK)
        A = M1 | M2 | S
        if (self.enemy_units | self.enemy_structures).exclude_type(UnitTypeId.SCV).exists:
            p = self.enemy_units | self.enemy_structures
            p = p.exclude_type(UnitTypeId.SCV).closest_to(self.start_location).position
            if self.supply_used > 190:
                for m in A:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        m.attack(p)
        else:
            if self.supply_used > 190:
                for m in A.idle:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        p = self.enemy_start_locations[0]  # p should be usually overwritten but it is intended to be an uncommon method
                        i = self.mineral_field
                        if i.exists:
                            p = i.random.position
                        m.attack(p)  # speaking of uncommon, this is untested
                        print("IDK")
                        await self.chat_send(":(")

    async def TEBuildOrder(self): # code copy pasted from zerg build order
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)

        if cc.ready.exists or oc.ready.exists:
            cci = cc.ready.idle | oc.ready.idle
            if cc.ready.idle.exists and self.can_afford(UnitTypeId.ORBITALCOMMAND) and b.ready.exists:
                c = cc.idle.ready.random
                c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
            """elif cci.exists and self.can_afford(UnitTypeId.SCV):
                for c in cci:
                    if self.can_afford(UnitTypeId.SCV):
                        c.train(UnitTypeId.SCV))"""

            if scv.exists and not sd.exists and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: AntiTerran")
                    await self.SupplyDepot1()
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        await self.Barracks1()
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.REFINERY).amount < 2 and not self.already_pending(
                            UnitTypeId.REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(UnitTypeId.COMMANDCENTER):
                        #  await self.expand_now() # code changed to accommodate getting killed early by common enemy push
                        await self.build(UnitTypeId.COMMANDCENTER, near=self.start_location)
                        print("New CC")
                    else:
                        if sd.amount == 1 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                            await self.SupplyDepot2()
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
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
                                await self.build(UnitTypeId.BARRACKS, p)
                        elif (self.structures(UnitTypeId.BARRACKS).amount > 1 and oc.exists) or self.supply_left <= 2:
                            if sd.amount < 3 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
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
                                await self.build(UnitTypeId.SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")
                            elif self.can_afford(UnitTypeId.FACTORY) and self.structures(UnitTypeId.FACTORY).amount < 1 and not self.already_pending(UnitTypeId.FACTORY):
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
                                await self.build(UnitTypeId.FACTORY, p)
                                print("FACTORY")

    async def TECommandCenter(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND)
        ccflying = self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        for c in cc.idle:
            m = self.mineral_field
            minnear = m.closer_than(15, c.position)
            cc2 = cc.further_than(3, c.position).closer_than(15, c.position)
            if not self.units(UnitTypeId.SCV).exists and not minnear.exists and not ccflying.exists:
                c(AbilityId.LIFT)
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
        for c in cc(UnitTypeId.COMMANDCENTER):
            if self.structures(UnitTypeId.BARRACKS).ready.exists:
                if self.can_afford(UnitTypeId.ORBITALCOMMAND):
                    print("CC_OC")
                    c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
                elif self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < (cc.amount*20) + 10 and self.units(UnitTypeId.SCV).amount < 70 and self.units(UnitTypeId.SCV).closer_than(20, c).amount < 24 and self.supply_left > 0:
                    c.train(UnitTypeId.SCV)
                    # coded this way to deal with a bug with expandnow()

    async def TEOrbitalCommand(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND)
        flyingcc = self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        for o in oc.ready.idle:
            scv = self.units(UnitTypeId.SCV).closer_than(10, o)
            m = self.mineral_field.closer_than(15, o)
            if not scv.exists and not m.exists and not flyingcc.exists:
                o(AbilityId.LIFT)
                p = await self.get_next_expansion()
                m = self.mineral_field
                if m.exists:
                    m1 = m.closest_to(p).position
                    print(p)
                    print(m1)
                    p2 = m1.towards(p, 5)
                    print(p2)
                    self.nextXpansionLocation = p2
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 65 and self.units(UnitTypeId.SCV).closer_than(20, o.position).amount < 24:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy == 200:
                a = self.units
                if a.exists:
                    aa = a.furthest_to(o.position).position
                    o(AbilityId.SCANNERSWEEP_SCAN, aa.offset((random.randint(-5, 5), random.randint(-5, 5))))
            elif o.energy > 100 and self.enemy_structures.amount == 0:
                o(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])  # can be improved with random
                o(AbilityId.SCANNERSWEEP_SCAN, self.mineral_field.random.position)
                print("SCAN SEARCH")
            elif o.energy >= 50:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 6:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)
                    print("mule")

    async def TELandCommandCenter(self):
        for cc in self.structures(UnitTypeId.COMMANDCENTERFLYING).idle | self.structures(UnitTypeId.ORBITALCOMMANDFLYING).idle:
            #p = await self.get_next_expansion()
            print(await self.get_next_expansion())
            p = self.nextXpansionLocation
            print(p)
            """if await self.can_cast(cc(AbilityId.LAND, self.nextXpansionLocation)):
                p = self.nextXpansionLocation
                cc(AbilityId.LAND, p))
            else:
                cc(MOVE, p))"""
            p = self.nextXpansionLocation
            cc(AbilityId.MOVE, p)
            cc(AbilityId.LAND, p)
            p = self.nextXpansionLocation
            m = self.mineral_field
            if m.exists:
                m1 = m.closest_to(p).position
                print(p)
                print(m1)
                p2 = p.towards(m1, -.5)
                print(p2)
                self.nextXpansionLocation = p2
                e = self.enemy_units.closer_than(15, self.nextXpansionLocation)
                if e.exists:
                    self.nextXpansionLocation = await self.get_next_expansion()
                    p3 = cc.position.towards(e.random.position, -1)
                    cc.move(p3)

    async def TEInBaseCommandCenter(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND) #  not flying
        ccflying = self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        if cc.amount > 1:
            cc1 = cc.closest_to(self.start_location)
            cc2 = cc.further_than(2, cc1.position).closer_than(15, cc1.position)
            for c in cc2.idle: # only happens if a cc2 exists*
                c(AbilityId.LIFT)
                p = await self.get_next_expansion()
                m = self.mineral_field
                if m.exists:
                    m1 = m.closest_to(p).position
                    print(p)
                    print(m1)
                    p2 = m1.towards(p, 5)
                    print(p2)
                    self.nextXpansionLocation = p2

    async def TMAddonAbductBuilding(self):
        b = self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORTFLYING)
        a = b|f|s
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)

        if t.exists and (f.exists or s.exists):
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f | s
            af = a2.first
            p = t.first.add_on_land_position
            af(AbilityId.LAND, p)

        elif r.exists and b.exists:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            bf = b.first
            bf(AbilityId.LAND, p)

        elif s.exists and r.exists and not self.structures(UnitTypeId.STARPORTREACTOR).exists:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            sf = s.first
            sf(AbilityId.LAND, p)

        elif b.exists and t.exists and not self.structures(UnitTypeId.BARRACKSTECHLAB).exists:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            bf = b.first
            bf(AbilityId.LAND, p)

    async def TMStarport(self):
        for s in self.structures(UnitTypeId.STARPORT).ready.idle:
            if s.add_on_tag == 0:
                s(AbilityId.LIFT)

            elif self.structures(UnitTypeId.STARPORTREACTOR).exists:
                id = self.structures(UnitTypeId.STARPORTREACTOR).random.tag
                if s.add_on_tag == id and self.supply_left > 4:
                    if self.can_afford(UnitTypeId.MEDIVAC) and self.units(UnitTypeId.MEDIVAC).amount < 8:
                        s.train(UnitTypeId.MEDIVAC)
                        if self.can_afford(UnitTypeId.MEDIVAC):
                            s.train(UnitTypeId.MEDIVAC) #replacement code

                    """if self.units(UnitTypeId.MEDIVAC).amount + 2 < self.units(VIKINGFIGHTER).amount:
                        if self.can_afford(UnitTypeId.MEDIVAC):
                            s.train(UnitTypeId.MEDIVAC))
                            if self.can_afford(UnitTypeId.MEDIVAC):
                                s.train(UnitTypeId.MEDIVAC))
                    else:
                        if self.minerals > 350 and self.vespene > 200:
                            s.train(VIKING))
                            s.train(VIKING))""" # tried a couple things to make this code work but gave up for future sprint
                elif self.supply_left > 2:
                    if self.can_afford(UnitTypeId.RAVEN):
                        s.train(UnitTypeId.RAVEN)

            else:
                if self.can_afford(UnitTypeId.RAVEN):
                    s.train(UnitTypeId.RAVEN)

    async def TMReplaceExpand(self):
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORY) | self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORT) | self.structures(UnitTypeId.STARPORTFLYING)
        e = self.structures(UnitTypeId.ENGINEERINGBAY)
        a = b.flying | f.flying | s.flying
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)

        if sd.ready.exists and cc.exists and not b.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

        if b.ready.exists and cc.exists and f.amount < 2 and not self.already_pending(UnitTypeId.FACTORY) and self.can_afford(UnitTypeId.FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.FACTORY, near=p)

        if f.ready.exists and cc.exists and not s.exists and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.STARPORT, near=p)

        if not e.exists and cc.exists and not self.already_pending(UnitTypeId.ENGINEERINGBAY) and self.can_afford(UnitTypeId.ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.ENGINEERINGBAY, near=p)

        if f.ready.exists and cc.exists and not self.structures(UnitTypeId.ARMORY).exists and not self.already_pending(UnitTypeId.ARMORY) and self.can_afford(UnitTypeId.ARMORY):
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.ARMORY, near=p)

        if b.amount == 1 and cc.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

        if self.minerals > 200 + (cc.amount * 200) and self.can_afford(UnitTypeId.COMMANDCENTER) and not cc.flying.exists and cc.amount < 5 and not self.already_pending(UnitTypeId.COMMANDCENTER):
            print("expand")
            #  await self.expand_now()
            p = self.start_location
            await self.build(UnitTypeId.COMMANDCENTER, near=p)

        if oc.amount > 1:
            if s.amount == 1 and cc.exists and not self.already_pending(UnitTypeId.STARPORT) and cc.amount > 2 and self.can_afford(UnitTypeId.STARPORT):
                print("NOT ENOUGH STARPORT")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(UnitTypeId.STARPORT, near=p)

        if b.amount < oc.amount * 2 and cc.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

    #Methods: ZERG"""
    async def ZMAttackInitiation(self, minwave, bubblesize):
        M1 = self.units(UnitTypeId.MARINE)
        M2 = self.units(UnitTypeId.MARAUDER)
        S = self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.SIEGETANKSIEGED)
        H = self.units(UnitTypeId.HELLION) | self.units(UnitTypeId.HELLIONTANK)
        A = M1 | M2 | S | H
        if self.enemy_structures.exists:
            p = self.enemy_structures.closest_to(self.start_location).position
            if self.time > 500 and self.time < 600 and A.amount > 30:
                MM = M1 | M2 | S.exclude_type(UnitTypeId.SIEGETANKSIEGED)
                for m in MM:
                    if MM.closer_than(bubblesize, m.position).amount >= minwave:
                        m.attack(p)
            elif self.supply_used > 190:
                MM = M1 | M2 | S.exclude_type(UnitTypeId.SIEGETANKSIEGED)
                for m in MM:
                    if MM.closer_than(bubblesize, m.position).amount >= minwave:
                        m.attack(p)
        else:
            if self.supply_used > 190:
                MM = M1 | M2 | S.exclude_type(UnitTypeId.SIEGETANKSIEGED)
                for m in MM:
                    if MM.closer_than(bubblesize, m.position).amount >= minwave:
                        p = self.enemy_start_locations[0]  # code can be improved with random number but uncommon
                        i = self.mineral_field
                        if i.exists:
                            p = i.random.position
                        m.attack(p)  # speaking of uncommon, this is untested
                        print("IDK")

    async def ZMHellionFollow(self, distance):
        h = self.units(UnitTypeId.HELLION).idle
        m = self.units(UnitTypeId.MARINE) | self.units(UnitTypeId.MARAUDER)
        e = self.enemy_units.not_flying
        for h1 in h:
            if m.exists and e.exists:
                mp = m.closest_to(e.closest_to(h1.position).position).position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))
                h1.attack(mp)

    async def ZMHellionProximity(self, proximity):
        if self.structures(UnitTypeId.ARMORY).ready.exists:
            for h in self.units(UnitTypeId.HELLION):
                if self.enemy_units.closer_than(proximity, h.position).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE).exists:
                    h(AbilityId.MORPH_HELLBAT)
                    print("MORPH HELLBAT")

    async def ZMHellbatProximity(self, proximity):
        if self.structures(UnitTypeId.ARMORY).ready.exists:
            for h in self.units(UnitTypeId.HELLIONTANK):
                death = self.enemy_units.closer_than(proximity, h.position).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
                if death.exists:
                    h.attack(death.random.position)
                    print("BURN")
                else:
                    h(AbilityId.MORPH_HELLION)
                    print("MORPH HELLBAT")

    async def ZMLurkerCheck(self):
        o = self.structures(UnitTypeId.ORBITALCOMMAND)
        l = self.enemy_units(UnitTypeId.LURKERMP) | self.enemy_units(UnitTypeId.LURKERMPBURROWED)
        if o.exists and l.exists:
            oo = o.random
            ll = l.random
            if oo.energy > 50:
                ap = ll.position
                oo(AbilityId.SCANNERSWEEP_SCAN, ap)

    async def ZEBuildOrder(self):
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
                        c.train(UnitTypeId.SCV)

            if scv.exists and not sd.exists and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: AntiZerg")
                    await self.SupplyDepot1()
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        await self.Barracks1()
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.REFINERY).amount < 2 and not self.already_pending(
                            UnitTypeId.REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(UnitTypeId.COMMANDCENTER):
                        await self.expand_now()
                        print("EXPAND")
                    elif oc.exists or self.already_pending(UnitTypeId.ORBITALCOMMAND) or self.structures(UnitTypeId.BARRACKSREACTOR).exists:
                        if sd.amount == 1 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                            await self.SupplyDepot2()
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
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
                                await self.build(UnitTypeId.BARRACKS, p)
                        elif self.structures(UnitTypeId.BARRACKS).amount > 1 and oc.exists:
                            if sd.amount < 3 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
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
                                await self.build(UnitTypeId.SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")
                            elif self.can_afford(UnitTypeId.FACTORY) and self.structures(UnitTypeId.FACTORY).amount < 1 and not self.already_pending(UnitTypeId.FACTORY):
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
                                await self.build(UnitTypeId.FACTORY, p)
                                print("FACTORY")

    async def ZEFactory(self):
        for f in self.structures(UnitTypeId.FACTORY).ready.idle:
            if self.supply_left > 2:
                # only allow one reactor
                if f.add_on_tag == 0:
                    if self.can_afford(UnitTypeId.FACTORYREACTOR):
                        f.build(UnitTypeId.FACTORYREACTOR)
                else:
                    if self.can_afford(UnitTypeId.HELLION):
                        f.train(UnitTypeId.HELLION)
                    if self.can_afford(UnitTypeId.HELLION):
                        f.train(UnitTypeId.HELLION)
            elif self.structures(UnitTypeId.FACTORYREACTOR).exists:
                f(AbilityId.LIFT)
                print("FLY!!!")

    async def ZMFactory(self):
        for f in self.structures(UnitTypeId.FACTORY).ready.idle:
            if f.add_on_tag == 0:
                f(AbilityId.LIFT)
                print("FLY!!!")
            elif self.units(UnitTypeId.SIEGETANK).closer_than(15, f.position).amount > 1 and self.time > 500 and self.time < 600:
                f(AbilityId.LIFT)
            elif self.units(UnitTypeId.SIEGETANK).closer_than(25, f.position).amount > 2 and self.supply_left < 4 and self.time > 700:
                f(AbilityId.LIFT)
            elif self.supply_used == 0:
                f(AbilityId.LIFT)
            elif self.structures(UnitTypeId.FACTORYREACTOR).exists and self.supply_left > 2:
                id = self.structures(UnitTypeId.FACTORYREACTOR).random.tag
                if self.structures(UnitTypeId.FACTORYREACTOR).amount > 1:
                    f(AbilityId.LIFT)
                    print("FLY!!!")
                elif f.add_on_tag == id:
                    if self.can_afford(UnitTypeId.HELLION):
                        f.train(UnitTypeId.HELLION)
                    if self.can_afford(UnitTypeId.HELLION):
                        f.train(UnitTypeId.HELLION)
                else:
                    if self.can_afford(UnitTypeId.SIEGETANK):
                        f.train(UnitTypeId.SIEGETANK)
            else:
                #add on exists no reactor(tech lab only possible)
                if self.can_afford(UnitTypeId.SIEGETANK):
                    f.train(UnitTypeId.SIEGETANK)
                elif self.can_afford(UnitTypeId.HELLION):
                    f.train(UnitTypeId.HELLION)

    async def ZMAddonAbductBuilding(self):
        b = self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORTFLYING)
        a = b|f|s
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)

        if t.exists and (f.exists or s.exists) and self.supply_used < 200:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            a2 = f | s
            af = a2.first
            p = t.first.add_on_land_position
            af(AbilityId.LAND, p)

        elif r.exists and b.exists and self.supply_used < 200:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            bf = b.first
            bf(AbilityId.LAND, p)

        elif f.exists and r.exists and not self.structures(UnitTypeId.FACTORYREACTOR).exists and self.supply_used < 200:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            ff = f.first
            ff(AbilityId.LAND, p)

        elif s.exists and r.exists and not self.structures(UnitTypeId.STARPORTREACTOR).exists and self.supply_used < 200:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.first.add_on_land_position
            sf = s.first
            sf(AbilityId.LAND, p)

        elif b.exists and t.exists and not self.structures(UnitTypeId.BARRACKSTECHLAB).exists and self.supply_used < 200:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.first.add_on_land_position
            bf = b.first
            bf(AbilityId.LAND, p)

    async def ZMReplaceExpand(self):
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        f = self.structures(UnitTypeId.FACTORY) | self.structures(UnitTypeId.FACTORYFLYING)
        s = self.structures(UnitTypeId.STARPORT) | self.structures(UnitTypeId.STARPORTFLYING)
        e = self.structures(UnitTypeId.ENGINEERINGBAY)
        a = b.flying | f.flying | s.flying
        t = self.structures(UnitTypeId.TECHLAB)
        r = self.structures(UnitTypeId.REACTOR)

        if sd.ready.exists and cc.exists and not b.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

        if b.ready.exists and cc.exists and f.amount < 2 and not self.already_pending(UnitTypeId.FACTORY) and self.can_afford(UnitTypeId.FACTORY):
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.FACTORY, near=p)

        if f.ready.exists and cc.exists and not s.exists and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT):
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.STARPORT, near=p)

        if not e.exists and cc.exists and not self.already_pending(UnitTypeId.ENGINEERINGBAY) and self.can_afford(UnitTypeId.ENGINEERINGBAY):
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.ENGINEERINGBAY, near=p)

        if f.ready.exists and cc.exists and not self.structures(UnitTypeId.ARMORY).exists and not self.already_pending(UnitTypeId.ARMORY) and self.can_afford(UnitTypeId.ARMORY):
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.ARMORY, near=p)

        if b.amount == 1 and cc.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

        if self.minerals > 400 and cc.amount < 5 and not self.already_pending(UnitTypeId.COMMANDCENTER):
            print("expand")
            await self.expand_now()

        if oc.amount > 1:
            if s.amount == 1 and cc.exists and not self.already_pending(UnitTypeId.STARPORT) and cc.amount > 2 and self.can_afford(UnitTypeId.STARPORT):
                print("NOT ENOUGH STARPORT")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(UnitTypeId.STARPORT, near=p)

        if b.amount < cc.amount and cc.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS):
            print("NOT ENOUGH BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

    async def ZMFTechlab(self):
        ft = self.structures(UnitTypeId.FACTORYTECHLAB).ready.idle
        h = self.units(UnitTypeId.HELLION) | self.units(UnitTypeId.HELLIONTANK)
        if ft.exists and h.exists:
            ft1 = ft.first
            if await self.can_cast(ft1, AbilityId.RESEARCH_INFERNALPREIGNITER) and self.can_afford(AbilityId.RESEARCH_INFERNALPREIGNITER):
                ft1(AbilityId.RESEARCH_INFERNALPREIGNITER)
                print("UPGRADE_FIRE")
            elif await self.can_cast(ft1, AbilityId.RESEARCH_SMARTSERVOS) and self.can_afford(AbilityId.RESEARCH_SMARTSERVOS):
                ft1(AbilityId.RESEARCH_SMARTSERVOS)
                print("UPGRADE_FIRE")

    #Methods: Protoss"""
    async def PMAttackInitiation(self, minwave, bubblesize):
        # Note: Poor letter choosing for variables is because I was too lazy to write a method twice and this mostly copy pasted from the AntiZerg equivelant method.
        M1 = self.units(UnitTypeId.MARINE)
        M2 = self.units(UnitTypeId.MARAUDER)
        S = self.units(UnitTypeId.SIEGETANK)
        A = M1 | M2 | S
        E = (self.enemy_units | self.enemy_structures).exclude_type(UnitTypeId.SCV)
        if E.exists:
            p = E.closest_to(self.start_location).position
            if self.supply_used > 190:
                for m in A:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        m.attack(p)
        else:
            if self.supply_used > 190:
                for m in A.idle:
                    if A.closer_than(bubblesize, m.position).amount >= minwave:
                        p = self.enemy_start_locations[0]  # p should be usually overwritten but it is intended to be an uncommon method
                        i = self.mineral_field
                        if i.exists:
                            p = i.random.position
                        m.attack(p)  # speaking of uncommon, this is untested
                        print("IDK")
                        await self.chat_send(":(")

    async def PEBuildOrder(self): # code copy pasted from terran build order
        scv = self.units(UnitTypeId.SCV)
        cc = self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.COMMANDCENTERFLYING) | self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        oc = self.structures(UnitTypeId.ORBITALCOMMAND) | self.structures(UnitTypeId.ORBITALCOMMANDFLYING)
        sd = self.structures(UnitTypeId.SUPPLYDEPOT) | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.BARRACKSFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)

        if cc.ready.exists or oc.ready.exists:
            cci = cc.ready.idle | oc.ready.idle
            if cc.ready.idle.exists and self.can_afford(UnitTypeId.ORBITALCOMMAND) and b.ready.exists:
                c = cc.idle.ready.random
                c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)

            if scv.exists and not sd.exists and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: AntiProtoss")
                    await self.SupplyDepot1()
                    print("SUPPLY DEPOT1")

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):

                        print("Ramp Data points:")
                        print(x)
                        print(xd)
                        print(y)
                        print(yd)
                        print(self.main_base_ramp.top_center)
                        await self.Barracks1()
                        print("BARRACKS1")

                elif b.exists:
                    if self.can_afford(UnitTypeId.REFINERY) and self.structures(UnitTypeId.REFINERY).amount < 2 and not self.already_pending(
                            UnitTypeId.REFINERY):
                        await self.GERefineryBuild()
                        print("gas")
                    elif oc.amount + cc.amount == 1 and self.can_afford(UnitTypeId.COMMANDCENTER):
                        #  await self.expand_now() # code changed to accommodate getting killed early by common enemy push
                        await self.build(UnitTypeId.COMMANDCENTER, near=self.start_location)
                        print("New CC")
                    else:
                        if sd.amount == 1 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                            await self.SupplyDepot2()
                            print("SUPPLYDEPOT2")
                        elif sd.amount <= 2 and b.amount < 2:
                            if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
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
                                await self.build(UnitTypeId.BARRACKS, p)
                        elif (self.structures(UnitTypeId.BARRACKS).amount > 1 and oc.exists) or self.supply_left <= 2:
                            if sd.amount < 3 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
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
                                await self.build(UnitTypeId.SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT3")
                            elif self.can_afford(UnitTypeId.FACTORY) and self.structures(UnitTypeId.FACTORY).amount < 1 and not self.already_pending(UnitTypeId.FACTORY):
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
                                await self.build(UnitTypeId.FACTORY, p)
                                print("FACTORY")
    
                                
    # Postupdate Methods
    async def SupplyDepot1(self):
        # method exists because Supply Depot 1 position was bugged
        p = self.cornors[0]
        await self.build(UnitTypeId.SUPPLYDEPOT, p)
        
    async def Barracks1(self):
        p = self.main_base_ramp.barracks_correct_placement
        await self.build(UnitTypeId.BARRACKS, p)
        
    async def SupplyDepot2(self):
        p = self.cornors[1]
        await self.build(UnitTypeId.SUPPLYDEPOT, p)