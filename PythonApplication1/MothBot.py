#from ast import If
#from operator import ifloordiv
#from pickle import TRUE
import sc2
from sc2 import maps
from sc2.bot_ai import BotAI
from sc2.data import Difficulty, Race
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
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
Note* A 
"""
class MothAI(BotAI):
    async def on_start(self):
        a = sc2.constants #uhm what is this?
        self.quarry()
        self.cornors = list(self.main_base_ramp.corner_depots) 
        self.Rally = None
        self.BattleWinningMath = 1.0 # unimplemented feature -> will be used to make good decisions
        self.target = None
        self.needToExpand = False
        self.enemyknown = False
        self.airHarrass = False
        self.earlyArmor = False
        self.STRAT="error"
        self.nextXpansionLocation = self.start_location
        #await self.GMResetNextXpansionLocation()
        if self.enemy_race == Race.Random:
            self.STRAT = "AntiRandom"
        elif self.enemy_race == Race.Terran:
            self.STRAT = "AntiTerran"
        elif self.enemy_race == Race.Zerg:
            self.STRAT = "AntiZerg"
        elif self.enemy_race == Race.Protoss:
            self.STRAT = "AntiProtoss"
        # print("Strat:")
        # print(self.STRAT)
    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(glhf)")
        self.combinedActions = []
        self.quarry()
        if self.STRAT == "AntiRandom":
            """Early Game"""
            if True:
                if iteration % 1 == 0:
                    await self.GECommandCenter()
                    await self.GEReaperProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                    await self.GELandCommandCenter()
                if iteration % 5 == 0:
                    await self.GESafeBuildOrder()
                    await self.GEReaperScout()
                    await self.GEUnfinishedBuildingCheck()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GECheckEnemy()
                    r = self.quarryUnits(UnitTypeId.REAPER).amount
                    await self.GEBarracks(False, r, r*2, 4, 0)
                if iteration % 10 == 5:
                    await self.GEOrbitalCommand()
                if iteration % 20 == 0:
                    await self.GEEarlyDefend()

        elif self.STRAT == "AntiTerran":
            if self.time <= 240:
                if iteration % 1 == 0:
                    await self.GEReaperProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                    await self.GMLandIdleBuildings(1) # code is GM instead of GE because it is only used in obscure situations
                    await self.GELandCommandCenter()
                if iteration % 5 == 0:
                    await self.GEUnfinishedBuildingCheck()
                    await self.GECommandCenter()
                    await self.GEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GEReaperScout()
                    await self.GESafeBuildOrder()
                    if self.airHarrass:
                        await self.GEAntiAirHarras(7.5)
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GEBuildingLift(10, 20)
                if iteration % 10 == 0:
                    # techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int
                    r = 1
                    if self.quarryEnemyStructure.exists:
                        r = 0
                    m = 1
                    if self.earlyArmor:
                        m = 8
                        r = 0
                    await self.GEBarracks(True, m, 12, r, 0)
                    await self.GEInBaseCommandCenter()
                    await self.GERally()
                    await self.GMAddonAbductBuilding()
                if iteration % 10 == 5:
                    # techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int
                    await self.GEFactory(True, False, 2, 0, 0)
                    #await self.GEBuildingDodge(12)
                    await self.GECheckEnemy()
                if iteration % 20 == 0:
                    await self.GEEarlyDefend()
                if iteration % 50 == 0:
                    await self.GMResetNextXpansionLocation()
            elif self.time > 240 and True:
                if iteration % 1 == 0:
                    await self.GELandCommandCenter()
                    await self.GEReaperProximity()
                    await self.GMRavenProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 4 == 0:
                    await self.GEUnfinishedBuildingCheck()
                    #await self.GEBuildingDodge(10)
                    await self.GMReaperMove(15)
                    await self.GMSiegeTankProximity(16, False)
                    await self.GMStepForwardBackward(17, 20)
                    await self.GMWidowTrapTravel(15, 40)
                    await self.GMAntiAirAttack(8)
                    # proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool
                    await self.GMWidowBurrowProximity(10, 40, 5, False, False)
                    await self.GMWidowUnburrowProximity(10, 40, 5, False, True)
                if iteration % 10 == 0:
                    await self.GECommandCenter()
                    await self.GEBuildingLift(20, 15)
                    if self.airHarrass:
                        await self.GEAntiAirHarras(7.5)
                if iteration % 10 == 1:
                    await self.GEOrbitalCommand()
                if iteration % 10 == 2:
                    # techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int
                    await self.GEBarracks(True, 14, 50, 1, 0)
                if iteration % 10 == 3:
                    # techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int
                    await self.GEFactory(False, False, 16, 3, 0)
                if iteration % 10 == 4:
                    #mm = (a(UnitTypeId.MARINE) | a(UnitTypeId.MARAUDER)).amount
                    m = self.quarryUnits(UnitTypeId.MEDIVAC).amount
                    v = self.quarryUnits(UnitTypeId.VIKINGFIGHTER).amount
                    await self.GMStarport(False, 8, m-2, v-2, 1)
                    # techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int
                if iteration % 9 == 5:
                    await self.GMLandIdleBuildings(1)
                    await self.GMPremptiveInvisibleCheck()
                if iteration % 9 == 6:
                    cc = self.quarryStructures
                    cc = cc(UnitTypeId.COMMANDCENTER) | cc(UnitTypeId.ORBITALCOMMAND) | cc(UnitTypeId.COMMANDCENTERFLYING) | cc(UnitTypeId.ORBITALCOMMANDFLYING)
                    await self.GMReplaceExpand(5, 3, 2, 2, 1, 1, 1, 1, 1, cc.amount * 2, 2, 2)
                    # ccmax: int, ocbuffer: int, barrcksmin: int, factorymin: int, starportmin: int, ebaymin: int, armorymin: int, ghostacademymin: int, fcoremin:int,barrackmax: int, factorymax: int, starportmax: int
                if iteration % 9 == 7:
                    await self.GERefineryBuild()
                    await self.GMManageSupply()
                if iteration % 9 == 8:
                    i = random.randint(0, 2)
                    if i == 0:
                        await self.GMEngineeringBay()
                    elif i == 1:
                        await self.GMArmory(True)
                    elif i == 2:
                        await self.GMBTechlab()
                if iteration % 6 == 0:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 3:
                    await self.distribute_workers()
                    await self.GMSiegeTankFollow(5)
                    await self.GMWidowFollow(10, False, True)
                    await self.GMAirFollow(6)
                    await self.GMMedivacProximity()
                if iteration % 9 == 3:
                    await self.GEInBaseCommandCenter()
                    await self.GMDefend()
                if iteration % 9 == 6:
                    await self.GMAddonAbductBuilding()
                if iteration % 20 == 0:
                    await self.GMGeneralAttackTriggers(20, 20)
                if iteration % 20 == 5:
                    await self.GMRally(10, 15)
                    await self.GMRepair(.5, 25)
                if iteration % 20 == 15:
                    await self.GMMarauderProximity(9)
                    await self.GMMarineProximity(8, 12)
                if iteration % 50 == 0:
                    await self.GMUpdateNeedToExpand()
                    await self.GMSiegedTankProximity(18, False)
                    await self.GMResetNextXpansionLocation()
                    await self.GMInvisibleTrack()
                if iteration % 100 == 0:
                    await self.GECheckEnemy()
                    await self.GMOrbitalScans(False, 50)

        elif self.STRAT == "AntiZerg":
            if self.time <= 240:
                if iteration % 1 == 0:
                    await self.GEReaperProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                    await self.GMLandIdleBuildings(1)
                    await self.GELandCommandCenter()
                if iteration % 5 == 0:
                    await self.GEUnfinishedBuildingCheck()
                    await self.GECommandCenter()
                    await self.GEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GEReaperScout()
                    await self.GESafeBuildOrder()
                    if self.airHarrass:
                        await self.GEAntiAirHarras(7.5)
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GEBuildingLift(10, 20)
                if iteration % 10 == 0:
                    # techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int
                    r = 1
                    if self.quarryEnemyStructure.exists:
                        r = 0
                    m = 1
                    if self.earlyArmor:
                        m = 8
                        r = 0
                    await self.GEBarracks(True, m, 12, r, 0)
                    await self.GEInBaseCommandCenter()
                    await self.GERally()
                    await self.GMAddonAbductBuilding()
                if iteration % 10 == 5:
                    # techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int
                    await self.GEFactory(True, False, 2, 0, 0)
                    #await self.GEBuildingDodge(12)
                    await self.GECheckEnemy()
                if iteration % 20 == 0:
                    await self.GEEarlyDefend()
                if iteration % 50 == 0:
                    await self.GMResetNextXpansionLocation()
            elif self.time > 240 and True:
                if iteration % 1 == 0:
                    await self.GELandCommandCenter()
                    await self.GEReaperProximity()
                    await self.GMRavenProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 4 == 0:
                    await self.GEUnfinishedBuildingCheck()
                    #await self.GEBuildingDodge(10)
                    await self.GMReaperMove(15)
                    await self.GMSiegeTankProximity(16, False)
                    await self.GMStepForwardBackward(17, 20)
                    await self.GMWidowTrapTravel(15, 40)
                    await self.GMAntiAirAttack(8)
                    # proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool
                    await self.GMWidowBurrowProximity(10, 40, 5, False, False)
                    await self.GMWidowUnburrowProximity(10, 40, 5, False, True)
                if iteration % 10 == 0:
                    await self.GECommandCenter()
                    await self.GEBuildingLift(20, 15)
                    if self.airHarrass:
                        await self.GEAntiAirHarras(7.5)
                if iteration % 10 == 1:
                    await self.GEOrbitalCommand()
                if iteration % 10 == 2:
                    # techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int
                    await self.GEBarracks(True, 14, 50, 1, 0)
                if iteration % 10 == 3:
                    # techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int
                    await self.GEFactory(False, False, 16, 3, 0)
                if iteration % 10 == 4:
                    # mm = (a(UnitTypeId.MARINE) | a(UnitTypeId.MARAUDER)).amount
                    m = self.quarryUnits(UnitTypeId.MEDIVAC).amount
                    v = self.quarryUnits(UnitTypeId.VIKINGFIGHTER).amount
                    await self.GMStarport(False, 8, m - 2, v - 2, 1)
                    # techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int
                if iteration % 9 == 5:
                    await self.GMLandIdleBuildings(1)
                    await self.GMPremptiveInvisibleCheck()
                if iteration % 9 == 6:
                    cc = self.quarryStructures
                    cc = cc(UnitTypeId.COMMANDCENTER) | cc(UnitTypeId.ORBITALCOMMAND) | cc(UnitTypeId.COMMANDCENTERFLYING) | cc(UnitTypeId.ORBITALCOMMANDFLYING)
                    await self.GMReplaceExpand(5, 3, 2, 2, 1, 1, 1, 1, 1, cc.amount * 2, 2, 2)
                    # ccmax: int, ocbuffer: int, barrcksmin: int, factorymin: int, starportmin: int, ebaymin: int, armorymin: int, ghostacademymin: int, fcoremin:int,barrackmax: int, factorymax: int, starportmax: int
                if iteration % 9 == 7:
                    await self.GERefineryBuild()
                    await self.GMManageSupply()
                if iteration % 9 == 8:
                    i = random.randint(0, 2)
                    if i == 0:
                        await self.GMEngineeringBay()
                    elif i == 1:
                        await self.GMArmory(True)
                    elif i == 2:
                        await self.GMBTechlab()
                if iteration % 6 == 0:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 3:
                    await self.distribute_workers()
                    await self.GMSiegeTankFollow(5)
                    await self.GMWidowFollow(10, False, True)
                    await self.GMAirFollow(6)
                    await self.GMMedivacProximity()
                if iteration % 9 == 3:
                    await self.GEInBaseCommandCenter()
                    await self.GMDefend()
                if iteration % 9 == 6:
                    await self.GMAddonAbductBuilding()
                if iteration % 20 == 0:
                    await self.GMGeneralAttackTriggers(20, 20)
                if iteration % 20 == 5:
                    await self.GMRally(10, 15)
                    await self.GMRepair(.5, 25)
                if iteration % 20 == 15:
                    await self.GMMarauderProximity(9)
                    await self.GMMarineProximity(8, 12)
                if iteration % 50 == 0:
                    await self.GMUpdateNeedToExpand()
                    await self.GMSiegedTankProximity(18, False)
                    await self.GMResetNextXpansionLocation()
                    await self.GMInvisibleTrack()
                if iteration % 100 == 0:
                    await self.GECheckEnemy()
                    await self.GMOrbitalScans(False, 50)

        elif self.STRAT == "AntiProtoss":
            if self.time <= 240:
                if iteration % 1 == 0:
                    await self.GEReaperProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                    await self.GMLandIdleBuildings(1)  # code is GM instead of GE because it is only used in obscure situations
                    await self.GELandCommandCenter()
                if iteration % 5 == 0:
                    await self.GEUnfinishedBuildingCheck()
                    await self.GECommandCenter()
                    await self.GEOrbitalCommand()
                    await self.GEReaperProximity()
                    await self.GEReaperScout()
                    await self.GESafeBuildOrder()
                    if self.airHarrass:
                        await self.GEAntiAirHarras(7.5)
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GEBuildingLift(10, 20)
                if iteration % 10 == 0:
                    # techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int
                    r = 1
                    if self.quarryEnemyStructure.exists:
                        r = 0
                    m = 1
                    if self.earlyArmor:
                        m = 8
                        r = 0
                    await self.GEBarracks(True, m, 12, r, 0)
                    await self.GEInBaseCommandCenter()
                    await self.GERally()
                    await self.GMAddonAbductBuilding()
                if iteration % 10 == 5:
                    # techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int
                    await self.GEFactory(True, False, 2, 0, 0)
                    #await self.GEBuildingDodge(12)
                    await self.GECheckEnemy()
                if iteration % 20 == 0:
                    await self.GEEarlyDefend()
                if iteration % 50 == 0:
                    await self.GMResetNextXpansionLocation()
            elif self.time > 240 and True:
                if iteration % 1 == 0:
                    await self.GELandCommandCenter()
                    await self.GEReaperProximity()
                    await self.GMRavenProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 4 == 0:
                    await self.GEUnfinishedBuildingCheck()
                    #await self.GEBuildingDodge(10)
                    await self.GMReaperMove(15)
                    await self.GMSiegeTankProximity(16, False)
                    await self.GMStepForwardBackward(17, 20)
                    await self.GMWidowTrapTravel(15, 40)
                    await self.GMAntiAirAttack(8)
                    # proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool
                    await self.GMWidowBurrowProximity(10, 40, 5, False, False)
                    await self.GMWidowUnburrowProximity(10, 40, 5, False, True)
                if iteration % 10 == 0:
                    await self.GECommandCenter()
                    await self.GELandCommandCenter()
                    await self.GEBuildingLift(20, 15)
                    if self.airHarrass:
                        await self.GEAntiAirHarras(7.5)
                if iteration % 10 == 1:
                    await self.GEOrbitalCommand()
                if iteration % 10 == 2:
                    # techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int
                    await self.GEBarracks(True, 14, 50, 1, 0)
                if iteration % 10 == 3:
                    # techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int
                    await self.GEFactory(False, False, 16, 3, 0)
                if iteration % 10 == 4:
                    # mm = (a(UnitTypeId.MARINE) | a(UnitTypeId.MARAUDER)).amount
                    m = self.quarryUnits(UnitTypeId.MEDIVAC).amount
                    v = self.quarryUnits(UnitTypeId.VIKINGFIGHTER).amount
                    await self.GMStarport(False, 8, m - 2, v - 2, 1)
                    # techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int
                if iteration % 9 == 5:
                    await self.GMLandIdleBuildings(1)
                    await self.GMPremptiveInvisibleCheck()
                if iteration % 9 == 6:
                    cc = self.quarryStructures
                    cc = cc(UnitTypeId.COMMANDCENTER) | cc(UnitTypeId.ORBITALCOMMAND) | cc(UnitTypeId.COMMANDCENTERFLYING) | cc(UnitTypeId.ORBITALCOMMANDFLYING)
                    await self.GMReplaceExpand(5, 3, 2, 2, 1, 1, 1, 1, 1, cc.amount * 2, 2, 2)
                    # ccmax: int, ocbuffer: int, barrcksmin: int, factorymin: int, starportmin: int, ebaymin: int, armorymin: int, ghostacademymin: int, fcoremin:int,barrackmax: int, factorymax: int, starportmax: int
                if iteration % 9 == 7:
                    await self.GERefineryBuild()
                    await self.GMManageSupply()
                if iteration % 9 == 8:
                    i = random.randint(0, 2)
                    if i == 0:
                        await self.GMEngineeringBay()
                    elif i == 1:
                        await self.GMArmory(True)
                    elif i == 2:
                        await self.GMBTechlab()
                if iteration % 6 == 0:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 3:
                    await self.distribute_workers()
                    await self.GMSiegeTankFollow(5)
                    await self.GMWidowFollow(10, False, True)
                    await self.GMAirFollow(6)
                    await self.GMMedivacProximity()
                if iteration % 9 == 3:
                    await self.GEInBaseCommandCenter()
                    await self.GMDefend()
                if iteration % 9 == 6:
                    await self.GMAddonAbductBuilding()
                if iteration % 20 == 0:
                    await self.GMGeneralAttackTriggers(20, 20)
                if iteration % 20 == 5:
                    await self.GMRally(10, 15)
                    await self.GMRepair(.5, 25)
                if iteration % 20 == 15:
                    await self.GMMarauderProximity(9)
                    await self.GMMarineProximity(8, 12)
                if iteration % 50 == 0:
                    await self.GMUpdateNeedToExpand()
                    await self.GMSiegedTankProximity(18, False)
                    await self.GMResetNextXpansionLocation()
                    await self.GMInvisibleTrack()
                if iteration % 100 == 0:
                    await self.GECheckEnemy()
                    await self.GMOrbitalScans(False, 50)

    """Methods: GENERAL"""
    # Build Orders
    async def GESafeBuildOrder(self):
        scv = (self.quarryUnits)(UnitTypeId.SCV)
        cc = (self.quarryStructures)(UnitTypeId.COMMANDCENTER) | (self.quarryStructures)(UnitTypeId.COMMANDCENTERFLYING)
        oc = (self.quarryStructures)(UnitTypeId.ORBITALCOMMAND) | (self.quarryStructures)(UnitTypeId.ORBITALCOMMANDFLYING)
        sd = (self.quarryStructures)(UnitTypeId.SUPPLYDEPOT) | (self.quarryStructures)(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = (self.quarryStructures)(UnitTypeId.BARRACKS) | (self.quarryStructures)(UnitTypeId.BARRACKSFLYING)
        f = (self.quarryStructures)(UnitTypeId.FACTORY) | (self.quarryStructures)(UnitTypeId.FACTORYFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)
        if cc.ready.exists or oc.ready.exists:
            if scv.exists and not sd.exists and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    # print("Build: 'Safe'")
                    p = self.cornors[0]
                    await self.build(UnitTypeId.SUPPLYDEPOT, p)

            elif sd.ready.exists and scv.exists:
                if not b.exists and not self.already_pending(UnitTypeId.BARRACKS):
                    if self.can_afford(UnitTypeId.BARRACKS):
                        p = self.main_base_ramp.barracks_correct_placement
                        await self.build(UnitTypeId.BARRACKS, p)

                elif b.exists:
                    if self.can_afford(UnitTypeId.REFINERY) and self.quarryStructures(UnitTypeId.REFINERY).amount < 2 and not self.already_pending(
                            UnitTypeId.REFINERY):
                        await self.GERefineryBuild()
                        # print("gas")
                    else:
                        if sd.amount == 1 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                            p = self.cornors[1]
                            await self.build(UnitTypeId.SUPPLYDEPOT, p)
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
                                # print("UnitTypeId.BARRACKS2")
                                await self.build(UnitTypeId.BARRACKS, p)
                        elif (self.quarryStructures(UnitTypeId.BARRACKS).amount > 1 and oc.exists) or self.supply_left <= 2:
                            if oc.amount + cc.amount == 1 and self.can_afford(UnitTypeId.COMMANDCENTER):
                                #  await self.expand_now() # code changed to accommodate getting killed early by common enemy push
                                if self.can_afford(UnitTypeId.COMMANDCENTER):
                                    await self.build(UnitTypeId.COMMANDCENTER, near=self.start_location)
                                    # print("Inbase expansion")
                            elif sd.amount < 3 and self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
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
                                # print("SUPPLYDEPOT3")
                            elif self.can_afford(UnitTypeId.FACTORY) and not f.exists and not self.already_pending(UnitTypeId.FACTORY):
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
                                # print("UnitTypeId.FACTORY")

    # Expansion Methods and Air Building Commands
    async def GERefineryBuild(self):
        for cc in self.quarryStructures(UnitTypeId.COMMANDCENTER).ready | self.quarryStructures(UnitTypeId.ORBITALCOMMAND):
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
                    if not self.quarryStructures(UnitTypeId.REFINERY).closer_than(1, ve).exists:
                        worker = self.select_build_worker(ve.position)
                        if worker is None:
                            break
                        worker.build(UnitTypeId.REFINERY, ve)
                        # print("UnitTypeId.REFINERY")

    async def GMManageSupply(self):
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER).ready | self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        s = self.quarryUnits(UnitTypeId.SCV)
        if cc.exists and s.exists and self.supply_used + self.supply_left < 200:
            if self.supply_left < self.supply_used/16 + 4 and not self.already_pending(UnitTypeId.SUPPLYDEPOT) and self.can_afford(UnitTypeId.SUPPLYDEPOT):
                if True:
                    e = self.quarryStructures(UnitTypeId.REACTOR) | self.quarryStructures(UnitTypeId.TECHLAB)
                    p = await self.find_placement(UnitTypeId.SUPPLYDEPOT, near=cc.random.position)
                    if e.closer_than(5, p).exists:
                        p = p.towards(e.closest_to(p).position, -5)
                    if not e.closer_than(5, p).exists: # not redundant, the check is to make sure it offset without issues
                        await self.build(UnitTypeId.SUPPLYDEPOT, p)
                        # print("SUPPLYDEPOT")
                    if self.minerals > 200:
                        p = await self.find_placement(UnitTypeId.SUPPLYDEPOT, near=cc.random.position)
                        if e.closer_than(5, p).exists:
                            p = p.towards(e.closest_to(p).position, -5)
                        if not e.closer_than(5, p).exists:
                            await self.build(UnitTypeId.SUPPLYDEPOT, p)
                            # print("SUPPLYDEPOT")
                        if self.minerals > 300:
                            p = await self.find_placement(UnitTypeId.SUPPLYDEPOT, near=cc.random.position)
                            if e.closer_than(5, p).exists:
                                p = p.towards(e.closest_to(p).position, -5)
                            if not e.closer_than(5, p).exists:
                                await self.build(UnitTypeId.SUPPLYDEPOT, p)
                                # print("SUPPLYDEPOT")
            elif self.supply_left < 0 and self.can_afford(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)
                """most code here is untested"""

    async def GMReplaceExpand(self, ccmax: int, ocbuffer: int, barrcksmin: int, factorymin: int, starportmin: int, ebaymin: int, armorymin: int, ghostacademymin: int, fcoremin:int,barrackmax: int, factorymax: int, starportmax: int):
        scv = self.quarryUnits(UnitTypeId.SCV)
        building = self.quarryStructures
        cc = building(UnitTypeId.COMMANDCENTER) | building(UnitTypeId.ORBITALCOMMAND) | building(UnitTypeId.COMMANDCENTERFLYING) | building(UnitTypeId.ORBITALCOMMANDFLYING)
        oc = building(UnitTypeId.ORBITALCOMMAND) | building(UnitTypeId.ORBITALCOMMANDFLYING)
        sd = building(UnitTypeId.SUPPLYDEPOT) | building(UnitTypeId.SUPPLYDEPOTLOWERED)
        b = building(UnitTypeId.BARRACKS) | building(UnitTypeId.BARRACKSFLYING)
        f = building(UnitTypeId.FACTORY) | building(UnitTypeId.FACTORYFLYING)
        s = building(UnitTypeId.STARPORT) | building(UnitTypeId.STARPORTFLYING)
        e = building(UnitTypeId.ENGINEERINGBAY)
        a = building(UnitTypeId.ARMORY)

        if sd.ready.exists and cc.exists and b.amount < barrcksmin and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS) and not self.needToExpand:
            # print("NO UnitTypeId.BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.BARRACKS, near=p)

        if b.ready.exists and cc.exists and f.amount < factorymin and not self.already_pending(UnitTypeId.FACTORY) and self.can_afford(UnitTypeId.FACTORY) and not self.needToExpand:
            # print("NO UnitTypeId.FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.FACTORY, near=p)

        if f.ready.exists and cc.exists and s.amount < starportmin and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT) and not self.needToExpand:
            # print("NO UnitTypeId.STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.STARPORT, near=p)

        if sd.exists and cc.exists and not self.already_pending(UnitTypeId.ENGINEERINGBAY) and e.amount < ebaymin and self.can_afford(UnitTypeId.ENGINEERINGBAY) and self.supply_left > 6 and not self.needToExpand:
            # print("NO UnitTypeId.ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.ENGINEERINGBAY, near=p)

        if f.ready.exists and cc.exists and a.amount < armorymin and not self.already_pending(UnitTypeId.ARMORY) and self.can_afford(UnitTypeId.ARMORY) and self.supply_left > 6 and not self.needToExpand:
            # print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(UnitTypeId.ARMORY, near=p)

        if self.minerals > 200 + (cc.amount * 100) and self.can_afford(UnitTypeId.COMMANDCENTER) and not cc.flying.exists and cc.amount < ccmax and not self.already_pending(UnitTypeId.COMMANDCENTER):
            # print("expand")
            p = self.start_location
            await self.build(UnitTypeId.COMMANDCENTER, near=p)

        if self.can_afford(UnitTypeId.COMMANDCENTER) and not cc.flying.exists and cc.amount < ccmax and not self.already_pending(UnitTypeId.COMMANDCENTER) and self.nextXpansionLocation:
            # print("expand")
            p = self.start_location
            await self.build(UnitTypeId.COMMANDCENTER, near=p) # sub-function is not redundant.

        if oc.amount >= ocbuffer:
            if s.amount < starportmax and cc.exists and not self.already_pending(UnitTypeId.STARPORT) and self.can_afford(UnitTypeId.STARPORT) and self.supply_left > 5 and not self.needToExpand and not s.flying.exists:
                # print("NOT ENOUGH UnitTypeId.STARPORT")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(UnitTypeId.STARPORT, near=p)

            if f.amount < factorymax and cc.exists and not self.already_pending(UnitTypeId.FACTORY) and cc.amount >= ocbuffer and self.can_afford(UnitTypeId.FACTORY) and self.supply_left > 5 and not self.needToExpand and not s.flying.exists:
                # print("NOT ENOUGH UnitTypeId.FACTORY")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(UnitTypeId.FACTORY, near=p)

            if b.amount < barrackmax and cc.exists and not self.already_pending(UnitTypeId.BARRACKS) and self.can_afford(UnitTypeId.BARRACKS) and not self.needToExpand and not b.flying.exists:
                # print("NOT ENOUGH UnitTypeId.BARRACKS")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(UnitTypeId.BARRACKS, near=p)

    async def GEAntiAirHarras(self, distance: float):
        if not self.already_pending(UnitTypeId.ENGINEERINGBAY) and not self.already_pending(UnitTypeId.MISSILETURRET):
            scv = self.quarryUnits(UnitTypeId.SCV)
            m = self.quarryUnits(UnitTypeId.MISSILETURRET)
            cc = self.quarryUnits(UnitTypeId.COMMANDCENTER) | self.quarryUnits(UnitTypeId.ORBITALCOMMAND)
            if cc.exists and scv.exists and self.can_afford(UnitTypeId.ENGINEERINGBAY):
                scv1 = scv.random
                if not self.quarryStructures(UnitTypeId.ENGINEERINGBAY).exists:
                    p = scv1.position.towards(self.start_location, 10)
                    p = await self.find_placement(UnitTypeId.ENGINEERINGBAY, near=p)
                    scv1.build(UnitTypeId.ENGINEERINGBAY, p)
                else:
                    m = self.quarryStructures(UnitTypeId.MISSILETURRET).closer_than(distance, scv1.position)
                    if not m.exists:
                        p = scv1.position
                        scv1.build(UnitTypeId.MISSILETURRET, p)

    """async def GMLandIdleBuildings(self, supplyBuffer: int): # This needs to be reworked
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER) | self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        b = self.quarryStructures(UnitTypeId.BARRACKSFLYING).idle
        f = self.quarryStructures(UnitTypeId.FACTORYFLYING).idle
        s = self.quarryStructures(UnitTypeId.STARPORTFLYING).idle
        e = self.quarryStructures(UnitTypeId.REACTOR) | self.quarryStructures(UnitTypeId.TECHLAB)
        if b.exists and self.supply_left >= supplyBuffer:
            if not self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists:
                b1 = b.random
                p = b1.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                if p != self.start_location:
                    p = p.towards(self.start_location, 10)
                b1.move(p)
                if self.can_afford(UnitTypeId.BARRACKSTECHLAB) and self.can_afford(UnitTypeId.BARRACKS):
                    p = await self.find_placement(UnitTypeId.BARRACKS, near=p.position)
                    if cc.exists:
                        p = p.towards(cc.closest_to(p).position, -2)
                    if e.exists:
                        p = p.towards(e.closest_to(p).position, -6)
                    b1.build(UnitTypeId.BARRACKSTECHLAB, near=p)
                    # print("LAND B_TECHLAB")
            elif not self.quarryStructures(UnitTypeId.REACTOR).exists:
                for b2 in b:
                    p = b2.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                    if p != self.start_location:
                        p = p.towards(self.start_location, 5)
                    b2.move(p)
                    if self.can_afford(UnitTypeId.BARRACKSREACTOR) and self.can_afford(UnitTypeId.BARRACKS):
                        p = await self.find_placement(UnitTypeId.BARRACKS, near=p.position)
                        if cc.exists:
                            p = p.towards(cc.closest_to(p).position, -3)
                        if e.exists:
                            p = p.towards(e.closest_to(p).position, -6)
                        b2.build(UnitTypeId.BARRACKSREACTOR, p)
                        # print("LAND B_TECHLAB")
        if f.exists and self.supply_left >= supplyBuffer:
            if not self.quarryStructures(UnitTypeId.TECHLAB).exists:  # Zerg does not gain replacement reactors intentionally
                for f2 in f:
                    p = f2.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                    if p != self.start_location:
                        p = p.towards(self.start_location, 5)
                    f2.move(p)
                    if self.can_afford(UnitTypeId.FACTORY):
                        p = await self.find_placement(UnitTypeId.FACTORY, near=f2.position)
                        if cc.exists:
                            p = p.towards(cc.closest_to(p).position, -3)
                        if e.exists:
                            p = p.towards(e.closest_to(p).position, -6)
                        f2.build(UnitTypeId.FACTORYTECHLAB, p)
                        # print("LAND F_TECHLAB")
        if s.exists and self.supply_left >= supplyBuffer:
            if not self.quarryStructures(UnitTypeId.REACTOR).exists:
                s1 = s.random
                p = s1.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                if p != self.start_location:
                    p = p.towards(self.start_location, 5)
                s1.move(p)
                if self.can_afford(UnitTypeId.STARPORT):
                    p = await self.find_placement(UnitTypeId.STARPORT, near=s1.position)
                    if cc.exists:
                        p = p.towards(cc.closest_to(p).position, -3)
                    if e.exists:
                        p = p.towards(e.closest_to(p).position, -6)
                    p = p.towards(self.quarryStructures.furthest_to(self.start_location).position, 5)
                    s1.build(UnitTypeId.STARPORTREACTOR, p)
                    # print("LAND S_UnitTypeId.REACTORLAB")
            else:
                for s2 in s:
                    p = s2.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                    if p != self.start_location:
                        p = p.towards(self.start_location, 5)
                    s2.move(p)
                    if self.can_afford(UnitTypeId.STARPORT):
                        p = await self.find_placement(UnitTypeId.STARPORT, near=s2.position)
                        if cc.exists:
                            p = p.towards(cc.closest_to(p).position, -3)
                        if e.exists:
                            p = p.towards(e.closest_to(p).position, -6)
                        s2.build(UnitTypeId.STARPORTTECHLAB, p)
                        # print("LAND S_TECHLAB")"""

    async def GELandCommandCenter(self):
        for cc in self.quarryStructures(UnitTypeId.COMMANDCENTERFLYING).idle | self.quarryStructures(UnitTypeId.ORBITALCOMMANDFLYING).idle:
            p = self.nextXpansionLocation
            #cc.move(p))
            cc(AbilityId.LAND, p)
            #p = self.nextXpansionLocation I don't know why this was here twice
            m = self.mineral_field | self.vespene_geyser
            if m.exists:
                m1 = m.closest_to(p).position
                p2 = p.towards(m1, -.5)
                self.nextXpansionLocation = p2
                e = self.quarryEnemyUnit.closer_than(15, self.nextXpansionLocation)
                if e.exists:
                    self.nextXpansionLocation = await self.get_next_expansion()
                    p3 = cc.position.towards(e.random.position, -1)
                    cc.move(p3)
        #if (self.quarryStructures(UnitTypeId.COMMANDCENTERFLYING).idle | self.quarryStructures(UnitTypeId.ORBITALCOMMANDFLYING).idle).exists:
        #    await self.GMResetNextXpansionLocation()

    async def GEInBaseCommandCenter(self):
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER).ready | self.quarryStructures(UnitTypeId.ORBITALCOMMAND) #  not flying
        ccflying = self.quarryStructures(UnitTypeId.COMMANDCENTERFLYING) | self.quarryStructures(UnitTypeId.ORBITALCOMMANDFLYING)
        min = self.mineral_field
        if cc.amount > 1:
            for c in cc.idle:
                cp = c.position
                ccc = cc.further_than(1, cp)#.closer_than(15, cp)
                c2 = ccc.closest_to(c.position).position
                if cp != self.start_location and min.exists:
                    m = min.closest_to(cp.towards(self.start_location, 4)).position
                else:
                    m = self.start_location
                #m = self.start_location # getting error despite checking to make sure min exists for min neing empty. Hack Fix
                a = cp.distance_to(m)
                b = c2.distance_to(m)
                if a > b:
                    self.nextXpansionLocation = await self.get_next_expansion()
                    c(AbilityId.LIFT)

    """async def GMAddonAbductBuilding(self):
        b = self.quarryStructures(UnitTypeId.BARRACKSFLYING)
        f = self.quarryStructures(UnitTypeId.FACTORYFLYING)
        s = self.quarryStructures(UnitTypeId.STARPORTFLYING)
        a = b|f|s
        t = self.quarryStructures(UnitTypeId.TECHLAB)
        r = self.quarryStructures(UnitTypeId.REACTOR)

        if t.exists and f.exists and self.supply_left > 3:
            # print("REPLACE TECHLAB SPOT TRY DO")
            p = t.closest_to(self.start_location).add_on_land_position
            fp = f.closest_to(p)
            fp(AbilityId.LAND, p)

        if t.exists and s.exists and not self.quarryStructures(UnitTypeId.STARPORTTECHLAB).exists and self.supply_left > 3:
            # print("REPLACE TECHLAB SPOT TRY DO")
            p = t.closest_to(self.start_location).add_on_land_position
            sp = s.closest_to(p)
            sp(AbilityId.LAND, p)

        if b.exists and t.exists and not self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists and self.supply_left > 3:
            # print("REPLACE TECHLAB SPOT TRY DO")
            p = t.closest_to(self.start_location).add_on_land_position
            bp = b.closest_to(p)
            bp(AbilityId.LAND, p)

        if s.exists and r.exists and not self.quarryStructures(UnitTypeId.REACTOR).exists and self.supply_left > 5:
            # print("REPLACE UnitTypeId.REACTOR SPOT TRY DO")
            p = r.closest_to(self.start_location).add_on_land_position
            sp = s.closest_to(p)
            sp(AbilityId.LAND, p)

        if r.exists and b.exists and self.supply_left > 3:
            # print("REPLACE UnitTypeId.REACTOR SPOT TRY DO")
            p = r.closest_to(self.start_location).add_on_land_position
            bp = b.closest_to(p)
            bp(AbilityId.LAND, p)"""

    """async def GEBuildingDodge(self, range: float): #redundant
        a = self.quarryStructures
        b = a(UnitTypeId.BARRACKSFLYING) | a(UnitTypeId.FACTORYFLYING) | a(UnitTypeId.STARPORTFLYING)
        c = a(UnitTypeId.COMMANDCENTERFLYING) | a(UnitTypeId.ORBITALCOMMANDFLYING)
        e = self.quarryEnemyUnit
        if e.exists:
            for aa in b:
                ap = aa.position
                ep = e.closest_to(ap).position
                d = ap.distance_to(ep)
                if d != 0 and d < range:
                    p = ep.towards(ap, range + 1)
                    aa.move(p)
            for cc in c:
                cp = cc.position
                ep = e.closest_to(cp).position
                d = cp.distance_to(ep)
                if d != 0 and d < range:
                    p = ep.towards(cp, range + 1)
                    cc.move(p)
                    self.nextXpansionLocation = await self.get_next_expansion()"""

    # Ground Building Commands
    async def GECommandCenter(self):
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER).ready | self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        ccflying = self.quarryStructures(UnitTypeId.COMMANDCENTERFLYING) | self.quarryStructures(UnitTypeId.ORBITALCOMMANDFLYING)
        for c in cc.idle:
            m = self.mineral_field
            minnear = m.closer_than(15, c.position)
            cc2 = cc.further_than(3, c.position).closer_than(15, c.position)
            if not self.quarryUnits(UnitTypeId.SCV).exists and not minnear.exists and not ccflying.exists:
                c(AbilityId.LIFT)
                p = await self.get_next_expansion()
                if m.exists:
                    m1 = m.closest_to(p).position
                    # print(m1)
                    p2 = m1.towards(p, 5)
                    # print(p2)
                    self.nextXpansionLocation = p2
        for c in cc(UnitTypeId.COMMANDCENTER).idle:
            ccc = cc.further_than(1, c.position).closer_than(10, c.position)
            if self.quarryStructures(UnitTypeId.BARRACKS).ready.exists and self.can_afford(UnitTypeId.ORBITALCOMMAND) and not ccc.exists:
                c(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
            elif self.can_afford(UnitTypeId.SCV) and self.quarryUnits(UnitTypeId.SCV).amount < (cc.amount*20) + 10 and self.quarryUnits(UnitTypeId.SCV).amount < 70 and self.quarryUnits(UnitTypeId.SCV).closer_than(20, c).amount < 24 and self.supply_left > 0:
                c.train(UnitTypeId.SCV)

    async def GEOrbitalCommand(self):
        oc = self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        flyingcc = self.quarryStructures(UnitTypeId.COMMANDCENTERFLYING) | self.quarryStructures(UnitTypeId.ORBITALCOMMANDFLYING)
        for o in oc.ready.idle:
            scv = self.quarryUnits(UnitTypeId.SCV).closer_than(10, o)
            m = self.mineral_field.closer_than(15, o)
            if not scv.exists and not m.exists and not flyingcc.exists:
                o(AbilityId.LIFT)
                p = await self.get_next_expansion()
                m = self.mineral_field
                if m.exists:
                    m1 = m.closest_to(p).position
                    
                    # print(m1)
                    p2 = m1.towards(p, 5)
                    # print(p2)
                    self.nextXpansionLocation = p2
            elif self.can_afford(UnitTypeId.SCV) and self.quarryUnits(UnitTypeId.SCV).amount < 65 and self.quarryUnits(UnitTypeId.SCV).closer_than(20, o.position).amount < 24:
                o.train(UnitTypeId.SCV)
        for o in oc.ready:
            if o.energy == 200:
                a = self.quarryUnits
                if a.exists:
                    aa = a.furthest_to(o.position).position
                    o(AbilityId.SCANNERSWEEP_SCAN, aa.offset((random.randint(-5, 5), random.randint(-5, 5))))
            elif o.energy > 100 and self.quarryEnemyStructure.amount == 0:
                o(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])  # can be improved with random
                o(AbilityId.SCANNERSWEEP_SCAN, self.mineral_field.random.position)
                # print("SCAN SEARCH")
            elif o.energy >= 50:
                m = self.mineral_field.closer_than(15, o.position)
                if m.amount >= 6:
                    o(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)
                    # print("mule")

    async def GEBarracks(self, techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int):
        if not self.needToExpand:
            for b in self.quarryStructures(UnitTypeId.BARRACKS).ready.idle:
            # if a(UnitTypeId.BARRACKS).ready.idle.exists:
                # b = a(UnitTypeId.BARRACKS).ready.idle.random
                m1 = self.quarryUnits(UnitTypeId.MARINE).amount
                m2 = self.quarryUnits(UnitTypeId.MARAUDER).amount
                r = self.quarryUnits(UnitTypeId.REAPER).amount # Gen 2 comment: uhm what? This bot doesn't make ghost and was never in scope
                g = self.quarryUnits(UnitTypeId.GHOST).amount
                if self.time > 240 and b.add_on_tag == 0:
                    b(AbilityId.LIFT)
                elif self.time > 240 and self.supply_left == 0 and not techlabresearch:
                    b(AbilityId.LIFT)
                elif self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists and self.supply_left > 0:
                    id = self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).random.tag
                    if b.add_on_tag == id:
                        if self.can_afford(UnitTypeId.MARAUDER) and m2 < maxmarauder:
                            b.train(UnitTypeId.MARAUDER)
                        elif self.can_afford(UnitTypeId.GHOST) and g < maxghost and self.quarryStructures(UnitTypeId.GHOSTACADEMY).ready.exists:
                            b.train(UnitTypeId.GHOST)
                        elif self.can_afford(UnitTypeId.REAPER) and r < maxreaper:
                            b.train(UnitTypeId.REAPER)
                        elif self.can_afford(UnitTypeId.MARINE) and m1 < maxmarine:
                            b.train(UnitTypeId.MARINE)
                    elif b.add_on_tag == 0:
                        if self.can_afford(UnitTypeId.BARRACKSREACTOR):
                            p = b.position.offset((2.5, -.5))
                            if await self.can_place(UnitTypeId.AUTOTURRET, p):
                                # print("B_UnitTypeId.REACTOR")
                                b.build(UnitTypeId.BARRACKSREACTOR)
                            else:
                                b(AbilityId.LIFT)

                        elif self.can_afford(UnitTypeId.MARINE) and m1 < maxmarine:
                            b.train(UnitTypeId.MARINE)
                    else:
                        if self.can_afford(UnitTypeId.REAPER) and  r < maxreaper:
                            b.train(UnitTypeId.REAPER)
                            if self.can_afford(UnitTypeId.REAPER):
                                b.train(UnitTypeId.REAPER)
                            elif self.can_afford(UnitTypeId.MARINE) and m1 < maxmarine:
                                b.train(UnitTypeId.MARINE)
                        else:
                            if self.can_afford(UnitTypeId.MARINE) and m1 < maxmarine:
                                b.train(UnitTypeId.MARINE)
                            if self.can_afford(UnitTypeId.MARINE):
                                b.train(UnitTypeId.MARINE)
                elif self.can_afford(UnitTypeId.BARRACKSTECHLAB) and not self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists:
                    b.build(UnitTypeId.BARRACKSTECHLAB)
                    # print("B_TECHLAB")
                elif techlabresearch:
                    if self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists:
                        id = self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).random.tag
                        #if b.add_on_tag == id:
                            # print("No Lift")
                        #else:
                        #    b(AbilityId.LIFT)
                        if not b.add_on_tag == id:
                            b(AbilityId.LIFT)

    async def GEFactory(self, techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int):
        if not self.needToExpand:
            work = True
            for f in self.quarryStructures(UnitTypeId.FACTORY).ready.idle:
            #if a(UnitTypeId.FACTORY).ready.idle.exists:
                #f = a(UnitTypeId.FACTORY).ready.idle.random
                s = (self.quarryUnits(UnitTypeId.SIEGETANK) | self.quarryUnits(UnitTypeId.SIEGETANKSIEGED)).amount
                h = (self.quarryUnits(UnitTypeId.HELLION) | self.quarryUnits(UnitTypeId.HELLIONTANK)).amount
                w = (self.quarryUnits(UnitTypeId.WIDOWMINE) | self.quarryUnits(UnitTypeId.WIDOWMINEBURROWED)).amount
                id = 0
                if self.quarryStructures(UnitTypeId.FACTORYREACTOR).exists:
                    if not allowreactor:
                        work = False
                    else:
                        id = self.quarryStructures(UnitTypeId.FACTORYREACTOR).random.tag
                if not work:
                    f(AbilityId.LIFT)
                elif self.supply_left > 2 and f.add_on_tag != id:
                    if self.time > 240 and f.add_on_tag == 0:
                        f(AbilityId.LIFT)
                    elif self.time <= 240 and f.add_on_tag == 0:
                        (f.build(UnitTypeId.FACTORYTECHLAB))
                        # add code if a different build is used that gets a factory before 3:30

                    elif self.can_afford(UnitTypeId.SIEGETANK) and s < maxmsiegetank:
                        f.train(UnitTypeId.SIEGETANK)
                    elif self.can_afford(UnitTypeId.HELLION) and h < maxhellion:
                        f.train(UnitTypeId.HELLION)
                    elif self.can_afford(UnitTypeId.WIDOWMINE) and w <maxwidowmine:
                        f.train(UnitTypeId.WIDOWMINE)
                #elif self.supply_left > 2 and f.add_on_tag == id and id != 0:
                    # await self.chat_send("NO CODE")
                    # code here when get to reactor/hellion/widowmine code
                else:
                    f(AbilityId.LIFT)
                    # print("FLY!!!")

    """async def GMStarport(self, techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int):
        if not self.needToExpand:
            m = self.quarryUnits(UnitTypeId.MEDIVAC).amount
            v = self.quarryUnits(UnitTypeId.VIKINGFIGHTER).amount
            l = self.quarryUnits(UnitTypeId.LIBERATOR).amount
            r = self.quarryUnits(UnitTypeId.RAVEN).amount
            id = 0 # I don't know why we're using tags
            if self.quarryUnits(UnitTypeId.STARPORTTECHLAB).exists:
                id = self.quarryStructures(UnitTypeId.STARPORTTECHLAB).random.tag
            for s in self.quarryStructures(UnitTypeId.STARPORT).ready.idle:
                if s.add_on_tag == 0:
                    s(AbilityId.LIFT)
                elif self.supply_left < 4:
                    s(AbilityId.LIFT)
                if s.add_on_tag != id and self.supply_left > 4:
                    if self.can_afford(UnitTypeId.MEDIVAC) and m < maxmedivac:
                        s.train(UnitTypeId.MEDIVAC)
                        if self.can_afford(UnitTypeId.MEDIVAC):
                            s.train(UnitTypeId.MEDIVAC)
                    elif v < maxviking:
                        if self.can_afford(AbilityId.STARPORTTRAIN_VIKINGFIGHTER):
                            s(AbilityId.STARPORTTRAIN_VIKINGFIGHTER)
                            if self.can_afford(AbilityId.STARPORTTRAIN_VIKINGFIGHTER):
                                s(AbilityId.STARPORTTRAIN_VIKINGFIGHTER)
                    elif l < maxliberator:
                        if self.can_afford(AbilityId.STARPORTTRAIN_LIBERATOR):
                            s(AbilityId.STARPORTTRAIN_LIBERATOR)
                            if self.can_afford(AbilityId.STARPORTTRAIN_LIBERATOR):
                                s(AbilityId.STARPORTTRAIN_LIBERATOR)
                elif self.supply_left > 2 and r < maxraven:
                    if self.can_afford(UnitTypeId.RAVEN):
                        s.train(UnitTypeId.RAVEN)
                # add code here for battlecruiser or banshee?
                elif self.supply_left > 2 and l < maxliberator:
                    if self.can_afford(AbilityId.STARPORTTRAIN_LIBERATOR):
                        s(AbilityId.STARPORTTRAIN_LIBERATOR)
                elif self.supply_left > 2 and l < maxviking:
                    if self.can_afford(AbilityId.STARPORTTRAIN_VIKINGFIGHTER):
                        s(AbilityId.STARPORTTRAIN_VIKINGFIGHTER)
                elif self.supply_left > 2 and l < maxmedivac:
                    if self.can_afford(UnitTypeId.MEDIVAC):
                        s.train(UnitTypeId.MEDIVAC)"""

    async def GMEngineeringBay(self):
        for e in self.quarryStructures(UnitTypeId.ENGINEERINGBAY).ready.idle.idle:
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

    async def GMArmory(self, air: bool):
        for a in self.quarryStructures(UnitTypeId.ARMORY).ready.idle.idle:
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
            elif air:
                if await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1):
                    a(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1)
                elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2):
                    a(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2)
                elif await self.can_cast(a, AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3) and self.can_afford(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3):
                    a(AbilityId.ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3)

    async def GMBTechlab(self):
        bt = self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).ready.idle
        if bt.exists:
            bt1 = bt.first
            if await self.can_cast(bt1, AbilityId.RESEARCH_COMBATSHIELD) and self.can_afford(AbilityId.RESEARCH_COMBATSHIELD):
                bt1(AbilityId.RESEARCH_COMBATSHIELD)
                # print("UPGRADE_SHIELD")
            elif await self.can_cast(bt1, AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK) and self.can_afford(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK):
                bt1(AbilityId.BARRACKSTECHLABRESEARCH_STIMPACK)
                # print("UPGRADE_STIMPACK")

    async def GEsupplydepotdown(self):
        for sd in self.quarryStructures(UnitTypeId.SUPPLYDEPOT).ready:
            e = self.quarryEnemyUnit.closer_than(8, sd.position).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

    async def GEsupplydepotup(self):
        for sd in self.quarryStructures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            e = self.quarryEnemyUnit.closer_than(10, sd.position).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            a = self.quarryUnits.not_flying.closer_than(1.5, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists and not a.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_RAISE)

    async def GEUnfinishedBuildingCheck(self):
        if self.quarryUnits(UnitTypeId.SCV).exists:
            for a in self.quarryStructures.not_ready.exclude_type(UnitTypeId.REACTOR).exclude_type(UnitTypeId.BARRACKSREACTOR).exclude_type(UnitTypeId.FACTORYREACTOR).exclude_type(UnitTypeId.STARPORTREACTOR).exclude_type(UnitTypeId.TECHLAB).exclude_type(UnitTypeId.BARRACKSTECHLAB).exclude_type(UnitTypeId.FACTORYTECHLAB).exclude_type(UnitTypeId.STARPORTTECHLAB):
                scvclose = self.quarryUnits(UnitTypeId.SCV).closer_than(4, a.position)
                e = self.quarryEnemyUnit.closer_than(6, a.position)
                if a.health_percentage < .3 and e.amount > a.health_percentage * 10:
                    a(AbilityId.CANCEL_BUILDINPROGRESS)
                if not scvclose.exists:
                    a(AbilityId.CANCEL_BUILDINPROGRESS)

    async def GEBuildingLift(self, distance: float, number: int):
        a = self.quarryStructures.ready.idle
        army = self.quarryUnits.not_flying.exclude_type(UnitTypeId.SCV)
        b = a(UnitTypeId.BARRACKS) | a(UnitTypeId.FACTORY) | a(UnitTypeId.STARPORT)
        c = a(UnitTypeId.COMMANDCENTER) | a(UnitTypeId.ORBITALCOMMAND)
        e = self.quarryEnemyUnit.not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
        for aa in b:
            ee = e.closer_than(distance, aa.position)
            army = army.closer_than(distance + 1, aa.position)
            if ee.amount >= number + army.amount:
                aa(AbilityId.LIFT)
        for cc in c:
            ee = e.closer_than(distance, cc.position)
            army = army.closer_than(distance + 1, cc.position)
            if ee.amount >= number + army.amount:
                cc(AbilityId.LIFT)
                self.nextXpansionLocation = cc.position

    # Macro Commands
    async def GMUpdateNeedToExpand(self):
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER) | self.quarryStructures(UnitTypeId.ORBITALCOMMAND) | self.quarryStructures(UnitTypeId.COMMANDCENTERFLYING) | self.quarryStructures(UnitTypeId.ORBITALCOMMANDFLYING)
        if cc.amount == 0 and self.can_afford(UnitTypeId.COMMANDCENTER):
            self.needToExpand = True
            # await self.chat_send("(gg)")
        elif self.supply_used == 100 and cc.amount < 3:
            self.needToExpand = True
            # # await self.chat_send("problem 1")
        else:
            i = 0
            for c in cc:
                s = self.quarryUnits(UnitTypeId.SCV).closer_than(20, c.position).amount
                m = self.mineral_field.closer_than(25, c.position).amount
                i = i + (s)
                i = i - (m*3)
            if i > 0:
                self.needToExpand = True
                # # await self.chat_send("problem 2")
        if cc.flying.exists:
            self.needToExpand = False
        elif self.already_pending(UnitTypeId.COMMANDCENTER):
            self.needToExpand = False
        elif cc.not_ready.exists:
            self.needToExpand = False
        elif cc.amount == 5:
            self.needToExpand = False

    async def GMResetNextXpansionLocation(self):
        self.nextXpansionLocation = await self.get_next_expansion()
        self.nextXpansionLocation = self.nextXpansionLocation.offset((random.randint(-1,1), random.randint(-1,1)))
        if self.can_afford(UnitTypeId.COMMANDCENTER):
            p = await self.find_placement(UnitTypeId.COMMANDCENTER, near = self.nextXpansionLocation)
            if p != self.nextXpansionLocation:
                self.nextXpansionLocation = self.nextXpansionLocation.towards(p, 2.5)
                m = (self.mineral_field | self.vespene_geyser).closer_than(12, self.nextXpansionLocation)
                for mm in m:
                    p = mm.position
                    self.nextXpansionLocation = self.nextXpansionLocation.towards(p, .1)

    async def get_next_expansion(self):
        # method name doesn't match naming convention because of overriding preexisting method
        p = self.start_location
        m = self.mineral_field
        mremove = self.mineral_field.closer_than(0, p)
        v = self.vespene_geyser
        cc = self.quarryStructures
        cc = cc(UnitTypeId.COMMANDCENTER) | cc(UnitTypeId.ORBITALCOMMAND)
        e = self.quarryEnemyStructure
        for m1 in m:
            if e.closer_than(15, m1.position).exists:
                mremove.append(m1)
            elif cc.closer_than(15, m1.position).exists:
                mremove.append(m1)
        for m1 in mremove:
            m.remove(m1)
        if m.exists:
            p = m.closest_to(p).position
            a = v.closer_than(14, p) | self.mineral_field.closer_than(14, p)
            for m2 in a:
                p2 = m2.position
                if p2 != p:
                    p = p.towards(p2, .3)
        return p

    async def GECheckEnemy(self):
        e = self.quarryEnemyUnit
        if e.exists:
            ea = e.closest_to(self.start_location)
            if ea.race == Race.Terran:
                # print("change to terran")
                self.STRAT = "AntiTerran"
                if self.time < 360 and not self.airHarrass:
                    if e(UnitTypeId.BANSHEE).exists or e(UnitTypeId.STARPORTTECHLAB).exists:
                        self.airHarrass = True
                        # await self.chat_send("NO CLOAK BANSHEES!!!")
                else:
                    self.airHarass = False
                if self.time < 360 and not self.earlyArmor:
                    if (e(UnitTypeId.MARAUDER) | e(UnitTypeId.SIEGETANK) | e(UnitTypeId.SIEGETANKSIEGED)).amount > 8:
                        self.earlyArmor = True
            elif ea.race == Race.Zerg:
                # print("change to zerg")
                self.STRAT = "AntiZerg"
                if self.time < 360 and not self.airHarrass:
                    if e(UnitTypeId.MUTALISK).exists or e(UnitTypeId.SPIRE).exists:
                        self.airHarrass = True
                        # await self.chat_send("NO CLOAK MUTALISK!!!")
                else:
                    self.airHarass = False
                if self.time < 360 and not self.earlyArmor:
                    if (e(UnitTypeId.ROACH)).amount > 8:
                        self.earlyArmor = True
            elif ea.race == Race.Protoss:
                # print("change to protoss")
                self.STRAT = "AntiProtoss"
                if self.time < 360 and not self.airHarrass:
                    if e(UnitTypeId.ORACLE).exists or e(UnitTypeId.PHOENIX).exists or e(UnitTypeId.STARPORT).exists:
                        self.airHarrass = True
                        # await self.chat_send("NO PHOENIX OR ORACLE!!!")
                else:
                    self.airHarass = False
                if self.time < 360 and not self.earlyArmor:
                    if (e(UnitTypeId.STALKER) | e(UnitTypeId.IMMORTAL) | e(UnitTypeId.COLOSSUS)).amount > 8:
                        self.earlyArmor = True

    async def GMOrbitalScans(self, attack: bool, distance: float):
        o = self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        if o.exists:
            oo = o.random
            a = self.quarryUnits.further_than(distance, oo.position).exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.REAPER).exclude_type(UnitTypeId.WIDOWMINEBURROWED)
            e = self.quarryEnemyUnit # this includes structures
            if oo.energy > 50 and a.exists and e.exists:
                ap = a.furthest_to(oo.position).position.towards(e.closest_to(oo.position).position, 10)
                oo(AbilityId.SCANNERSWEEP_SCAN, ap)
                e2 = self.quarryEnemyUnit.closer_than(16, ap)
                if e2.exists and attack:
                    e2p = e2.random.position
                    for aa in a.closer_than(25, ap):
                        aa.attack(e2p)

    async def GMPremptiveInvisibleCheck(self):
        e = self.quarryEnemyUnit
        e = e(UnitTypeId.BANSHEE) | e(UnitTypeId.GHOST) | e(UnitTypeId.WIDOWMINE) | e(UnitTypeId.WIDOWMINEBURROWED) | e(UnitTypeId.LURKERMP) | e(UnitTypeId.SWARMHOSTMP) | e(UnitTypeId.MOTHERSHIP)
        if e.exists:
            oc = self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
            if oc.exists:
                oc = oc.random
                if oc.energy > 50:
                    oc(AbilityId.SCANNERSWEEP_SCAN, e.random.position)

    async def GMInvisibleTrack(self):
        e = self.quarryEnemyUnit
        for ee in e:
            if not ee.is_visible:
                oc = self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
                if oc.exists:
                    oc = oc.random
                    if oc.energy > 50:
                        oc(AbilityId.SCANNERSWEEP_SCAN, e.random.position)

    async def GMDefend(self):
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER) | self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        for c in cc:
            threat = self.quarryEnemyUnit.closer_than(25, c.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE).exclude_type(UnitTypeId.OVERSEER).exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.PROBE)
            if threat.exists:
                army = self.quarryUnits(UnitTypeId.MARINE) | self.quarryUnits(UnitTypeId.MARAUDER) | self.quarryUnits(UnitTypeId.SIEGETANK) | self.quarryUnits(UnitTypeId.HELLION) | self.quarryUnits(UnitTypeId.VIKINGFIGHTER)
                p = threat.random.position
                for a in army:
                    a.attack(p)

    async def GERally(self):
        b = self.quarryStructures.exclude_type(UnitTypeId.COMMANDCENTER).exclude_type(UnitTypeId.ORBITALCOMMAND)
        if b.exists:
            p = b.furthest_to(self.start_location).position
            if p != self.start_location:
                p = p.towards(self.start_location, 3)
            for a in b:
                a(AbilityId.RALLY_BUILDING, p)

    async def GMRally(self, distance: float, move: float):
        building = self.quarryStructures(UnitTypeId.SUPPLYDEPOT) | self.quarryStructures(UnitTypeId.SUPPLYDEPOTLOWERED) | self.quarryStructures(UnitTypeId.COMMANDCENTER) | self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        if self.quarryEnemyStructure.exists and building.exists:
            e = building.closest_to(self.quarryEnemyStructure.closest_to(self.start_location).position).position
            if e != self.game_info.map_center:
                e = e.towards(self.game_info.map_center, move)
            self.RallyPoint = building.closest_to(e).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        else:
            self.RallyPoint = self.start_location
        for a in self.quarrySelf.idle.not_flying.exclude_type(UnitTypeId.HELLION):
            if a.distance_to(self.RallyPoint) > distance:
                p = self.RallyPoint.offset((random.randint(-distance, distance), random.randint(-distance, distance)))
                a.attack(p)

    async def GMGeneralAttackTriggers(self, minwave: int, bubblesize: float):
            # Note: Poor letter choosing for variables is because I was too lazy to write a method twice and this mostly copy pasted from the AntiZerg equivelant method.
            M1 = self.quarryUnits(UnitTypeId.MARINE)
            M2 = self.quarryUnits(UnitTypeId.MARAUDER)
            S = self.quarryUnits(UnitTypeId.SIEGETANK)
            A = M1 | M2 | S
            e = self.notSafeUnit | self.quarryEnemyStructure
            if e.exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.PROBE).exclude_type(UnitTypeId.OVERSEER).exists:
                p = e.closest_to(self.start_location).position
                if self.supply_used > 190:
                    for m in A:
                        if A.closer_than(bubblesize, m.position).amount >= minwave:
                            m.attack(p)
                    # print("Supply Attack")
                    if not self.enemyknown:
                        self.enemyknown = True
                        # await self.chat_send("Here's Moth Bot")
            else:
                if self.supply_used > 190:
                    for m in A.idle:
                        if A.closer_than(bubblesize, m.position).amount >= minwave:
                            p = self.enemy_start_locations[0]
                            i = self.mineral_field
                            if i.exists:
                                p = i.random.position
                            m.attack(p)
                    # print("enemy not found")
                    # await self.chat_send("All scouting and no play makes MothBot a dull AI")
                    await self.chat_send(":(")
                    self.enemyknown = False

    async def GMReaperMove(self, distance: int):
        for r in self.quarryUnits(UnitTypeId.REAPER):
            move = False
            p = r.position
            enemy = self.quarryEnemyUnit.closer_than(distance, p).exclude_type([UnitTypeId.SCV, UnitTypeId.DRONE, UnitTypeId.PROBE])
            a = self.quarrySelf.closer_than(distance, p)
            if enemy.amount * 2 > a.amount:
                e = enemy.closest_to(p).position
                p = p.towards(e, -10)
                move = True
            elif not r.is_moving:
                scv = self.quarryEnemyUnit
                scv = scv(UnitTypeId.SCV) | scv(UnitTypeId.DRONE) | scv(UnitTypeId.PROBE)
                scv = scv.closer_than(distance, p)
                if self.quarryEnemyStructure.exists and not scv.exists:
                    if self.supply_used > 190:
                        a = self.quarryUnits(UnitTypeId.MARINE)
                        if a.exists:
                            e = self.quarryEnemyStructure.closest_to(self.start_location).position
                            a2 = a.closest_to(e)
                            if a2.distance_to(e) < 25:
                                m = m = self.mineral_field.closer_than(25, e)
                            else:
                                m = self.quarryUnits(UnitTypeId.MARINE).closer_than(10, a2.position)
                        else:
                            m = self.mineral_field.closer_than((self.supply_used * 1), self.start_location)
                    else:
                        m = self.mineral_field.closer_than((self.supply_used * 1), self.start_location)
                    self.enemyknown = True
                else:
                    m = self.mineral_field.closer_than((self.supply_used*4), self.start_location)
                    self.enemyknown = False
                if scv.exists:
                    p = scv.random.position
                    move = True
                elif m.exists:
                    p = m.random.position
                    move = True
                    
            if move:
                r.move(p)  # converted to move because of proximity command

    async def GEReaperScout(self):
        i = len(self.enemy_start_locations)
        j = random.randint(0, i-1)
        self.enemyknown = False
        self.target = self.enemy_start_locations[j]
        if self.quarryEnemyStructure.exists:
            self.enemyknown = True
            self.target = self.quarryEnemyStructure.random.position
        m = self.mineral_field.closer_than(20, self.target)
        if m.exists:
            self.target = m.random.position
        for r in self.quarryUnits(UnitTypeId.REAPER).idle:
            r.move(self.target)

    async def GMRepair(self, percent: float, distance: float):
        scv = self.quarryUnits(UnitTypeId.SCV)
        s = self.quarryStructures | self.quarryUnits(UnitTypeId.MEDIVAC) | self.quarryUnits(UnitTypeId.SIEGETANK) | self.quarryUnits(UnitTypeId.RAVEN)
        if scv.exists:
            damagedList = []
            for s1 in s:
                if s1.health_percentage < percent:
                    if scv.closer_than(distance, s1.position).exists:
                        damagedList.append(s1)
            s = self.quarryStructures.not_structure
            for s1 in damagedList:
                s.append(s1)
            for s1 in damagedList:
                scv1 = scv.closest_to(s1.position)
                s2 = s.closest_to(scv1.position)
                scv1(AbilityId.EFFECT_REPAIR_SCV, s2) # This is designed to have redundant calls.

    # Army Proximity and Micro Commands
    async def GMMarineProximity(self, proximity: float, friends: float):
        for m in self.quarryUnits(UnitTypeId.MARINE):
            a = self.quarryUnits.closer_than(friends, m.position)
            threat = self.quarryEnemyUnit.closer_than(proximity, m.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if True:
                if threat.exists and m.health_percentage > 2/8 and not threat.amount > a.amount * 2:
                    # print("M_ATTACK")
                    if await self.can_cast(m, AbilityId.EFFECT_STIM_MARINE) and m.health_percentage > 6/8 and not m.has_buff(BuffId.STIMPACK):
                        m(AbilityId.EFFECT_STIM_MARINE)
                        # print("STIM")
                        m.attack(threat.closest_to(m.position).position)
                elif threat.amount > a.amount * 2:
                    if threat.closest_to(m.position).position.distance_to(m.position) > 6:
                        p = m.position.towards(self.start_location, 5)
                        m.move(p)

    async def GEMarineAttack(self):
        for m in self.quarryUnits(UnitTypeId.MARINE):
            threat = self.quarryEnemyUnit.not_structure.closer_than(6, m.position)
            if threat.exists and m.weapon_cooldown < 0.1:
                ea = threat
                if ea.exists:
                    target = ea.closest_to(m.position)
                    priority = ea(UnitTypeId.LIBERATORAG) | ea(UnitTypeId.MEDIVAC) | ea(UnitTypeId.VIKINGFIGHTER) | ea(UnitTypeId.SIEGETANK) | ea(UnitTypeId.SIEGETANKSIEGED) | ea(UnitTypeId.LIBERATOR) | ea(UnitTypeId.WIDOWMINE) | ea(UnitTypeId.WIDOWMINEBURROWED) | ea(UnitTypeId.BANELING) | ea(UnitTypeId.LURKER) | ea(UnitTypeId.LURKERMP) | ea(UnitTypeId.CARRIER)
                    if priority.exists:
                        target = priority.closest_to(m.position)
                    m.attack(target)
            threat = threat.closer_than(4, m.position)
            if threat.exists and m.weapon_cooldown > 0.1:
                p = m.position.towards(threat.closest_to(m.position).position, -1)
                m.move(p)

    async def GMMarauderProximity(self, proximity: float):
        for m in self.quarryUnits(UnitTypeId.MARAUDER):
            threat = self.quarryEnemyUnit.not_structure.not_flying.closer_than(proximity, m.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if threat.exists:
                # print("M_ATTACK")
                if await self.can_cast(m, AbilityId.EFFECT_STIM_MARAUDER) and m.health_percentage > 7/10 and not m.has_buff(BuffId.STIMPACKMARAUDER):
                    m(AbilityId.EFFECT_STIM_MARAUDER)
                    # print("STIM")
                    m.attack(threat.closest_to(m.position).position)

    async def GEMarauderAttack(self):
        for m in self.quarryUnits(UnitTypeId.MARAUDER):
            threat = self.quarryEnemyUnit.not_structure.closer_than(7.1, m.position).not_flying
            if threat.exists and m.weapon_cooldown < 0.1:
                ea = threat.closer_than(6.1, m.position)
                if ea.exists:
                    target = ea.closest_to(m.position)
                    priority = ea(UnitTypeId.SIEGETANK) | ea(UnitTypeId.SIEGETANKSIEGED) | ea(UnitTypeId.WIDOWMINE) | ea(UnitTypeId.WIDOWMINEBURROWED) | ea(UnitTypeId.LURKER) | ea(UnitTypeId.LURKERMP) | ea(UnitTypeId.BANELING)
                    if priority.exists:
                        target = priority.closest_to(m.position)
                    m.attack(target)
            threat = threat.closer_than(6, m.position)
            if threat.exists and m.weapon_cooldown > 0.1:
                p = m.position.towards(threat.closest_to(m.position).position, -1)
                m.move(p)

    async def GMStepForwardBackward(self, allydistance: float, enemydistance: float):
        a = self.quarryUnits
        b = a(UnitTypeId.MARINE) | a(UnitTypeId.MARAUDER) | a(UnitTypeId.SIEGETANK)
        f = a(UnitTypeId.RAVEN) | a(UnitTypeId.MEDIVAC)
        e = self.quarryEnemyUnit
        ee = e.not_structure
        if e.exists:
            for m in b:
                p = m.position
                if e.closer_than(enemydistance, p).exists and m.weapon_cooldown > .15:
                    eee = ee.closer_than(enemydistance, p).amount
                    aa = a.closer_than(allydistance, p).amount
                    if aa > eee * 3:
                        ep = e.closest_to(p).position
                        if ep != p:
                            p = p.towards(ep, 2)
                            m.move(p)
                    if aa * 3 < eee:
                        ep = e.closest_to(p).position
                        if ep != p:
                            p = p.towards(ep, -10)
                            m.move(p)
            for ff in f:
                antiair = e(UnitTypeId.MISSILETURRET) | e(UnitTypeId.SPORECRAWLER)
                if antiair.exists:
                    p = ff.position
                    p2 = antiair.closest_to(ff).position
                    if p2.distance_to(p) < (7 + 5): # range of missile turret + my fear of losing units
                        p = p.towards(p2, -3)
                        ff.move(p)

    async def GEReaperProximity(self):
        for r in self.quarryUnits(UnitTypeId.REAPER):
            threat = self.quarryEnemyUnit.closer_than(10, r.position).not_structure.not_flying
            if threat.exists:
                death = threat.closest_to(r.position)
                p = death.position.towards(r.position, 1)
                if p.distance_to(r.position) < 6:
                    if await self.can_cast(r, AbilityId.KD8CHARGE_KD8CHARGE, p):
                        r(AbilityId.KD8CHARGE_KD8CHARGE, p)
                    elif r.weapon_cooldown == 0:
                        r.attack(death)
                    else:
                        p = death.position.towards(r.position, 5.5)
                        r.move(p)
                if r.health_percentage < 3 / 7:
                    nodeath = r.position.towards(death.position, -4)
                    r.move(nodeath)

    async def GMSiegeTankProximity(self, proximity: float, structure: bool):
        for s in self.quarryUnits(UnitTypeId.SIEGETANK):
            threat = self.quarryEnemyUnit.closer_than(proximity, s).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if not structure:
                threat =  threat.not_structure
            if threat.exists:
                s(AbilityId.SIEGEMODE_SIEGEMODE)
                # print("SIEGE")

    async def GMSiegedTankProximity(self, proximity: float, structure: bool):
        for s in self.quarryUnits(UnitTypeId.SIEGETANKSIEGED):
            threat = self.quarryEnemyUnit.closer_than(proximity, s).not_flying.exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            if not structure:
                threat =  threat.not_structure
            if not threat.exists:
                s(AbilityId.UNSIEGE_UNSIEGE)
                # print("UNSIEGE")

    async def GMSiegeTankFollow(self, distance: float):
        s = self.quarryUnits(UnitTypeId.SIEGETANK).idle
        m = self.quarryUnits(UnitTypeId.MARINE) | self.quarryUnits(UnitTypeId.MARAUDER)
        for s1 in s:
            if m.exists:
                mp = m.closest_to(s1.position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                s1.attack(mp)

    async def GMWidowBurrowProximity(self, proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool):
        # note: to disable non-boolean modes, set floats to zero
        for w in self.quarryUnits(UnitTypeId.WIDOWMINE):
            threat = self.quarryEnemyUnit.closer_than(proximity, w.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            burrow = False
            if not structure:
                threat = threat.not_structure
            if threat.exists:
                burrow = True
            mineral = self.mineral_field.closer_than(mineraldistance, w.position)
            if mineral.exists and self.quarryEnemyStructure.closer_than(enemybasedistance, w.position).exists:
                    burrow = True
            if defend:
                scv = self.quarryUnits(UnitTypeId.SCV).closer_than(proximity / 2, w.position)
                if scv.exists and mineral.exists:
                    burrow = True
            if burrow:
                w(AbilityId.BURROWDOWN_WIDOWMINE)

    async def GMWidowUnburrowProximity(self, proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool):
        # note: to disable non-boolean modes, set floats to zero
        for w in self.quarryUnits(UnitTypeId.WIDOWMINEBURROWED):
            threat = self.quarryEnemyUnit.closer_than(proximity, w.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE)
            unburrow = True
            if not structure:
                threat = threat.not_structure
            mineral = self.mineral_field.closer_than(mineraldistance, w.position)
            if defend:
                scv = self.quarryUnits(UnitTypeId.SCV).closer_than(proximity/2, w.position)
                if scv.exists and mineral.exists:
                    unburrow = False
            if mineral.exists:
                if self.quarryEnemyStructure.closer_than(enemybasedistance, w.position).exists:
                    unburrow = False
            if threat.exists:
                unburrow = False
            if unburrow:
                w(AbilityId.BURROWUP_WIDOWMINE)

    async def GMWidowTrapTravel(self, mindistance: float, maxdistance: float):
        e = self.quarryEnemyStructure
        if e.exists:
            ep = e.closest_to(self.start_location).position
            distance = ep.distance_to(self.start_location)
            m = self.mineral_field.closer_than(maxdistance, ep).further_than(mindistance, ep).closer_than(distance, self.start_location)
            if m.exists:
                for w in self.quarryUnits(UnitTypeId.WIDOWMINE).idle:
                    p = m.random.position
                    w.move(p)

    async def GMWidowFollow(self, distance: float, scv: bool, army: bool):
        w = self.quarryUnits(UnitTypeId.WIDOWMINE).idle
        m = self.quarryUnits(UnitTypeId.MARINE) | self.quarryUnits(UnitTypeId.MARAUDER) | self.quarryUnits(UnitTypeId.SIEGETANK) | self.quarryUnits(UnitTypeId.SIEGETANKSIEGED)
        s = self.quarryUnits(UnitTypeId.SCV)
        a = self.quarryUnits(UnitTypeId.ZERGLING) # This was initially coded wrong. This is a cheap fix.
        if scv:
            a = a | s
        if army:
            a = a | m
        if a.exists:
            for ww in w:
                e = self.quarryEnemyUnit
                if e.exists:
                    mp = a.closest_to(e.closest_to(ww.position).position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                else:
                    mp = a.closest_to(ww.position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                ww.move(mp)

    async def GMMedivacProximity(self):
        m = self.quarryUnits(UnitTypeId.MARINE) | self.quarryUnits(UnitTypeId.MARAUDER)
        if m.exists:
            for medivac in self.quarryUnits(UnitTypeId.MEDIVAC):
                p = m.furthest_to(self.start_location).position.towards(self.start_location, 2)
                p = p.offset((random.randint(-4, 4), random.randint(-4, 4)))
                medivac.attack(p)

    async def GMAirFollow(self, distance: float):
        s = self.quarryUnits(UnitTypeId.VIKINGFIGHTER) | self.quarryUnits(UnitTypeId.LIBERATOR)
        m = self.quarryUnits(UnitTypeId.MEDIVAC) | self.quarryUnits(UnitTypeId.RAVEN)
        for s1 in s:
            if m.exists:
                mp = m.closest_to(s1.position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                s1.attack(mp)

    async def GMAntiAirAttack(self, proximity: float):
        s = self.quarryUnits(UnitTypeId.VIKINGFIGHTER) | self.quarryUnits(UnitTypeId.LIBERATOR)
        e = self.quarryEnemyUnit.flying
        for s1 in s:
            ea = e.closer_than(proximity, s1.position)
            if ea and s1.weapon_cooldown < .1:
                s1.attack(ea.closest_to(s1.position))

    async def GMRavenProximity(self):
        for r in self.quarryUnits(UnitTypeId.RAVEN):
            e = self.quarryEnemyUnit.not_structure.closer_than(11, r.position).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE).exclude_type(UnitTypeId.OVERSEER).exclude_type(UnitTypeId.PROBE).exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.LARVA).exclude_type(UnitTypeId.EGG)
            if e.exists and r.energy > 75:
                eMechPriority = e(UnitTypeId.SIEGETANKSIEGED) | e(UnitTypeId.VIKINGFIGHTER) | e(UnitTypeId.LIBERATOR) | e(UnitTypeId.LIBERATORAG) |e(UnitTypeId.BATTLECRUISER) | e(UnitTypeId.WIDOWMINE) | e(UnitTypeId.WIDOWMINEBURROWED) | e(UnitTypeId.THOR) | e(UnitTypeId.CARRIER) | e(UnitTypeId.VOIDRAY) | e(UnitTypeId.CARRIER) | e(UnitTypeId.COLOSSUS) | e(UnitTypeId.MOTHERSHIP) | e(UnitTypeId.TEMPEST)
                if eMechPriority.exists:
                    ea = eMechPriority.random
                    if await self.can_cast(r, AbilityId.EFFECT_INTERFERENCEMATRIX, ea) and not ea.has_buff(BuffId.DISABLEABILS):
                        r(AbilityId.EFFECT_INTERFERENCEMATRIX, ea)
                        # print("INTERENCE MATRIX")
                        # await self.chat_send("INTERENCE MATRIX!!!")
                else:
                    ea = e.random
                    eap = ea.position
                    e2 = e.closer_than(3, eap)
                    r2 = self.quarrySelf.closer_than(5, eap)  # arbituary numbers used
                    if r.position.distance_to(ea.position) > 6 and e2.amount > r2.amount + 2 and await self.can_cast(r, AbilityId.EFFECT_ANTIARMORMISSILE, ea) and not ea.has_buff(BuffId.RAVENSHREDDERMISSILEARMORREDUCTION):
                        r(AbilityId.EFFECT_ANTIARMORMISSILE, ea)
                        # print("ORANGE!!!")
                        # await self.chat_send("ORANGE!!!")
                    else:
                        # print("idk debug this")
                        """
                        if self.can_afford(AUTOTURRET):
                            p = await self.find_placement(AUTOTURRET, near=r.position)
                            x = p.x
                            y = p.y
                            p3 = p.to3(2)
                            if await self.can_cast(r(AbilityId.UnitTypeId.RAVENBUILD_AUTOTURRET, p)):
                                r(AbilityId.UnitTypeId.RAVENBUILD_AUTOTURRET, p))"""
            elif e.exists:
                ea = e.closest_to(r.position)
                p = ea.position.towards(r.position, 13)
                r.move(p)
            else:
                a = self.quarryUnits(UnitTypeId.MARINE) | self.quarryUnits(UnitTypeId.MARAUDER) | self.quarryUnits(UnitTypeId.SIEGETANK) | self.quarryUnits(UnitTypeId.SIEGETANKSIEGED)
                if a.exists and r.is_idle:
                    p = a.furthest_to(self.start_location).position.towards(self.start_location, 3)
                    p = p.towards(a.closest_to(r.position).position, 4)
                    r.move(p)

    # gen 2 methods
    # other methods are updated but new methods and majorly reworked methods go here          
    def quarry(self): #exists a solution to reduce how many api calls are needed to try to improve performance
        self.quarryUnits = self.units
        self.quarryStructures = self.structures
        self.quarrySelf = self.quarryUnits | self.quarryStructures
        self.quarryEnemyUnit = self.enemy_units
        self.quarryEnemyStructure = self.enemy_structures
        self.quarryEnemy = self.quarryEnemyUnit | self.quarryStructures
        self.notSafeUnit = self.quarryEnemyUnit.exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.DRONE).exclude_type(UnitTypeId.PROBE).exclude_type(UnitTypeId.CHANGELING).exclude_type(UnitTypeId.CHANGELINGMARINESHIELD).exclude_type(UnitTypeId.CHANGELINGMARINE).exclude_type(UnitTypeId.OVERLORD).exclude_type(UnitTypeId.OVERSEER).exclude_type(UnitTypeId.PROBE)
        
    # "# This needs to be reworked"
    async def GMLandIdleBuildings(self, supplyBuffer: int):
        # I feel like this does not fall out of scope. Scope is to maintain logic and improve performance so it could be argued either way but several unnessary math calls makes bot performance go down.
        # Variable names maintained from previous reworked method to make conversion easier. Old me has bad variable names.
        # Using random instead of logic because origial bot used random.
        cc = self.quarryStructures(UnitTypeId.COMMANDCENTER) | self.quarryStructures(UnitTypeId.ORBITALCOMMAND)
        b = self.quarryStructures(UnitTypeId.BARRACKSFLYING).idle
        f = self.quarryStructures(UnitTypeId.FACTORYFLYING).idle
        s = self.quarryStructures(UnitTypeId.STARPORTFLYING).idle
        e = self.quarryStructures(UnitTypeId.REACTOR) | self.quarryStructures(UnitTypeId.TECHLAB)
        m = self.mineral_field
        fly = b | f | s
        if fly.exists: # supplycheck removed from previous bot because it's checked next step and we need these moving
            p = fly.random.position # I forget why but cluster them together
            if p != self.start_location:
                    p = p.towards(self.start_location, 10) # bias towards bot base
            p = p.towards(self.enemy_start_locations[0], 8) # bias towards center / couldn't find map_center in this api and enemy is assumably other side of map center
            p = p.offset((random.randint(-20, 20), random.randint(-20, 20))) # required thematic from prervious method / see original scope
            if cc.exists:
                p = p.towards(cc[cc.amount-1].position, 4) # changed from last # bias away from clutter or something idk
                p = p.towards(cc.closest_to(p).position, -2) # bias away from command center
            if m.exists:
                p.towards(m.closest_to(p).position, -10) # bias reducing huge problem with placing on expansions from previous bot
            if e.exists:
                        p = p.towards(e.closest_to(p).position, -6) # encourage them away from addons to block
            if e.exists:
                for ff in fly:
                    ff.move(e.closest_to(ff.position).position.offset((random.randint(-4, 4), random.randint(-4, 4)))) # This should exist
            else:
                for ff in fly:
                    ff.move(p) # this move command should get overridden by next command if valid
            if self.supply_left >= supplyBuffer and self.can_afford(UnitTypeId.BARRACKSTECHLAB) and self.can_afford(UnitTypeId.BARRACKSREACTOR): # A previous comment mentions this
                for bb in b:
                    p2 = await self.find_placement(UnitTypeId.BARRACKS, near=p)
                    if m.closest_to(p2).distance_to(p2) < 10:
                        p2.towards(m.closest_to(p2).position, -10)
                    if not self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists and not self.already_pending(UnitTypeId.BARRACKSTECHLAB) and not e(UnitTypeId.TECHLAB).exists: # I think this is poorly written for reusability but maintaining intented logic from previous bot
                        bb.build(UnitTypeId.BARRACKSTECHLAB, p2)
                    elif not self.already_pending(UnitTypeId.BARRACKSREACTOR) and not e(UnitTypeId.REACTOR).exists:
                        bb.build(UnitTypeId.BARRACKSREACTOR, p2) # previous bot used p instead of near=p at equivelent line
                if not self.already_pending(UnitTypeId.FACTORYTECHLAB) and not e(UnitTypeId.TECHLAB).exists:
                    for ff in f:
                        p2 = await self.find_placement(UnitTypeId.FACTORY, near=p)
                        if m.closest_to(p2).distance_to(p2) < 10:
                            p2.towards(m.closest_to(p2).position, -10)
                        ff.build(UnitTypeId.FACTORYTECHLAB, p2) # previous bot used p instead of near=p at equivelent line
                for ss in s: # Previous bot doesn't build reactor but does build tech lab. It doesn't fit playstyle. Possibly for mass raven? It doesn't tech into cruiser.
                    p2 = await self.find_placement(UnitTypeId.STARPORT, near=p)
                    if m.closest_to(p2).distance_to(p2) < 10:
                        p2.towards(m.closest_to(p2).position, -10)
                    if not self.quarryStructures(UnitTypeId.STARPORTTECHLAB).exists and not self.already_pending(UnitTypeId.STARPORTTECHLAB) and not e(UnitTypeId.TECHLAB).exists:
                        ss.build(UnitTypeId.STARPORTTECHLAB, p2) # previous bot used p instead of near=p at equivelent line
                    elif not self.already_pending(UnitTypeId.STARPORTREACTOR) and not e(UnitTypeId.REACTOR).exists:
                        ss.build(UnitTypeId.STARPORTREACTOR, p2) # didn't exist which makes low sense because other bot builds medivacs and vikin
                        
    async def GMAddonAbductBuilding(self): # I strongly disagree with this and the reworked version of this but maintaining for original scope. Can be reworked in a bot 6
        if self.supply_left > 3:
            b = self.quarryStructures(UnitTypeId.BARRACKSFLYING)
            f = self.quarryStructures(UnitTypeId.FACTORYFLYING)
            s = self.quarryStructures(UnitTypeId.STARPORTFLYING)
            for r in self.quarryStructures(UnitTypeId.REACTOR):
                p = r.add_on_land_position
                if b.idle.exists:
                    b.idle.closest_to(p)(AbilityId.LAND, p)
                elif s.idle.exists:
                    s.idle.closest_to(p)(AbilityId.LAND, p)
            for t in self.quarryStructures(UnitTypeId.TECHLAB):
                p = t.add_on_land_position
                if f.idle.exists:
                    f.idle.closest_to(p)(AbilityId.LAND, p)
                elif s.idle.exists and not self.quarryStructures(UnitTypeId.STARPORTTECHLAB).exists:
                    s.idle.closest_to(p)(AbilityId.LAND, p)
                elif b.idle.exists and not self.quarryStructures(UnitTypeId.BARRACKSTECHLAB).exists:
                    b.idle.closest_to(p)(AbilityId.LAND, p)
                    
    async def GEEarlyDefend(self): # don't know why this was included previously
        threat = self.notSafeUnit.closer_than(30, self.start_location)
        workers = self.quarryEnemyUnit(UnitTypeId.SCV) | self.quarryEnemyUnit(UnitTypeId.DRONE) | self.quarryEnemyUnit(UnitTypeId.PROBE)
        workers = workers.closer_than(30, self.start_location)
        if workers.amount > 3:
            threat = threat | workers
        if threat.exists:
            army = self.quarryUnits.exclude_type(UnitTypeId.SCV).exclude_type(UnitTypeId.MULE)
            if threat.amount > army.amount + 4:
                army = self.quarryUnits
            for a in army:
                a.attack(threat.random)
                
    async def GMStarport(self, techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int):
        if not self.needToExpand:
            m = self.quarryUnits(UnitTypeId.MEDIVAC).amount
            v = self.quarryUnits(UnitTypeId.VIKINGFIGHTER).amount
            l = self.quarryUnits(UnitTypeId.LIBERATOR).amount
            r = self.quarryUnits(UnitTypeId.RAVEN).amount
            if self.quarryUnits(UnitTypeId.STARPORTTECHLAB).exists:
                id = self.quarryStructures(UnitTypeId.STARPORTTECHLAB).random.tag
            else:
                id = 0
            for s in self.quarryStructures(UnitTypeId.STARPORT).ready.idle:
                if s.add_on_tag == 0:
                    s(AbilityId.LIFT)
                if self.supply_left > 2:
                    if s.add_on_tag == id and self.can_afford(UnitTypeId.RAVEN) and r < maxraven:
                        s.train(UnitTypeId.RAVEN)
                    elif self.supply_left > 4:
                        if self.can_afford(UnitTypeId.MEDIVAC) and m < maxmedivac:
                            s.train(UnitTypeId.MEDIVAC)
                            if self.can_afford(UnitTypeId.MEDIVAC):
                                s.train(UnitTypeId.MEDIVAC)
                        elif v < maxviking:
                            if self.can_afford(AbilityId.STARPORTTRAIN_VIKINGFIGHTER):
                                s(AbilityId.STARPORTTRAIN_VIKINGFIGHTER)
                                if self.can_afford(AbilityId.STARPORTTRAIN_VIKINGFIGHTER):
                                    s(AbilityId.STARPORTTRAIN_VIKINGFIGHTER)
                        elif l < maxliberator:
                            if self.can_afford(AbilityId.STARPORTTRAIN_LIBERATOR):
                                s(AbilityId.STARPORTTRAIN_LIBERATOR)
                                if self.can_afford(AbilityId.STARPORTTRAIN_LIBERATOR):
                                    s(AbilityId.STARPORTTRAIN_LIBERATOR)
                    