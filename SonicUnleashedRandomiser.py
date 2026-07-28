import random
import re
import base64
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

SEED_CODE = None


STAGE_ENTRIES = [
    {
        "name": "Apotos D Act 1",
        "file": Path("#Application/SR_EnterMykonosDayTutorial.seq.xml"),
        "default_archive": "ActD_MykonosAct1",
        "default_is_evil": "false"
    },
    {
        "name": "Apotos D Act 2",
        "file": Path("#Application/SR_EnterMykonosDayAction.seq.xml"),
        "default_archive": "ActD_MykonosAct2",
        "default_is_evil": "false"
    },
    {
        "name": "Apotos D Act 3",
        "file": Path("#Application/SR_EnterMykonosDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubMykonos_01",
        "default_is_evil": "false"
    },
    {
        "name": "Apotos D Act 4",
        "file": Path("#Application/SR_EnterMykonosDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubMykonos_02",
        "default_is_evil": "false"
    },
    {
        "name": "Apotos N Act 1",
        "file": Path("#Application/SR_EnterMykonosNightAction.seq.xml"),
        "default_archive": "ActN_MykonosEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Apotos N Act 2",
        "file": Path("#Application/SR_EnterMykonosNightActionSub01.seq.xml"),
        "default_archive": "ActN_MykonosEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Spagonia D Act 1",
        "file": Path("#Application/SR_EnterEUDayAction.seq.xml"),
        "default_archive": "ActD_EU",
        "default_is_evil": "false"
    },
    {
        "name": "Spagonia D Act 2",
        "file": Path("#Application/SR_EnterEUDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubEU_01",
        "default_is_evil": "false"
    },
    {
        "name": "Spagonia D Act 3",
        "file": Path("#Application/SR_EnterEUDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubEU_02",
        "default_is_evil": "false"
    },
    {
        "name": "Spagonia D Act 4",
        "file": Path("#Application/SR_EnterEUDayActionSub03.seq.xml"),
        "default_archive": "ActD_SubEU_03",
        "default_is_evil": "false"
    },
    {
        "name": "Spagonia D Act 5",
        "file": Path("#Application/SR_EnterEUDayActionSub04.seq.xml"),
        "default_archive": "ActD_SubEU_04",
        "default_is_evil": "false"
    },
    {
        "name": "Egg Ray Boss Battle",
        "file": Path("#Application/SR_EnterEUDayBoss.seq.xml"),
        "default_archive": "BossEggRayBird",
        "default_is_evil": "false"
    },
    {
        "name": "Spagonia N Act 1",
        "file": Path("#Application/SR_EnterEUNightAction.seq.xml"),
        "default_archive": "ActN_EUEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Spagonia N Act 2",
        "file": Path("#Application/SR_EnterEUNightActionSub01.seq.xml"),
        "default_archive": "ActN_SubEU_01",
        "default_is_evil": "true"
    },
    {
        "name": "Mazuri D Act 1",
        "file": Path("#Application/SR_EnterAfricaDayAction.seq.xml"),
        "default_archive": "ActD_Africa",
        "default_is_evil": "false"
    },
    {
        "name": "Mazuri D Act 2",
        "file": Path("#Application/SR_EnterAfricaDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubAfrica_01",
        "default_is_evil": "false"
    },
    {
        "name": "Mazuri D Act 3",
        "file": Path("#Application/SR_EnterAfricaDayActionSub03.seq.xml"),
        "default_archive": "ActD_SubAfrica_03",
        "default_is_evil": "false"
    },
    {
        "name": "Mazuri D Act 4",
        "file": Path("#Application/SR_EnterAfricaDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubAfrica_02",
        "default_is_evil": "false"
    },
    {
        "name": "Egg Beetle Boss Battle",
        "file": Path("#Application/SR_EnterAfricaDayBoss.seq.xml"),
        "default_archive": "BossEggBeetle",
        "default_is_evil": "false"
    },
    {
        "name": "Mazuri N Act 1",
        "file": Path("#Application/SR_EnterAfricaNightAction.seq.xml"),
        "default_archive": "ActN_AfricaEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Mazuri N Act 2",
        "file": Path("#Application/SR_EnterAfricaNightActionSub01.seq.xml"),
        "default_archive": "ActN_SubAfrica_01",
        "default_is_evil": "true"
    },
    {
        "name": "Mazuri N Act 3",
        "file": Path("#Application/SR_EnterAfricaNightActionSub02.seq.xml"),
        "default_archive": "ActN_SubAfrica_02",
        "default_is_evil": "true"
    },
    {
        "name": "Mazuri N Act 4",
        "file": Path("#Application/SR_EnterAfricaNightActionSub03.seq.xml"),
        "default_archive": "ActN_SubAfrica_03",
        "default_is_evil": "true"
    },
    {
        "name": "Empire State D Act 1",
        "file": Path("#Application/SR_EnterNYDayAction.seq.xml"),
        "default_archive": "ActD_NY",
        "default_is_evil": "false"
    },
    {
        "name": "Empire State D Act 2",
        "file": Path("#Application/SR_EnterNYDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubNY_01",
        "default_is_evil": "false"
    },
    {
        "name": "Empire State D Act 3",
        "file": Path("#Application/SR_EnterNYDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubNY_02",
        "default_is_evil": "false"
    },
    {
        "name": "Empire State N Act 1",
        "file": Path("#Application/SR_EnterNYNightAction.seq.xml"),
        "default_archive": "ActN_NYEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Empire State N Act 2",
        "file": Path("#Application/SR_EnterNYNightActionSub01.seq.xml"),
        "default_archive": "ActN_SubNY_01",
        "default_is_evil": "true"
    },
    {
        "name": "Shamar D Act 1",
        "file": Path("#Application/SR_EnterPetraDayAction.seq.xml"),
        "default_archive": "ActD_Petra",
        "default_is_evil": "false"
    },
    {
        "name": "Shamar D Act 2",
        "file": Path("#Application/SR_EnterPetraDayActionSub03.seq.xml"),
        "default_archive": "ActD_SubPetra_03",
        "default_is_evil": "false"
    },
    {
        "name": "Shamar N Act 1",
        "file": Path("#Application/SR_EnterPetraNightAction.seq.xml"),
        "default_archive": "ActN_PetraEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Shamar N Act 2",
        "file": Path("#Application/SR_EnterPetraNightActionSub02.seq.xml"),
        "default_archive": "ActN_SubPetra_02",
        "default_is_evil": "true"
    },
    {
        "name": "Dark Guardian Boss Battle",
        "file": Path("#Application/SR_EnterPetraNightBoss.seq.xml"),
        "default_archive": "BossPetra",
        "default_is_evil": "true"
    },
    {
        "name": "Holoska D Act 1",
        "file": Path("#Application/SR_EnterSnowDayAction.seq.xml"),
        "default_archive": "ActD_Snow",
        "default_is_evil": "false"
    },
    {
        "name": "Holoska D Act 2",
        "file": Path("#Application/SR_EnterSnowDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubSnow_01",
        "default_is_evil": "false"
    },
    {
        "name": "Holoska D Act 3",
        "file": Path("#Application/SR_EnterSnowDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubSnow_02",
        "default_is_evil": "false"
    },
    {
        "name": "Holoska D Act 4",
        "file": Path("#Application/SR_EnterSnowDayActionSub03.seq.xml"),
        "default_archive": "ActD_SubSnow_03",
        "default_is_evil": "false"
    },
    {
        "name": "Holoska N Act 1",
        "file": Path("#Application/SR_EnterSnowNightAction.seq.xml"),
        "default_archive": "ActN_SnowEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Holoska N Act 2",
        "file": Path("#Application/SR_EnterSnowNightActionSub01.seq.xml"),
        "default_archive": "ActN_SubSnow_01",
        "default_is_evil": "true"
    },
    {
        "name": "Holoska N Act 3",
        "file": Path("#Application/SR_EnterSnowNightActionSub02.seq.xml"),
        "default_archive": "ActN_SubSnow_02",
        "default_is_evil": "true"
    },
    {
        "name": "Dark Gaia Moray Boss Battle",
        "file": Path("#Application/SR_EnterSnowNightBoss.seq.xml"),
        "default_archive": "BossDarkGaiaMoray",
        "default_is_evil": "true"
    },
    {
        "name": "Adabat D Act 1",
        "file": Path("#Application/SR_EnterBeachDayAction.seq.xml"),
        "default_archive": "ActD_Beach",
        "default_is_evil": "false"
    },
    {
        "name": "Adabat D Act 2",
        "file": Path("#Application/SR_EnterBeachDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubBeach_02",
        "default_is_evil": "false"
    },
    {
        "name": "Adabat D Act 3",
        "file": Path("#Application/SR_EnterBeachDayActionSub04.seq.xml"),
        "default_archive": "ActD_SubBeach_04",
        "default_is_evil": "false"
    },
    {
        "name": "Adabat D Act 4",
        "file": Path("#Application/SR_EnterBeachDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubBeach_01",
        "default_is_evil": "false"
    },
    {
        "name": "Adabat D Act 5",
        "file": Path("#Application/SR_EnterBeachDayActionSub03.seq.xml"),
        "default_archive": "ActD_SubBeach_03",
        "default_is_evil": "false"
    },
    {
        "name": "Egg Lancer Boss Battle",
        "file": Path("#Application/SR_EnterBeachDayBoss.seq.xml"),
        "default_archive": "BossEggLancer",
        "default_is_evil": "false"
    },
    {
        "name": "Adabat N Act 1",
        "file": Path("#Application/SR_EnterBeachNightAction.seq.xml"),
        "default_archive": "ActN_BeachEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Adabat N Act 2",
        "file": Path("#Application/SR_EnterBeachNightActionSub01.seq.xml"),
        "default_archive": "ActN_SubBeach_01",
        "default_is_evil": "true"
    },
    {
        "name": "Chun Nan D Act 1",
        "file": Path("#Application/SR_EnterChinaDayAction.seq.xml"),
        "default_archive": "ActD_China",
        "default_is_evil": "false"
    },
    {
        "name": "Chun Nan D Act 2",
        "file": Path("#Application/SR_EnterChinaDayActionSub03.seq.xml"),
        "default_archive": "ActD_SubChina_03",
        "default_is_evil": "false"
    },
    {
        "name": "Chun Nan D Act 3",
        "file": Path("#Application/SR_EnterChinaDayActionSub04.seq.xml"),
        "default_archive": "ActD_SubChina_04",
        "default_is_evil": "false"
    },
    {
        "name": "Chun Nan D Act 4",
        "file": Path("#Application/SR_EnterChinaDayActionSub01.seq.xml"),
        "default_archive": "ActD_SubChina_01",
        "default_is_evil": "false"
    },
    {
        "name": "Chun Nan D Act 5",
        "file": Path("#Application/SR_EnterChinaDayActionSub02.seq.xml"),
        "default_archive": "ActD_SubChina_02",
        "default_is_evil": "false"
    },
    {
        "name": "Dark Gaia Pheonix Boss Battle",
        "file": Path("#Application/SR_EnterChinaNightBoss.seq.xml"),
        "default_archive": "BossPhoenix",
        "default_is_evil": "true"
    },
    {
        "name": "Chun Nan N Act 1",
        "file": Path("#Application/SR_EnterChinaNightAction.seq.xml"),
        "default_archive": "ActN_ChinaEvil",
        "default_is_evil": "true"
    },
    {
        "name": "Chun Nan N Act 2",
        "file": Path("#Application/SR_EnterChinaNightActionSub01.seq.xml"),
        "default_archive": "ActN_SubChina_01",
        "default_is_evil": "true"
    },
    {
        "name": "Chun Nan N Act 3",
        "file": Path("#Application/SR_EnterChinaNightActionSub02.seq.xml"),
        "default_archive": "ActN_SubChina_02",
        "default_is_evil": "true"
    },
    
]

STAGE_DATA = {"ActD_MykonosAct1": {
        "loading_resource_id": "MD",
        "rank_table": {"S": 150000, "A": 135000, "B": 100000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1200,
        "checkpoint_num": 1,
        "time_bonus_efficient": None,
    },
    "ActD_MykonosAct2": {
        "loading_resource_id": "MD",
        "rank_table": {"S": 150000, "A": 135000, "B": 100000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 750,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    "ActD_SubMykonos_01": {
        "loading_resource_id": "MD",
        "rank_table": {"S": 100000, "A": 90000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 700,
        "checkpoint_num": 0,
        "time_bonus_efficient": None,
    },
    "ActD_SubMykonos_02": {
        "loading_resource_id": "MD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    "ActN_MykonosEvil": {
        "loading_resource_id": "MD",
        "rank_table": {"S": 300000, "A": 200000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 3600,
        "checkpoint_num": None,
        "time_bonus_efficient": 30
    },
    "ActN_SubMykonos_01": {
        "loading_resource_id": "MD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1800,
        "checkpoint_num": None,
        "time_bonus_efficient": 80
    },
    "ActD_EU": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 135000, "B": 100000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    "ActD_SubEU_01": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 90000, "A": 70000, "B": 50000, "C": 30000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    "ActD_SubEU_02": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 100000, "A": 90000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 300,
        "checkpoint_num": 0,
        "time_bonus_efficient": 500
    },
    "ActD_SubEU_03": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": 0,
        "time_bonus_efficient": None
    },
    "ActD_SubEU_04": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": 0,
        "time_bonus_efficient": None
    },
    "ActN_EUEvil": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 300000, "A": 200000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 2700,
        "checkpoint_num": None,
        "time_bonus_efficient": 50
    },
    "ActN_SubEU_01": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": 80
    },
    "BossEggRayBird": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 50000, "A": 40000, "B": 30000, "C": 20000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": 80
    },
    "ActD_Africa": {
        "loading_resource_id": "AD",
        "rank_table": {"S": 150000, "A": 135000, "B": 100000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 900,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    "ActD_SubAfrica_01": {
        "loading_resource_id": "AD",
        "rank_table": {"S": 100000, "A": 90000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 75,
        "checkpoint_num": 0,
        "time_bonus_efficient": 5500
    },
    "ActD_SubAfrica_02": {
        "loading_resource_id": "AD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    "ActD_SubAfrica_03": {
        "loading_resource_id": "AD",
        "rank_table": {"S": 100000, "A": 90000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 50,
        "checkpoint_num": 0,
        "time_bonus_efficient": 4000
    },
    "BossEggBeetle": {
        "loading_resource_id": "AD",
        "rank_table": {"S": 40000, "A": 30000, "B": 20000, "C": 15000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None
    },
    "ActN_AfricaEvil": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 300000, "A": 200000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 2100,
        "checkpoint_num": None,
        "time_bonus_efficient": 200
    },
    "ActN_SubAfrica_01": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1800,
        "checkpoint_num": None,
        "time_bonus_efficient": 80
    },
    "ActN_SubAfrica_02": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": 0,
        "time_bonus_efficient": None
    },
    "ActN_SubAfrica_03": {
        "loading_resource_id": "ED",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": 0,
        "time_bonus_efficient": None
    },
    "ActD_NY": {
        "loading_resource_id": "ND",
        "rank_table": {"S": 200000, "A": 180000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 1500,
        "checkpoint_num": 0,
        "time_bonus_efficient": None
    },
    "ActD_SubNY_01": {
        "loading_resource_id": "ND",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None
    },
    "ActD_SubNY_02": {
        "loading_resource_id": "ND",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None
    },
    "ActN_NYEvil": {
        "loading_resource_id": "NN",
        "rank_table": {"S": 300000, "A": 200000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 3600,
        "checkpoint_num": None,
        "time_bonus_efficient": 60
    },
    "ActN_SubNY_01": {
        "loading_resource_id": "NN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None
    },
    "ActD_Petra": {
        "loading_resource_id": "PD",
        "rank_table": {"S": 200000, "A": 180000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 330,
        "checkpoint_num": 0,
        "time_bonus_efficient": 450
    },
    "ActD_SubPetra_01": {
        "loading_resource_id": "PD",
        "rank_table": {"S": 55000, "A": 40000, "B": 30000, "C": 20000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None
    },
    "ActD_SubPetra_03": {
        "loading_resource_id": "PD",
        "rank_table": {"S": 100000, "A": 90000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 80,
        "checkpoint_num": None,
        "time_bonus_efficient": 2500
    },
    "ActN_PetraEvil": {
        "loading_resource_id": "PD",
        "rank_table": {"S": 300000, "A": 200000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 3600,
        "checkpoint_num": None,
        "time_bonus_efficient": 60
    },
    "ActN_SubPetra_02": {
        "loading_resource_id": "PN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None
    },
    "BossPetra": {
        "loading_resource_id": "PN",
        "rank_table": {"S": 60000, "A": 55000, "B": 50000, "C": 45000, "D": 30000, "E": 0},
        "base_time": 750,
        "checkpoint_num": None,
        "time_bonus_efficient": 100
    },
    "ActD_China": {
        "loading_resource_id": "CD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1800,
        "checkpoint_num": None,
        "time_bonus_efficient": 80,
    },

    "ActD_SubChina_01": {
        "loading_resource_id": "CD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubChina_02": {
        "loading_resource_id": "CD",
        "rank_table": {"S": 65000, "A": 50000, "B": 30000, "C": 20000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubChina_03": {
        "loading_resource_id": "CD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubChina_04": {
        "loading_resource_id": "CD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActN_ChinaEvil": {
        "loading_resource_id": "CN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1800,
        "checkpoint_num": None,
        "time_bonus_efficient": 80,
    },

    "ActN_SubChina_01": {
        "loading_resource_id": "CN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActN_SubChina_02": {
        "loading_resource_id": "CN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "BossPhoenix": {
        "loading_resource_id": "CN",
        "rank_table": {"S": 60000, "A": 55000, "B": 50000, "C": 45000, "D": 30000, "E": 0},
        "base_time": 750,
        "checkpoint_num": None,
        "time_bonus_efficient": 100,
    },

    "ActD_Beach": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1800,
        "checkpoint_num": None,
        "time_bonus_efficient": 80,
    },

    "ActD_SubBeach_01": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 50000, "A": 40000, "B": 30000, "C": 20000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubBeach_02": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 90000, "A": 70000, "B": 50000, "C": 30000, "D": 20000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubBeach_03": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubBeach_04": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 50000, "A": 40000, "B": 30000, "C": 20000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActN_BeachEvil": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 1800,
        "checkpoint_num": None,
        "time_bonus_efficient": 80,
    },

    "ActN_SubBeach_01": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "BossEggLancer": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 70000, "A": 60000, "B": 50000, "C": 40000, "D": 30000, "E": 0},
        "base_time": 1000,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
        "ActD_Snow": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 150000, "A": 135000, "B": 100000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 400,
        "checkpoint_num": None,
        "time_bonus_efficient": 400,
    },

    "ActD_SubSnow_01": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 100000, "A": 90000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": 3,
        "time_bonus_efficient": None,
    },

    "ActD_SubSnow_02": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 40000, "A": 35000, "B": 30000, "C": 25000, "D": 10000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActD_SubSnow_03": {
        "loading_resource_id": "SD",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActN_SnowEvil": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 300000, "A": 200000, "B": 150000, "C": 100000, "D": 50000, "E": 0},
        "base_time": 2700,
        "checkpoint_num": None,
        "time_bonus_efficient": 100,
    },

    "ActN_SubSnow_01": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "ActN_SubSnow_02": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 150000, "A": 100000, "B": 75000, "C": 50000, "D": 25000, "E": 0},
        "base_time": 500,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },

    "BossDarkGaiaMoray": {
        "loading_resource_id": "SN",
        "rank_table": {"S": 85000, "A": 75000, "B": 65000, "C": 55000, "D": 45000, "E": 0},
        "base_time": 1000,
        "checkpoint_num": None,
        "time_bonus_efficient": None,
    },
    
}

ARCHIVE_TO_ID = {
    "ActD_MykonosAct1": 0,
    "ActD_MykonosAct2": 1,
    "ActD_SubMykonos_01": 2,
    "ActD_SubMykonos_02": 3,
    "ActN_MykonosEvil": 4,
    "ActN_SubMykonos_01": 5,

    "ActD_EU": 6,
    "ActD_SubEU_01": 7,
    "ActD_SubEU_02": 8,
    "ActD_SubEU_03": 9,
    "ActD_SubEU_04": 10,
    "ActN_EUEvil": 11,
    "ActN_SubEU_01": 12,

    "ActD_Africa": 13,
    "ActD_SubAfrica_01": 14,
    "ActD_SubAfrica_02": 15,
    "ActD_SubAfrica_03": 16,
    "ActN_AfricaEvil": 17,
    "ActN_SubAfrica_01": 18,
    "ActN_SubAfrica_02": 19,
    "ActN_SubAfrica_03": 20,

    "ActD_NY": 21,
    "ActD_SubNY_01": 22,
    "ActD_SubNY_02": 23,
    "ActN_NYEvil": 24,
    "ActN_SubNY_01": 25,

    "ActD_Petra": 26,
    "ActD_SubPetra_03": 27,
    "ActN_PetraEvil": 28,
    "ActN_SubPetra_02": 29,

    "ActD_Snow": 30,
    "ActD_SubSnow_01": 31,
    "ActD_SubSnow_02": 32,
    "ActD_SubSnow_03": 33,
    "ActN_SnowEvil": 34,
    "ActN_SubSnow_01": 35,
    "ActN_SubSnow_02": 36,

    "ActD_Beach": 37,
    "ActD_SubBeach_01": 38,
    "ActD_SubBeach_02": 39,
    "ActD_SubBeach_03": 40,
    "ActD_SubBeach_04": 41,
    "ActN_BeachEvil": 42,
    "ActN_SubBeach_01": 43,

    "ActD_China": 44,
    "ActD_SubChina_01": 45,
    "ActD_SubChina_02": 46,
    "ActD_SubChina_03": 47,
    "ActD_SubChina_04": 48,
    "ActN_ChinaEvil": 49,
    "ActN_SubChina_01": 50,
    "ActN_SubChina_02": 51,

    "BossEggBeetle": 52,
    "BossEggRayBird": 53,
    "BossPhoenix": 54,
    "BossEggLancer": 55,
    "BossDarkGaiaMoray": 56,
    "BossPetra": 57,
}

ID_TO_ARCHIVE = {
    stage_id: archive
    for archive, stage_id in ARCHIVE_TO_ID.items()
}

ARCHIVE_DISPLAY_NAMES = {
    "ActD_MykonosAct1": "Apotos - Day Act 1",
    "ActD_MykonosAct2": "Apotos - Day Act 2",
    "ActD_SubMykonos_01": "Apotos - Day Act 3",
    "ActD_SubMykonos_02": "Apotos - Day Act 4",
    "ActN_MykonosEvil": "Apotos - Night Act 1",
    "ActN_SubMykonos_01": "Apotos - Night Act 2",

    "ActD_EU": "Spagonia - Day Act 1",
    "ActD_SubEU_01": "Spagonia - Day Act 2",
    "ActD_SubEU_02": "Spagonia - Day Act 3",
    "ActD_SubEU_03": "Spagonia - Day Act 4",
    "ActD_SubEU_04": "Spagonia - Day Act 5",
    "ActN_EUEvil": "Spagonia - Night Act 1",
    "ActN_SubEU_01": "Spagonia - Night Act 2",

    "ActD_Africa": "Mazuri - Day Act 1",
    "ActD_SubAfrica_01": "Mazuri - Day Act 2",
    "ActD_SubAfrica_03": "Mazuri - Day Act 3",
    "ActD_SubAfrica_02": "Mazuri - Day Act 4",
    "ActN_AfricaEvil": "Mazuri - Night Act 1",
    "ActN_SubAfrica_01": "Mazuri - Night Act 2",
    "ActN_SubAfrica_02": "Mazuri - Night Act 3",
    "ActN_SubAfrica_03": "Mazuri - Night Act 4",

    "ActD_NY": "Empire City - Day Act 1",
    "ActD_SubNY_01": "Empire City - Day Act 2",
    "ActD_SubNY_02": "Empire City - Day Act 3",
    "ActN_NYEvil": "Empire City - Night Act 1",
    "ActN_SubNY_01": "Empire City - Night Act 2",

    "ActD_Petra": "Shamar - Day Act 1",
    "ActD_SubPetra_03": "Shamar - Day Act 2",
    "ActN_PetraEvil": "Shamar - Night Act 1",
    "ActN_SubPetra_02": "Shamar - Night Act 2",

    "ActD_Snow": "Holoska - Day Act 1",
    "ActD_SubSnow_01": "Holoska - Day Act 2",
    "ActD_SubSnow_02": "Holoska - Day Act 3",
    "ActD_SubSnow_03": "Holoska - Day Act 4",
    "ActN_SnowEvil": "Holoska - Night Act 1",
    "ActN_SubSnow_01": "Holoska - Night Act 2",
    "ActN_SubSnow_02": "Holoska - Night Act 3",

    "ActD_Beach": "Adabat - Day Act 1",
    "ActD_SubBeach_02": "Adabat - Day Act 2",
    "ActD_SubBeach_04": "Adabat - Day Act 3",
    "ActD_SubBeach_01": "Adabat - Day Act 4",
    "ActD_SubBeach_03": "Adabat - Day Act 5",
    "ActN_BeachEvil": "Adabat - Night Act 1",
    "ActN_SubBeach_01": "Adabat - Night Act 2",

    "ActD_China": "Chun-nan - Day Act 1",
    "ActD_SubChina_03": "Chun-nan - Day Act 2",
    "ActD_SubChina_04": "Chun-nan - Day Act 3",
    "ActD_SubChina_01": "Chun-nan - Day Act 4",
    "ActD_SubChina_02": "Chun-nan - Day Act 5",
    "ActN_ChinaEvil": "Chun-nan - Night Act 1",
    "ActN_SubChina_01": "Chun-nan - Night Act 2",
    "ActN_SubChina_02": "Chun-nan - Night Act 3",

    "BossEggBeetle": "Egg Beetle",
    "BossEggRayBird": "Egg Devil Ray",
    "BossPhoenix": "Dark Gaia Phoenix",
    "BossEggLancer": "Egg Lancer",
    "BossDarkGaiaMoray": "Dark Moray",
    "BossPetra": "Dark Guardian",
}

def get_stage_display_name(archive: str) -> str:
    """Return a readable stage name, retaining the archive as a fallback."""
    return ARCHIVE_DISPLAY_NAMES.get(archive, archive)

NO_UPGRADE_POOL = [
    {"archive": "ActD_MykonosAct1", "is_evil": "false"},
    {"archive": "ActD_MykonosAct2", "is_evil": "false"},
    {"archive": "ActD_SubMykonos_01", "is_evil": "false"},
    {"archive": "ActD_SubMykonos_02", "is_evil": "false"},
    {"archive": "ActN_MykonosEvil", "is_evil": "true"},
    {"archive": "ActN_SubMykonos_01", "is_evil": "true"},
    {"archive": "ActD_SubNY_01", "is_evil": "false"},
    {"archive": "ActD_SubNY_02", "is_evil": "false"},
    {"archive": "ActN_NYEvil", "is_evil": "true"},
    {"archive": "ActN_SubNY_01", "is_evil": "true"},
    #{"archive": "ActD_SubPetra_02", "is_evil": "false"}, Chao collection mission does not complete when loaded through randomised entry.
    {"archive": "ActD_SubPetra_03", "is_evil": "false"},
    {"archive": "ActN_PetraEvil", "is_evil": "true"},
    {"archive": "ActN_SubPetra_02", "is_evil": "true"},
    {"archive": "ActD_SubSnow_01", "is_evil": "false"},
    {"archive": "ActD_SubSnow_02", "is_evil": "false"},
    {"archive": "ActN_SnowEvil", "is_evil": "true"},
    {"archive": "ActN_SubSnow_01", "is_evil": "true"},
    {"archive": "ActN_SubSnow_02", "is_evil": "true"},
    {"archive": "ActD_Africa", "is_evil": "false"},
    {"archive": "ActD_SubAfrica_01", "is_evil": "false"},
    {"archive": "ActN_AfricaEvil", "is_evil": "true"},
    {"archive": "ActN_SubAfrica_01", "is_evil": "true"},
    {"archive": "ActN_SubAfrica_02", "is_evil": "true"},
    {"archive": "ActN_SubAfrica_03", "is_evil": "true"},
    {"archive": "ActD_SubBeach_01", "is_evil": "false"},
    {"archive": "ActD_SubBeach_03", "is_evil": "false"},
    {"archive": "ActD_SubBeach_04", "is_evil": "false"},
    {"archive": "ActN_BeachEvil", "is_evil": "true"},
    {"archive": "ActN_SubBeach_01", "is_evil": "true"},
    {"archive": "ActD_China", "is_evil": "false"},
    {"archive": "ActD_SubChina_02", "is_evil": "false"},
    {"archive": "ActN_ChinaEvil", "is_evil": "true"},
    {"archive": "ActN_SubChina_01", "is_evil": "true"},
    {"archive": "ActN_SubChina_02", "is_evil": "true"},
    {"archive": "ActD_SubEU_03", "is_evil": "false"},
    {"archive": "ActN_EUEvil", "is_evil": "true"},
    {"archive": "ActN_SubEU_01", "is_evil": "true"},
]


pool = [
    {"archive": "ActD_MykonosAct1", "is_evil": "false"},
    {"archive": "ActD_MykonosAct2", "is_evil": "false"},
    {"archive": "ActD_SubMykonos_01", "is_evil": "false"},
    {"archive": "ActD_SubMykonos_02", "is_evil": "false"},
    {"archive": "ActN_MykonosEvil", "is_evil": "true"},
    {"archive": "ActN_SubMykonos_01", "is_evil": "true"},
    {"archive": "ActD_NY", "is_evil": "false"},
    {"archive": "ActD_SubNY_01", "is_evil": "false"},
    {"archive": "ActD_SubNY_02", "is_evil": "false"},
    {"archive": "ActN_NYEvil", "is_evil": "true"},
    {"archive": "ActN_SubNY_01", "is_evil": "true"},
    {"archive": "ActD_Petra", "is_evil": "false"},
    #{"archive": "ActD_SubPetra_02", "is_evil": "false"}, Chao collection mission does not complete when loaded through randomised entry.
    {"archive": "ActD_SubPetra_03", "is_evil": "false"},
    {"archive": "ActN_PetraEvil", "is_evil": "true"},
    {"archive": "ActN_SubPetra_02", "is_evil": "true"},
    {"archive": "ActD_Snow", "is_evil": "false"},
    {"archive": "ActD_SubSnow_01", "is_evil": "false"},
    {"archive": "ActD_SubSnow_02", "is_evil": "false"},
    {"archive": "ActD_SubSnow_03", "is_evil": "false"},
    {"archive": "ActN_SnowEvil", "is_evil": "true"},
    {"archive": "ActN_SubSnow_01", "is_evil": "true"},
    {"archive": "ActN_SubSnow_02", "is_evil": "true"},
    {"archive": "ActD_Africa", "is_evil": "false"},
    {"archive": "ActD_SubAfrica_01", "is_evil": "false"},
    {"archive": "ActD_SubAfrica_02", "is_evil": "false"},
    {"archive": "ActD_SubAfrica_03", "is_evil": "false"},
    {"archive": "ActN_AfricaEvil", "is_evil": "true"},
    {"archive": "ActN_SubAfrica_01", "is_evil": "true"},
    {"archive": "ActN_SubAfrica_02", "is_evil": "true"},
    {"archive": "ActN_SubAfrica_03", "is_evil": "true"},
    {"archive": "ActD_Beach", "is_evil": "false"},
    {"archive": "ActD_SubBeach_01", "is_evil": "false"},
    {"archive": "ActD_SubBeach_02", "is_evil": "false"},
    {"archive": "ActD_SubBeach_03", "is_evil": "false"},
    {"archive": "ActD_SubBeach_04", "is_evil": "false"},
    {"archive": "ActN_BeachEvil", "is_evil": "true"},
    {"archive": "ActN_SubBeach_01", "is_evil": "true"},
    {"archive": "ActD_China", "is_evil": "false"},
    {"archive": "ActD_SubChina_01", "is_evil": "false"},
    {"archive": "ActD_SubChina_02", "is_evil": "false"},
    {"archive": "ActD_SubChina_03", "is_evil": "false"},
    {"archive": "ActD_SubChina_04", "is_evil": "false"},
    {"archive": "ActN_ChinaEvil", "is_evil": "true"},
    {"archive": "ActN_SubChina_01", "is_evil": "true"},
    {"archive": "ActN_SubChina_02", "is_evil": "true"},
    {"archive": "ActD_EU", "is_evil": "false"},
    {"archive": "ActD_SubEU_01", "is_evil": "false"},
    {"archive": "ActD_SubEU_03", "is_evil": "false"},
    {"archive": "ActD_SubEU_04", "is_evil": "false"},
    {"archive": "ActN_EUEvil", "is_evil": "true"},
    {"archive": "ActN_SubEU_01", "is_evil": "true"}

]

bossPool = [
    #{"archive": "BossPetra", "is_evil": "true"},
    {"archive": "BossEggRayBird", "is_evil": "false"},
    #{"archive": "BossPhoenix", "is_evil": "true"},
    {"archive": "BossEggLancer", "is_evil": "false"},
    #{"archive": "BossDarkGaiaMoray", "is_evil": "true"},
    {"archive": "BossEggBeetle", "is_evil": "false"}#requires a custom SR_RandoAfricaDayBoss wrapper
]

DEFAULT_LOCKED_BOSSES = [
    "BossPetra",
    "BossPhoenix",
    "BossDarkGaiaMoray",
]

# Stages in this set remain in their original world-map locations and are not
# included in the random stage pool or seed code.
FIXED_STAGE_ARCHIVES = {
    "ActD_SubEU_02",  # Spagonia Day Act 3 soft-locks Chao collection mission does not complete when loaded through randomised entry.
}


generated_seed_ids = []
seed_replay_ids = []
seed_replay_index = 0


def encode_seed(stage_ids: list[int]) -> str:
    raw_bytes = bytes(stage_ids)

    return base64.urlsafe_b64encode(raw_bytes).decode("utf-8").rstrip("=")


def decode_seed(seed_code: str) -> list[int]:
    padding = "=" * (-len(seed_code) % 4)

    raw_bytes = base64.urlsafe_b64decode(seed_code + padding)

    return list(raw_bytes)


def find_stage_by_archive(stage_pool: list[dict], archive: str) -> dict:
    for stage in stage_pool:
        if stage["archive"] == archive:
            return stage

    raise ValueError(f"Archive '{archive}' was not found in this pool.")

def pick_stage(stage_pool: list[dict]) -> dict:
    global seed_replay_index

    if SEED_CODE is None:
        chosen = random.choice(stage_pool)
        generated_seed_ids.append(ARCHIVE_TO_ID[chosen["archive"]])
    else:
        if seed_replay_index >= len(seed_replay_ids):
            raise ValueError("Seed ended before all stage entries were randomised.")

        stage_id = seed_replay_ids[seed_replay_index]
        seed_replay_index += 1

        archive = ID_TO_ARCHIVE[stage_id]
        chosen = find_stage_by_archive(stage_pool, archive)

    stage_pool.remove(chosen)
    return chosen

def set_stage_data(xml_path: Path, stage: dict) -> None:
    text = xml_path.read_text(encoding="utf-8")

    text, archive_count = re.subn(
        r"<ArchiveName>.*?</ArchiveName>",
        f"<ArchiveName>{stage['archive']}</ArchiveName>",
        text,
        count=1,
        flags=re.DOTALL,
    )

    text, evil_count = re.subn(
        r"<IsEvil>.*?</IsEvil>",
        f"<IsEvil>{str(stage['is_evil']).lower()}</IsEvil>",
        text,
        count=1,
        flags=re.DOTALL,
    )

    if archive_count == 0:
        raise ValueError(f"No <ArchiveName> found in {xml_path}")

    if evil_count == 0:
        raise ValueError(f"No <IsEvil> found in {xml_path}")

    text = apply_stage_data(text, stage)

    xml_path.write_text(text, encoding="utf-8")

def apply_stage_data(text: str, stage: dict) -> str:
    data = STAGE_DATA[stage["archive"]]

    default_case_pattern = (
        r'(<Case flag="eFlag_TrialMissionType" '
        r'operation="E" '
        r'value="eFlag_TrialMissionType_Default">.*?</Case>)'
    )

    match = re.search(default_case_pattern, text, flags=re.DOTALL)

    if not match:
        return text

    default_block = match.group(1)

    default_block = re.sub(
        r"<LoadingResourceID>.*?</LoadingResourceID>",
        f"<LoadingResourceID>{data['loading_resource_id']}</LoadingResourceID>",
        default_block,
        count=1,
        flags=re.DOTALL,
    )

    ranks = data["rank_table"]

    rank_block = (
        "<RankTable>\n"
        f"    <S>{ranks['S']}</S>\n"
        f"    <A>{ranks['A']}</A>\n"
        f"    <B>{ranks['B']}</B>\n"
        f"    <C>{ranks['C']}</C>\n"
        f"    <D>{ranks['D']}</D>\n"
        f"    <E>{ranks['E']}</E>\n"
        "</RankTable>"
    )

    default_block = re.sub(
        r"<RankTable>.*?</RankTable>",
        rank_block,
        default_block,
        count=1,
        flags=re.DOTALL,
    )

    default_block = re.sub(
        r"<BaseTime>.*?</BaseTime>",
        f"<BaseTime>{data['base_time']}</BaseTime>",
        default_block,
        count=1,
    )

    if data["checkpoint_num"] is not None:
        checkpoint_block = f"<CheckPointNum>{data['checkpoint_num']}</CheckPointNum>"

        if "<CheckPointNum>" in default_block:
            default_block = re.sub(
                r"<CheckPointNum>.*?</CheckPointNum>",
                checkpoint_block,
                default_block,
                count=1,
            )
        else:
            default_block = default_block.replace(
                "<!--<CheckPointNum>3</CheckPointNum>-->",
                checkpoint_block,
            )

    if data["time_bonus_efficient"] is not None:
        time_bonus_block = (
            f"<TimeBonusEfficient>{data['time_bonus_efficient']}</TimeBonusEfficient>"
        )

        if "<TimeBonusEfficient>" in default_block:
            default_block = re.sub(
                r"<TimeBonusEfficient>.*?</TimeBonusEfficient>",
                time_bonus_block,
                default_block,
                count=1,
            )
        else:
            default_block = default_block.replace(
                "</BaseTime>",
                f"</BaseTime>\n          {time_bonus_block}",
            )

    text = text[:match.start()] + default_block + text[match.end():]

    return text


def disable_first_play(xml_path: Path) -> None:
    text = xml_path.read_text(encoding="utf-8")

    first_play_pattern = re.compile(
        r"""
        <If\s+flag="[^"]+"\s+operation="E"\s+value="true">\s*
            <OverWriteSetData>\s*
                <Name>FirstPlay</Name>\s*
                <FileName>dummy\.set\.xml</FileName>\s*
            </OverWriteSetData>\s*
        </If>
        """,
        re.VERBOSE,
    )

    replacement = """<OverWriteSetData>
        <Name>FirstPlay</Name>
        <FileName>dummy.set.xml</FileName>
      </OverWriteSetData>"""

    new_text, count = first_play_pattern.subn(replacement, text, count=1)

    if count > 0:
        xml_path.write_text(new_text, encoding="utf-8")
        print(f"Disabled FirstPlay in {xml_path}")



def reset_all_files() -> None:
    print("Resetting files to default...")

    for entry in STAGE_ENTRIES:
        default_stage = {
            "archive": entry["default_archive"],
            "is_evil": entry["default_is_evil"],
        }

        set_stage_data(entry["file"], default_stage)
        print(f'Reset {entry["name"]} -> {entry["default_archive"]}')


def write_metadata_file(seed_code: str) -> None:
    metadata = {
        "randomiser_name": "Sonic Unleashed Randomiser",
        "version": "1.2.0",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "seed": seed_code,
        "settings": {
            "shuffle_stages": True,
            "shuffle_bosses": True,
            "allow_day_night_swaps": True,
            "first_stage_uses_no_upgrade_pool": True,
            "fixed_stages": sorted(FIXED_STAGE_ARCHIVES),
        }
    }

    metadata_path = Path("randomiser_metadata.json")
    metadata_path.write_text(
        json.dumps(metadata, indent=4),
        encoding="utf-8"
    )

    print(f"Metadata written to: {metadata_path}")


def main() -> None:

    base_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
    global seed_replay_ids
    global seed_replay_index

    generated_seed_ids.clear()
    seed_replay_index = 0

    global SEED_CODE

    while True:
        seed_input = input(
            "\nEnter a seed code (leave blank for a random seed): "
        ).strip()

        if not seed_input:
            SEED_CODE = None
            break

        try:
            decoded = decode_seed(seed_input)

            expected_seed_length = len([
                entry for entry in STAGE_ENTRIES
                if entry["default_archive"] not in DEFAULT_LOCKED_BOSSES
                and entry["default_archive"] not in FIXED_STAGE_ARCHIVES
            ])

            if len(decoded) != expected_seed_length:
                print(
                    f"Invalid seed. Expected {expected_seed_length} seed entries "
                    f"but found {len(decoded)}."
                )
                continue

            SEED_CODE = seed_input
            break

        except Exception:
            print("Invalid seed code. Please try again.")

    if SEED_CODE is None:
        seed_replay_ids = []
    else:
        seed_replay_ids = decode_seed(SEED_CODE)

    reset_all_files()

    available_no_upgrade_pool = NO_UPGRADE_POOL.copy()
    available_pool = pool.copy()
    available_boss_pool = bossPool.copy()

    log_lines = []
    log_lines.append("SONIC UNLEASHED RANDOMISER - SEED SPOILER LOG")
    log_lines.append("=" * 54)
    log_lines.append(f"Generated: {datetime.now().strftime('%d %B %Y at %H:%M:%S')}")
    log_lines.append("Seed Code: PENDING")
    log_lines.append("")
    log_lines.append("HOW TO READ THIS LOG")
    log_lines.append("The stage on the left is the location selected on the world map.")
    log_lines.append("The stage on the right is what will actually be played there.")
    log_lines.append("")
    log_lines.append("STAGE LOCATIONS")
    log_lines.append("-" * 54)
    print(len(pool))
    print(len([e for e in STAGE_ENTRIES if "Boss Battle" not in e["name"]]))

    stage_entry_archives = [
    e["default_archive"]
    for e in STAGE_ENTRIES
    if "Boss Battle" not in e["name"]
]

    pool_archives = [s["archive"] for s in pool]

    print("Normal entries:", len(stage_entry_archives))
    print("Pool:", len(pool_archives))

    print("Missing from pool:")
    for archive in stage_entry_archives:
        if archive not in pool_archives:
            print(archive)

    print("Extra in pool:")
    for archive in pool_archives:
        if archive not in stage_entry_archives:
            print(archive)

    print()
    print("=== RANDOMISING STAGES ===")
    print()

    for entry in STAGE_ENTRIES:
        if "Boss Battle" in entry["name"]:
            if entry["default_archive"] in DEFAULT_LOCKED_BOSSES:
                chosen = {
                    "archive": entry["default_archive"],
                    "is_evil": entry["default_is_evil"],
        }
            elif len(available_boss_pool) > 0:
                chosen = pick_stage(available_boss_pool)
            else:
                chosen = {
                "archive": entry["default_archive"],
                "is_evil": entry["default_is_evil"],
        }
                

        elif entry["default_archive"] in FIXED_STAGE_ARCHIVES:
            chosen = {
                "archive": entry["default_archive"],
                "is_evil": entry["default_is_evil"],
            }

        elif entry["name"] == "Apotos D Act 1":
            chosen = pick_stage(available_no_upgrade_pool)

            try:
                matching_stage = find_stage_by_archive(available_pool, chosen["archive"])
                available_pool.remove(matching_stage)
            except ValueError:
                pass

        else:
            chosen = pick_stage(available_pool)

        set_stage_data(entry["file"], chosen)
        disable_first_play(entry["file"])

        destination_name = get_stage_display_name(chosen["archive"])
        if entry["default_archive"] in FIXED_STAGE_ARCHIVES:
            result_line = f'{entry["name"]:<28} -> {destination_name} (Default)'
        else:
            result_line = f'{entry["name"]:<28} -> {destination_name}'

        print(result_line)
        log_lines.append(result_line)

    if SEED_CODE is None:
        final_seed_code = encode_seed(generated_seed_ids)
    else:
        final_seed_code = SEED_CODE

    log_lines[3] = f"Seed Code: {final_seed_code}"
    log_lines.append("")
    log_lines.append("Keep this seed code to replay or share the same randomisation.")

    log_path = base_dir / "randomiser_log.txt"
    log_path.write_text("\n".join(log_lines), encoding="utf-8")
    write_metadata_file(final_seed_code)

    print()
    print(f"Seed Code: {final_seed_code}")
    print(f"Log written to: {log_path}")


    hedgearcpack = base_dir / "HedgeArcPack.exe"
    application_folder = base_dir / "#Application"

    try:
        subprocess.run(
            [str(hedgearcpack), str(application_folder), "-P", "-T=hh"],
            check=True
        )
        print("Archive packed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"HedgeArcPack failed with exit code {e.returncode}")

    except FileNotFoundError:
        print("HedgeArcPack.exe not found.")


if __name__ == "__main__":
    main()
