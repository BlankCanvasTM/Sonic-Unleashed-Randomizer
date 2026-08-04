from dataclasses import dataclass
from pathlib import Path
import shutil

from medal_validator import StageAssignment


@dataclass
class XMLWriteResult:
    entrance_name: str
    stage_name: str
    source_path: Path
    destination_path: Path


def resolve_level_file(
    level_file: str | Path,
    directory: Path,
) -> Path:

    return directory / Path(level_file).name


def validate_assignment_files(
    assignments: list[StageAssignment],
    source_directory: Path,
) -> None:
    missing_files: list[Path] = []

    for assignment in assignments:
        source_path = resolve_level_file(
            assignment.stage.file,
            source_directory,
        )

        if not source_path.is_file():
            missing_files.append(source_path)

    if missing_files:
        missing_text = "\n".join(
            f"  {path}"
            for path in missing_files
        )

        raise FileNotFoundError(
            "The following clean source XML files are missing:\n"
            f"{missing_text}"
        )


def write_xml_assignments(
    assignments: list[StageAssignment],
    source_directory: str | Path,
    output_directory: str | Path,
    create_backup: bool = True,
    print_progress: bool = True,
) -> list[XMLWriteResult]:

    source_directory = Path(source_directory)
    output_directory = Path(output_directory)

    if not source_directory.is_dir():
        raise FileNotFoundError(
            f"Source XML directory does not exist: "
            f"{source_directory}"
        )

    if not output_directory.is_dir():
        raise FileNotFoundError(
            f"Output XML directory does not exist: "
            f"{output_directory}"
        )

    validate_assignment_files(
        assignments,
        source_directory,
    )

    # Read all clean source XMLs before writing anything.
    source_contents: dict[Path, bytes] = {}

    for assignment in assignments:
        source_path = resolve_level_file(
            assignment.stage.file,
            source_directory,
        )

        if source_path not in source_contents:
            source_contents[source_path] = source_path.read_bytes()

    results: list[XMLWriteResult] = []

    for assignment in assignments:
        source_path = resolve_level_file(
            assignment.stage.file,
            source_directory,
        )

        destination_path = resolve_level_file(
            assignment.entrance.file,
            output_directory,
        )

        if not destination_path.exists():
            raise FileNotFoundError(
                f"Destination entrance XML is missing: "
                f"{destination_path}"
            )

        if create_backup:
            backup_path = destination_path.with_suffix(
                destination_path.suffix + ".backup"
            )

            if not backup_path.exists():
                shutil.copy2(
                    destination_path,
                    backup_path,
                )

        destination_path.write_bytes(
            source_contents[source_path]
        )

        result = XMLWriteResult(
            entrance_name=assignment.entrance.name,
            stage_name=assignment.stage.name,
            source_path=source_path,
            destination_path=destination_path,
        )

        results.append(result)

        if print_progress:
            print(
                f"{assignment.entrance.name:<40} "
                f"-> {assignment.stage.name}"
            )
            print(
                f"  {source_path.name} "
                f"-> {destination_path.name}"
            )

    return results