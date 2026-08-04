from assignment_generator import (
    generate_valid_randomiser_assignments,
    get_no_upgrade_levels,
    get_non_dlc_levels,
)
from data import LevelState
from medal_validator import validate_accessible_progression

from assignment_generator import assignments_to_file_mapping


level_state = LevelState()

participating_levels = get_non_dlc_levels(level_state)

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
print("VALID ASSIGNMENT SET")
print("=" * 70)

for assignment in assignments:
    print(
        f"{assignment.entrance.name:<40} "
        f"-> {assignment.stage.name}"
    )


print()
print("=" * 70)
print("ACCESSIBILITY SIMULATION")
print("=" * 70)

final_result = validate_accessible_progression(
    assignments,
    print_progress=True,
)


print()
print("=" * 70)
print(f"Valid: {final_result.valid}")
print(
    f"Completed entrances: "
    f"{final_result.completed_entrances}/"
    f"{final_result.total_entrances}"
)
print(f"Final Sun Medals: {final_result.final_sun_medals}")
print(f"Final Moon Medals: {final_result.final_moon_medals}")





file_mapping = assignments_to_file_mapping(assignments)

print()
print("=" * 70)
print("XML FILE MAPPING")
print("=" * 70)

for entrance_file, stage_file in file_mapping.items():
    print(
        f"{entrance_file.name:<45} "
        f"-> {stage_file.name}"
    )