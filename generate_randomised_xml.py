from pathlib import Path

from assignment_generator import (
    generate_valid_randomiser_assignments,
    get_no_upgrade_levels,
    get_non_dlc_levels,
)
from data import LevelState
from medal_validator import validate_accessible_progression
from xml_writer import write_xml_assignments


def main() -> None:
    level_state = LevelState()

    participating_levels = get_non_dlc_levels(
        level_state
    )

    first_stage_pool = get_no_upgrade_levels(
        participating_levels
    )

    assignments, result = generate_valid_randomiser_assignments(
        entrances=participating_levels,
        randomisable_stages=participating_levels,
        first_entrance=level_state.WID1,
        first_stage_pool=first_stage_pool,
        fixed_levels=set(),
        max_attempts=10_000,
        print_attempts=True,
    )

    print()
    print("=" * 70)
    print("VALID RANDOMISATION FOUND")
    print("=" * 70)

    for assignment in assignments:
        print(
            f"{assignment.entrance.name:<40} "
            f"-> {assignment.stage.name}"
        )

    print()
    print("=" * 70)
    print("FINAL ACCESSIBILITY CHECK")
    print("=" * 70)

    final_result = validate_accessible_progression(
        assignments,
        print_progress=True,
    )

    if not final_result.valid:
        raise RuntimeError(
            "The generated assignments failed final validation."
        )

    print()
    print("=" * 70)
    print("WRITING XML ASSIGNMENTS")
    print("=" * 70)

    write_xml_assignments(
        assignments=assignments,
        source_directory=Path("Stages"),
        output_directory=Path("#Application"),
        create_backup=True,
        print_progress=True,
    )

    print()
    print("=" * 70)
    print("RANDOMISED XML FILES READY")
    print("=" * 70)
    print(
        f"Completed entrances: "
        f"{final_result.completed_entrances}/"
        f"{final_result.total_entrances}"
    )
    print(
        f"Maximum obtainable medals: "
        f"{final_result.final_sun_medals} Sun, "
        f"{final_result.final_moon_medals} Moon"
    )
    print()
    print("#Application is ready to pack.")


if __name__ == "__main__":
    main()