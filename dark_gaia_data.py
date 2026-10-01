from dataclasses import dataclass


@dataclass(frozen=True)
class DarkGaiaStageData:
    archive: str
    completion_sets: tuple[str, ...]


DARK_GAIA_STAGE_DATA = {
    # Main day stages
    "Windmill Isle Day Act 1": DarkGaiaStageData(
        archive="+#ActD_MykonosAct1",
        completion_sets=("Normal.set.xml",),
    ),
    "Windmill Isle Day Act 2": DarkGaiaStageData(
        archive="+#ActD_MykonosAct2",
        completion_sets=("Normal.set.xml",),
    ),
    "Savannah Citadel Day Act 1": DarkGaiaStageData(
        archive="+#ActD_Africa",
        completion_sets=("Normal.set.xml",),
    ),
    "Cool Edge Day Act 1": DarkGaiaStageData(
        archive="+#ActD_Snow",
        completion_sets=("Base.set.xml",),
    ),
    "Rooftop Run Day Act 1": DarkGaiaStageData(
        archive="+#ActD_EU",
        completion_sets=("Normal.set.xml",),
    ),
    "Dragon Road Day Act 1": DarkGaiaStageData(
        archive="+#ActD_China",
        completion_sets=("Base.set.xml",),
    ),
    "Arid Sands Day Act 1": DarkGaiaStageData(
        archive="+#ActD_Petra",
        completion_sets=("Mainbase.set.xml",),
    ),
    "Skyscraper Scamper Day Act 1": DarkGaiaStageData(
        archive="+#ActD_NY",
        completion_sets=("Normal.set.xml",),
    ),
    "Jungle Joyride Day Act 1": DarkGaiaStageData(
        archive="+#ActD_Beach",
        completion_sets=("Base.set.xml",),
    ),
    # Day side stages
    "Windmill Isle Day Act 3": DarkGaiaStageData(
        archive="+#ActD_SubMykonos_01",
        completion_sets=("Base.set.xml",),
    ),
    "Savannah Citadel Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubAfrica_01",
        completion_sets=("Rap3.5.set.xml",),
    ),
    "Savannah Citadel Day Act 3": DarkGaiaStageData(
        archive="+#ActD_SubAfrica_03",
        completion_sets=("Rap04.set.xml",),
    ),
    "Rooftop Run Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubEU_01",
        completion_sets=("Set3.set.xml",),
    ),
    "Cool Edge Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubSnow_01",
        completion_sets=("Sub_Layer3_Set.set.xml",),
    ),
    "Dragon Road Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubChina_03",
        completion_sets=("Rap0302.set.xml",),
    ),
    "Dragon Road Day Act 3": DarkGaiaStageData(
        archive="+#ActD_SubChina_04",
        completion_sets=("Base.set.xml",),
    ),
    "Arid Sands Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubPetra_03",
        completion_sets=("Set1.set.xml",),
    ),
    "Skyscraper Scamper Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubNY_01",
        completion_sets=("Set.set.xml",),
    ),
    "Jungle Joyride Day Act 2": DarkGaiaStageData(
        archive="+#ActD_SubBeach_02",
        completion_sets=("Rap04.set.xml",),
    ),
    "Jungle Joyride Day Act 3": DarkGaiaStageData(
        archive="+#ActD_SubBeach_04",
        completion_sets=("Base.set.xml",),
    ),
    # DLC day stages
    "Windmill Isle Day Act 4": DarkGaiaStageData(
        archive="+#ActD_SubMykonos_02",
        completion_sets=("Base.set.xml",),
    ),
    "Savannah Citadel Day Act 4": DarkGaiaStageData(
        archive="+#ActD_SubAfrica_02",
        completion_sets=("Base.set.xml",),
    ),
    "Dragon Road Day Act 4": DarkGaiaStageData(
        archive="+#ActD_SubChina_01",
        completion_sets=("Download.set.xml",),
    ),
    "Dragon Road Day Act 5": DarkGaiaStageData(
        archive="+#ActD_SubChina_02",
        completion_sets=("Rap04.set.xml",),
    ),
    "Skyscraper Scamper Day Act 3": DarkGaiaStageData(
        archive="+#ActD_SubNY_02",
        completion_sets=("area03_gimmickset.set.xml",),
    ),
    "Jungle Joyride Day Act 4": DarkGaiaStageData(
        archive="+#ActD_SubBeach_01",
        completion_sets=("DLC.set.xml",),
    ),
    "Jungle Joyride Day Act 5": DarkGaiaStageData(
        archive="+#ActD_SubBeach_03",
        completion_sets=("DLC.set.xml",),
    ),
    "Windmill Isle Day Act 1-2": DarkGaiaStageData(
        archive="+#ActD_SubMykonos_04",
        completion_sets=("Download03.set.xml",),
    ),
    "Savannah Citadel Day Act 1-2": DarkGaiaStageData(
        archive="+#ActD_SubAfrica_05",
        completion_sets=("Base.set.xml",),
    ),
    "Savannah Citadel Day Act 3-2": DarkGaiaStageData(
        archive="+#ActD_SubAfrica_06",
        completion_sets=("Base.set.xml",),
    ),
    "Rooftop Run Day Act 2-2": DarkGaiaStageData(
        archive="+#ActD_SubEU_06",
        completion_sets=("0301.set.xml",),
    ),
    "Dragon Road Day Act 1-2": DarkGaiaStageData(
        archive="+#ActD_SubChina_05",
        completion_sets=("DLC.set.xml",),
    ),
    "Dragon Road Day Act 2-2": DarkGaiaStageData(
        archive="+#ActD_SubChina_06",
        completion_sets=("Rap0502.set.xml",),
    ),
    "Arid Sands Day Act 1-2": DarkGaiaStageData(
        archive="+#ActD_SubPetra_04",
        completion_sets=("Mainbase.set.xml",),
    ),
    "Skyscraper Scamper Day Act 1-2": DarkGaiaStageData(
        archive="+#ActD_SubNY_03",
        completion_sets=("Base.set.xml",),
    ),
    "Jungle Joyride Day Act 1-2": DarkGaiaStageData(
        archive="+#ActD_SubBeach_05",
        completion_sets=("Base.set.xml",),
    ),
    "Savannah Citadel Day Act 5": DarkGaiaStageData(
        archive="+#ActD_SubAfrica_04",
        completion_sets=("rap04.set.xml",),
    ),
    # Main night stages
    "Windmill Isle Night Act 1": DarkGaiaStageData(
        archive="+#ActN_MykonosEvil",
        completion_sets=("area23_gimmickset.set.xml",),
    ),
    "Savannah Citadel Night Act 1": DarkGaiaStageData(
        archive="+#ActN_AfricaEvil",
        completion_sets=("system.set.xml",),
    ),
    "Rooftop Run Night Act 1": DarkGaiaStageData(
        archive="+#ActN_EUEvil",
        completion_sets=("area17_gimmickset.set.xml",),
    ),
    "Dragon Road Night Act 1": DarkGaiaStageData(
        archive="+#ActN_ChinaEvil",
        completion_sets=(
            "area11_gimmickset.set.xml",
            "area20_gimmickset.set.xml",
        ),
    ),
    "Cool Edge Night Act 1": DarkGaiaStageData(
        archive="+#ActN_SnowEvil",
        completion_sets=("system.set.xml",),
    ),
    "Skyscraper Scamper Night Act 1": DarkGaiaStageData(
        archive="+#ActN_NYEvil",
        completion_sets=("area10_gimmickset.set.xml",),
    ),
    "Jungle Joyride Night Act 1": DarkGaiaStageData(
        archive="+#ActN_BeachEvil",
        completion_sets=(
            "area06_gimmickset.set.xml",
            "area08_gimmickset.set.xml",
        ),
    ),
    "Arid Sands Night Act 1": DarkGaiaStageData(
        archive="+#ActN_PetraEvil",
        completion_sets=(
            "Set.set.xml",
            "system.set.xml",
        ),
    ),
    # Savannah Citadel
    "Savannah Citadel Night Act 2": DarkGaiaStageData(
        archive="+#ActN_SubAfrica_01",
        completion_sets=("area01_gimmickset.set.xml",),
    ),
    "Savannah Citadel Night Act 3": DarkGaiaStageData(
        archive="+#ActN_SubAfrica_02",
        completion_sets=("Area04_Gimmickset.set.xml",),
    ),
    "Savannah Citadel Night Act 4": DarkGaiaStageData(
        archive="+#ActN_SubAfrica_03",
        completion_sets=("area05_gimmickset.set.xml",),
    ),
    # Rooftop Run
    "Rooftop Run Night Act 2": DarkGaiaStageData(
        archive="+#ActN_SubEU_01",
        completion_sets=("system.set.xml",),
    ),
    # Dragon Road
    "Dragon Road Night Act 2": DarkGaiaStageData(
        archive="+#ActN_SubChina_01",
        completion_sets=("area01_gimmickset.set.xml",),
    ),
    "Dragon Road Night Act 3": DarkGaiaStageData(
        archive="+#ActN_SubChina_02",
        completion_sets=("system.set.xml",),
    ),
    "Dragon Road Night Act 1-2": DarkGaiaStageData(
        archive="+#ActN_SubChina_03",
        completion_sets=("area25_enemyset.set.xml",),
    ),
    # Windmill Isle
    "Windmill Isle Night Act 2": DarkGaiaStageData(
        archive="+#ActN_SubMykonos_01",
        completion_sets=("area02_gimmickset.set.xml",),
    ),
    "Windmill Isle Night Act 1-2": DarkGaiaStageData(
        archive="+#ActN_SubMykonos_03",
        completion_sets=("area13_gimmickset.set.xml",),
    ),
    # Arid Sands
    "Arid Sands Night Act 2": DarkGaiaStageData(
        archive="+#ActN_SubPetra_02",
        completion_sets=("area05_gimmickset.set.xml",),
    ),
    "Arid Sands Night Act 3": DarkGaiaStageData(
        archive="+#ActN_SubPetra_03",
        completion_sets=("area23_enemyset.set.xml",),
    ),
    # Jungle Joyride
    "Jungle Joyride Night Act 2": DarkGaiaStageData(
        archive="+#ActN_SubBeach_01",
        completion_sets=("area04_gimmickset.set.xml",),
    ),
    "Jungle Joyride Night Act 1-2": DarkGaiaStageData(
        archive="+#ActN_SubBeach_03",
        completion_sets=("area07_gimmickset.set.xml",),
    ),
    "Jungle Joyride Night Act 3": DarkGaiaStageData(
        archive="+#ActN_SubBeach_02",
        completion_sets=("system.set.xml",),
    ),
}
