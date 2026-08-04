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


def is_dlc(level: Level) -> bool:
    return level.type in DLC_STAGE_TYPES

def get_non_dlc_levels(level_state: LevelState) -> list[Level]:
    return [
        level
        for level in level_state.levels
        if not is_dlc(level)
    ]

def get_no_upgrade_levels(
    levels: list[Level],
) -> list[Level]:
    return [
        level
        for level in levels
        if not level.req_shoe
    ]

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
        if stage in stage_set
        and stage not in fixed_levels
    ]

    if not usable_first_stage_pool:
        raise ValueError(
            "The first-stage pool contains no usable stages."
        )

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
        stage
        for stage in randomisable_stages
        if stage not in fixed_levels
    ]

    chosen_first_stage = rng.choice(
        usable_first_stage_pool
    )

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
        if entrance not in fixed_levels
        and entrance is not first_entrance
    ]

    if len(remaining_entrances) != len(available_stages):
        raise ValueError(
            "The remaining entrance and stage counts do not match. "
            f"Entrances: {len(remaining_entrances)}, "
            f"stages: {len(available_stages)}"
        )

    rng.shuffle(available_stages)

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
        "Could not generate a valid assignment set after "
        f"{max_attempts} attempts."
    )




