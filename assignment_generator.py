import random

from data import Level, LevelState, Stage
from medal_validator import (
    AccessibilityValidationResult,
    StageAssignment,
    validate_accessible_progression,
)

DLC_STAGE_TYPES = {
    Stage.DAY_DLC,
    Stage.NIGHT_DLC,
}

FORBIDDEN_STAGE_ENTRANCE_PAIRS = {
    ("Egg Beetle", "Tornado Defense Act 1"),
    ("Egg Beetle", "Tornado Defense Act 2"),
    ("Windmill Isle Night Act 1", "Tornado Defense Act 1"),
    ("Windmill Isle Night Act 1", "Tornado Defense Act 2"),
}

DARK_GAIA_EXCLUDED_STAGE_TYPES = {
    Stage.DAY_BOSS,
    Stage.NIGHT_BOSS,
    Stage.DAY_DLC,
    Stage.NIGHT_DLC,
}

DARK_GAIA_EXCLUDED_STAGE_NAMES = {
    # Special stages
    "Tornado Defense Act 1",
    "Tornado Defense Act 2",
    "Rooftop Run Day Act 3",  # Chao stage
    "Eggmanland",
    # Confirmed incompatible Dark Gaia destinations
    "Arid Sands Night Act 1",
    "Cool Edge Day Act 2",
    "Dragon Road Night Act 2",
    "Skyscraper Scamper Day Act 2",
    # Currently broken day DLC stages
    "Rooftop Run Day Act 4",
    "Rooftop Run Day Act 5",
    "Cool Edge Day Act 3",
    "Cool Edge Day Act 4",
    "Arid Sands Day Act 3",
    "Windmill Isle Day Act 2-2",
    "Rooftop Run Day Act 1-2",
    "Cool Edge Day Act 1-2",
    "Cool Edge Day Act 2-2",
    # Broken night DLC stages
    "Cool Edge Night Act 2",
    "Cool Edge Night Act 3",
    "Skyscraper Scamper Night Act 2",
    "Windmill Isle Night Act 1-3",
    "Rooftop Run Night Act 1-2",
    "Skyscraper Scamper Night Act 3",
}


def get_dark_gaia_stage_pool(
    levels: list[Level],
) -> list[Level]:
    return [
        level
        for level in levels
        if level.type not in DARK_GAIA_EXCLUDED_STAGE_TYPES
        and level.name not in DARK_GAIA_EXCLUDED_STAGE_NAMES
    ]


def has_forbidden_assignment(
    assignments: list[StageAssignment],
) -> bool:
    return any(
        (assignment.entrance.name, assignment.stage.name)
        in FORBIDDEN_STAGE_ENTRANCE_PAIRS
        for assignment in assignments
    )


def is_dlc(level: Level) -> bool:
    return level.type in DLC_STAGE_TYPES


def get_non_dlc_levels(level_state: LevelState) -> list[Level]:
    return [level for level in level_state.levels if not is_dlc(level)]


def get_no_upgrade_levels(
    levels: list[Level],
) -> list[Level]:
    return [level for level in levels if not level.req_shoe]


def build_randomiser_assignments(
    entrances: list[Level],
    randomisable_stages: list[Level],
    first_entrance: Level,
    first_stage_pool: list[Level],
    fixed_levels: set[Level] | None = None,
    rng: random.Random | None = None,
) -> list[StageAssignment]:

    if rng is None:
        rng = random.Random()

    if fixed_levels is None:
        fixed_levels = set()

    entrance_set = set(entrances)
    stage_set = set(randomisable_stages)

    if first_entrance not in entrance_set:
        raise ValueError(
            f"First entrance is not present in the entrance list: "
            f"{first_entrance.name}"
        )

    for fixed_level in fixed_levels:
        if fixed_level not in entrance_set:
            raise ValueError(
                f"Fixed level is not present in the entrance list: "
                f"{fixed_level.name}"
            )

    usable_first_stage_pool = [
        stage
        for stage in first_stage_pool
        if stage in stage_set and stage not in fixed_levels
    ]

    if not usable_first_stage_pool:
        raise ValueError("The first-stage pool contains no usable stages.")

    assignments: list[StageAssignment] = []

    # Fixed entrances remain unchanged.
    for fixed_level in fixed_levels:
        assignments.append(
            StageAssignment(
                entrance=fixed_level,
                stage=fixed_level,
            )
        )

    available_stages = [
        stage for stage in randomisable_stages if stage not in fixed_levels
    ]

    chosen_first_stage = rng.choice(usable_first_stage_pool)

    assignments.append(
        StageAssignment(
            entrance=first_entrance,
            stage=chosen_first_stage,
        )
    )

    available_stages.remove(chosen_first_stage)

    remaining_entrances = [
        entrance
        for entrance in entrances
        if entrance not in fixed_levels and entrance is not first_entrance
    ]

    if len(remaining_entrances) != len(available_stages):
        raise ValueError(
            "The remaining entrance and stage counts do not match. "
            f"Entrances: {len(remaining_entrances)}, "
            f"stages: {len(available_stages)}"
        )

    rng.shuffle(available_stages)

    dark_gaia_entrance_indices = [
        index
        for index, entrance in enumerate(remaining_entrances)
        if entrance.type == Stage.DARK_GAIA_RUN
    ]

    dark_gaia_stage_pool = set(get_dark_gaia_stage_pool(available_stages))

    for dark_gaia_entrance_index in dark_gaia_entrance_indices:
        assigned_dark_gaia_stage = available_stages[dark_gaia_entrance_index]

        assigned_stage_is_valid = assigned_dark_gaia_stage in dark_gaia_stage_pool and (
            assigned_dark_gaia_stage.type != Stage.DARK_GAIA_RUN
            or assigned_dark_gaia_stage is remaining_entrances[dark_gaia_entrance_index]
        )

        if assigned_stage_is_valid:
            continue

        protected_indices = set(dark_gaia_entrance_indices)

        valid_swap_indices = [
            index
            for index, stage in enumerate(available_stages)
            if (
                index not in protected_indices
                and stage in dark_gaia_stage_pool
                and stage.type != Stage.DARK_GAIA_RUN
            )
        ]

        if not valid_swap_indices:
            raise RuntimeError("No valid stage is available for a Dark Gaia run.")

        swap_index = rng.choice(valid_swap_indices)

        (
            available_stages[dark_gaia_entrance_index],
            available_stages[swap_index],
        ) = (
            available_stages[swap_index],
            available_stages[dark_gaia_entrance_index],
        )

    for entrance, stage in zip(
        remaining_entrances,
        available_stages,
    ):

        assignments.append(
            StageAssignment(
                entrance=entrance,
                stage=stage,
            )
        )

    return assignments


def generate_valid_randomiser_assignments(
    entrances: list[Level],
    randomisable_stages: list[Level],
    first_entrance: Level,
    first_stage_pool: list[Level],
    seed: int,
    fixed_levels: set[Level] | None = None,
    max_attempts: int = 10_000,
    print_attempts: bool = False,
) -> tuple[
    list[StageAssignment],
    AccessibilityValidationResult,
]:

    rng = random.Random(seed)

    for attempt in range(1, max_attempts + 1):
        assignments = build_randomiser_assignments(
            entrances=entrances,
            randomisable_stages=randomisable_stages,
            first_entrance=first_entrance,
            first_stage_pool=first_stage_pool,
            fixed_levels=fixed_levels,
            rng=rng,
        )

        if has_forbidden_assignment(assignments):
            if print_attempts:
                print(f"Attempt {attempt}: invalid (forbidden stage/entrance pairing)")
            continue

        result = validate_accessible_progression(
            assignments,
            print_progress=False,
        )

        if print_attempts:
            if result.valid:
                print(f"Attempt {attempt}: valid")
            else:
                print(
                    f"Attempt {attempt}: invalid "
                    f"({result.completed_entrances}/"
                    f"{result.total_entrances} completed)"
                )

        if result.valid:
            return assignments, result

    raise RuntimeError(
        "Could not generate a valid assignment set after " f"{max_attempts} attempts."
    )
