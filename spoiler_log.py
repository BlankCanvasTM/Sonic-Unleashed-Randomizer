from datetime import datetime
from pathlib import Path

from medal_validator import (
    AccessibilityValidationResult,
    StageAssignment,
)

from data import Stage

def get_stage_category(stage_type: Stage) -> str:

    if stage_type in {
        Stage.DAY_MAIN,
        Stage.NIGHT_MAIN,
    }:
        return "MAIN"

    if stage_type in {
        Stage.DAY_SIDE,
        Stage.NIGHT_SIDE,
    }:
        return "SIDE"

    if stage_type in {
        Stage.DAY_DLC,
        Stage.NIGHT_DLC,
    }:
        return "DLC"

    if stage_type in {
        Stage.DAY_BOSS,
        Stage.NIGHT_BOSS,
    }:
        return "BOSS"

    if stage_type in {
        Stage.DAY_TUT,
        Stage.NIGHT_TUT,
    }:
        return "TUTORIAL"

    return "UNKNOWN"


def create_spoiler_log_lines(
    seed_code: str,
    assignments: list[StageAssignment],
    validation_result: AccessibilityValidationResult,
    include_dlc: bool,
    fixed_levels: set,
) -> list[str]:

    lines: list[str] = []

    lines.append("SONIC UNLEASHED RANDOMISER - SPOILER LOG")
    lines.append("=" * 70)
    lines.append(
        f"Generated: "
        f"{datetime.now().strftime('%d %B %Y at %H:%M:%S')}"
    )
    lines.append(f"Seed Code: {seed_code}")
    lines.append("")

    lines.append("RANDOMISATION SETTINGS")
    lines.append("-" * 70)
    lines.append(
    f"DLC stages included: {'Yes' if include_dlc else 'No'}"
    )
    lines.append("Boss and regular stage swaps: Yes")
    lines.append("All shoe upgrades available from start: Yes")
    lines.append("Medal progression validation: Yes")
    lines.append("")

    lines.append("")

    lines.append("HOW TO READ THIS LOG")
    lines.append("-" * 70)
    lines.append(
        "The entrance on the left is the location selected on the world map."
    )
    lines.append(
        "The stage on the right is what will actually be played there."
    )
    lines.append("")

    lines.append("STAGE ASSIGNMENTS")
    lines.append("-" * 70)

    if include_dlc:
        lines.append("FIXED DLC STAGES")
        lines.append("-" * 70)

        for assignment in assignments:
            if (
                assignment.entrance in fixed_levels
                and assignment.entrance.type in {
                    Stage.DAY_DLC,
                    Stage.NIGHT_DLC,
                }
            ):
                lines.append(
                    f"[DLC     ] "
                    f"{assignment.entrance.name:<40} "
                    f"-> "
                    f"[DLC     ] "
                    f"{assignment.stage.name}"
                )

        lines.append("")
        
            

    lines.append("")
    lines.append("FIXED BOSSES")
    lines.append("-" * 70)

    for assignment in assignments:
        if (
            assignment.entrance in fixed_levels
            and assignment.entrance.type in {
                Stage.DAY_BOSS,
                Stage.NIGHT_BOSS,
            }
        ):
            lines.append(
                f"[BOSS    ] "
                f"{assignment.entrance.name:<40} "
                f"-> "
                f"[BOSS    ] "
                f"{assignment.stage.name}"
            )

    lines.append("")
    lines.append("RANDOMISED STAGES")
    lines.append("-" * 70)

    for assignment in assignments:

        if assignment.entrance in fixed_levels:
            continue

        entrance_category = get_stage_category(
            assignment.entrance.type
        )

        stage_category = get_stage_category(
            assignment.stage.type
        )

        lines.append(
            f"[{entrance_category:<8}] "
            f"{assignment.entrance.name:<40} "
            f"-> "
            f"[{stage_category:<8}] "
            f"{assignment.stage.name}"
        )


    """lines.append("")
    lines.append("DLC ENTRANCES TO TEST")
    lines.append("-" * 70)


    for assignment in assignments:
    
                if assignment.entrance.type not in {
                    Stage.DAY_DLC,
                    Stage.NIGHT_DLC,
                }:
                    continue
    
                stage_category = get_stage_category(
                    assignment.stage.type
                )
    
                lines.append(
                    f"{assignment.entrance.name:<40} "
                    f"-> "
                    f"[{stage_category:<8}] "
                    f"{assignment.stage.name}"
                )"""
    
    
    return lines


def write_spoiler_log(
    seed_code: str,
    assignments: list[StageAssignment],
    validation_result: AccessibilityValidationResult,
    output_path: str | Path,
    include_dlc: bool,
    fixed_levels: set,
) -> Path:
    """
    Creates and writes the spoiler log.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    lines = create_spoiler_log_lines(
    seed_code=seed_code,
    assignments=assignments,
    validation_result=validation_result,
    include_dlc=include_dlc,
    fixed_levels=fixed_levels,
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output_path