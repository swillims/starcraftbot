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


class MarineReaperBotEasy(BotAI):


    async def on_step(self, iteration):
        """worker1 = self.units.worker().random"""

        await self.distribute_workers()
        await self.trainreaper()
        await self.trainmarine()
        await self.buildscv()
        await self.checksupply()
        await self.buildbarracks()
        await self.buildrefinery()
        await self.expand()
        await self.reaperscout()
        await self.flood()
        await self.reapernotdie()

    async def buildscv(self):
        for cc in self.structures(UnitTypeId.COMMANDCENTER).idle:
            if self.can_afford(UnitTypeId.SCV) and self.units(UnitTypeId.SCV).amount < (self.structures(UnitTypeId.COMMANDCENTER).amount * 14) +10:
                cc.train(UnitTypeId.SCV)

    async def checksupply(self):
        if self.supply_left < 2 + (self.supply_used/10) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            cc = self.structures(UnitTypeId.COMMANDCENTER).ready
            if cc.exists:
                if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                    if self.structures(UnitTypeId.SUPPLYDEPOT).amount > 0:
                        sd = self.structures(UnitTypeId.SUPPLYDEPOT)
                        await self.build(UnitTypeId.SUPPLYDEPOT, near=sd.first)
                    else:
                        if self.units(UnitTypeId.SCV).amount>0:
                            s = self.units(UnitTypeId.SCV).random
                            p = s.position.towards(self.start_location, 10)
                            await self.build(UnitTypeId.SUPPLYDEPOT, p)


    async def buildbarracks(self):
        if self.structures(UnitTypeId.BARRACKS).amount + 0 < 4 + self.structures(UnitTypeId.COMMANDCENTER).amount - 1:
            cc = self.structures(UnitTypeId.COMMANDCENTER).ready
            sd = self.structures(UnitTypeId.SUPPLYDEPOT)
            if cc.exists and sd.exists:
                if self.can_afford(UnitTypeId.BARRACKS):
                    await self.build(UnitTypeId.BARRACKS, near=sd.random)

    async def buildrefinery(self):
        if self.structures(UnitTypeId.BARRACKS).amount > 1 and self.structures(UnitTypeId.REFINERY).amount <= 1:
            for cc in self.structures(UnitTypeId.COMMANDCENTER).ready:
                v = self.vespene_geyser.closer_than(15.0, cc)
                for ve in v:
                    if self.can_afford(UnitTypeId.REFINERY):
                            if not self.structures(UnitTypeId.REFINERY).closer_than(1,ve).exists:
                                worker = self.select_build_worker(ve.position)
                                if worker is None:
                                    break
                                worker.build(UnitTypeId.REFINERY, ve)

    async def expand(self):
        if self.can_afford(UnitTypeId.COMMANDCENTER):
                if self.structures(UnitTypeId.COMMANDCENTER).amount < 3:
                    await self.expand_now()

    async def trainmarine(self):
        if True:
            for b in self.structures(UnitTypeId.BARRACKS).idle:
                if self.can_afford(UnitTypeId.MARINE):
                    b.train(UnitTypeId.MARINE)

    async def trainreaper(self):
        if True:
            for b in self.structures(UnitTypeId.BARRACKS).idle:
                if self.can_afford(UnitTypeId.REAPER):
                    b.train(UnitTypeId.REAPER)

    async def reaperscout(self):
        if True:
            for r in self.units(UnitTypeId.REAPER):
                if len(self.enemy_structures)==0:
                    if r.is_idle:
                        #el = self.enemy_start_locations[0]
                        el = self.mineral_field.random.position
                        r.attack(el)
                else:
                    if r.is_idle:
                        p = self.game_info.map_center.towards(self.enemy_structures.random.position, (self.supply_used)+4)
                        r.attack(p) 

    async def reapernotdie(self):
        if True:
            for r in self.units(UnitTypeId.REAPER):
                death = self.enemy_units.closer_than(3,  r)
                if death.exists:
                    p = r.position.towards(death[0].position,  -7)
                    r.move(p)
                else:
                    if r.health_percentage < 5/7:
                        p = self.game_info.map_center.towards(self.enemy_start_locations[0], (self.supply_used)-10)
                        r.move(p)

    async def flood(self):
        if True:
            if len(self.enemy_structures)>0:
               if self.units.idle.amount > 30:
                    for a in self.units(UnitTypeId.MARINE):
                        a.attack(self.enemy_structures[0].position)
            else:
                if self.units.idle.amount > 80:
                    for a in self.units:
                        a.attack(self.mineral_field.random.position)


"""TEST SCRIPT BELOW"""
"""
run_game(maps.get("Abyssal Reef LE"), [
    Bot(Race.Terran, MarineReaperBotEasy()),
    Computer(Race.Random, Difficulty.Easy)
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