from random import Random
import unittest

from narfecritters.db.models import *
from narfecritters.game.world import Encounter, World


class TestWorld(unittest.TestCase):
    def test_attack(self):
        random = Random(x=12345)
        world = World(random=random)
        critter2 = world.encyclopedia.create(random, id=1, level=5)
        critter1 = world.encyclopedia.create(random, id=4, level=5)

        scratch = Move(id=1, name="scratch", power=35, type_id=1)
        self.assertEqual(4, world.attack(critter1, critter2, scratch).damage)
        ember = Move(id=2, name="ember", power=35, type_id=10)
        self.assertEqual(14, world.attack(critter1, critter2, ember).damage)

    def test_turn(self):
        random = Random(x=12345)
        world = World(random=random)
        critter1 = world.encyclopedia.create(random, id=4, level=5)
        critter2 = world.encyclopedia.create(random, id=1, level=5)
        world.player.add_critter(critter1)
        world.encounter = Encounter(critter2, active_critter_index=0)

        player_move = world.moves.find_by_id(critter1.moves[0].id)
        self.assertEqual(5, critter1.level)
        self.assertEqual(125, critter1.experience)
        world.turn_player(player_move.name, [])
        world.turn_enemy([])
        self.assertEqual(11, critter1.current_hp)
        self.assertEqual(16, critter2.current_hp)

        world.turn_player(player_move.name, [])
        world.turn_player(player_move.name, [])
        world.turn_player(player_move.name, [])
        world.turn_player(player_move.name, [])
        self.assertEqual(0, critter2.current_hp)
        self.assertEqual(190, critter1.experience)

    def test_save_load(self):
        npc = NPC(x=15, y=15)
        npc_slot = 5
        saves = Save.load()
        saves.players[npc_slot] = npc
        saves.save()
        saves = Save.load()
        new_npc = saves.players[npc_slot]
        self.assertEqual(npc.x, new_npc.x)
        self.assertEqual(npc.y, new_npc.y)
        self.assertEqual(npc, new_npc)
