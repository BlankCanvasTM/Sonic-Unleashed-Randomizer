from data import LevelState
from medal_validator import (
    StageAssignment,
    validate_accessible_progression,
)


level_state = LevelState()

assignments = [
    StageAssignment(
        entrance=level_state.WID1,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.WID2,
        stage=level_state.WID2,
    ),
    StageAssignment(
        entrance=level_state.WIN1,
        stage=level_state.SCN1,
    ),
    StageAssignment(
        entrance=level_state.SCN1,
        stage=level_state.SCD1,
    ),
    StageAssignment(
        entrance=level_state.SCD1,
        stage=level_state.WIN1,
    ),
    StageAssignment(
        entrance=level_state.BOSS_EGG_BEETLE,
        stage=level_state.BOSS_EGG_BEETLE,
    ),
    StageAssignment(
        entrance=level_state.RRN1,
        stage=level_state.RRN1,
    ),
    StageAssignment(
        entrance=level_state.WID3,
        stage=level_state.WID3,
    ),
]

result = validate_accessible_progression(
    assignments,
    print_progress=True,
)

print()
print("=" * 60)
print(f"Valid: {result.valid}")
print(
    f"Completed: "
    f"{result.completed_entrances}/"
    f"{result.total_entrances}"
)
print(f"Final Sun Medals: {result.final_sun_medals}")
print(f"Final Moon Medals: {result.final_moon_medals}")