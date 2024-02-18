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
Note* A 
"""
class MothAI(BotAI):
    def on_start(self):
        a = sc2.constants
        self.Rally = None
        self.BattleWinningMath = 1.0 # unimplemented feature -> will be used to make good decisions
        self.target = None
        self.needToExpand = False
        self.enemyknown = False
        self.airHarrass = False
        self.earlyArmor = False
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
        print("D")
    async def on_step(self, iteration):
        print("A")
        if iteration == 0:
            print("B")
            await self.chat_send("(glhf)")
            print("C")
        self.combinedActions = []

        if self.STRAT == "AntiRandom":
            """Early Game"""
            if iteration == 0:
                await self.chat_send("ENEMY RANDOM")
            if True:# self.time <= 240:
                if iteration % 1 == 0:
                    await self.GEReaperProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 5 == 0:
                    await self.GESafeBuildOrder()
                    await self.GEReaperScout()
                    await self.GEUnfinshedBuildingCheck()
                if iteration % 6 == 3:
                    await self.GEsupplydepotup()
                    await self.GEsupplydepotdown()
                if iteration % 6 == 0:
                    await self.distribute_workers()
                    await self.GECheckEnemy()
                    r = self.units(REAPER).amount
                    await self.GEBarracks(False, r, r*2, 4, 0)
                if iteration % 10 == 5:
                    await self.GEOrbitalCommand()
#                if iteration % 150 == 0:
#                    await self.GEEarlyDefend()

        elif self.STRAT == "AntiTerran":
            if self.time <= 240:
                if iteration % 1 == 0:
                    await self.GEReaperProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                    await self.GMLandIdleBuildings() # code is GM instead of GE because it is only used in obscure situations
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
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
                    if self.known_enemy_structures.exists:
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
                    await self.GEBuildingDodge(12)
                    await self.GECheckEnemy()
#                if iteration % 150 == 0:
 #                   await self.GEEarlyDefend()
            elif self.time > 240 and True:
                if iteration % 1 == 0:
                    await self.GELandCommandCenter()
                    await self.GEReaperProximity()
                    await self.GMRavenProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 4 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.GEBuildingDodge(10)
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
                    a = self.units.flying
                    #mm = (a(MARINE) | a(MARAUDER)).amount
                    m = a(MEDIVAC).amount
                    v = a(VIKINGFIGHTER).amount
                    await self.GMStarport(False, 8, m-2, v-2, 5)
                    # techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int
                if iteration % 9 == 5:
                    await self.GMLandIdleBuildings()
                    await self.GMPremptiveInvisibleCheck()
                if iteration % 9 == 6:
                    cc = self.units.structure
                    cc = cc(COMMANDCENTER) | cc(ORBITALCOMMAND) | cc(COMMANDCENTERFLYING) | cc(ORBITALCOMMANDFLYING)
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
                    await self.GMLandIdleBuildings()
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
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
                    if self.known_enemy_structures.exists:
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
                    await self.GEBuildingDodge(12)
                    await self.GECheckEnemy()
                #                if iteration % 150 == 0:
                #                   await self.GEEarlyDefend()
            elif self.time > 240 and True:
                if iteration % 1 == 0:
                    await self.GELandCommandCenter()
                    await self.GEReaperProximity()
                    await self.GMRavenProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 4 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.GEBuildingDodge(10)
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
                    a = self.units.flying
                    # mm = (a(MARINE) | a(MARAUDER)).amount
                    m = a(MEDIVAC).amount
                    v = a(VIKINGFIGHTER).amount
                    await self.GMStarport(False, 8, m - 2, v - 2, 5)
                    # techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int
                if iteration % 9 == 5:
                    await self.GMLandIdleBuildings()
                    await self.GMPremptiveInvisibleCheck()
                if iteration % 9 == 6:
                    cc = self.units.structure
                    cc = cc(COMMANDCENTER) | cc(ORBITALCOMMAND) | cc(COMMANDCENTERFLYING) | cc(ORBITALCOMMANDFLYING)
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
                    await self.GMLandIdleBuildings()  # code is GM instead of GE because it is only used in obscure situations
                if iteration % 5 == 0:
                    await self.GEUnfinshedBuildingCheck()
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
                    if self.known_enemy_structures.exists:
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
                    await self.GEBuildingDodge(12)
                    await self.GECheckEnemy()
                #                if iteration % 150 == 0:
                #                   await self.GEEarlyDefend()
            elif self.time > 240 and True:
                if iteration % 1 == 0:
                    await self.GELandCommandCenter()
                    await self.GEReaperProximity()
                    await self.GMRavenProximity()
                    await self.GEMarineAttack()
                    await self.GEMarauderAttack()
                if iteration % 4 == 0:
                    await self.GEUnfinshedBuildingCheck()
                    await self.GEBuildingDodge(10)
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
                    a = self.units.flying
                    # mm = (a(MARINE) | a(MARAUDER)).amount
                    m = a(MEDIVAC).amount
                    v = a(VIKINGFIGHTER).amount
                    await self.GMStarport(False, 8, m - 2, v - 2, 5)
                    # techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int
                if iteration % 9 == 5:
                    await self.GMLandIdleBuildings()
                    await self.GMPremptiveInvisibleCheck()
                if iteration % 9 == 6:
                    cc = self.units.structure
                    cc = cc(COMMANDCENTER) | cc(ORBITALCOMMAND) | cc(COMMANDCENTERFLYING) | cc(ORBITALCOMMANDFLYING)
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


        await self.do_actions(self.combinedActions)

    """Methods: GENERAL"""
    # Build Orders
    async def GESafeBuildOrder(self):
        scv = self.units(SCV)
        cc = self.units(COMMANDCENTER) | self.units(COMMANDCENTERFLYING)
        oc = self.units(ORBITALCOMMAND) | self.units(ORBITALCOMMANDFLYING)
        sd = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED)
        b = self.units(BARRACKS) | self.units(BARRACKSFLYING)
        f = self.units(FACTORY) | self.units(FACTORYFLYING)
        x = self.main_base_ramp.top_center.x
        y = self.main_base_ramp.top_center.y
        lp = self.main_base_ramp.lower
        xd = sum([lpx.x for lpx in lp]) / len(lp)
        yd = sum([lpy.y for lpy in lp]) / len(lp)
        if cc.ready.exists or oc.ready.exists:
            if scv.exists and not sd.exists and not self.already_pending(SUPPLYDEPOT):
                s = scv.furthest_to(self.start_location)
                if self.can_afford(SUPPLYDEPOT):
                    # Test results are for placement only. Timings and interference excluded.
                    print("Build: 'Safe'")
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
                    self.combinedActions.append(s.build(SUPPLYDEPOT, p))
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
                            if oc.amount + cc.amount == 1 and self.can_afford(COMMANDCENTER):
                                #  await self.expand_now() # code changed to accommodate getting killed early by common enemy push
                                if self.can_afford(COMMANDCENTER):
                                    await self.build(COMMANDCENTER, near=self.start_location)
                                    print("Inbase expansion")
                            elif sd.amount < 3 and self.can_afford(SUPPLYDEPOT) and not self.already_pending(
                                    SUPPLYDEPOT):
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
                            elif self.can_afford(FACTORY) and not f.exists and not self.already_pending(FACTORY):
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

    # Expansion Methods and Air Building Commands
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
                        self.combinedActions.append(worker.build(REFINERY, ve))
                        print("REFINERY")

    async def GMManageSupply(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND)
        s = self.units(SCV)
        if cc.exists and s.exists and self.supply_used + self.supply_left < 200:
            if self.supply_left < self.supply_used/16 + 4 and not self.already_pending(SUPPLYDEPOT) and self.can_afford(SUPPLYDEPOT):
                if True:
                    e = self.units(REACTOR) | self.units(TECHLAB)
                    p = await self.find_placement(SUPPLYDEPOT, near=cc.random.position)
                    if e.closer_than(5, p).exists:
                        p = p.towards(e.closest_to(p).position, -5)
                    if not e.closer_than(5, p).exists: # not redundant, the check is to make sure it offset without issues
                        await self.build(SUPPLYDEPOT, p)
                        print("SUPPLYDEPOT")
                    if self.minerals > 200:
                        p = await self.find_placement(SUPPLYDEPOT, near=cc.random.position)
                        if e.closer_than(5, p).exists:
                            p = p.towards(e.closest_to(p).position, -5)
                        if not e.closer_than(5, p).exists:
                            await self.build(SUPPLYDEPOT, p)
                            print("SUPPLYDEPOT")
                        if self.minerals > 300:
                            p = await self.find_placement(SUPPLYDEPOT, near=cc.random.position)
                            if e.closer_than(5, p).exists:
                                p = p.towards(e.closest_to(p).position, -5)
                            if not e.closer_than(5, p).exists:
                                await self.build(SUPPLYDEPOT, p)
                                print("SUPPLYDEPOT")
            elif self.supply_left < 0 and self.can_afford(SUPPLYDEPOT):
                await self.build(SUPPLYDEPOT, near=cc.random)
                """most code here is untested"""

    async def GMReplaceExpand(self, ccmax: int, ocbuffer: int, barrcksmin: int, factorymin: int, starportmin: int, ebaymin: int, armorymin: int, ghostacademymin: int, fcoremin:int,barrackmax: int, factorymax: int, starportmax: int):
        scv = self.units(SCV)
        building = self.units.structure
        cc = building(COMMANDCENTER) | building(ORBITALCOMMAND) | building(COMMANDCENTERFLYING) | building(ORBITALCOMMANDFLYING)
        oc = building(ORBITALCOMMAND) | building(ORBITALCOMMANDFLYING)
        sd = building(SUPPLYDEPOT) | building(SUPPLYDEPOTLOWERED)
        b = building(BARRACKS) | building(BARRACKSFLYING)
        f = building(FACTORY) | building(FACTORYFLYING)
        s = building(STARPORT) | building(STARPORTFLYING)
        e = building(ENGINEERINGBAY)
        a = building(ARMORY)

        if sd.ready.exists and cc.exists and b.amount < barrcksmin and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS) and not self.needToExpand:
            print("NO BARRACKS")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(BARRACKS, near=p)

        if b.ready.exists and cc.exists and f.amount < factorymin and not self.already_pending(FACTORY) and self.can_afford(FACTORY) and not self.needToExpand:
            print("NO FACTORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(FACTORY, near=p)

        if f.ready.exists and cc.exists and s.amount < starportmin and not self.already_pending(STARPORT) and self.can_afford(STARPORT) and not self.needToExpand:
            print("NO STARPORT")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(STARPORT, near=p)

        if sd.exists and cc.exists and not self.already_pending(ENGINEERINGBAY) and e.amount < ebaymin and self.can_afford(ENGINEERINGBAY) and self.supply_left > 6 and not self.needToExpand:
            print("NO ENGINEERINGBAY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(ENGINEERINGBAY, near=p)

        if f.ready.exists and cc.exists and a.amount < armorymin and not self.already_pending(ARMORY) and self.can_afford(ARMORY) and self.supply_left > 6 and not self.needToExpand:
            print("NO ARMORY")
            c = cc.random.position
            sc = scv.closer_than(10, c)
            if sc.exists:
                scvp = sc.random.position
                p = scvp.towards(c, random.randint(8, 12))
                await self.build(ARMORY, near=p)

        if self.minerals > 200 + (cc.amount * 100) and self.can_afford(COMMANDCENTER) and not cc.flying.exists and cc.amount < ccmax and not self.already_pending(COMMANDCENTER):
            print("expand")
            p = self.start_location
            await self.build(COMMANDCENTER, near=p)

        if self.can_afford(COMMANDCENTER) and not cc.flying.exists and cc.amount < ccmax and not self.already_pending(COMMANDCENTER) and self.nextXpansionLocation:
            print("expand")
            p = self.start_location
            await self.build(COMMANDCENTER, near=p) # sub-function is not redundant.

        if oc.amount >= ocbuffer:
            if s.amount < starportmax and cc.exists and not self.already_pending(STARPORT) and self.can_afford(STARPORT) and self.supply_left > 5 and not self.needToExpand and not s.flying.exists:
                print("NOT ENOUGH STARPORT")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(STARPORT, near=p)

            if f.amount < factorymax and cc.exists and not self.already_pending(FACTORY) and cc.amount >= ocbuffer and self.can_afford(FACTORY) and self.supply_left > 5 and not self.needToExpand and not s.flying.exists:
                print("NOT ENOUGH FACTORY")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(FACTORY, near=p)

            if b.amount < barrackmax and cc.exists and not self.already_pending(BARRACKS) and self.can_afford(BARRACKS) and not self.needToExpand and not b.flying.exists:
                print("NOT ENOUGH BARRACKS")
                c = cc.random.position
                sc = scv.closer_than(10, c)
                if sc.exists:
                    scvp = sc.random.position
                    p = scvp.towards(c, random.randint(8, 12))
                    await self.build(BARRACKS, near=p)

    async def GEAntiAirHarras(self, distance: float):
        if not self.already_pending(ENGINEERINGBAY) and not self.already_pending(MISSILETURRET):
            a = self.units
            scv = a(SCV)
            m = a(MISSILETURRET)
            cc = a(COMMANDCENTER) | a(ORBITALCOMMAND)
            if cc.exists and scv.exists and self.can_afford(ENGINEERINGBAY):
                scv1 = scv.random
                if not a(ENGINEERINGBAY).exists:
                    p = scv1.position.towards(self.start_location, 10)
                    p = await self.find_placement(ENGINEERINGBAY, near=p)
                    self.combinedActions.append(scv1.build(ENGINEERINGBAY, p))
                else:
                    m = a(MISSILETURRET).closer_than(distance, scv1.position)
                    if not m.exists:
                        p = scv1.position
                        self.combinedActions.append(scv1.build(MISSILETURRET, p))

    async def GMLandIdleBuildings(self): # This needs to be reworked
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        b = self.units(BARRACKSFLYING).idle
        f = self.units(FACTORYFLYING).idle
        s = self.units(STARPORTFLYING).idle
        e = self.units(REACTOR) | self.units(TECHLAB)
        if b.exists and self.supply_left > 7:
            if not self.units(BARRACKSTECHLAB).exists:
                b1 = b.random
                p = b1.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                if p != self.start_location:
                    p = p.towards(self.start_location, 5)
                self.combinedActions.append(b1.move(p))
                if self.can_afford(BARRACKSTECHLAB) and self.can_afford(BARRACKS):
                    p = await self.find_placement(BARRACKS, near=b1.position)
                    if cc.exists:
                        p = p.towards(cc.closest_to(p).position, -3)
                    if e.exists:
                        p = p.towards(e.closest_to(p).position, -6)
                    self.combinedActions.append(b1.build(BARRACKSTECHLAB, p))
                    print("LAND B_TECHLAB")
            elif not self.units(REACTOR).exists:
                for b2 in b:
                    p = b2.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                    if p != self.start_location:
                        p = p.towards(self.start_location, 5)
                    self.combinedActions.append(b2.move(p))
                    if self.can_afford(BARRACKSREACTOR) and self.can_afford(BARRACKS):
                        p = await self.find_placement(BARRACKS, near=b2.position)
                        if cc.exists:
                            p = p.towards(cc.closest_to(p).position, -3)
                        if e.exists:
                            p = p.towards(e.closest_to(p).position, -6)
                        self.combinedActions.append(b2.build(BARRACKSREACTOR, p))
                        print("LAND B_TECHLAB")

        if f.exists and self.supply_left > 7:
            if not self.units(TECHLAB).exists:  # Zerg does not gain replacement reactors intentionally
                for f2 in f:
                    p = f2.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                    if p != self.start_location:
                        p = p.towards(self.start_location, 5)
                    self.combinedActions.append(f2.move(p))
                    if self.can_afford(FACTORY):
                        p = await self.find_placement(FACTORY, near=f2.position)
                        if cc.exists:
                            p = p.towards(cc.closest_to(p).position, -3)
                        if e.exists:
                            p = p.towards(e.closest_to(p).position, -6)
                        self.combinedActions.append(f2.build(FACTORYTECHLAB, p))
                        print("LAND F_TECHLAB")

        if s.exists and self.supply_left > 7:
            if not self.units(STARPORTREACTOR).exists:
                s1 = s.random
                p = s1.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                if p != self.start_location:
                    p = p.towards(self.start_location, 5)
                self.combinedActions.append(s1.move(p))
                if self.can_afford(STARPORT):
                    p = await self.find_placement(STARPORT, near=s1.position)
                    if cc.exists:
                        p = p.towards(cc.closest_to(p).position, -3)
                    if e.exists:
                        p = p.towards(e.closest_to(p).position, -6)
                    p = p.towards(self.units.structure.furthest_to(self.start_location).position, 5)
                    self.combinedActions.append(s1.build(STARPORTREACTOR, p))
                    print("LAND S_REACTORLAB")
            else:
                for s2 in s:
                    p = s2.position.offset((random.randint(-20, 20), random.randint(-20, 20)))
                    if p != self.start_location:
                        p = p.towards(self.start_location, 5)
                    self.combinedActions.append(s2.move(p))
                    if self.can_afford(STARPORT):
                        p = await self.find_placement(STARPORT, near=s2.position)
                        if cc.exists:
                            p = p.towards(cc.closest_to(p).position, -3)
                        if e.exists:
                            p = p.towards(e.closest_to(p).position, -6)
                        self.combinedActions.append(s2.build(STARPORTTECHLAB, p))
                        print("LAND S_TECHLAB")

    async def GELandCommandCenter(self):
        for cc in self.units(COMMANDCENTERFLYING).idle | self.units(ORBITALCOMMANDFLYING).idle:
            p = self.nextXpansionLocation
            print(p)
            #self.combinedActions.append(cc.move(p))
            self.combinedActions.append(cc(LAND, p))
            p = self.nextXpansionLocation
            m = self.state.mineral_field | self.state.vespene_geyser
            if m.exists:
                m1 = m.closest_to(p).position
                p2 = p.towards(m1, -.5)
                print(p2)
                self.nextXpansionLocation = p2
                e = self.known_enemy_units.closer_than(15, self.nextXpansionLocation)
                if e.exists:
                    self.nextXpansionLocation = await self.get_next_expansion()
                    p3 = cc.position.towards(e.random.position, -1)
                    self.combinedActions.append(cc.move(p3))

    async def GEInBaseCommandCenter(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND) #  not flying
        ccflying = self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        if cc.amount > 1 and self.state.mineral_field.exists:
            for c in cc.idle:
                cp = c.position
                ccc = cc.further_than(1, cp)
                c2 = ccc.closest_to(c.position).position
                if cp != self.start_location:
                    min = self.state.mineral_field
                    m = min.closest_to(cp.towards(self.start_location, 4)).position
                else:
                    m = self.start_location
                a = cp.distance_to(m)
                b = c2.distance_to(m)
                if a > b:
                    self.nextXpansionLocation = await self.get_next_expansion()
                    self.combinedActions.append(c(LIFT))

    async def GMAddonAbductBuilding(self):
        b = self.units(BARRACKSFLYING)
        f = self.units(FACTORYFLYING)
        s = self.units(STARPORTFLYING)
        a = b|f|s
        t = self.units(TECHLAB)
        r = self.units(REACTOR)

        if t.exists and f.exists and self.supply_left > 3:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.closest_to(self.start_location).add_on_land_position
            fp = f.closest_to(p)
            self.combinedActions.append(fp(LAND, p))

        if t.exists and s.exists and not self.units(STARPORTTECHLAB).exists and self.supply_left > 3:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.closest_to(self.start_location).add_on_land_position
            sp = s.closest_to(p)
            self.combinedActions.append(sp(LAND, p))

        if b.exists and t.exists and not self.units(BARRACKSTECHLAB).exists and self.supply_left > 3:
            print("REPLACE TECHLAB SPOT TRY DO")
            p = t.closest_to(self.start_location).add_on_land_position
            bp = b.closest_to(p)
            self.combinedActions.append(bp(LAND, p))

        if s.exists and r.exists and not self.units(STARPORTREACTOR).exists and self.supply_left > 5:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.closest_to(self.start_location).add_on_land_position
            sp = s.closest_to(p)
            self.combinedActions.append(sp(LAND, p))

        if r.exists and b.exists and self.supply_left > 3:
            print("REPLACE REACTOR SPOT TRY DO")
            p = r.closest_to(self.start_location).add_on_land_position
            bp = b.closest_to(p)
            self.combinedActions.append(bp(LAND, p))

    async def GEBuildingDodge(self, range: float):
        a = self.units.structure
        b = a(BARRACKSFLYING) | a(FACTORYFLYING) | a(STARPORTFLYING)
        c = a(COMMANDCENTERFLYING) | a(ORBITALCOMMANDFLYING)
        e = self.known_enemy_units
        if e.exists:
            for aa in b:
                ap = aa.position
                ep = e.closest_to(ap).position
                d = ap.distance_to(ep)
                if d != 0 and d < range:
                    p = ep.towards(ap, range + 1)
                    self.combinedActions.append(aa.move(p))
            for cc in c:
                cp = cc.position
                ep = e.closest_to(cp).position
                d = cp.distance_to(ep)
                if d != 0 and d < range:
                    p = ep.towards(cp, range + 1)
                    self.combinedActions.append(cc.move(p))
                    self.nextXpansionLocation = await self.get_next_expansion()

    # Ground Building Commands
    async def GECommandCenter(self):
        cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND)
        ccflying = self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        for c in cc.noqueue:
            m = self.state.mineral_field
            minnear = m.closer_than(15, c.position)
            cc2 = cc.further_than(3, c.position).closer_than(15, c.position)
            if not self.units(SCV).exists and not minnear.exists and not ccflying.exists:
                self.combinedActions.append(c(LIFT))
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
        for c in cc(COMMANDCENTER).noqueue:
            if self.units(BARRACKS).ready.exists and self.can_afford(ORBITALCOMMAND):
                print("CC_OC")
                self.combinedActions.append(c(UPGRADETOORBITAL_ORBITALCOMMAND))
            elif self.can_afford(SCV) and self.units(SCV).amount < (cc.amount*20) + 10 and self.units(SCV).amount < 70 and self.units(SCV).closer_than(20, c).amount < 24 and self.supply_left > 0:
                self.combinedActions.append(c.train(SCV))

    async def GEOrbitalCommand(self):
        oc = self.units(ORBITALCOMMAND)
        flyingcc = self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        for o in oc.ready.noqueue:
            scv = self.units(SCV).closer_than(10, o)
            m = self.state.mineral_field.closer_than(15, o)
            if not scv.exists and not m.exists and not flyingcc.exists:
                self.combinedActions.append(o(LIFT))
                p = await self.get_next_expansion()
                m = self.state.mineral_field
                if m.exists:
                    m1 = m.closest_to(p).position
                    print(p)
                    print(m1)
                    p2 = m1.towards(p, 5)
                    print(p2)
                    self.nextXpansionLocation = p2
            elif self.can_afford(SCV) and self.units(SCV).amount < 65 and self.units(SCV).closer_than(20, o.position).amount < 24:
                self.combinedActions.append(o.train(SCV))
        for o in oc.ready:
            if o.energy == 200:
                a = self.units.not_structure
                if a.exists:
                    aa = a.furthest_to(o.position).position
                    self.combinedActions.append(o(SCANNERSWEEP_SCAN, aa.offset((random.randint(-5, 5), random.randint(-5, 5)))))
            elif o.energy > 100 and self.known_enemy_structures.amount == 0:
                self.combinedActions.append(o(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))  # can be improved with random
                self.combinedActions.append(o(SCANNERSWEEP_SCAN, self.state.mineral_field.random.position))
                print("SCAN SEARCH")
            elif o.energy >= 50:
                m = self.state.mineral_field.closer_than(15, o.position)
                if m.amount >= 6:
                    self.combinedActions.append(o(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")

    async def GEBarracks(self, techlabresearch: bool, maxmarauder: int, maxmarine: int, maxreaper: int, maxghost: int):
        if not self.needToExpand:
            a = self.units
            for b in a(BARRACKS).ready.noqueue:
            # if a(BARRACKS).ready.noqueue.exists:
                # b = a(BARRACKS).ready.noqueue.random
                m1 = self.units(MARINE).amount
                m2 = self.units(MARAUDER).amount
                r = self.units(REAPER).amount
                g = self.units(GHOST).amount
                if self.time > 240 and b.add_on_tag == 0:
                    self.combinedActions.append(b(LIFT))
                elif self.time > 240 and self.supply_left == 0 and not techlabresearch:
                    self.combinedActions.append(b(LIFT))
                elif self.units(BARRACKSTECHLAB).exists and self.supply_left > 0:
                    id = self.units(BARRACKSTECHLAB).random.tag
                    if b.add_on_tag == id:
                        if self.can_afford(MARAUDER) and m2 < maxmarauder:
                            self.combinedActions.append(b.train(MARAUDER))
                        elif self.can_afford(GHOST) and g < maxghost and a(GHOSTACADEMY).ready.exists:
                            self.combinedActions.append(b.train(GHOST))
                        elif self.can_afford(REAPER) and r < maxreaper:
                            self.combinedActions.append(b.train(REAPER))
                        elif self.can_afford(MARINE) and m1 < maxmarine:
                            self.combinedActions.append(b.train(MARINE))
                    elif b.add_on_tag == 0:
                        if self.can_afford(BARRACKSREACTOR):
                            p = b.position.offset((2.5, -.5))
                            if await self.can_place(AUTOTURRET, p):
                                print("B_REACTOR")
                                self.combinedActions.append(b.build(BARRACKSREACTOR))
                            else:
                                self.combinedActions.append(b(LIFT))

                        elif self.can_afford(MARINE) and m1 < maxmarine:
                            self.combinedActions.append(b.train(MARINE))
                    else:
                        if self.can_afford(REAPER) and  r < maxreaper:
                            self.combinedActions.append(b.train(REAPER))
                            if self.can_afford(REAPER):
                                await self.do(b.train(REAPER))
                            elif self.can_afford(MARINE) and m1 < maxmarine:
                                await self.do(b.train(MARINE))
                        else:
                            if self.can_afford(MARINE) and m1 < maxmarine:
                                self.combinedActions.append(b.train(MARINE))
                            if self.can_afford(MARINE):
                                await self.do(b.train(MARINE))
                elif self.can_afford(BARRACKSTECHLAB) and not self.units(BARRACKSTECHLAB).exists:
                    self.combinedActions.append(b.build(BARRACKSTECHLAB))
                    print("B_TECHLAB")
                elif techlabresearch:
                    if self.units(BARRACKSTECHLAB).exists:
                        id = self.units(BARRACKSTECHLAB).random.tag
                        if b.add_on_tag == id:
                            print("No Lift")
                        else:
                            self.combinedActions.append(b(LIFT))

    async def GEFactory(self, techlabresearch: bool, allowreactor: bool, maxmsiegetank: int, maxwidowmine: int, maxhellion: int):
        if not self.needToExpand:
            a = self.units
            work = True
            for f in a(FACTORY).ready.noqueue:
            #if a(FACTORY).ready.noqueue.exists:
                #f = a(FACTORY).ready.noqueue.random
                s = (a(SIEGETANK) | a(SIEGETANKSIEGED)).amount
                h = (a(HELLION) | a(HELLIONTANK)).amount
                w = (a(WIDOWMINE) | a(WIDOWMINEBURROWED)).amount
                id = 0
                if a(FACTORYREACTOR).exists:
                    if not allowreactor:
                        work = False
                    else:
                        id = a(FACTORYREACTOR).random.tag
                if not work:
                    self.combinedActions.append(f(LIFT))
                elif self.supply_left > 2 and f.add_on_tag != id:
                    if self.time > 240 and f.add_on_tag == 0:
                        self.combinedActions.append(f(LIFT))
                    elif self.time <= 240 and f.add_on_tag == 0:
                        self.combinedActions.append((f.build(FACTORYTECHLAB)))
                        # add code if a different build is used that gets a factory before 3:30

                    elif self.can_afford(SIEGETANK) and s < maxmsiegetank:
                        self.combinedActions.append(f.train(SIEGETANK))
                    elif self.can_afford(HELLION) and h < maxhellion:
                        self.combinedActions.append(f.train(HELLION))
                    elif self.can_afford(WIDOWMINE) and w <maxwidowmine:
                        self.combinedActions.append(f.train(WIDOWMINE))
                elif self.supply_left > 2 and f.add_on_tag == id and id != 0:
                    await self.chat_send("NO CODE")
                    # code here when get to reactor/hellion/widowmine code
                else:
                    self.combinedActions.append(f(LIFT))
                    print("FLY!!!")

    async def GMStarport(self, techlabresearch: bool, maxmedivac: int, maxviking: int, maxliberator: int, maxraven: int):
        if not self.needToExpand:
            a = self.units
            m = a(MEDIVAC).amount
            v = a(VIKINGFIGHTER).amount
            l = a(LIBERATOR).amount
            r = a(RAVEN).amount
            id = 0
            if a(STARPORTTECHLAB).exists:
                id = a(STARPORTTECHLAB).random.tag
            for s in a(STARPORT).ready.noqueue:
            #if self.units(STARPORT).ready.noqueue.exists:
                #s = self.units(STARPORT).ready.noqueue.random
                if s.add_on_tag == 0:
                    self.combinedActions.append(s(LIFT))
                elif self.supply_left < 4:
                    self.combinedActions.append(s(LIFT))
                if s.add_on_tag != id and self.supply_left > 4:
                    if self.can_afford(MEDIVAC) and m < maxmedivac:
                        await self.do(s.train(MEDIVAC))
                        if self.can_afford(MEDIVAC):
                            self.combinedActions.append(s.train(MEDIVAC))
                    elif v < maxviking:
                        if self.can_afford(STARPORTTRAIN_VIKINGFIGHTER):
                            await self.do(s(STARPORTTRAIN_VIKINGFIGHTER))
                            if self.can_afford(STARPORTTRAIN_VIKINGFIGHTER):
                                self.combinedActions.append(s(STARPORTTRAIN_VIKINGFIGHTER))
                    elif l < maxliberator:
                        if self.can_afford(STARPORTTRAIN_LIBERATOR):
                            await self.do(s(STARPORTTRAIN_LIBERATOR))
                            if self.can_afford(STARPORTTRAIN_LIBERATOR):
                                self.combinedActions.append(s(STARPORTTRAIN_LIBERATOR))
                elif self.supply_left > 2 and r < maxraven:
                    if self.can_afford(RAVEN):
                        self.combinedActions.append(s.train(RAVEN))
                # add code here for battlecruiser or banshee?
                elif self.supply_left > 2 and l < maxliberator:
                    if self.can_afford(STARPORTTRAIN_LIBERATOR):
                        self.combinedActions.append(s(STARPORTTRAIN_LIBERATOR))
                elif self.supply_left > 2 and l < maxviking:
                    if self.can_afford(STARPORTTRAIN_VIKINGFIGHTER):
                        self.combinedActions.append(s(STARPORTTRAIN_VIKINGFIGHTER))
                elif self.supply_left > 2 and l < maxmedivac:
                    if self.can_afford(MEDIVAC):
                        self.combinedActions.append(s.train(MEDIVAC))

    async def GMEngineeringBay(self):
        for e in self.units(ENGINEERINGBAY).ready.idle.noqueue:
            if await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1):
                self.combinedActions.append(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL1))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2):
                self.combinedActions.append(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL2))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3):
                self.combinedActions.append(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYWEAPONSLEVEL3))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1):
                self.combinedActions.append(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL1))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2):
                self.combinedActions.append(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL2))
            elif await self.can_cast(e, ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3) and self.can_afford(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3):
                self.combinedActions.append(e(ENGINEERINGBAYRESEARCH_TERRANINFANTRYARMORLEVEL3))

    async def GMArmory(self, air: bool):
        for a in self.units(ARMORY).ready.idle.noqueue:
            if await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1):
                self.combinedActions.append(a(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL1))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2):
                self.combinedActions.append(a(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL2))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3):
                self.combinedActions.append(a(ARMORYRESEARCH_TERRANVEHICLEWEAPONSLEVEL3))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1):
                self.combinedActions.append(a(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL1))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2):
                self.combinedActions.append(a(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL2))
            elif await self.can_cast(a, ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3) and self.can_afford(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3):
                self.combinedActions.append(a(ARMORYRESEARCH_TERRANVEHICLEANDSHIPPLATINGLEVEL3))
            elif air:
                if await self.can_cast(a, ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1) and self.can_afford(ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1):
                    self.combinedActions.append(a(ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL1))
                elif await self.can_cast(a, ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2) and self.can_afford(ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2):
                    self.combinedActions.append(a(ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL2))
                elif await self.can_cast(a, ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3) and self.can_afford(ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3):
                    self.combinedActions.append(a(ARMORYRESEARCH_TERRANSHIPWEAPONSLEVEL3))

    async def GMBTechlab(self):
        bt = self.units(BARRACKSTECHLAB).ready.noqueue
        if bt.exists:
            bt1 = bt.first
            if await self.can_cast(bt1, RESEARCH_COMBATSHIELD) and self.can_afford(RESEARCH_COMBATSHIELD):
                self.combinedActions.append(bt1(RESEARCH_COMBATSHIELD))
                print("UPGRADE_SHIELD")
            elif await self.can_cast(bt1, BARRACKSTECHLABRESEARCH_STIMPACK) and self.can_afford(BARRACKSTECHLABRESEARCH_STIMPACK):
                self.combinedActions.append(bt1(BARRACKSTECHLABRESEARCH_STIMPACK))
                print("UPGRADE_STIMPACK")

    async def GEsupplydepotdown(self):
        for sd in self.units(SUPPLYDEPOT).ready:
            e = self.known_enemy_units.closer_than(8, sd.position).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                self.combinedActions.append(sd(MORPH_SUPPLYDEPOT_LOWER))

    async def GEsupplydepotup(self):
        for sd in self.units(SUPPLYDEPOTLOWERED).ready:
            e = self.known_enemy_units.closer_than(10, sd.position).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            a = self.units.not_structure.not_flying.closer_than(1.5, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists and not a.exists:
                self.combinedActions.append(sd(MORPH_SUPPLYDEPOT_RAISE))

    async def GEUnfinshedBuildingCheck(self):
        if self.units(SCV).exists:
            for a in self.units.structure.not_ready.exclude_type(REACTOR).exclude_type(BARRACKSREACTOR).exclude_type(FACTORYREACTOR).exclude_type(STARPORTREACTOR).exclude_type(TECHLAB).exclude_type(BARRACKSTECHLAB).exclude_type(FACTORYTECHLAB).exclude_type(STARPORTTECHLAB):
                scvclose = self.units(SCV).closer_than(4, a.position)
                # buildingcheck = False
                # for s in scvclose: # code no work
                    #print(s.is_constructing_scv)
                    #if s.is_constructing_scv:
                     #   buildingcheck = True
                #if not buildingcheck:
                    #scvfar = self.units(SCV).closest_to(a.position)
                    #await self.do(scvfar(BUILD, a))
                e = self.known_enemy_units.closer_than(6, a.position)
                if a.health_percentage < .3 and e.amount > a.health_percentage * 10:
                    self.combinedActions.append(a(CANCEL_BUILDINPROGRESS))
                if not scvclose.exists:
                    self.combinedActions.append(a(CANCEL_BUILDINPROGRESS))

    async def GEBuildingLift(self, distance: float, number: int):
        a = self.units.structure.ready.noqueue
        army = self.units.not_structure.not_flying.exclude_type(SCV)
        b = a(BARRACKS) | a(FACTORY) | a(STARPORT)
        c = a(COMMANDCENTER) | a(ORBITALCOMMAND)
        e = self.known_enemy_units.not_structure.not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
        for aa in b:
            ee = e.closer_than(distance, aa.position)
            army = army.closer_than(distance + 1, aa.position)
            if ee.amount >= number + army.amount:
                self.combinedActions.append(aa(LIFT))
        for cc in c:
            ee = e.closer_than(distance, cc.position)
            army = army.closer_than(distance + 1, cc.position)
            if ee.amount >= number + army.amount:
                self.combinedActions.append(cc(LIFT))
                self.nextXpansionLocation = cc.position

    # Macro Commands
    async def GMUpdateNeedToExpand(self):
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND) | self.units(COMMANDCENTERFLYING) | self.units(ORBITALCOMMANDFLYING)
        if cc.amount == 0 and self.can_afford(COMMANDCENTER):
            self.needToExpand = True
            await self.chat_send("(gg)")
        elif self.supply_used == 100 and cc.amount < 3:
            self.needToExpand = True
            # await self.chat_send("problem 1")
        else:
            i = 0
            for c in cc:
                s = self.units(SCV).closer_than(20, c.position).amount
                m = self.state.mineral_field.closer_than(25, c.position).amount
                i = i + (s)
                i = i - (m*3)
            if i > 0:
                self.needToExpand = True
                # await self.chat_send("problem 2")
        if cc.flying.exists:
            self.needToExpand = False
        elif self.already_pending(COMMANDCENTER):
            self.needToExpand = False
        elif cc.not_ready.exists:
            self.needToExpand = False
        elif cc.amount == 5:
            self.needToExpand = False

    async def GMResetNextXpansionLocation(self):
        self.nextXpansionLocation = await self.get_next_expansion()
        self.nextXpansionLocation = self.nextXpansionLocation.offset((random.randint(-1,1), random.randint(-1,1)))
        if self.can_afford(COMMANDCENTER):
            p = await self.find_placement(COMMANDCENTER, near = self.nextXpansionLocation)
            if p != self.nextXpansionLocation:
                self.nextXpansionLocation = self.nextXpansionLocation.towards(p, 2.5)
                m = (self.state.mineral_field | self.state.vespene_geyser).closer_than(12, self.nextXpansionLocation)
                for mm in m:
                    p = mm.position
                    self.nextXpansionLocation = self.nextXpansionLocation.towards(p, .1)

    async def get_next_expansion(self):
        # method name doesn't match naming convention because of overriding preexisting method
        p = self.start_location
        m = self.state.mineral_field
        mremove = self.state.mineral_field.closer_than(0, p)
        v = self.state.vespene_geyser
        cc = self.units.structure
        cc = cc(COMMANDCENTER) | cc(ORBITALCOMMAND)
        e = self.known_enemy_structures
        for m1 in m:
            if e.closer_than(15, m1.position).exists:
                mremove.append(m1)
            elif cc.closer_than(15, m1.position).exists:
                mremove.append(m1)
        for m1 in mremove:
            m.remove(m1)
        if m.exists:
            p = m.closest_to(p).position
            a = v.closer_than(14, p) | self.state.mineral_field.closer_than(14, p)
            for m2 in a:
                p2 = m2.position
                if p2 != p:
                    p = p.towards(p2, .3)
        return p

    async def GECheckEnemy(self):
        e = self.known_enemy_units
        if e.exists:
            ea = e.closest_to(self.start_location)
            if ea.race == Race.Terran:
                print("change to terran")
                self.STRAT = "AntiTerran"
                if self.time < 360 and not self.airHarrass:
                    if e(BANSHEE).exists or e(STARPORTTECHLAB).exists:
                        self.airHarrass = True
                        await self.chat_send("NO CLOAK BANSHEES!!!")
                else:
                    self.airHarass = False
                if self.time < 360 and not self.earlyArmor:
                    if (e(MARAUDER) | e(SIEGETANK) | e(SIEGETANKSIEGED)).amount > 8:
                        self.earlyArmor = True
            elif ea.race == Race.Zerg:
                print("change to zerg")
                self.STRAT = "AntiZerg"
                if self.time < 360 and not self.airHarrass:
                    if e(MUTALISK).exists or e(SPIRE).exists:
                        self.airHarrass = True
                        await self.chat_send("NO CLOAK MUTALISK!!!")
                else:
                    self.airHarass = False
                if self.time < 360 and not self.earlyArmor:
                    if (e(ROACH)).amount > 8:
                        self.earlyArmor = True
            elif ea.race == Race.Protoss:
                print("change to protoss")
                self.STRAT = "AntiProtoss"
                if self.time < 360 and not self.airHarrass:
                    if e(ORACLE).exists or e(PHOENIX).exists or e(STARPORT).exists:
                        self.airHarrass = True
                        await self.chat_send("NO PHOENIX OR ORACLE!!!")
                else:
                    self.airHarass = False
                if self.time < 360 and not self.earlyArmor:
                    if (e(STALKER) | e(IMMORTAL) | e(COLOSSUS)).amount > 8:
                        self.earlyArmor = True

    async def GMOrbitalScans(self, attack: bool, distance: float):
        o = self.units(ORBITALCOMMAND)
        if o.exists:
            oo = o.random
            a = self.units.not_structure.further_than(distance, oo.position).exclude_type(SCV).exclude_type(REAPER).exclude_type(WIDOWMINEBURROWED)
            e = self.known_enemy_units # this includes structures
            if oo.energy > 50 and a.exists and e.exists:
                ap = a.furthest_to(oo.position).position.towards(e.closest_to(oo.position).position, 10)
                self.combinedActions.append(oo(SCANNERSWEEP_SCAN, ap))
                e2 = self.known_enemy_units.closer_than(16, ap)
                if e2.exists and attack:
                    e2p = e2.random.position
                    for aa in a.closer_than(25, ap):
                        self.combinedActions.append(aa.attack(e2p))

    async def GMPremptiveInvisibleCheck(self):
        e = self.known_enemy_units
        e = e(BANSHEE) | e(GHOST) | e(WIDOWMINE) | e(WIDOWMINEBURROWED) | e(LURKERMP) | e(SWARMHOSTMP) | e(MOTHERSHIP)
        if e.exists:
            oc = self.units(ORBITALCOMMAND)
            if oc.exists:
                oc = oc.random
                if oc.energy > 50:
                    self.combinedActions.append(oc(SCANNERSWEEP_SCAN, e.random.position))

    async def GMInvisibleTrack(self):
        e = self.known_enemy_units.not_structure
        for ee in e:
            if not ee.is_visible:
                oc = self.units(ORBITALCOMMAND)
                if oc.exists:
                    oc = oc.random
                    if oc.energy > 50:
                        self.combinedActions.append(oc(SCANNERSWEEP_SCAN, e.random.position))

    async def GMDefend(self):
        cc = self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        for c in cc:
            threat = self.known_enemy_units.closer_than(25, c.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE).exclude_type(OVERSEER).exclude_type(SCV).exclude_type(DRONE).exclude_type(PROBE)
            if threat.exists:
                army = self.units(MARINE) | self.units(MARAUDER) | self.units(SIEGETANK) | self.units(HELLION) | self.units(VIKINGFIGHTER)
                p = threat.random.position
                for a in army:
                    self.combinedActions.append(a.attack(p))

    async def GERally(self):
        b = self.units.structure.exclude_type(COMMANDCENTER).exclude_type(ORBITALCOMMAND)
        if b.exists:
            p = b.furthest_to(self.start_location).position
            if p != self.start_location:
                p = p.towards(self.start_location, 3)
            for a in b:
                self.combinedActions.append(a(RALLY_BUILDING, p))

    async def GMRally(self, distance: float, move: float):
        building = self.units(SUPPLYDEPOT) | self.units(SUPPLYDEPOTLOWERED) | self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND)
        if self.known_enemy_structures.exists and building.exists:
            e = building.closest_to(self.known_enemy_structures.closest_to(self.start_location).position).position
            if e != self.game_info.map_center:
                e = e.towards(self.game_info.map_center, move)
            self.RallyPoint = building.closest_to(e).position
        elif building.exists:
            self.RallyPoint = building.furthest_to(self.start_location).position
        else:
            self.RallyPoint = self.start_location
        for a in self.units.idle.not_structure.not_flying.exclude_type(HELLION):
            if a.distance_to(self.RallyPoint) > distance:
                p = self.RallyPoint.offset((random.randint(-distance, distance), random.randint(-distance, distance)))
                self.combinedActions.append(a.attack(p))

    async def GMGeneralAttackTriggers(self, minwave: int, bubblesize: float):
            # Note: Poor letter choosing for variables is because I was too lazy to write a method twice and this mostly copy pasted from the AntiZerg equivelant method.
            M1 = self.units(MARINE)
            M2 = self.units(MARAUDER)
            S = self.units(SIEGETANK)
            A = M1 | M2 | S
            if self.known_enemy_units.exclude_type(SCV).exclude_type(DRONE).exclude_type(PROBE).exclude_type(OVERSEER).exists:
                p = self.known_enemy_units.exclude_type(SCV).exclude_type(DRONE).exclude_type(PROBE).exclude_type(OVERSEER).closest_to(self.start_location).position
                if self.supply_used > 190:
                    for m in A:
                        if A.closer_than(bubblesize, m.position).amount >= minwave:
                            self.combinedActions.append(m.attack(p))
                    print("Supply Attack")
                    if not self.enemyknown:
                        self.enemyknown = True
                        await self.chat_send("Here's Moth Bot")
            else:
                if self.supply_used > 190:
                    for m in A.idle:
                        if A.closer_than(bubblesize, m.position).amount >= minwave:
                            p = self.enemy_start_locations[0]
                            i = self.state.mineral_field
                            if i.exists:
                                p = i.random.position
                            self.combinedActions.append(m.attack(p))
                    print("enemy not found")
                    await self.chat_send("All scouting and no play makes MothBot a dull AI")
                    await self.chat_send(":(")
                    self.enemyknown = False

    async def GMReaperMove(self, distance: int):
        for r in self.units(REAPER):
            move = False
            p = r.position
            enemy = self.known_enemy_units.closer_than(distance, p).not_structure.exclude_type([SCV, DRONE, PROBE])
            a = self.units.closer_than(distance, p)
            if enemy.amount * 2 > a.amount:
                e = enemy.closest_to(p).position
                p = p.towards(e, -10)
                move = True
            elif not r.is_moving:
                scv = self.known_enemy_units
                scv = scv(SCV) | scv(DRONE) | scv(PROBE)
                scv = scv.closer_than(distance, p)
                if scv.exists:
                    print()
                elif self.known_enemy_structures.exists:
                    if self.supply_used > 190:
                        a = self.units(MARINE)
                        if a.exists:
                            e = self.known_enemy_structures.closest_to(self.start_location).position
                            a2 = a.closest_to(e)
                            if a2.distance_to(e) < 25:
                                m = m = self.state.mineral_field.closer_than(25, e)
                            else:
                                m = self.units(MARINE).closer_than(10, a2.position)
                        else:
                            m = self.state.mineral_field.closer_than((self.supply_used * 1), self.start_location)
                    else:
                        m = self.state.mineral_field.closer_than((self.supply_used * 1), self.start_location)
                    self.enemyknown = True
                else:
                    m = self.state.mineral_field.closer_than((self.supply_used*4), self.start_location)
                    self.enemyknown = False
                    await self.chat_send("...")
                if scv.exists:
                    p = scv.random.position
                    move = True
                    print("WORKER SPOTTED")
                elif m.exists:
                    p = m.random.position
                    move = True
                    print("SCOUT")
            if move:
                self.combinedActions.append(r.move(p))  # converted to move because of proximity command

    async def GEReaperScout(self):
        i = len(self.enemy_start_locations)
        j = random.randint(0, i-1)
        self.enemyknown = False
        self.target = self.enemy_start_locations[j]
        if self.known_enemy_structures.exists:
            self.enemyknown = True
            self.target = self.known_enemy_structures.random.position
        m = self.state.mineral_field.closer_than(20, self.target)
        if m.exists:
            self.target = m.random.position
        for r in self.units(REAPER).idle:
            print("Moving")
            print(self.target)
            # await self.chat_send("Killing Workers")
            self.combinedActions.append(r.move(self.target))

    async def GMRepair(self, percent: float, distance: float):
        s = self.units
        scv = s(SCV)
        s = s.structure | s(MEDIVAC) | s(SIEGETANK) | s(RAVEN)
        if scv.exists:
            damagedList = []
            for s1 in s:
                if s1.health_percentage < percent:
                    if scv.closer_than(distance, s1.position).exists:
                        damagedList.append(s1)
            s = self.units.structure.not_structure
            for s1 in damagedList:
                s.append(s1)
            for s1 in damagedList:
                scv1 = scv.closest_to(s1.position)
                s2 = s.closest_to(scv1.position)
                self.combinedActions.append(scv1(EFFECT_REPAIR_SCV, s2)) # This is designed to have redundant calls.

    # Army Proximity and Micro Commands
    async def GMMarineProximity(self, proximity: float, friends: float):
        for m in self.units(MARINE):
            a = self.units.closer_than(friends, m.position)
            threat = self.known_enemy_units.not_structure.closer_than(proximity, m.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if True:
                if threat.exists and m.health_percentage > 2/8 and not threat.amount > a.amount * 2:
                    print("M_ATTACK")
                    if await self.can_cast(m, EFFECT_STIM_MARINE) and m.health_percentage > 6/8 and not m.has_buff(BuffId.STIMPACK):
                        self.combinedActions.append(m(EFFECT_STIM_MARINE))
                        print("STIM")
                        self.combinedActions.append(m.attack(threat.closest_to(m.position).position))
                elif threat.amount > a.amount * 2:
                    if threat.closest_to(m.position).position.distance_to(m.position) > 6:
                        p = m.position.towards(self.start_location, 5)
                        self.combinedActions.append(m.move(p))

    async def GEMarineAttack(self):
        for m in self.units(MARINE):
            threat = self.known_enemy_units.not_structure.closer_than(6, m.position)
            if threat.exists and m.weapon_cooldown < 0.1:
                ea = threat
                if ea.exists:
                    target = ea.closest_to(m.position)
                    priority = ea(LIBERATORAG) | ea(MEDIVAC) | ea(VIKINGFIGHTER) | ea(SIEGETANK) | ea(SIEGETANKSIEGED) | ea(LIBERATOR) | ea(WIDOWMINE) | ea(WIDOWMINEBURROWED) | ea(BANELING) | ea(LURKER) | ea(LURKERMP) | ea(CARRIER)
                    if priority.exists:
                        target = priority.closest_to(m.position)
                    self.combinedActions.append(m.attack(target))
            threat = threat.closer_than(4, m.position)
            if threat.exists and m.weapon_cooldown > 0.1:
                p = m.position.towards(threat.closest_to(m.position).position, -1)
                self.combinedActions.append(m.move(p))

    async def GMMarauderProximity(self, proximity: float):
        for m in self.units(MARAUDER):
            threat = self.known_enemy_units.not_structure.not_flying.closer_than(proximity, m.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if threat.exists:
                print("M_ATTACK")
                if await self.can_cast(m, EFFECT_STIM_MARAUDER) and m.health_percentage > 7/10 and not m.has_buff(BuffId.STIMPACKMARAUDER):
                    self.combinedActions.append(m(EFFECT_STIM_MARAUDER))
                    print("STIM")
                    self.combinedActions.append(m.attack(threat.closest_to(m.position).position))

    async def GEMarauderAttack(self):
        for m in self.units(MARAUDER):
            threat = self.known_enemy_units.not_structure.closer_than(7.1, m.position).not_flying
            if threat.exists and m.weapon_cooldown < 0.1:
                ea = threat.closer_than(6.1, m.position)
                if ea.exists:
                    target = ea.closest_to(m.position)
                    priority = ea(SIEGETANK) | ea(SIEGETANKSIEGED) | ea(WIDOWMINE) | ea(WIDOWMINEBURROWED) | ea(LURKER) | ea(LURKERMP) | ea(BANELING)
                    if priority.exists:
                        target = priority.closest_to(m.position)
                    self.combinedActions.append(m.attack(target))
            threat = threat.closer_than(6, m.position)
            if threat.exists and m.weapon_cooldown > 0.1:
                p = m.position.towards(threat.closest_to(m.position).position, -1)
                self.combinedActions.append(m.move(p))

    async def GMStepForwardBackward(self, allydistance: float, enemydistance: float):
        a = self.units.not_structure
        b = a(MARINE) | a(MARAUDER) | a(SIEGETANK)
        f = a(RAVEN) | a(MEDIVAC)
        e = self.known_enemy_units
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
                            self.combinedActions.append(m.move(p))
                    if aa * 3 < eee:
                        ep = e.closest_to(p).position
                        if ep != p:
                            p = p.towards(ep, -10)
                            self.combinedActions.append(m.move(p))
            for ff in f:
                antiair = e(MISSILETURRET) | e(SPORECRAWLER)
                if antiair.exists:
                    p = ff.position
                    p2 = antiair.closest_to(ff).position
                    if p2.distance_to(p) < (7 + 5): # range of missile turret + my fear of losing units
                        p = p.towards(p2, -3)
                        self.combinedActions.append(ff.move(p))

    async def GEReaperProximity(self):
        for r in self.units(REAPER):
            threat = self.known_enemy_units.closer_than(10, r.position).not_structure.not_flying
            if threat.exists:
                death = threat.closest_to(r.position)
                p = death.position.towards(r.position, 1)
                if p.distance_to(r.position) < 6:
                    if await self.can_cast(r, KD8CHARGE_KD8CHARGE, p):
                        self.combinedActions.append(r(KD8CHARGE_KD8CHARGE, p))
                        print("GRENADE")
                        print(p)
                        await self.chat_send("GRENADE!!!")
                    elif r.weapon_cooldown == 0:
                        self.combinedActions.append(r.attack(death))
                    else:
                        p = death.position.towards(r.position, 5.5)
                        self.combinedActions.append(r.move(p))
                if r.health_percentage < 3 / 7:
                    nodeath = r.position.towards(death.position, -4)
                    self.combinedActions.append(r.move(nodeath))

    async def GMSiegeTankProximity(self, proximity: float, structure: bool):
        for s in self.units(SIEGETANK):
            threat = self.known_enemy_units.closer_than(proximity, s).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if not structure:
                threat =  threat.not_structure
            if threat.exists:
                self.combinedActions.append(s(SIEGEMODE_SIEGEMODE))
                print("SIEGE")

    async def GMSiegedTankProximity(self, proximity: float, structure: bool):
        for s in self.units(SIEGETANKSIEGED):
            threat = self.known_enemy_units.closer_than(proximity, s).not_flying.exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            if not structure:
                threat =  threat.not_structure
            if not threat.exists:
                self.combinedActions.append(s(UNSIEGE_UNSIEGE))
                print("UNSIEGE")

    async def GMSiegeTankFollow(self, distance: float):
        s = self.units(SIEGETANK).idle
        m = self.units(MARINE) | self.units(MARAUDER)
        for s1 in s:
            if m.exists:
                mp = m.closest_to(s1.position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                self.combinedActions.append(s1.attack(mp))

    async def GMWidowBurrowProximity(self, proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool):
        # note: to disable non-boolean modes, set floats to zero
        for w in self.units(WIDOWMINE):
            threat = self.known_enemy_units.closer_than(proximity, w.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            burrow = False
            if not structure:
                threat = threat.not_structure
            if threat.exists:
                burrow = True
            mineral = self.state.mineral_field.closer_than(mineraldistance, w.position)
            if mineral.exists and self.known_enemy_structures.closer_than(enemybasedistance, w.position).exists:
                    burrow = True
            if defend:
                scv = self.units(SCV).closer_than(proximity / 2, w.position)
                if scv.exists and mineral.exists:
                    burrow = True
            if burrow:
                self.combinedActions.append(w(BURROWDOWN_WIDOWMINE))

    async def GMWidowUnburrowProximity(self, proximity: float, enemybasedistance: float, mineraldistance: float, structure: bool, defend: bool):
        # note: to disable non-boolean modes, set floats to zero
        for w in self.units(WIDOWMINEBURROWED):
            threat = self.known_enemy_units.closer_than(proximity, w.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE)
            unburrow = True
            if not structure:
                threat = threat.not_structure
            mineral = self.state.mineral_field.closer_than(mineraldistance, w.position)
            if defend:
                scv = self.units(SCV).closer_than(proximity/2, w.position)
                if scv.exists and mineral.exists:
                    unburrow = False
            if mineral.exists:
                if self.known_enemy_structures.closer_than(enemybasedistance, w.position).exists:
                    unburrow = False
            if threat.exists:
                unburrow = False
            if unburrow:
                self.combinedActions.append(w(BURROWUP_WIDOWMINE))

    async def GMWidowTrapTravel(self, mindistance: float, maxdistance: float):
        e = self.known_enemy_structures
        if e.exists:
            ep = e.closest_to(self.start_location).position
            distance = ep.distance_to(self.start_location)
            m = self.state.mineral_field.closer_than(maxdistance, ep).further_than(mindistance, ep).closer_than(distance, self.start_location)
            if m.exists:
                for w in self.units(WIDOWMINE).idle:
                    p = m.random.position
                    self.combinedActions.append(w.move(p))

    async def GMWidowFollow(self, distance: float, scv: bool, army: bool):
        w = self.units(WIDOWMINE).idle
        a = self.units
        m = a(MARINE) | a(MARAUDER) | a(SIEGETANK) | a(SIEGETANKSIEGED)
        s = a(SCV)
        a = a.structure.not_structure
        if scv:
            a = a | s
        if army:
            a = a | m
        if a.exists:
            for w1 in w:
                e = self.known_enemy_units
                if e.exists:
                    mp = m.closest_to(e.closest_to(w1.position).position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                else:
                    mp = m.closest_to(w1.position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                self.combinedActions.append(w1.move(mp))

    async def GMMedivacProximity(self):
        m = self.units(MARINE) | self.units(MARAUDER)
        if m.exists:
            for medivac in self.units(MEDIVAC):
                p = m.furthest_to(self.start_location).position.towards(self.start_location, 2)
                p = p.offset((random.randint(-4, 4), random.randint(-4, 4)))
                self.combinedActions.append(medivac.attack(p))

    async def GMAirFollow(self, distance: float):
        s = self.units.idle
        s = s(VIKINGFIGHTER) | s(LIBERATOR)
        m = self.units(MEDIVAC) | self.units(RAVEN)
        for s1 in s:
            if m.exists:
                mp = m.closest_to(s1.position.offset((random.randint(-distance, distance), random.randint(-distance, distance)))).position
                self.combinedActions.append(s1.attack(mp))

    async def GMAntiAirAttack(self, proximity: float):
        s = self.units
        s = s(VIKINGFIGHTER) | s(LIBERATOR)
        e = self.known_enemy_units.flying
        for s1 in s:
            ea = e.closer_than(proximity, s1.position)
            if ea and s1.weapon_cooldown < .1:
                self.combinedActions.append(s1.attack(ea.closest_to(s1.position)))

    async def GMRavenProximity(self):
        for r in self.units(RAVEN):
            e = self.known_enemy_units.not_structure.closer_than(11, r.position).exclude_type(CHANGELING).exclude_type(CHANGELINGMARINESHIELD).exclude_type(CHANGELINGMARINE).exclude_type(OVERSEER).exclude_type(PROBE).exclude_type(SCV).exclude_type(DRONE).exclude_type(LARVA).exclude_type(EGG)
            if e.exists and r.energy > 75:
                eMechPriority = e(SIEGETANKSIEGED) | e(VIKINGFIGHTER) | e(LIBERATOR) | e(LIBERATORAG) |e(BATTLECRUISER) | e(WIDOWMINE) | e(WIDOWMINEBURROWED) | e(THOR) | e(CARRIER) | e(VOIDRAY) | e(CARRIER) | e(COLOSSUS) | e(MOTHERSHIP) | e(TEMPEST)
                if eMechPriority.exists:
                    ea = eMechPriority.random
                    if await self.can_cast(r, EFFECT_INTERFERENCEMATRIX, ea) and not ea.has_buff(BuffId.DISABLEABILS):
                        self.combinedActions.append(r(EFFECT_INTERFERENCEMATRIX, ea))
                        print("INTERENCE MATRIX")
                        await self.chat_send("INTERENCE MATRIX!!!")
                else:
                    ea = e.random
                    eap = ea.position
                    e2 = e.closer_than(3, eap)
                    r2 = self.units.closer_than(5, eap)  # arbituary numbers used
                    if r.position.distance_to(ea.position) > 6 and e2.amount > r2.amount + 2 and await self.can_cast(r, EFFECT_ANTIARMORMISSILE, ea) and not ea.has_buff(BuffId.RAVENSHREDDERMISSILEARMORREDUCTION):
                        self.combinedActions.append(r(EFFECT_ANTIARMORMISSILE, ea))
                        print("ORANGE!!!")
                        await self.chat_send("ORANGE!!!")
                    else:
                        print("idk debug this")
                        """
                        if self.can_afford(AUTOTURRET):
                            p = await self.find_placement(AUTOTURRET, near=r.position)
                            x = p.x
                            y = p.y
                            p3 = p.to3(2)
                            if await self.can_cast(r(AbilityId.RAVENBUILD_AUTOTURRET, p)):
                                await self.do(r(AbilityId.RAVENBUILD_AUTOTURRET, p))"""
            elif e.exists:
                ea = e.closest_to(r.position)
                p = ea.position.towards(r.position, 13)
                self.combinedActions.append(r.move(p))
            else:
                a = self.units(MARINE) | self.units(MARAUDER) | self.units(SIEGETANK) | self.units(SIEGETANKSIEGED)
                if a.exists and r.is_idle:
                    p = a.furthest_to(self.start_location).position.towards(self.start_location, 3)
                    p = p.towards(a.closest_to(r.position).position, 4)
                    self.combinedActions.append(r.move(p))
