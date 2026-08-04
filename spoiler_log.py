from datetime import datetime
from pathlib import Path

from medal_validator import (
    AccessibilityValidationResult,
    StageAssignment,
)


def create_spoiler_log_lines(
    seed_code: str,
    assignments: list[StageAssignment],
    validation_result: AccessibilityValidationResult,
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
    lines.append("DLC stages included: No")
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

    for assignment in assignments:
        lines.append(
            f"{assignment.entrance.name:<40} "
            f"-> {assignment.stage.name}"
        )

    return lines


def write_spoiler_log(
    seed_code: str,
    assignments: list[StageAssignment],
    validation_result: AccessibilityValidationResult,
    output_path: str | Path,
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
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output_path