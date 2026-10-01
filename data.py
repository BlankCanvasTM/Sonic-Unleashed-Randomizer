from dataclasses import dataclass
from enum import Enum
import typing
from collections.abc import Sequence
from pathlib import Path


class Stage(Enum):
    DAY_TUT = 0
    NIGHT_TUT = 1  # unused
    DAY_MAIN = 2
    NIGHT_MAIN = 3
    DAY_SIDE = 4
    NIGHT_SIDE = 5
    DAY_BOSS = 6
    NIGHT_BOSS = 7
    DAY_DLC = 8
    NIGHT_DLC = 9
    DARK_GAIA_RUN = 10


class Shoe(Enum):
    NONE = 0
    STOMP = 1
    WALL = 2
    AIR = 3
    LIGHT = 4


MEDAL_COUNT = [0, 0, 15, 30, 45, 60, 80, 120]


class Level:
    def __init__(
        self,
        levels,
        name: str,
        type: Stage,
        level: int,
        parent: typing.Optional["Level"],
        file: str,
        recv_shoe: Shoe,
        req_shoe: Sequence[Shoe],
    ):
        self.name = name  # Human-Readable name
        self.type = type
        self.parent = (
            parent  # Which entrance do we need to complete to access this level
        )
        self.children = []
        if self.parent:
            self.parent.children.append(self)

        self.file = Path("+#Application") / f"SR_Enter{file}.seq.xml"
        self.required_medal = level  # Sun/Moon can be obtained via the expression "type & 1" (0 for sun/day, 1 for moon/night)
        self.recv_shoe = recv_shoe  # What shoe we get BEFORE entering the entrance
        self.req_shoe = req_shoe  # What shoes are required to beat the stage

        match type:
            case Stage.DAY_TUT:
                self.sun = 0
                self.moon = 0
            case Stage.NIGHT_TUT:
                self.sun = 0
                self.moon = 0
            case Stage.DAY_MAIN:
                self.sun = 3
                self.moon = 7
            case Stage.NIGHT_MAIN:
                self.sun = 10
                self.moon = 6
            case Stage.DAY_SIDE:
                self.sun = 1
                self.moon = 2
            case Stage.NIGHT_SIDE:
                self.sun = 4
                self.moon = 1
            case Stage.DAY_BOSS:
                self.sun = 2
                self.moon = 3
            case Stage.NIGHT_BOSS:
                self.sun = 3
                self.moon = 2
            case Stage.DAY_DLC:
                self.sun = 0
                self.moon = 0
            case Stage.NIGHT_DLC:
                self.sun = 0
                self.moon = 0
            case Stage.DARK_GAIA_RUN:
                self.sun = 0
                self.moon = 0

        levels.append(self)


class LevelState:
    def __init__(self):
        self.levels = []

        self.WID1 = WID1 = Level(
            self.levels,
            "Windmill Isle Day Act 1",
            Stage.DAY_TUT,
            0,
            None,
            "MykonosDayTutorial",
            Shoe.NONE,
            [],
        )
        self.WID2 = WID2 = Level(
            self.levels,
            "Windmill Isle Day Act 2",
            Stage.DAY_MAIN,
            0,
            WID1,
            "MykonosDayAction",
            Shoe.NONE,
            [],
        )
        self.WIN1 = WIN1 = Level(
            self.levels,
            "Windmill Isle Night Act 1",
            Stage.NIGHT_MAIN,
            0,
            WID2,
            "MykonosNightAction",
            Shoe.NONE,
            [],
        )
        self.SCN1 = SCN1 = Level(
            self.levels,
            "Savannah Citadel Night Act 1",
            Stage.NIGHT_MAIN,
            0,
            WIN1,
            "AfricaNightAction",
            Shoe.NONE,
            [],
        )
        self.SCD1 = SCD1 = Level(
            self.levels,
            "Savannah Citadel Day Act 1",
            Stage.DAY_MAIN,
            0,
            SCN1,
            "AfricaDayAction",
            Shoe.NONE,
            [],
        )
        self.BOSS_EGG_BEETLE = BOSS_EGG_BEETLE = Level(
            self.levels,
            "Egg Beetle",
            Stage.DAY_BOSS,
            0,
            SCD1,
            "AfricaDayBoss",
            Shoe.NONE,
            [],
        )
        self.RRN1 = RRN1 = Level(
            self.levels,
            "Rooftop Run Night Act 1",
            Stage.NIGHT_MAIN,
            15,
            BOSS_EGG_BEETLE,
            "EUNightAction",
            Shoe.NONE,
            [],
        )
        self.CED1 = CED1 = Level(
            self.levels,
            "Cool Edge Day Act 1",
            Stage.DAY_MAIN,
            15,
            RRN1,
            "SnowDayAction",
            Shoe.STOMP,
            [Shoe.STOMP],
        )
        self.DRN1 = DRN1 = Level(
            self.levels,
            "Dragon Road Night Act 1",
            Stage.NIGHT_MAIN,
            30,
            CED1,
            "ChinaNightAction",
            Shoe.NONE,
            [],
        )
        self.RRD1 = RRD1 = Level(
            self.levels,
            "Rooftop Run Day Act 1",
            Stage.DAY_MAIN,
            30,
            DRN1,
            "EUDayAction",
            Shoe.WALL,
            [Shoe.WALL],
        )
        self.BOSS_DARK_GAIA_PHEONIX = BOSS_DARK_GAIA_PHEONIX = Level(
            self.levels,
            "Dark Gaia Phoenix",
            Stage.NIGHT_BOSS,
            0,
            DRN1,
            "ChinaNightBoss",
            Shoe.NONE,
            [],
        )
        self.DRD1 = DRD1 = Level(
            self.levels,
            "Dragon Road Day Act 1",
            Stage.DAY_MAIN,
            45,
            RRD1,
            "ChinaDayAction",
            Shoe.AIR,
            [],
        )
        self.BOSS_EGG_DEVIL_RAY = BOSS_EGG_DEVIL_RAY = Level(
            self.levels,
            "Egg Devil Ray",
            Stage.DAY_BOSS,
            0,
            RRD1,
            "EUDayBoss",
            Shoe.NONE,
            [],
        )
        self.CEN1 = CEN1 = Level(
            self.levels,
            "Cool Edge Night Act 1",
            Stage.NIGHT_MAIN,
            45,
            BOSS_EGG_DEVIL_RAY,
            "SnowNightAction",
            Shoe.NONE,
            [],
        )
        self.BOSS_DARK_MORAY = BOSS_DARK_MORAY = Level(
            self.levels,
            "Dark Moray",
            Stage.NIGHT_BOSS,
            0,
            CEN1,
            "SnowNightBoss",
            Shoe.NONE,
            [],
        )
        self.ASD1 = ASD1 = Level(
            self.levels,
            "Arid Sands Day Act 1",
            Stage.DAY_MAIN,
            45,
            BOSS_DARK_MORAY,
            "PetraDayAction",
            Shoe.LIGHT,
            [Shoe.WALL],
        )
        self.SSD1 = SSD1 = Level(
            self.levels,
            "Skyscraper Scamper Day Act 1",
            Stage.DAY_MAIN,
            60,
            ASD1,
            "NYDayAction",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.SSN1 = SSN1 = Level(
            self.levels,
            "Skyscraper Scamper Night Act 1",
            Stage.NIGHT_MAIN,
            60,
            ASD1,
            "NYNightAction",
            Shoe.NONE,
            [],
        )
        self.JJN1 = JJN1 = Level(
            self.levels,
            "Jungle Joyride Night Act 1",
            Stage.NIGHT_MAIN,
            60,
            ASD1,
            "BeachNightAction",
            Shoe.NONE,
            [],
        )
        self.ASN1 = ASN1 = Level(
            self.levels,
            "Arid Sands Night Act 1",
            Stage.NIGHT_MAIN,
            80,
            ASD1,
            "PetraNightAction",
            Shoe.NONE,
            [],
        )
        self.BOSS_DARK_GUARDIAN = BOSS_DARK_GUARDIAN = Level(
            self.levels,
            "Dark Guardian",
            Stage.NIGHT_BOSS,
            0,
            ASN1,
            "PetraNightBoss",
            Shoe.NONE,
            [],
        )
        self.JJD1 = JJD1 = Level(
            self.levels,
            "Jungle Joyride Day Act 1",
            Stage.DAY_MAIN,
            120,
            ASD1,
            "BeachDayAction",
            Shoe.NONE,
            [Shoe.STOMP, Shoe.WALL],
        )
        self.BOSS_EGG_LANCER = BOSS_EGG_LANCER = Level(
            self.levels,
            "Egg Lancer",
            Stage.DAY_BOSS,
            0,
            JJD1,
            "BeachDayBoss",
            Shoe.NONE,
            [],
        )
        self.EGGMANLAND = EGGMANLAND = Level(
            self.levels,
            "Eggmanland",
            Stage.DAY_MAIN,
            0,
            JJD1,
            "EggManLandAction",
            Shoe.NONE,
            [Shoe.LIGHT, Shoe.STOMP, Shoe.WALL, Shoe.AIR],
        )
        self.BOSS_EGG_DRAGOON = BOSS_EGG_DRAGOON = Level(
            self.levels,
            "Egg Dragoon",
            Stage.NIGHT_BOSS,
            0,
            EGGMANLAND,
            "EggManLandBoss",
            Shoe.NONE,
            [],
        )

        self.WID3 = WID3 = Level(
            self.levels,
            "Windmill Isle Day Act 3",
            Stage.DAY_SIDE,
            30,
            WID2,
            "MykonosDayActionSub01",
            Shoe.NONE,
            [],
        )
        self.WID4 = WID4 = Level(
            self.levels,
            "Windmill Isle Day Act 4",
            Stage.DAY_DLC,
            0,
            WID2,
            "MykonosDayActionSub02",
            Shoe.NONE,
            [],
        )
        self.WIN2 = WIN2 = Level(
            self.levels,
            "Windmill Isle Night Act 2",
            Stage.NIGHT_SIDE,
            30,
            WIN1,
            "MykonosNightActionSub01",
            Shoe.NONE,
            [],
        )

        self.SCD2 = SCD2 = Level(
            self.levels,
            "Savannah Citadel Day Act 2",
            Stage.DAY_SIDE,
            30,
            SCD1,
            "AfricaDayActionSub01",
            Shoe.NONE,
            [],
        )
        self.SCD3 = SCD3 = Level(
            self.levels,
            "Savannah Citadel Day Act 3",
            Stage.DAY_SIDE,
            30,
            SCD1,
            "AfricaDayActionSub03",
            Shoe.NONE,
            [],
        )
        self.SCD4 = SCD4 = Level(
            self.levels,
            "Savannah Citadel Day Act 4",
            Stage.DAY_DLC,
            0,
            SCD1,
            "AfricaDayActionSub02",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.SCN2 = SCN2 = Level(
            self.levels,
            "Savannah Citadel Night Act 2",
            Stage.NIGHT_SIDE,
            30,
            SCN1,
            "AfricaNightActionSub01",
            Shoe.NONE,
            [],
        )
        self.SCN3 = SCN3 = Level(
            self.levels,
            "Savannah Citadel Night Act 3",
            Stage.NIGHT_DLC,
            0,
            SCN1,
            "AfricaNightActionSub02",
            Shoe.NONE,
            [],
        )
        self.SCN4 = SCN4 = Level(
            self.levels,
            "Savannah Citadel Night Act 4",
            Stage.NIGHT_DLC,
            0,
            SCN1,
            "AfricaNightActionSub03",
            Shoe.NONE,
            [],
        )

        self.RRD2 = RRD2 = Level(
            self.levels,
            "Rooftop Run Day Act 2",
            Stage.DAY_SIDE,
            45,
            RRD1,
            "EUDayActionSub01",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.RRD3 = RRD3 = Level(
            self.levels,
            "Rooftop Run Day Act 3",
            Stage.DAY_SIDE,
            45,
            RRD1,
            "EUDayActionSub02",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.RRD4 = RRD4 = Level(
            self.levels,
            "Rooftop Run Day Act 4",
            Stage.DAY_DLC,
            0,
            RRD1,
            "EUDayActionSub03",
            Shoe.NONE,
            [],
        )  # Doesnt Load correct stage similar to WI2-2
        self.RRD5 = RRD5 = Level(
            self.levels,
            "Rooftop Run Day Act 5",
            Stage.DAY_DLC,
            0,
            RRD1,
            "EUDayActionSub04",
            Shoe.NONE,
            [],
        )  # Doesn't load correct stage similar to WI2-2
        self.RRN2 = RRN2 = Level(
            self.levels,
            "Rooftop Run Night Act 2",
            Stage.NIGHT_DLC,
            0,
            RRN1,
            "EUNightActionSub01",
            Shoe.NONE,
            [],
        )

        self.CED2 = CED2 = Level(
            self.levels,
            "Cool Edge Day Act 2",
            Stage.DAY_SIDE,
            45,
            CED1,
            "SnowDayActionSub01",
            Shoe.NONE,
            [],
        )
        self.CED3 = CED3 = Level(
            self.levels,
            "Cool Edge Day Act 3",
            Stage.DAY_DLC,
            0,
            CED1,
            "SnowDayActionSub02",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.CED4 = CED4 = Level(
            self.levels,
            "Cool Edge Day Act 4",
            Stage.DAY_DLC,
            0,
            CED1,
            "SnowDayActionSub03",
            Shoe.NONE,
            [Shoe.STOMP, Shoe.AIR],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.CEN2 = CEN2 = Level(
            self.levels,
            "Cool Edge Night Act 2",
            Stage.NIGHT_DLC,
            0,
            CEN1,
            "SnowNightActionSub01",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.CEN3 = CEN3 = Level(
            self.levels,
            "Cool Edge Night Act 3",
            Stage.NIGHT_DLC,
            0,
            CEN1,
            "SnowNightActionSub02",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE

        self.DRD2 = DRD2 = Level(
            self.levels,
            "Dragon Road Day Act 2",
            Stage.DAY_SIDE,
            30,
            DRD1,
            "ChinaDayActionSub03",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.DRD3 = DRD3 = Level(
            self.levels,
            "Dragon Road Day Act 3",
            Stage.DAY_SIDE,
            60,
            DRD1,
            "ChinaDayActionSub04",
            Shoe.NONE,
            [],
        )
        self.DRD4 = DRD4 = Level(
            self.levels,
            "Dragon Road Day Act 4",
            Stage.DAY_DLC,
            0,
            DRD1,
            "ChinaDayActionSub01",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.DRD5 = DRD5 = Level(
            self.levels,
            "Dragon Road Day Act 5",
            Stage.DAY_DLC,
            0,
            DRD1,
            "ChinaDayActionSub02",
            Shoe.NONE,
            [],
        )
        self.DRN2 = DRN2 = Level(
            self.levels,
            "Dragon Road Night Act 2",
            Stage.NIGHT_SIDE,
            45,
            DRN1,
            "ChinaNightActionSub01",
            Shoe.NONE,
            [],
        )
        self.DRN3 = DRN3 = Level(
            self.levels,
            "Dragon Road Night Act 3",
            Stage.NIGHT_DLC,
            0,
            DRN1,
            "ChinaNightActionSub02",
            Shoe.NONE,
            [],
        )

        self.ASD2 = ASD2 = Level(
            self.levels,
            "Arid Sands Day Act 2",
            Stage.DAY_SIDE,
            45,
            ASD1,
            "PetraDayActionSub03",
            Shoe.NONE,
            [],
        )
        self.ASD3 = ASD3 = Level(
            self.levels,
            "Arid Sands Day Act 3",
            Stage.DAY_DLC,
            0,
            ASD1,
            "PetraDayActionSub01",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.ASN2 = ASN2 = Level(
            self.levels,
            "Arid Sands Night Act 2",
            Stage.NIGHT_DLC,
            0,
            ASN1,
            "PetraNightActionSub01",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.ASN3 = ASN3 = Level(
            self.levels,
            "Arid Sands Night Act 3",
            Stage.NIGHT_DLC,
            0,
            ASN1,
            "PetraNightActionSub02",
            Shoe.NONE,
            [],
        )

        self.SSD2 = SSD2 = Level(
            self.levels,
            "Skyscraper Scamper Day Act 2",
            Stage.DAY_SIDE,
            60,
            SSD1,
            "NYDayActionSub01",
            Shoe.NONE,
            [],
        )
        self.SSD3 = SSD3 = Level(
            self.levels,
            "Skyscraper Scamper Day Act 3",
            Stage.DAY_DLC,
            0,
            SSD1,
            "NYDayActionSub02",
            Shoe.NONE,
            [],
        )
        self.SSN2 = SSN2 = Level(
            self.levels,
            "Skyscraper Scamper Night Act 2",
            Stage.NIGHT_DLC,
            0,
            SSN1,
            "NYNightActionSub01",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE

        self.JJD2 = JJD2 = Level(
            self.levels,
            "Jungle Joyride Day Act 2",
            Stage.DAY_SIDE,
            60,
            JJD1,
            "BeachDayActionSub02",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.JJD3 = JJD3 = Level(
            self.levels,
            "Jungle Joyride Day Act 3",
            Stage.DAY_SIDE,
            45,
            JJD1,
            "BeachDayActionSub04",
            Shoe.NONE,
            [],
        )
        self.JJD4 = JJD4 = Level(
            self.levels,
            "Jungle Joyride Day Act 4",
            Stage.DAY_DLC,
            0,
            JJD1,
            "BeachDayActionSub01",
            Shoe.NONE,
            [],
        )
        self.JJD5 = JJD5 = Level(
            self.levels,
            "Jungle Joyride Day Act 5",
            Stage.DAY_DLC,
            0,
            JJD1,
            "BeachDayActionSub03",
            Shoe.NONE,
            [],
        )
        self.JJN2 = JJN2 = Level(
            self.levels,
            "Jungle Joyride Night Act 2",
            Stage.NIGHT_SIDE,
            60,
            JJN1,
            "BeachNightActionSub01",
            Shoe.NONE,
            [],
        )

        self.TD1 = TD1 = Level(
            self.levels,
            "Tornado Defense Act 1",
            Stage.DAY_MAIN,
            0,
            None,
            "ExAction1",
            Shoe.NONE,
            [],
        )
        self.TD2 = TD2 = Level(
            self.levels,
            "Tornado Defense Act 2",
            Stage.DAY_SIDE,
            0,
            None,
            "ExAction2",
            Shoe.NONE,
            [],
        )
        self.WID1_2 = WID1_2 = Level(
            self.levels,
            "Windmill Isle Day Act 1-2",
            Stage.DAY_DLC,
            0,
            WID2,
            "MykonosDayActionSub04",
            Shoe.NONE,
            [],
        )
        self.WID2_2 = WID2_2 = Level(
            self.levels,
            "Windmill Isle Day Act 2-2",
            Stage.DAY_DLC,
            0,
            WID2,
            "MykonosDayActionSub06",
            Shoe.NONE,
            [Shoe.WALL, Shoe.LIGHT],
        )  # CURRENTLY BROKEN LOADS STAGE BUT NOT ASSETS NEEDED FOR THE HARD MODE
        self.WIN1_2 = WIN1_2 = Level(
            self.levels,
            "Windmill Isle Night Act 1-2",
            Stage.NIGHT_DLC,
            0,
            WIN1,
            "MykonosNightActionSub03",
            Shoe.NONE,
            [],
        )
        self.WIN1_3 = WIN1_3 = Level(
            self.levels,
            "Windmill Isle Night Act 1-3",
            Stage.NIGHT_DLC,
            0,
            WIN1,
            "MykonosNightActionSub02",
            Shoe.NONE,
            [],
        )  # CURRENTLY BROKEN LOADS STAGE BUT NOT ASSETS NEEDED FOR THE BACKWARDS LEVEL
        self.SCD1_2 = SCD1_2 = Level(
            self.levels,
            "Savannah Citadel Day Act 1-2",
            Stage.DAY_DLC,
            0,
            SCD1,
            "AfricaDayActionSub05",
            Shoe.NONE,
            [],
        )
        self.SCD3_2 = SCD3_2 = Level(
            self.levels,
            "Savannah Citadel Day Act 3-2",
            Stage.DAY_DLC,
            0,
            SCD1,
            "AfricaDayActionSub06",
            Shoe.NONE,
            [],
        )
        self.RRD1_2 = RRD1_2 = Level(
            self.levels,
            "Rooftop Run Day Act 1-2",
            Stage.DAY_DLC,
            0,
            RRD1,
            "EUDayActionSub05",
            Shoe.NONE,
            [Shoe.WALL],
        )  # CURRENTLY BROKEN LOADS STAGE BUT NOT ASSETS NEEDED FOR THE HARD MODE
        self.RRD2_2 = RRD2_2 = Level(
            self.levels,
            "Rooftop Run Day Act 2-2",
            Stage.DAY_DLC,
            0,
            RRD1,
            "EUDayActionSub06",
            Shoe.NONE,
            [Shoe.WALL],
        )
        self.RRN1_2 = RRN1_2 = Level(
            self.levels,
            "Rooftop Run Night Act 1-2",
            Stage.NIGHT_DLC,
            0,
            RRN1,
            "EUNightActionSub02",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.CED1_2 = CED1_2 = Level(
            self.levels,
            "Cool Edge Day Act 1-2",
            Stage.DAY_DLC,
            0,
            CED1,
            "SnowDayActionSub04",
            Shoe.NONE,
            [Shoe.STOMP, Shoe.WALL],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.CED2_2 = CED2_2 = Level(
            self.levels,
            "Cool Edge Day Act 2-2",
            Stage.DAY_DLC,
            0,
            CED1,
            "SnowDayActionSub05",
            Shoe.NONE,
            [],
        )  # BROKEN ONLY LOADS ORIGINAL STAGE
        self.DRD1_2 = DRD1_2 = Level(
            self.levels,
            "Dragon Road Day Act 1-2",
            Stage.DAY_DLC,
            0,
            DRD1,
            "ChinaDayActionSub05",
            Shoe.NONE,
            [Shoe.LIGHT],
        )
        self.DRD2_2 = DRD2_2 = Level(
            self.levels,
            "Dragon Road Day Act 2-2",
            Stage.DAY_DLC,
            0,
            DRD1,
            "ChinaDayActionSub06",
            Shoe.NONE,
            [Shoe.WALL, Shoe.LIGHT],
        )
        self.DRN1_2 = DRN1_2 = Level(
            self.levels,
            "Dragon Road Night Act 1-2",
            Stage.NIGHT_DLC,
            0,
            DRN1,
            "ChinaNightActionSub03",
            Shoe.NONE,
            [],
        )
        self.ASD1_2 = ASD1_2 = Level(
            self.levels,
            "Arid Sands Day Act 1-2",
            Stage.DAY_DLC,
            0,
            ASD1,
            "PetraDayActionSub04",
            Shoe.NONE,
            [Shoe.WALL, Shoe.LIGHT],
        )
        self.SSD1_2 = SSD1_2 = Level(
            self.levels,
            "Skyscraper Scamper Day Act 1-2",
            Stage.DAY_DLC,
            0,
            SSD1,
            "NYDayActionSub03",
            Shoe.NONE,
            [Shoe.LIGHT],
        )
        self.JJD1_2 = JJD1_2 = Level(
            self.levels,
            "Jungle Joyride Day Act 1-2",
            Stage.DAY_DLC,
            0,
            JJD1,
            "BeachDayActionSub05",
            Shoe.NONE,
            [],
        )
        self.JJN1_2 = JJN1_2 = Level(
            self.levels,
            "Jungle Joyride Night Act 1-2",
            Stage.NIGHT_DLC,
            0,
            JJN1,
            "BeachNightActionSub03",
            Shoe.NONE,
            [],
        )

        self.SCD5 = SCD5 = Level(
            self.levels,
            "Savannah Citadel Day Act 5",
            Stage.DAY_DLC,
            0,
            SCD1,
            "AfricaDayActionSub04",
            Shoe.NONE,
            [],
        )
        self.SSN3 = SSN3 = Level(
            self.levels,
            "Skyscraper Scamper Night Act 3",
            Stage.NIGHT_DLC,
            0,
            SSN1,
            "NYNightActionSub01",
            Shoe.NONE,
            [],
        )  # BROKEN(?)
        self.JJN3 = JJN3 = Level(
            self.levels,
            "Jungle Joyride Night Act 3",
            Stage.NIGHT_DLC,
            0,
            JJN1,
            "BeachNightActionSub02",
            Shoe.NONE,
            [],
        )
        self.DARK_GAIA_RUN_1 = DARK_GAIA_RUN_1 = Level(
            self.levels,
            "Dark Gaia Run 1",
            Stage.DARK_GAIA_RUN,
            0,
            None,
            "DarkGaiaRun1",
            Shoe.NONE,
            [],
        )
        self.DARK_GAIA_RUN_2 = DARK_GAIA_RUN_2 = Level(
            self.levels,
            "Dark Gaia Run 2",
            Stage.DARK_GAIA_RUN,
            0,
            None,
            "DarkGaiaRun2",
            Shoe.NONE,
            [],
        )
        self.DARK_GAIA_RUN_3 = DARK_GAIA_RUN_3 = Level(
            self.levels,
            "Dark Gaia Run 3",
            Stage.DARK_GAIA_RUN,
            0,
            None,
            "DarkGaiaRun3",
            Shoe.NONE,
            [],
        )
