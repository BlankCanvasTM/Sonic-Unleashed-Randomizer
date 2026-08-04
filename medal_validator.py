from dataclasses import dataclass

from data import Level, Stage

@dataclass

class StageAssignment:
    entrance: Level
    stage: Level


@dataclass
class BlockedEntrance:
    entrance_name: str
    medal_type: str | None
    required_medals: int
    available_medals: int
    parent_name: str | None
    parent_completed: bool


@dataclass
class AccessibilityValidationResult:
    valid: bool
    final_sun_medals: int
    final_moon_medals: int
    completed_entrances: int
    total_entrances: int
    blocked_entrances: list[BlockedEntrance]

def get_required_medal_type(entrance: Level) -> str | None:

    if entrance.required_medal <= 0:
        return None

    if entrance.type in {
        Stage.DAY_TUT,
        Stage.DAY_MAIN,
        Stage.DAY_SIDE,
        Stage.DAY_DLC,
        Stage.DAY_BOSS
    }:
        return "sun"

    if entrance.type in {
            Stage.NIGHT_TUT,
            Stage.NIGHT_MAIN,
            Stage.NIGHT_SIDE,
            Stage.NIGHT_DLC,
            Stage.NIGHT_BOSS
        }:
            return "moon"

    raise ValueError(
         f"Could not determine medal type for entrance: {entrance.name}"
    )


def validate_accessible_progression(
    assignments: list[StageAssignment],
    print_progress: bool = False,
) -> AccessibilityValidationResult:


    current_sun = 0
    current_moon = 0

    completed: set[Level] = set()

    #round_number = 0

    while True:
        #round_number += 1
        playable: list[StageAssignment] = []

        for assignment in assignments:
            entrance = assignment.entrance

            if entrance in completed:
                continue

            parent_completed = (
                entrance.parent is None
                or entrance.parent in completed
            )

            if not parent_completed:
                continue

            medal_type = get_required_medal_type(entrance)
            required_medals = entrance.required_medal

            if medal_type == "sun":
                if current_sun < required_medals:
                    continue

            if medal_type == "moon":
                if current_moon < required_medals:
                    continue

            playable.append(assignment)

        if not playable:
            break

        """
        if print_progress:
            print()
            print("=" * 60)
            print(f"ROUND {round_number}")
            print("=" * 60)
            print(
                f"Medals before round: "
                f"{current_sun} Sun, {current_moon} Moon"
            )
            print(f"Playable entrances: {len(playable)}")
            """

        for assignment in playable:
            entrance = assignment.entrance
            stage = assignment.stage

            completed.add(entrance)

            current_sun += stage.sun
            current_moon += stage.moon

            """
            if print_progress:
                print()
                print(f"Completed entrance: {entrance.name}")
                print(f"Randomised stage: {stage.name}")
                print(
                    f"Stage medals: "
                    f"{stage.sun} Sun, {stage.moon} Moon"
                )
                print(
                    f"New total: "
                    f"{current_sun} Sun, {current_moon} Moon"
                )
                """

    blocked_entrances: list[BlockedEntrance] = []

    for assignment in assignments:
        entrance = assignment.entrance

        if entrance in completed:
            continue

        parent_completed = (
            entrance.parent is None
            or entrance.parent in completed
        )

        medal_type = get_required_medal_type(entrance)

        if medal_type == "sun":
            available_medals = current_sun
        elif medal_type == "moon":
            available_medals = current_moon
        else:
            available_medals = 0

        blocked_entrances.append(
            BlockedEntrance(
                entrance_name=entrance.name,
                medal_type=medal_type,
                required_medals=entrance.required_medal,
                available_medals=available_medals,
                parent_name=(
                    entrance.parent.name
                    if entrance.parent is not None
                    else None
                ),
                parent_completed=parent_completed,
            )
        )

    valid = len(completed) == len(assignments)

    """
    if print_progress:
        print()
        print("=" * 60)

        if valid:
            print("ACCESSIBILITY PROGRESSION IS VALID")
        else:
            print("ACCESSIBILITY PROGRESSION IS INVALID")
            print(
                f"Completed {len(completed)} of "
                f"{len(assignments)} entrances."
            )

            print()
            print("Blocked entrances:")

            for blocked in blocked_entrances:
                print()
                print(blocked.entrance_name)

                if not blocked.parent_completed:
                    print(
                        f"  Parent incomplete: "
                        f"{blocked.parent_name}"
                    )
                elif blocked.medal_type is not None:
                    print(
                        f"  Requires {blocked.required_medals} "
                        f"{blocked.medal_type.title()} Medals"
                    )
                    print(
                        f"  Available: "
                        f"{blocked.available_medals}"
                    )
                    """

    return AccessibilityValidationResult(
        valid=valid,
        final_sun_medals=current_sun,
        final_moon_medals=current_moon,
        completed_entrances=len(completed),
        total_entrances=len(assignments),
        blocked_entrances=blocked_entrances,
    )

    