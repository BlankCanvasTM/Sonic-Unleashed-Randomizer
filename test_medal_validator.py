from data import LevelState
from medal_validator import StageAssignment, validate_medal_progression


level_state = LevelState()


assignments = [
    StageAssignment(
        entrance=level_state.WID1,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.WID2,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.WIN1,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.SCN1,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.SCD1,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.BOSS_EGG_BEETLE,
        stage=level_state.WID1,
    ),
    StageAssignment(
        entrance=level_state.RRN1,
        stage=level_state.RRN1,
    ),
]


result = validate_medal_progression(
    assignments,
    print_progress=True,
)

print()
print("=" * 50)

if result.valid:
    print("The medal progression is valid.")
    print(f"Final Sun Medals: {result.final_sun_medals}")
    print(f"Final Moon Medals: {result.final_moon_medals}")
else:
    print("The medal progression is invalid.")

    failure = result.failure

    if failure is not None:
        print(f"Blocked entrance: {failure.entrance_name}")
        print(f"Medal type: {failure.medal_type}")
        print(f"Required: {failure.required_medals}")
        print(f"Available: {failure.available_medals}")