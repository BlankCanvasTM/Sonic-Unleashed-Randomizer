from __future__ import annotations


class Enemy:
	def __init__(
		self,
		enemies,
		name: str,
		class_name: str,
		parameters: dict[str, object],
		extra_archives: list[str] | None = None,
		randomisable_source: bool = True,
		randomisable_target: bool = True,
	):
		self.name = name
		self.class_name = class_name
		self.parameters = parameters
		self.extra_archives = extra_archives or []
		self.randomisable_source = randomisable_source
		self.randomisable_target = randomisable_target

		enemies.append(self)


# ---------------------------------------------------------------------------
# Default parameter templates
#
# Position, Rotation and SetObjectID are intentionally NOT stored here.
# Those belong to the original spawn slot and must be preserved.
#
# StartWayPointID is always forced to 0 when the replacement class needs it.
# TargetList is always emitted empty.
# ---------------------------------------------------------------------------

EGG_FIGHTER_PARAMETERS = {
	"FirstState": "0",
	"GroundOffset": "0",
	"PatrolType": "0",
	"Personality": "1",
	"StartWayPointID": "0",
}

KILLER_BEE_PARAMETERS = {
	"FirstState": "0",
	"GroundOffset": "0",
	"PatrolType": "1",
	"Personality": "0",
	"StartWayPointID": "0",
}

MASTER_PARAMETERS = {
	"FirstState": "0",
	"GroundOffset": "0",
	"PatrolType": "0",
	"Personality": "3",
	"StartWayPointID": "0",
	"TargetList": {},
}

NIGHTMARE_R_PARAMETERS = {
	"FirstState": "0",
	"GroundOffset": "0",
	"PatrolType": "0",
	"Personality": "0",
	"StartWayPointID": "0",
}

NIGHTMARE_D_PARAMETERS = {
	"FirstState": "0",
	"GroundOffset": "0",
	"PatrolType": "0",
	"Personality": "2",
	"StartWayPointID": "0",
}

RECKLESS_PARAMETERS = {
	"FirstState": "0",
	"GroundOffset": "0",
	"Personality": "0",
}

SPOOKY_PARAMETERS = {
	"Aggression": "0",
	"FirstState": "0",
	"GroundOffset": "0",
}

BIG_MOTHER_PARAMETERS = {
	"GroundOffset": "0",
	"Personality": "0",
}

TITAN_PARAMETERS = {
	"GroundOffset": "0",
	"Personality": "0",
}

FLOWER_PARAMETERS = {
	"GroundOffset": "0",
}

FLOAT_NORMAL_PARAMETERS = {
	"AlivePoint": {
		"w": "0",
		"x": "0",
		"y": "0",
		"z": "0",
	},
	"GroundOffset": "0",
	"IsRevival": "false",
}

FLOAT_THUNDER_PARAMETERS = {
	"AttackInterval": "5",
	"AttackTime": "1",
	"GroundOffset": "0",
	"StartTime": "2",
}

ELEMENT_PARAMETERS = {
	"AttackInterval": "5",
	"AttackTime": "1",
	"GroundOffset": "0",
	"MoveType": "0",
	"StartTime": "2",
}

THUNDER_BALL_PARAMETERS = {
	"AttackInterval": "5",
	"AttackTime": "5",
	"GroundOffset": "0",
	"MoveType": "0",
	"StartTime": "10",
}


class EnemyState:
	def __init__(self):
		self.enemies = []

		# -------------------------------------------------------------------
		# Direct enemies
		# -------------------------------------------------------------------

		self.BIG_MOTHER = Enemy(
			self.enemies,
			"Big Mother",
			"EvilEnemyBigMother",
			BIG_MOTHER_PARAMETERS.copy(),
		)

		# Egg Fighters all use the EvilEnemyEggFighterR parameter layout.
		self.EGG_FIGHTER_R = Enemy(
			self.enemies,
			"Egg Fighter",
			"EvilEnemyEggFighterR",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.EGG_SHOOTER = Enemy(
			self.enemies,
			"Egg Shooter",
			"EvilEnemyEggFighterG",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.EGG_FIGHTER_SWORD = Enemy(
			self.enemies,
			"Egg Fighter Sword",
			"EvilEnemyEggFighterW",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.EGG_FIGHTER_SHIELD = Enemy(
			self.enemies,
			"Egg Fighter Shield",
			"EvilEnemyEggFighterS",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.EGG_FIGHTER_KNIGHT = Enemy(
			self.enemies,
			"Egg Fighter Knight",
			"EvilEnemyEggFighterK",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.EGG_FIGHTER_SHIELD_LIGHTNING = Enemy(
			self.enemies,
			"Egg Fighter Shield Lightning",
			"EvilEnemyEggFighterST",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.EGG_SHOOTER_CHIBI = Enemy(
			self.enemies,
			"Egg Shooter Chibi",
			"EvilEnemyEggFighterC",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)
		self.CHIBI_FIGHTER = Enemy(
			self.enemies,
			"Little Fighter",
			"EvilEnemyChibiFighter",
			EGG_FIGHTER_PARAMETERS.copy(),
			["EvilEnemyEggFighter", "EggFighterEquipments"],
		)

		# Floats remain valid replacement targets, but their original direct
		# placements are protected in Version 1.
		self.FLOAT_NORMAL = Enemy(
			self.enemies,
			"Dark Bat",
			"EvilEnemyFloatNormal",
			FLOAT_NORMAL_PARAMETERS.copy(),
			randomisable_source=False,
		)
		self.FLOAT_THUNDER = Enemy(
			self.enemies,
			"Thunder Bat",
			"EvilEnemyFloatThunder",
			FLOAT_THUNDER_PARAMETERS.copy(),
			randomisable_source=False,
		)

		self.FLOWER = Enemy(
			self.enemies,
			"Evil Flower",
			"EvilEnemyFlower",
			FLOWER_PARAMETERS.copy(),
		)

		self.KILLER_BEE = Enemy(
			self.enemies,
			"Killer Bee",
			"EvilEnemyKillerBee",
			KILLER_BEE_PARAMETERS.copy(),
		)
		self.KILLER_BEE_RED = Enemy(
			self.enemies,
			"Red Killer Bee",
			"EvilEnemyKillerBeeRed",
			KILLER_BEE_PARAMETERS.copy(),
		)

		# Master variants all use the EvilEnemyMasterSpooky parameter layout.
		self.MASTER_CURE = Enemy(
			self.enemies,
			"Cure Master",
			"EvilEnemyMasterCure",
			MASTER_PARAMETERS.copy(),
		)
		self.MASTER_POWER = Enemy(
			self.enemies,
			"Power Master",
			"EvilEnemyMasterPower",
			MASTER_PARAMETERS.copy(),
		)
		self.MASTER_SPOOKY = Enemy(
			self.enemies,
			"Fright Master",
			"EvilEnemyMasterSpooky",
			MASTER_PARAMETERS.copy(),
		)
		self.MASTER_FIRE = Enemy(
			self.enemies,
			"Fire Master",
			"EvilEnemyMasterFire",
			MASTER_PARAMETERS.copy(),
		)

		self.MASTER_LIGHTNING = Enemy(
					self.enemies,
					"Lightning Master",
					"EvilEnemyMasterLightning",
					MASTER_PARAMETERS.copy(),
				)

		self.NIGHTMARE_R = Enemy(
			self.enemies,
			"Nightmare",
			"EvilEnemyNightmareR",
			NIGHTMARE_R_PARAMETERS.copy(),
		)
		self.NIGHTMARE_D = Enemy(
			self.enemies,
			"Deep Nightmare",
			"EvilEnemyNightmareD",
			NIGHTMARE_D_PARAMETERS.copy(),
		)

		self.RECKLESS_L = Enemy(
			self.enemies,
			"Little Rex",
			"EvilEnemyRecklessL",
			RECKLESS_PARAMETERS.copy(),
		)
		self.RECKLESS_R = Enemy(
			self.enemies,
			"Red Rex",
			"EvilEnemyRecklessR",
			RECKLESS_PARAMETERS.copy(),
		)

		self.SPOOKY = Enemy(
			self.enemies,
			"Dark Fright",
			"EvilEnemySpooky",
			SPOOKY_PARAMETERS.copy(),
		)

		self.SPOOKY_R = Enemy(
					self.enemies,
					"Red Fright",
					"EvilEnemySpookyR",
					SPOOKY_PARAMETERS.copy(),
				)

		self.TITAN = Enemy(
			self.enemies,
			"Titan",
			"EvilEnemyTitan",
			TITAN_PARAMETERS.copy(),
		)

		# Existing eFlame/eBlizzard direct slots are protected because they can
		# be progression-related, but both remain valid replacement targets.
		self.EGG_FLAME = Enemy(
			self.enemies,
			"Egg Flame",
			"eFlame",
			ELEMENT_PARAMETERS.copy(),
			["EvilEnemyEggElement", "SonicEnemyEElement"],
			randomisable_source=False,
		)
		self.EGG_BLIZZARD = Enemy(
			self.enemies,
			"Egg Blizzard",
			"eBlizzard",
			ELEMENT_PARAMETERS.copy(),
			["EvilEnemyEggElement", "SonicEnemyEElement"],
			randomisable_source=False,
			randomisable_target = False,
		)
		self.EGG_TYPHOON = Enemy(
			self.enemies,
			"Egg Typhoon",
			"eTyphoon",
			ELEMENT_PARAMETERS.copy(),
			["EvilEnemyEggElement", "SonicEnemyEElement"],
		)

		self.THUNDER_BALL = Enemy(
			self.enemies,
			"Thunder Ball",
			"eThunderBall",
			THUNDER_BALL_PARAMETERS.copy(),
			["EvilEnemyEThunderBall", "SonicEnemyEThunderBall"],
		)

		# Lookups used while parsing direct enemy objects.
		self.by_class = {
			enemy.class_name: enemy
			for enemy in self.enemies
		}

	@property
	def direct_sources(self):
		return [
			enemy
			for enemy in self.enemies
			if enemy.randomisable_source
		]

	@property
	def direct_targets(self):
		return [
			enemy
			for enemy in self.enemies
			if enemy.randomisable_target
		]


# ---------------------------------------------------------------------------
# EnemyObjEnemyHole metadata
#
# Hole objects are never converted into direct enemies. Version 1 only
# changes EnemyType while preserving the rest of the EnemyObjEnemyHole.
# ---------------------------------------------------------------------------

HOLE_ENEMY_TYPES = {
	0:  ("Nightmare", "EvilEnemyNightmareR"),
	1:  ("Deep Nightmare", "EvilEnemyNightmareD"),
	2:  ("Little Rex", "EvilEnemyRecklessL"),
	3:  ("Dark Fright", "EvilEnemySpooky"),
	4:  ("Red Fright", "EvilEnemySpookyR"),
	5:  ("Killer Bee", "EvilEnemyKillerBee"),
	6:  ("Red Killer Bee", "EvilEnemyKillerBeeRed"),
	7:  ("Egg Shooter", "EvilEnemyEggFighterG"),
	8:  ("Egg Fighter Sword", "EvilEnemyEggFighterW"),
	9:  ("Egg Fighter Shield", "EvilEnemyEggFighterS"),
	10: ("Egg Fighter Knight", "EvilEnemyEggFighterK"),
	11: ("Egg Fighter Knight Lightning", "EvilEnemyEggFighterK"),
	12: ("Egg Fighter Shield Lightning", "EvilEnemyEggFighterST"),
	13: ("Egg Fighter Shield Lightning (Type 13)", "EvilEnemyEggFighterST"),
	14: ("Little Fighter", "EvilEnemyChibiFighter"),
	15: ("Cure Master", "EvilEnemyMasterCure"),
	16: ("Power Master", "EvilEnemyMasterPower"),
	17: ("Fright Master", "EvilEnemyMasterSpooky"),
	18: ("Fire Master", "EvilEnemyMasterFire"),
	19: ("Lightning Master", "EvilEnemyMasterLightning"),
	20: ("Evil Flower", "EvilEnemyFlower"),
	21: ("Dark Bat", "EvilEnemyFloatNormal"),
	22: ("Dark Sniper Bat", "EvilEnemyFloatCannon"),
	23: ("Thunder Bat", "EvilEnemyFloatThunder"),
	24: ("Egg Flame", "eFlame"),
	25: ("Egg Blizzard", "eBlizzard"),
	26: ("Egg Typhoon", "eTyphoon"),
	27: ("Thunder Ball", "eThunderBall"),
	28: ("Red Rex", "EvilEnemyRecklessR"),
	29: ("Egg Fighter R/L Preset", None),
	30: ("Egg Shooter Chibi", "EvilEnemyEggFighterC"),
}

HOLE_FIRST_STATE_OVERRIDES = {
    0: 0,  # Nightmare
	1: 0,  # Deep Nightmare
}

PROTECTED_HOLE_SOURCE_TYPES = {
	21,  # Dark Bat / EvilEnemyFloatNormal
	22,  # Dark Sniper Bat / EvilEnemyFloatCannon
	23,  # Thunder Bat / EvilEnemyFloatThunder
	24,  # Egg Flame
	25,  # Egg Blizzard
}

EXCLUDED_HOLE_TARGET_TYPES = {
    25,  # Egg Blizzard
}

HOLE_RANDOM_TARGETS = [
	enemy_type
	for enemy_type in HOLE_ENEMY_TYPES
	if enemy_type not in EXCLUDED_HOLE_TARGET_TYPES
]


def get_hole_enemy_name(enemy_type: int) -> str:
	return HOLE_ENEMY_TYPES[enemy_type][0]
