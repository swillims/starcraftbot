import sc2
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer, Human
from sc2.constants import *
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
        for cc in self.units(COMMANDCENTER) | self.units(ORBITALCOMMAND):
            enemyclose = self.known_enemy_units.closer_than(12, cc.position)
            if enemyclose.amount > 2:
                p = enemyclose.random.position
                for scv in self.units.not_structure.closer_than(30, cc.position):
                    await self.do(scv.attack(p))
                    """it's also non scv units"""
                for lazy in self.units.not_structure.idle.closer_than(50, cc.position):
                    await self.do(lazy.attack(p))
                for r in self.units(REAPER) | self.units(HELLION):
                    await self.do(r.attack(p))
                for b in self.units(BARRACKS):
                    await self.do(b(RALLY_BUILDING, p))
                print("defend")

    async def reaperscout(self):
        for r in self.units(REAPER).idle:
            if len(self.known_enemy_structures) == 0:
                m = self.state.mineral_field.closer_than((self.supply_used*2)+20, self.start_location).random.position
                await self.do(r.attack(m))
                print("SCOUT")
            else:
                if self.units(REAPER).amount > 5:
                    if self.units(REAPER).closer_than(6, r).amount < 5:
                        p = self.units(REAPER).random.position
                        await self.do(r.attack(p))
                        print("GROUP")
                        for r1 in self.units(REAPER).closer_than(10, r):
                            await self.do(r1.attack(self.known_enemy_structures.random.position))
                            print("KILL")
                else:
                    m = self.state.mineral_field.closer_than((self.supply_used) + 10, self.start_location).random.position
                    await self.do(r.attack(m))
                    print("SCOUT")

    async def reapernotdie(self):
        for r in self.units(REAPER):
            death = self.known_enemy_units.closer_than(4.5, r).not_structure.not_flying
            if death.exists:
                p = r.position.towards(death.random.position, -7)
                if await self.can_cast(r,KD8CHARGE_KD8CHARGE,death.random.position):
                    await self.do(r(KD8CHARGE_KD8CHARGE, death.random.position))
                    print("GRENDADE")
                await self.do(r.move(p))
                print("MOVE BACK")
            elif r.health_percentage < 5/7:
                death2 = self.known_enemy_units.closer_than(8, r)
                if death2.exists:
                    p = r.position.towards(death2.random.position, -12)
                    await self.do(r.move(p))
                    print("RETREAT!!!")

    async def hellionproximity(self):
        if self.units(ARMORY).ready.exists:
            for h in self.units(HELLION):
                if self.known_enemy_units.closer_than(10, h.position).not_structure.not_flying.exists:
                    await self.do(h(MORPH_HELLBAT))
                    print("MORPH HELLBAT")

    async def hellbatproximity(self):
        if self.units(ARMORY).ready.exists:
            for h in self.units(HELLIONTANK):
                death = self.known_enemy_units.closer_than(20, h.position).not_structure.not_flying
                if death.exists:
                    await self.do(h.attack(death.random.position))
                    print("BURN")
                else:
                    await self.do(h(MORPH_HELLION))
                    print("MORPH HELLBAT")

    async def siegetankproximity(self):
        threat = self.known_enemy_units
        if threat.exists:
            for s in self.units(SIEGETANK):
                death = threat.closer_than(12, s)
                if death.exists:
                    await self.do(s(SIEGEMODE_SIEGEMODE))
                    print("SIEGE")

    async def siegedtankproximity(self):
        threat = self.known_enemy_units
        if threat.exists:
            for s in self.units(SIEGETANKSIEGED):
                death = threat.closer_than(15, s)
                if not death.exists:
                    await self.do(s(UNSIEGE_UNSIEGE))
                    print("UNSIEGE")


    async def militarygroup(self):
        mr = self.units(MARAUDER)
        for m in self.units(MARINE).idle | self.units(MARAUDER).idle:
            if self.units(SUPPLYDEPOTLOWERED).amount > 0:
                await self.do(m.attack(self.units.structure.random.position))
        hel = self.units(HELLION)
        if hel.amount < 8:
            for h in hel.idle:
                await self.do(h.attack(self.units.not_structure.random.position))
        else:
            m = self.state.mineral_field.closer_than(self.supply_used + 30, self.start_location)
            if m.exists:
                for h in hel.idle:
                    await self.do(h.attack(m.random.position))
        for s in self.units(SIEGETANK).idle:
            await self.do(s.attack(self.units.random.position))

    async def armyattack(self):
        y = self.units(MARINE)
        x = self.units(MARAUDER)
        r = self.units(REAPER)
        h = self.units(HELLION)
        s = self.units(SIEGETANK) | self.units(HELLIONTANK)
        if self.known_enemy_units.amount > 0 and self.known_enemy_units.closer_than(50, self.start_location).amount > 5:
            p = self.known_enemy_units.random.position
            for a in x | y | h | r | s:
                await self.do(a.attack(p))
        elif self.known_enemy_structures.amount > 0 and x.amount + (y.amount*1.5) + (s.amount*2) > 35 and self.units(ORBITALCOMMAND).amount < 2:
            p = self.known_enemy_structures.random.position
            for a in x | y | h | r | s:
                await self.do(a.attack(p))
        elif self.known_enemy_structures.amount > 0 and x.idle.amount + (y.idle.amount*1.25) + (s.idle.amount*2) > 50:
            p = self.known_enemy_structures.random.position
            for a in x | y | h | r | s:
                await self.do(a.attack(p))

    """building methods"""

    async def commandcenter(self):
        for cc in self.units(COMMANDCENTER).ready.noqueue:
            if self.units(BARRACKS).amount >= 2 and self.units(COMMANDCENTER).not_ready.amount > 0:
                    if self.can_afford(ORBITALCOMMAND):
                        await self.do(cc(UPGRADETOORBITAL_ORBITALCOMMAND))
            elif self.units(SCV).amount < (self.units(COMMANDCENTER).amount * 14) + (self.units(ORBITALCOMMAND).amount * 12 ) + 8:
                if self.can_afford(SCV) and self.units(SCV).amount < 40 and self.supply_used < 200:
                    await self.do(cc.train(SCV))
                elif self.units(BARRACKS).amount >= 2 and self.units(COMMANDCENTER).noqueue.amount >= 2 and not self.already_pending(ORBITALCOMMAND):
                    if self.can_afford(ORBITALCOMMAND) and self.units(ORBITALCOMMAND).amount < 3:
                        await self.do(cc(UPGRADETOORBITAL_ORBITALCOMMAND))
                    elif self.can_afford(PLANETARYFORTRESS) and self.units(ENGINEERINGBAY).ready.exists:
                        await self.do(cc(UPGRADETOPLANETARYFORTRESS_PLANETARYFORTRESS))

    async def orbitalcommand(self):
        for cc in self.units(ORBITALCOMMAND).ready:
            if cc.energy > 100 and not self.known_enemy_structures.amount > 0:
                    await self.do(cc(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))
                    await self.do(cc(SCANNERSWEEP_SCAN, self.state.mineral_field.random.position))
                    print("scan")

            elif cc.energy > 50 and self.supply_left <= 0 and self.supply_used != 200:
                if self.units(SUPPLYDEPOT).amount > 0:
                    await self.do(cc(SUPPLYDROP_SUPPLYDROP, self.units(SUPPLYDEPOT).random))
                    print("supplies")
                elif self.units(SUPPLYDEPOTLOWERED).amount>0:
                    await self.do(cc(SUPPLYDROP_SUPPLYDROP, self.units(SUPPLYDEPOTLOWERED).random))

            elif cc.energy > 75 and self.known_enemy_structures.amount > 0:
                m = self.state.mineral_field.closer_than(8, cc.position)
                if m.amount > 5:
                    await self.do(cc(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")

            elif cc.energy == 200:
                await self.do(cc(SCANNERSWEEP_SCAN, self.units.random.position))
                await self.do(cc(SCANNERSWEEP_SCAN, self.enemy_start_locations[0]))
                print("scan")
                m = self.state.mineral_field.closer_than(8, cc.position)
                if m.amount > 5:
                    await self.do(cc(CALLDOWNMULE_CALLDOWNMULE, m.random))
                    print("mule")

            if self.units(SCV).amount < (self.units(COMMANDCENTER).amount * 10) + self.units(ORBITALCOMMAND).amount * 6:
                """significantly below other methods for scv production on purpose"""
                if self.can_afford(SCV) and self.units(SCV).amount < 40 and self.supply_used < 200:
                    await self.do(cc.train(SCV))

                    """
            if cc.energy == 200 and self.known_enemy_structures.amount > 0:
                p = self.known_enemy_structures.random.position
                await self.do(cc(SCANNERSWEEP_SCAN, p))
                await self.do(cc(CALLDOWNMULE_CALLDOWNMULE, p.towards(self.game_info.map_center, -3)))
                print("Manner Muling")
                
                code removed for being pointless but it is funny
                """

    async def barracks(self):
        oc = self.units(ORBITALCOMMAND).ready
        for b in self.units(BARRACKS).ready.noqueue:
            if b.add_on_tag == 0 and self.supply_used < 200:
                if self.can_afford(REAPER):
                    if self.units(REAPER).amount > 0:
                        if self.units(BARRACKSTECHLAB).amount < 2:
                            await self.do(b.build(BARRACKSTECHLAB))
                            if oc.amount > 0:
                                occ = oc.random
                                scv = self.units(SCV).closer_than(6, occ)
                                if scv.amount>0:
                                    scv = scv.random
                                    p = occ.position.towards(scv.position, -8)
                                    await self.do(b.build((BARRACKSTECHLAB),p))
                            else:
                                await self.do(b.train(MARINE))
                        else:
                            await self.do(b.train(MARINE))
                    elif self.units(REAPER).amount <= self.units(MARINE).amount / 5:
                        await self.do(b.train(REAPER))
                    else:
                        await self.do(b.train(MARINE))
                elif self.can_afford(MARINE):
                    await self.do(b.train(MARINE))
            elif self.supply_used < 200:
                if self.can_afford(MARAUDER):
                    await self.do(b.train(MARAUDER))
                elif self.can_afford(MARINE):
                    await self.do(b.train(MARINE))

    async def factory(self):
        if self.supply_used < 200:
            for f in self.units(FACTORY).ready.idle:
                ftl = self.units(FACTORYTECHLAB)
                if ftl.exists:
                    id = self.units(FACTORYTECHLAB).random.tag
                    if f.add_on_tag == 0:
                        if self.can_afford(SIEGETANK):
                            await self.do(f.build(FACTORYREACTOR))
                            scv = self.units(SCV).random
                            p = scv.position.towards(self.game_info.map_center, random.randint(4, 8))
                            await self.do(f.build(FACTORYREACTOR, p))
                        elif self.can_afford(HELLION):
                            await self.do(f.train(HELLION))
                    elif f.add_on_tag == id:
                        if self.can_afford(SIEGETANK):
                            await self.do(f.train(SIEGETANK))
                        elif self.can_afford(HELLION):
                            await self.do(f.train(HELLION))
                    elif self.can_afford(HELLION):
                        await self.do(f.train(HELLION))
                        if self.can_afford(HELLION):
                            await self.do(f.train(HELLION))
                elif self.can_afford(HELLION):
                    if self.can_afford(SIEGETANK):
                        await self.do(f.build(FACTORYTECHLAB))
                        scv = self.units(SCV)
                        if scv.amount >= 20:
                            s1 = scv.random
                            s2 = scv.random
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            await self.do(f.build(FACTORYTECHLAB, p))
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            await self.do(f.build(FACTORYTECHLAB, p))
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            await self.do(f.build(FACTORYTECHLAB, p))
                            p = s1.position.towards(s2.position, random.randint(4, 8))
                            await self.do(f.build(FACTORYTECHLAB, p))
                            """random places until it works*"""
                    else:
                        await self.do(f.train(HELLION))


    async def supplydepotdown(self):
        for sd in self.units(SUPPLYDEPOT).ready:
            e = self.known_enemy_units.closer_than(6, sd.position)
            """numbers don't match on purpose as a taunt"""
            if not e.exists:
                await self.do(sd(MORPH_SUPPLYDEPOT_LOWER))

    async def supplydepotup(self):
        for sd in self.units(SUPPLYDEPOTLOWERED).ready:
            e = self.known_enemy_units.closer_than(8, sd.position)
            """numbers don't match on purpose as a taunt"""
            if e.exists:
                await self.do(sd(MORPH_SUPPLYDEPOT_RAISE))

    async def landstuff(self):
        for b in self.units(BARRACKSFLYING).idle:
            """This code is a back up code to patch a problem. It is buggy and should not be relied on"""
            print("fly b")
            p = self.start_location
            cc = self.units(COMMANDCENTER) or self.units(ORBITALCOMMAND) or self.units(SUPPLYDEPOTLOWERED) or self.units(BARRACKS) or self.units(SUPPLYDEPOT)
            if cc.amount > 0:
                c = cc.random
                p = c.position.towards(self.enemy_start_locations[0], random.randint(1, 11))
            await self.do(b(LAND_BARRACKS, p))
        for f in self.units(FACTORYFLYING).idle:
            print("fly f")
            p = self.start_location
            cc = self.units(COMMANDCENTER) or self.units(ORBITALCOMMAND) or self.units(SUPPLYDEPOTLOWERED) or self.units(BARRACKS) or self.units(SUPPLYDEPOT)
            if cc.amount > 0:
                c = cc.random
                p = c.position.towards(self.enemy_start_locations[0], random.randint(1, 11))
            await self.do(f(LAND_FACTORY, p))

    async def rallyset(self, ):
        p = self.start_location.towards(self.game_info.map_center, 8)
        s = self.units(SUPPLYDEPOT).ready
        if s.exists:
            p = s.random.position.towards(self.game_info.map_center, 1.5)
        for b in self.units(BARRACKS) | self.units(FACTORY):
            await self.do(b(RALLY_BUILDING, p))
        self.rallypos = p

    "build methods"
    async def buildstuff(self):
        cc = self.units(COMMANDCENTER).ready
        oc = self.units(ORBITALCOMMAND).ready
        sd = (self.units(SUPPLYDEPOT).ready | self.units(SUPPLYDEPOTLOWERED).ready)
        if self.can_afford(COMMANDCENTER):
            if self.minerals > 300 + self.supply_used*3:
                await self.expand_now()
        if self.can_afford(BARRACKS):
            if (cc.exists or oc.exists) and sd.exists:
                if self.units(BARRACKS).amount < 1 + cc.amount + (oc.amount*1):
                    if self.units(BARRACKSFLYING).amount == 0:
                        if self.units(BARRACKS).amount == 0:
                            p = self.start_location.towards(self.game_info.map_center, 5)
                            await self.build(BARRACKS, p)
                        else:
                            if cc.exists:
                                a = cc.random
                                re = self.units(REFINERY).closer_than(10, a.position)
                                if re.amount > 0:
                                    r = re.random
                                    p = a.position.towards(r.position, -8)
                                    await self.build(BARRACKS, p)
                                else:
                                    await self.build(BARRACKS, near=sd.first)
                            elif oc.exists:
                                a = oc.random
                                re = self.units(REFINERY).closer_than(10, a.position)
                                if re.amount > 0:
                                    r = re.random
                                    p = a.position.towards(r.position, -8)
                                    await self.build(BARRACKS, near=p)
                else:
                    if self.can_afford(FACTORY) and oc.exists:
                        if self.units(ENGINEERINGBAY).amount == 0 and self.units(FACTORY).amount > 0:
                            if oc.exists and not self.already_pending(ENGINEERINGBAY):
                                await self.build(ENGINEERINGBAY, near=sd.first)
                        else:
                            if self.units(FACTORY).amount + self.units(FACTORYFLYING).amount < 2 and not self.already_pending(FACTORY):
                                await self.build(FACTORY, near=sd.first)
                            elif oc.exists:
                                if self.units(ARMORY).amount < 1 and oc.amount > 0 and not self.already_pending(ARMORY):
                                    await self.build(ARMORY, near=sd.first)

    async def managesupply(self):
        if self.supply_left < 2 + (self.supply_used/10) and not self.already_pending(SUPPLYDEPOT):
            cc = self.units(COMMANDCENTER).ready | self.units(ORBITALCOMMAND).ready
            if cc.exists:
                if self.can_afford(SUPPLYDEPOT) and self.units(SUPPLYDEPOTLOWERED).amount < 14:
                    if self.units(SUPPLYDEPOT).amount > 0:
                        await self.build(SUPPLYDEPOT, near=cc.random)
                        """this has been changed because of lowering"""
                    else:
                        if self.units(SCV).amount>0:
                            p = self.start_location.towards(self.game_info.map_center, 11)
                            await self.build(SUPPLYDEPOT, p)
        elif self.supply_left < 0 and self.can_afford(SUPPLYDEPOT):
            await self.build(SUPPLYDEPOT, near=cc.random)

    async def getgas(self):
        if self.units(BARRACKS).amount > 0 and self.units(REFINERY).amount < self.units(COMMANDCENTER).amount + (self.units(ORBITALCOMMAND).amount):
            for cc in self.units(COMMANDCENTER).ready:
                v = self.state.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(REFINERY) and not self.already_pending(REFINERY):
                            if not self.units(REFINERY).closer_than(1, ve).exists:
                                worker = self.select_build_worker(ve.position)
                                if worker is None:
                                    break
                                await self.do(worker.build(REFINERY, ve))

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