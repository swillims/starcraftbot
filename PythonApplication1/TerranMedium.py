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

class TerranMediumAI(BotAI):
    async def on_step(self, iteration):

        """commands sorted based off of processing priority"""
        if iteration % 5 == 0:
            await self.reapernotdie()

        if iteration % 10 == 0:
            await self.reaperscout()
            await self.distribute_workers()
            await self.buildstuff()
            await self.managesupply()
            await self.commandcenter()
            await self.supplydepotup()

        if iteration % 15 == 0:
            await self.barracks()
            await self.factory()
            await self.hellionproximity()

        if iteration % 20 == 0:
            await self.workerdefend()
            await self.getgas()

        if iteration % 25 == 0:
            await self.siegetankproximity()

        if iteration % 50 == 0:
            await self.landstuff()

        if iteration % 200 == 0:
            await self.armyattack()
            await self.orbitalcommand()
            await self.supplydepotdown()
            await self.hellbatproximity()

        if iteration % 500 == 0:
            await self.supplydepotdown()
            await self.siegedtankproximity()

        if iteration % 2000 == 0:
            await self.rallyset()
            await self.militarygroup()


        """potentially buggy commands"""
        """Smoke testing says pretty much all methods are fineish but I believe that all of them are"""

        """methods declared"""

    """army methods"""

    async def workerdefend(self):
        for cc in self.structures(UnitTypeId.COMMANDCENTER) | self.structures(UnitTypeId.ORBITALCOMMAND):
            enemyclose = self.enemy_units.closer_than(12, cc.position)
            if enemyclose.amount > 2:
                p = enemyclose.random.position
                for scv in self.units.not_structure.closer_than(30, cc.position):
                    scv.attack(p)
                    """it's also non scv units"""
                for lazy in self.units.not_structure.idle.closer_than(50, cc.position):
                    lazy.attack(p)
                for r in self.units(UnitTypeId.REAPER) | self.units(UnitTypeId.HELLION):
                    r.attack(p)
                for b in self.structures(UnitTypeId.BARRACKS):
                    b(AbilityId.RALLY_BUILDING, p)
                print("defend")

    async def reaperscout(self):
        for r in self.units(UnitTypeId.REAPER).idle:
            if len(self.enemy_structures) == 0:
                m = self.mineral_field.closer_than((self.supply_used*2)+20, self.start_location).random.position
                r.attack(m)
            else:
                if self.units(UnitTypeId.REAPER).amount > 5:
                    if self.units(UnitTypeId.REAPER).closer_than(6, r).amount < 5:
                        p = self.units(UnitTypeId.REAPER).random.position
                        r.attack(p)
                        print("GROUP")
                        for r1 in self.units(UnitTypeId.REAPER).closer_than(10, r):
                            r1.attack(self.enemy_structures.random.position)
                            print("KILL")
                else:
                    m = self.mineral_field.closer_than((self.supply_used) + 10, self.start_location).random.position
                    r.attack(m)
    
    async def reapernotdie(self):
        for r in self.units(UnitTypeId.REAPER):
            death = self.enemy_units.closer_than(4.5, r).not_structure.not_flying
            if death.exists:
                p = r.position.towards(death.random.position, -7)
                if self.can_cast(r,AbilityId.KD8CHARGE_KD8CHARGE,death.random.position):
                    r(AbilityId.KD8CHARGE_KD8CHARGE, death.random.position)
                r.move(p)
            elif r.health_percentage < 5/7:
                death2 = self.enemy_units.closer_than(8, r)
                if death2.exists:
                    p = r.position.towards(death2.random.position, -12)
                    r.move(p)

    async def hellionproximity(self):
        if self.structures(UnitTypeId.ARMORY).ready.exists:
            for h in self.units(UnitTypeId.HELLION):
                if self.enemy_units.closer_than(10, h.position).not_structure.not_flying.exists:
                    h(AbilityId.MORPH_HELLBAT)

    async def hellbatproximity(self):
        if self.structures(UnitTypeId.ARMORY).ready.exists:
            for h in self.units(UnitTypeId.HELLIONTANK):
                death = self.enemy_units.closer_than(20, h.position).not_structure.not_flying
                if death.exists:
                    h.attack(death.random.position)
                else:
                    h(AbilityId.MORPH_HELLION)

    async def siegetankproximity(self):
        threat = self.enemy_units
        if threat.exists:
            for s in self.units(UnitTypeId.SIEGETANK):
                death = threat.closer_than(12, s)
                if death.exists:
                    s(AbilityId.SIEGEMODE_SIEGEMODE)

    async def siegedtankproximity(self):
        threat = self.enemy_units
        if threat.exists:
            for s in self.units(UnitTypeId.SIEGETANKSIEGED):
                death = threat.closer_than(15, s)
                if not death.exists:
                    s(AbilityId.UNSIEGE_UNSIEGE)

    async def militarygroup(self):
        mr = self.units(UnitTypeId.MARAUDER)
        for m in self.units(UnitTypeId.MARINE).idle | self.units(UnitTypeId.MARAUDER).idle:
            if self.units(UnitTypeId.SUPPLYDEPOTLOWERED).amount > 0:
                m.attack(self.units.structure.random.position)
        hel = self.units(UnitTypeId.HELLION)
        if hel.amount < 8:
            for h in hel.idle:
                h.attack(self.units.not_structure.random.position)
        else:
            m = self.mineral_field.closer_than(self.supply_used + 30, self.start_location)
            if m.exists:
                for h in hel.idle:
                    h.attack(m.random.position)
        for s in self.units(UnitTypeId.SIEGETANK).idle:
            s.attack(self.units.random.position)

    async def armyattack(self):
        y = self.units(UnitTypeId.MARINE)
        x = self.units(UnitTypeId.MARAUDER)
        r = self.units(UnitTypeId.REAPER)
        h = self.units(UnitTypeId.HELLION)
        s = self.units(UnitTypeId.SIEGETANK) | self.units(UnitTypeId.HELLIONTANK)
        if self.enemy_units.amount > 0 and self.enemy_units.closer_than(50, self.start_location).amount > 5:
            p = self.enemy_units.random.position
            for a in x | y | h | r | s:
                a.attack(p)
        elif self.enemy_structures.amount > 0 and x.amount + (y.amount*1.5) + (s.amount*2) > 35 and self.units(UnitTypeId.ORBITALCOMMAND).amount < 2:
            p = self.enemy_structures.random.position
            for a in x | y | h | r | s:
                a.attack(p)
        elif self.enemy_structures.amount > 0 and x.idle.amount + (y.idle.amount*1.25) + (s.idle.amount*2) > 50:
            p = self.enemy_structures.random.position
            for a in x | y | h | r | s:
                a.attack(p)

    """methods"""

    async def commandcenter(self):
        for cc in self.structures(UnitTypeId.COMMANDCENTER).idle:
            if self.structures(UnitTypeId.BARRACKS).amount >= 2 and self.structures(UnitTypeId.COMMANDCENTER).not_ready.amount > 0:
                    if self.can_afford(UnitTypeId.ORBITALCOMMAND):
                        cc(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
            elif self.units(UnitTypeId.SCV).amount < (self.structures(UnitTypeId.COMMANDCENTER).amount * 14) + (self.structures(UnitTypeId.ORBITALCOMMAND).amount * 12 ) + 8:
                if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 40 and self.supply_used < 200:
                    cc.train(UnitTypeId.SCV)
                elif self.structures(UnitTypeId.BARRACKS).amount >= 2 and self.structures(UnitTypeId.COMMANDCENTER).amount >= 2 and not self.already_pending(UnitTypeId.ORBITALCOMMAND):
                    if self.can_afford(UnitTypeId.ORBITALCOMMAND) and self.structures(UnitTypeId.ORBITALCOMMAND).amount < 3:
                        cc(AbilityId.UPGRADETOORBITAL_ORBITALCOMMAND)
                    elif self.can_afford(UnitTypeId.PLANETARYFORTRESS) and self.structures(UnitTypeId.ENGINEERINGBAY).ready.exists:
                        cc(AbilityId.UPGRADETOPLANETARYFORTRESS_PLANETARYFORTRESS)

    async def orbitalcommand(self):
        for cc in self.structures(UnitTypeId.ORBITALCOMMAND).ready:
            if cc.energy > 100 and not self.enemy_structures.amount > 0:
                    cc(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])
                    cc(AbilityId.SCANNERSWEEP_SCAN, self.mineral_field.random.position)

            elif cc.energy > 50 and self.supply_left <= 0 and self.supply_used != 200:
                if self.structures(UnitTypeId.SUPPLYDEPOT).amount > 0:
                    cc(AbilityId.SUPPLYDROP_SUPPLYDROP, self.structures(UnitTypeId.SUPPLYDEPOT).random)
                elif self.structures(AbilityId.SUPPLYDEPOTLOWERED).amount>0:
                    cc(AbilityId.SUPPLYDROP_SUPPLYDROP, self.structures(AbilityId.SUPPLYDEPOTLOWERED).random)

            elif cc.energy > 75 and self.enemy_structures.amount > 0:
                m = self.mineral_field.closer_than(8, cc.position)
                if m.amount > 5:
                    cc(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)

            elif cc.energy == 200:
                cc(AbilityId.SCANNERSWEEP_SCAN, self.units.random.position)
                cc(AbilityId.SCANNERSWEEP_SCAN, self.enemy_start_locations[0])
                m = self.mineral_field.closer_than(8, cc.position)
                if m.amount > 5:
                    cc(AbilityId.CALLDOWNMULE_CALLDOWNMULE, m.random)

            if self.units(UnitTypeId.SCV).amount < (self.structures(UnitTypeId.COMMANDCENTER).amount * 10) + self.structures(UnitTypeId.ORBITALCOMMAND).amount * 6:
                """significantly below other methods for scv production on purpose"""
                if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < 40 and self.supply_used < 200:
                    cc.train(UnitTypeId.SCV)

                    """
            if cc.energy == 200 and self.enemy_structures.amount > 0:
                p = self.enemy_structures.random.position
                cc(SCANNERSWEEP_SCAN, p))
                cc(CALLDOWNMULE_CALLDOWNMULE, p.towards(self.game_info.map_center, -3)))
                
                code removed for being pointless but it is funny
                """

    async def barracks(self):
        oc = self.structures(UnitTypeId.ORBITALCOMMAND).ready
        for b in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if b.add_on_tag == 0 and self.supply_used < 200:
                if self.can_afford(UnitTypeId.REAPER):
                    if self.units(UnitTypeId.REAPER).amount > 0:
                        if self.structures(UnitTypeId.BARRACKSTECHLAB).amount < 2:
                            b.build(UnitTypeId.BARRACKSTECHLAB)
                            if oc.amount > 0:
                                occ = oc.random
                                scv = self.units(UnitTypeId.SCV).closer_than(6, occ)
                                if scv.amount>0:
                                    scv = scv.random
                                    p = occ.position.towards(scv.position, -8)
                                    b.build((UnitTypeId.BARRACKSTECHLAB),p)
                            else:
                                b.train(UnitTypeId.MARINE)
                        else:
                            b.train(UnitTypeId.MARINE)
                    elif self.units(UnitTypeId.REAPER).amount <= self.units(UnitTypeId.MARINE).amount / 5:
                        b.train(UnitTypeId.REAPER)
                    else:
                        b.train(UnitTypeId.MARINE)
                elif self.can_afford(UnitTypeId.MARINE):
                    b.train(UnitTypeId.MARINE)
            elif self.supply_used < 200:
                if self.can_afford(UnitTypeId.MARAUDER):
                    b.train(UnitTypeId.MARAUDER)
                elif self.can_afford(UnitTypeId.MARINE):
                    b.train(UnitTypeId.MARINE)

    async def factory(self):
        if self.supply_used < 200:
            for f in self.structures(UnitTypeId.FACTORY).ready.idle:
                ftl = self.structures(UnitTypeId.FACTORYTECHLAB)
                if ftl.exists:
                    id = self.structures(UnitTypeId.FACTORYTECHLAB).random.tag
                    if f.add_on_tag == 0:
                        if self.can_afford(UnitTypeId.SIEGETANK):
                            f.build(UnitTypeId.FACTORYREACTOR)
                            scv = self.units(UnitTypeId.SCV).random
                            p = scv.position.towards(self.game_info.map_center, random.randint(4, 8))
                            f.build(UnitTypeId.FACTORYREACTOR, p)
                        elif self.can_afford(UnitTypeId.HELLION):
                            f.train(UnitTypeId.HELLION)
                    elif f.add_on_tag == id:
                        if self.can_afford(UnitTypeId.SIEGETANK):
                            f.train(UnitTypeId.SIEGETANK)
                        elif self.can_afford(UnitTypeId.HELLION):
                            f.train(UnitTypeId.HELLION)
                    elif self.can_afford(UnitTypeId.HELLION):
                        f.train(UnitTypeId.HELLION)
                        if self.can_afford(UnitTypeId.HELLION):
                            f.train(UnitTypeId.HELLION)
                elif self.can_afford(UnitTypeId.HELLION):
                    if self.can_afford(UnitTypeId.SIEGETANK):
                        f.build(UnitTypeId.FACTORYTECHLAB)
                        scv = self.units(UnitTypeId.SCV)
                        if scv.amount >= 20:
                            s1 = scv.random
                            s2 = scv.random
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            f.build(UnitTypeId.FACTORYTECHLAB, p)
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            f.build(UnitTypeId.FACTORYTECHLAB, p)
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            f.build(UnitTypeId.FACTORYTECHLAB, p)
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            f.build(UnitTypeId.FACTORYTECHLAB, p)
                            """random places until it works*"""
                    else:
                        f.train(UnitTypeId.HELLION)


    async def supplydepotdown(self):
        for sd in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
            e = self.enemy_units.closer_than(6, sd.position)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

    async def supplydepotup(self):
        for sd in self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            e = self.enemy_structures.closer_than(8, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists:
                sd(AbilityId.MORPH_SUPPLYDEPOT_RAISE)

    async def landstuff(self):
        for b in self.structures(UnitTypeId.BARRACKSFLYING).idle:
            """This code is a back up code to patch a problem. It is buggy and should not be relied on"""
            print("fly b")
            p = self.start_location
            cc = self.structures(UnitTypeId.COMMANDCENTER) or self.structures(UnitTypeId.ORBITALCOMMAND) or self.structures(UnitTypeId.SUPPLYDEPOTLOWERED) or self.structures(UnitTypeId.BARRACKS) or self.structures(UnitTypeId.SUPPLYDEPOT)
            if cc.amount > 0:
                c = cc.random
                p = c.position.towards(self.enemy_start_locations[0], random.randint(1, 11))
            b(AbilityId.LAND, p)
        for f in self.structures(UnitTypeId.FACTORYFLYING).idle:
            print("fly f")
            p = self.start_location
            cc = self.structures(UnitTypeId.COMMANDCENTER) or self.structures(UnitTypeId.ORBITALCOMMAND) or self.structures(UnitTypeId.SUPPLYDEPOTLOWERED) or self.structures(UnitTypeId.BARRACKS) or self.structures(UnitTypeId.SUPPLYDEPOT)
            if cc.amount > 0:
                c = cc.random
                p = c.position.towards(self.enemy_start_locations[0], random.randint(1, 11))
            f(AbilityId.LAND, p)

    async def rallyset(self, ):
        p = self.start_location.towards(self.game_info.map_center, 8)
        s = self.structures(UnitTypeId.SUPPLYDEPOT).ready
        if s.exists:
            p = s.random.position.towards(self.game_info.map_center, 1.5)
        for b in self.structures(UnitTypeId.BARRACKS) | self.structures(UnitTypeId.FACTORY):
            b(AbilityId.RALLY_BUILDING, p)
        self.rallypos = p

    "build methods"
    async def buildstuff(self):
        cc = self.structures(UnitTypeId.COMMANDCENTER).ready
        oc = self.structures(UnitTypeId.ORBITALCOMMAND).ready
        sd = (self.structures(UnitTypeId.SUPPLYDEPOT).ready | self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).ready)
        if self.can_afford(UnitTypeId.COMMANDCENTER):
            if self.minerals > 300 + self.supply_used*3:
                await self.expand_now()
        if self.can_afford(UnitTypeId.BARRACKS):
            if (cc.exists or oc.exists) and sd.exists:
                if self.structures(UnitTypeId.BARRACKS).amount < 1 + cc.amount + (oc.amount*1):
                    if self.structures(UnitTypeId.BARRACKSFLYING).amount == 0:
                        if self.structures(UnitTypeId.BARRACKS).amount == 0:
                            p = self.start_location.towards(self.game_info.map_center, 5)
                            await self.build(UnitTypeId.BARRACKS, p)
                        else:
                            if cc.exists:
                                a = cc.random
                                re = self.structures(UnitTypeId.REFINERY).closer_than(10, a.position)
                                if re.amount > 0:
                                    r = re.random
                                    p = a.position.towards(r.position, -8)
                                    await self.build(UnitTypeId.BARRACKS, p)
                                else:
                                    await self.build(UnitTypeId.BARRACKS, near=sd.first)
                            elif oc.exists:
                                a = oc.random
                                re = self.structures(UnitTypeId.REFINERY).closer_than(10, a.position)
                                if re.amount > 0:
                                    r = re.random
                                    p = a.position.towards(r.position, -8)
                                    await self.build(UnitTypeId.BARRACKS, near=p)
                else:
                    if self.can_afford(UnitTypeId.FACTORY) and oc.exists:
                        if self.structures(UnitTypeId.ENGINEERINGBAY).amount == 0 and self.structures(UnitTypeId.FACTORY).amount > 0:
                            if oc.exists and not self.already_pending(UnitTypeId.ENGINEERINGBAY):
                                await self.build(UnitTypeId.ENGINEERINGBAY, near=sd.first)
                        else:
                            if self.structures(UnitTypeId.FACTORY).amount + self.structures(UnitTypeId.FACTORYFLYING).amount < 2 and not self.already_pending(UnitTypeId.FACTORY):
                                await self.build(UnitTypeId.FACTORY, near=sd.first)
                            elif oc.exists:
                                if self.structures(UnitTypeId.ARMORY).amount < 1 and oc.amount > 0 and not self.already_pending(UnitTypeId.ARMORY):
                                    await self.build(UnitTypeId.ARMORY, near=sd.first)

    async def managesupply(self):
        if self.supply_left < 2 + (self.supply_used/10) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            cc = self.structures(UnitTypeId.COMMANDCENTER).ready | self.structures(UnitTypeId.ORBITALCOMMAND).ready
            if cc.exists:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT) and self.structures(UnitTypeId.SUPPLYDEPOTLOWERED).amount < 14:
                    if self.structures(UnitTypeId.SUPPLYDEPOT).amount > 0:
                        await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)
                        """this has been changed because of lowering"""
                    else:
                        if self.units(UnitTypeId.SCV).amount>0:
                            p = self.start_location.towards(self.game_info.map_center, 11)
                            await self.build(UnitTypeId.SUPPLYDEPOT, p)
        elif self.supply_left < 0 and self.can_afford(UnitTypeId.SUPPLYDEPOT):
            await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.random)

    async def getgas(self):
        if self.structures(UnitTypeId.BARRACKS).amount > 0 and self.structures(UnitTypeId.REFINERY).amount < self.structures(UnitTypeId.COMMANDCENTER).amount + (self.structures(UnitTypeId.ORBITALCOMMAND).amount):
            for cc in self.structures(UnitTypeId.COMMANDCENTER).ready:
                v = self.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
                            if not self.structures(UnitTypeId.REFINERY).closer_than(1, ve).exists:
                                #worker = self.select_self.build_worker(ve.position)
                                #if worker is None:
                                #    break
                                #worker.self.build(UnitTypeId.REFINERY, ve)
                                await self.build(UnitTypeId.REFINERY, ve)

"""end class"""

"""TEST SCRIPT BELOW"""
"""
run_game(maps.get("(2)16-Bit LE"), [
    Bot(Race.Terran, TerranMediumAI()),
    Computer(Race.Random, Difficulty.Medium)
], realtime=True)

run_game(maps.get("(2)16-Bit LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("(2)Acid Plant LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("Odyssey LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)
run_game(maps.get("Proxima Station LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
], realtime=True)"""