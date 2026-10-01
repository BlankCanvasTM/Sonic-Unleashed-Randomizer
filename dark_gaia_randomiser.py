from pathlib import Path
import xml.etree.ElementTree as ET
import shutil

from dark_gaia_data import DARK_GAIA_STAGE_DATA

DARK_GAIA_RUN_1_NAME = "Dark Gaia Run 1"
DARK_GAIA_RUN_1_RETURN_EVENT = "DarkGaiaReturnRun1"

DARK_GAIA_RUN_2_NAME = "Dark Gaia Run 2"
DARK_GAIA_RUN_2_RETURN_EVENT = "DarkGaiaReturnRun2"

DARK_GAIA_RUN_3_NAME = "Dark Gaia Run 3"
DARK_GAIA_RUN_3_RETURN_EVENT = "DarkGaiaReturnRun3"


def find_dark_gaia_run_1_assignment(assignments):
    for assignment in assignments:
        if assignment.entrance.name == DARK_GAIA_RUN_1_NAME:
            return assignment

    raise RuntimeError("Could not find the Dark Gaia Run 1 assignment.")


def find_dark_gaia_run_2_assignment(assignments):
    for assignment in assignments:
        if assignment.entrance.name == DARK_GAIA_RUN_2_NAME:
            return assignment

    raise RuntimeError("Could not find the Dark Gaia Run 2 assignment.")


def find_dark_gaia_run_3_assignment(assignments):
    for assignment in assignments:
        if assignment.entrance.name == DARK_GAIA_RUN_3_NAME:
            return assignment

    raise RuntimeError("Could not find the Dark Gaia Run 3 assignment.")


def create_return_collision(
    goal_ring: ET.Element,
    return_event: str,
) -> ET.Element:
    position = goal_ring.find("Position")
    rotation = goal_ring.find("Rotation")

    if position is None:
        raise RuntimeError("GoalRing does not contain a Position.")

    collision = ET.Element("SequenceChangeCollision")

    ET.SubElement(
        collision,
        "Collision_Height",
    ).text = "10"

    ET.SubElement(
        collision,
        "Collision_Length",
    ).text = "10"

    ET.SubElement(
        collision,
        "Collision_Width",
    ).text = "10"

    ET.SubElement(
        collision,
        "DefaultStatus",
    ).text = "0"

    ET.SubElement(
        collision,
        "Event",
    ).text = return_event

    ET.SubElement(
        collision,
        "GroundOffset",
    ).text = "0"

    collision.append(
        ET.fromstring(
            ET.tostring(
                position,
                encoding="unicode",
            )
        )
    )

    if rotation is not None:
        collision.append(
            ET.fromstring(
                ET.tostring(
                    rotation,
                    encoding="unicode",
                )
            )
        )
    else:
        rotation_element = ET.SubElement(
            collision,
            "Rotation",
        )

        ET.SubElement(rotation_element, "w").text = "1"
        ET.SubElement(rotation_element, "x").text = "0"
        ET.SubElement(rotation_element, "y").text = "0"
        ET.SubElement(rotation_element, "z").text = "0"

    ET.SubElement(
        collision,
        "SetObjectID",
    ).text = "900001"

    ET.SubElement(
        collision,
        "Shape_Type",
    ).text = "0"

    ET.SubElement(
        collision,
        "Type",
    ).text = "0"

    return collision


def replace_goal_ring_with_return_collision(
    set_file: Path,
    return_event: str,
) -> None:

    if not set_file.is_file():
        raise FileNotFoundError(
            f"Dark Gaia completion SET file does not exist: {set_file}"
        )

    tree = ET.parse(set_file)
    root = tree.getroot()

    goal_rings = root.findall("GoalRing")

    if not goal_rings:
        raise RuntimeError(f"No GoalRing found in {set_file}")

    for goal_ring in goal_rings:
        children = list(root)
        goal_index = children.index(goal_ring)

        return_collision = create_return_collision(
            goal_ring,
            return_event,
        )

        root.remove(goal_ring)
        root.insert(
            goal_index,
            return_collision,
        )

    ET.indent(
        tree,
        space="  ",
    )

    tree.write(
        set_file,
        encoding="utf-8",
        xml_declaration=True,
    )


def restore_goal_rings_from_clean_set(
    working_set_file: Path,
    clean_set_file: Path,
) -> int:

    if not working_set_file.is_file():
        return 0

    if not clean_set_file.is_file():
        raise FileNotFoundError(
            "Clean Dark Gaia completion SET file does not exist: " f"{clean_set_file}"
        )

    working_tree = ET.parse(working_set_file)
    working_root = working_tree.getroot()

    clean_tree = ET.parse(clean_set_file)
    clean_root = clean_tree.getroot()

    return_collisions = [
        collision
        for collision in working_root.findall("SequenceChangeCollision")
        if collision.findtext("Event")
        in {
            DARK_GAIA_RUN_1_RETURN_EVENT,
            DARK_GAIA_RUN_2_RETURN_EVENT,
            DARK_GAIA_RUN_3_RETURN_EVENT,
        }
    ]

    if not return_collisions:
        return 0

    clean_goal_rings = clean_root.findall("GoalRing")

    if len(clean_goal_rings) != len(return_collisions):
        raise RuntimeError(
            "Dark Gaia reset could not safely restore GoalRings in "
            f"{working_set_file}. "
            f"Return collisions: {len(return_collisions)}, "
            f"clean GoalRings: {len(clean_goal_rings)}"
        )

    for return_collision, clean_goal_ring in zip(
        return_collisions,
        clean_goal_rings,
    ):
        children = list(working_root)
        collision_index = children.index(return_collision)

        restored_goal_ring = ET.fromstring(
            ET.tostring(
                clean_goal_ring,
                encoding="unicode",
            )
        )

        working_root.remove(return_collision)
        working_root.insert(
            collision_index,
            restored_goal_ring,
        )

    ET.indent(
        working_tree,
        space="  ",
    )

    working_tree.write(
        working_set_file,
        encoding="utf-8",
        xml_declaration=True,
    )

    return len(return_collisions)


def remove_dark_gaia_run_1_entrance_collision(
    set_file: Path,
) -> None:

    if not set_file.is_file():
        raise FileNotFoundError(f"Dark Gaia Run 1 SET file does not exist: {set_file}")

    tree = ET.parse(set_file)
    root = tree.getroot()

    for collision in root.findall("SequenceChangeCollision"):
        event = collision.findtext("Event")
        object_id = collision.findtext("SetObjectID")

        if event == "SR_EnterDarkGaiaRun1" and object_id == "900000":
            root.remove(collision)

            ET.indent(
                tree,
                space="  ",
            )

            tree.write(
                set_file,
                encoding="utf-8",
                xml_declaration=True,
            )

            return

    raise RuntimeError("Could not find the Dark Gaia Run 1 entrance collision.")


def remove_dark_gaia_run_2_entrance_collision(
    set_file: Path,
) -> None:

    if not set_file.is_file():
        raise FileNotFoundError(f"Dark Gaia Run 2 SET file does not exist: {set_file}")

    tree = ET.parse(set_file)
    root = tree.getroot()

    for collision in root.findall("SequenceChangeCollision"):
        event = collision.findtext("Event")
        object_id = collision.findtext("SetObjectID")

        if event == "SR_EnterDarkGaiaRun2" and object_id == "900000":
            root.remove(collision)

            ET.indent(
                tree,
                space="  ",
            )

            tree.write(
                set_file,
                encoding="utf-8",
                xml_declaration=True,
            )

            return

    raise RuntimeError("Could not find the Dark Gaia Run 2 entrance collision.")


def remove_dark_gaia_run_3_entrance_collision(
    set_file: Path,
) -> None:

    if not set_file.is_file():
        raise FileNotFoundError(f"Dark Gaia Run 3 SET file does not exist: {set_file}")

    tree = ET.parse(set_file)
    root = tree.getroot()

    for collision in root.findall("SequenceChangeCollision"):
        event = collision.findtext("Event")
        object_id = collision.findtext("SetObjectID")

        if event == "SR_EnterDarkGaiaRun3" and object_id == "900000":
            root.remove(collision)

            ET.indent(
                tree,
                space="  ",
            )

            tree.write(
                set_file,
                encoding="utf-8",
                xml_declaration=True,
            )

            return

    raise RuntimeError("Could not find the Dark Gaia Run 3 entrance collision.")


def prepare_dark_gaia_run_1_archive(
    base_directory: Path,
) -> Path:

    source_folder = base_directory / "DGR" / "+#BossDarkGaia1_1Run"

    working_folder = base_directory / "Edited Archives" / "+#BossDarkGaia1_1Run"

    if not source_folder.is_dir():
        raise FileNotFoundError(
            "Dark Gaia Run 1 source archive does not exist: " f"{source_folder}"
        )

    required_files = (
        "Set.set.xml",
        "Return.set.xml",
        "SequenceAlternative.xml",
        "Stage.stg.xml",
        "Destination.set.xml",
    )

    working_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    for file_name in required_files:
        source_file = source_folder / file_name
        destination_file = working_folder / file_name

        if not source_file.is_file():
            raise FileNotFoundError(
                "Required Dark Gaia Run 1 file does not exist: " f"{source_file}"
            )

        shutil.copy2(
            source_file,
            destination_file,
        )

    return working_folder


def prepare_dark_gaia_run_2_archive(
    base_directory: Path,
) -> Path:

    source_folder = base_directory / "DGR" / "+#BossDarkGaia1_2Run"

    working_folder = base_directory / "Edited Archives" / "+#BossDarkGaia1_2Run"

    if not source_folder.is_dir():
        raise FileNotFoundError(
            "Dark Gaia Run 2 source archive does not exist: " f"{source_folder}"
        )

    required_files = (
        "Set.set.xml",
        "Return.set.xml",
        "SequenceAlternative.xml",
        "Stage.stg.xml",
        "Destination.set.xml",
    )

    working_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    for file_name in required_files:
        source_file = source_folder / file_name
        destination_file = working_folder / file_name

        if not source_file.is_file():
            raise FileNotFoundError(
                "Required Dark Gaia Run 2 file does not exist: " f"{source_file}"
            )

        shutil.copy2(
            source_file,
            destination_file,
        )

    return working_folder


def prepare_dark_gaia_run_3_archive(
    base_directory: Path,
) -> Path:

    source_folder = base_directory / "DGR" / "+#BossDarkGaia1_3Run"

    working_folder = base_directory / "Edited Archives" / "+#BossDarkGaia1_3Run"

    if not source_folder.is_dir():
        raise FileNotFoundError(
            "Dark Gaia Run 3 source archive does not exist: " f"{source_folder}"
        )

    required_files = (
        "Set.set.xml",
        "Return.set.xml",
        "SequenceAlternative.xml",
        "Stage.stg.xml",
        "Destination.set.xml",
    )

    working_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    for file_name in required_files:
        source_file = source_folder / file_name
        destination_file = working_folder / file_name

        if not source_file.is_file():
            raise FileNotFoundError(
                "Required Dark Gaia Run 3 file does not exist: " f"{source_file}"
            )

        shutil.copy2(
            source_file,
            destination_file,
        )

    return working_folder


def prepare_dark_gaia_run_1(
    assignments,
    base_directory: str | Path,
) -> tuple[Path, Path]:

    base_directory = Path(base_directory)

    assignment = find_dark_gaia_run_1_assignment(assignments)

    stage_name = assignment.stage.name

    dark_gaia_archive = prepare_dark_gaia_run_1_archive(base_directory)

    if stage_name == DARK_GAIA_RUN_1_NAME:
        dark_gaia_set_file = dark_gaia_archive / "Set.set.xml"

        remove_dark_gaia_run_1_entrance_collision(dark_gaia_set_file)

        print()
        print("DARK GAIA RUN 1 READY")
        print(f"  Assigned stage: {stage_name}")
        print("  Self-roll: using vanilla Dark Gaia Run 1")
        print(f"  Dark Gaia archive: {dark_gaia_archive}")

        return dark_gaia_archive, dark_gaia_archive

    if stage_name not in DARK_GAIA_STAGE_DATA:
        raise RuntimeError(
            "Dark Gaia Run 1 was assigned a stage with "
            "no Dark Gaia metadata: "
            f"{stage_name}"
        )

    stage_data = DARK_GAIA_STAGE_DATA[stage_name]

    clean_archive_name = stage_data.archive.removeprefix("+#")

    if stage_data.archive.startswith("+#ActD_"):
        clean_stage_folder = (
            base_directory / "Base Areas" / "Day Stages" / clean_archive_name
        )
    else:
        clean_stage_folder = base_directory / "Base Areas" / clean_archive_name

    working_stage_folder = (
        base_directory / "Stages To Randomise Enemies" / stage_data.archive
    )

    if not working_stage_folder.is_dir():
        working_stage_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

    for completion_set in stage_data.completion_sets:
        clean_set_file = clean_stage_folder / completion_set
        working_set_file = working_stage_folder / completion_set

        if not clean_set_file.is_file():
            raise FileNotFoundError(
                "Clean Dark Gaia completion SET file does not exist: "
                f"{clean_set_file}"
            )

        # If another randomiser feature has already created this SET,
        # preserve those changes. Otherwise begin with the clean version.
        shutil.copy2(
            clean_set_file,
            working_set_file,
        )

        # Replace the stage's normal GoalRing with the collision
        # that starts the Dark Gaia return chain.
        replace_goal_ring_with_return_collision(
            working_set_file,
            DARK_GAIA_RUN_1_RETURN_EVENT,
        )

        print(f"  Clean SET: {clean_set_file}")
        print(f"  Working SET: {working_set_file}")

    print()
    print("DARK GAIA RUN 1 READY")
    print(f"  Assigned stage: {stage_name}")
    print(f"  Return event: {DARK_GAIA_RUN_1_RETURN_EVENT}")
    print(f"  Dark Gaia archive: {dark_gaia_archive}")
    return dark_gaia_archive, working_stage_folder


def prepare_dark_gaia_run_2(
    assignments,
    base_directory: str | Path,
) -> tuple[Path, Path]:

    base_directory = Path(base_directory)

    assignment = find_dark_gaia_run_2_assignment(assignments)

    stage_name = assignment.stage.name

    dark_gaia_archive = prepare_dark_gaia_run_2_archive(base_directory)

    # Self-roll: preserve vanilla Dark Gaia Run 2 behaviour.
    if stage_name == DARK_GAIA_RUN_2_NAME:
        dark_gaia_set_file = dark_gaia_archive / "Set.set.xml"

        remove_dark_gaia_run_2_entrance_collision(dark_gaia_set_file)

        print()
        print("DARK GAIA RUN 2 READY")
        print(f"  Assigned stage: {stage_name}")
        print("  Self-roll: using vanilla Dark Gaia Run 2")
        print(f"  Dark Gaia archive: {dark_gaia_archive}")

        return dark_gaia_archive, dark_gaia_archive

    if stage_name not in DARK_GAIA_STAGE_DATA:
        raise RuntimeError(
            "Dark Gaia Run 2 was assigned a stage with "
            "no Dark Gaia metadata: "
            f"{stage_name}"
        )

    stage_data = DARK_GAIA_STAGE_DATA[stage_name]

    clean_archive_name = stage_data.archive.removeprefix("+#")

    if stage_data.archive.startswith("+#ActD_"):
        clean_stage_folder = (
            base_directory / "Base Areas" / "Day Stages" / clean_archive_name
        )
    else:
        clean_stage_folder = base_directory / "Base Areas" / clean_archive_name

    working_stage_folder = (
        base_directory / "Stages To Randomise Enemies" / stage_data.archive
    )

    if not working_stage_folder.is_dir():
        working_stage_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

    for completion_set in stage_data.completion_sets:
        clean_set_file = clean_stage_folder / completion_set
        working_set_file = working_stage_folder / completion_set

        if not clean_set_file.is_file():
            raise FileNotFoundError(
                "Clean Dark Gaia completion SET file does not exist: "
                f"{clean_set_file}"
            )

        shutil.copy2(
            clean_set_file,
            working_set_file,
        )

        replace_goal_ring_with_return_collision(
            working_set_file,
            DARK_GAIA_RUN_2_RETURN_EVENT,
        )

        print(f"  Clean SET: {clean_set_file}")
        print(f"  Working SET: {working_set_file}")

    print()
    print("DARK GAIA RUN 2 READY")
    print(f"  Assigned stage: {stage_name}")
    print(f"  Return event: {DARK_GAIA_RUN_2_RETURN_EVENT}")
    print(f"  Dark Gaia archive: {dark_gaia_archive}")

    return dark_gaia_archive, working_stage_folder


def prepare_dark_gaia_run_3(
    assignments,
    base_directory: str | Path,
) -> tuple[Path, Path]:

    base_directory = Path(base_directory)

    assignment = find_dark_gaia_run_3_assignment(assignments)

    stage_name = assignment.stage.name

    dark_gaia_archive = prepare_dark_gaia_run_3_archive(base_directory)

    # Self-roll: preserve vanilla Dark Gaia Run 3 behaviour.
    if stage_name == DARK_GAIA_RUN_3_NAME:
        dark_gaia_set_file = dark_gaia_archive / "Set.set.xml"

        remove_dark_gaia_run_3_entrance_collision(dark_gaia_set_file)

        print()
        print("DARK GAIA RUN 3 READY")
        print(f"  Assigned stage: {stage_name}")
        print("  Self-roll: using vanilla Dark Gaia Run 3")
        print(f"  Dark Gaia archive: {dark_gaia_archive}")

        return dark_gaia_archive, dark_gaia_archive

    if stage_name not in DARK_GAIA_STAGE_DATA:
        raise RuntimeError(
            "Dark Gaia Run 3 was assigned a stage with "
            "no Dark Gaia metadata: "
            f"{stage_name}"
        )

    stage_data = DARK_GAIA_STAGE_DATA[stage_name]

    clean_archive_name = stage_data.archive.removeprefix("+#")

    if stage_data.archive.startswith("+#ActD_"):
        clean_stage_folder = (
            base_directory / "Base Areas" / "Day Stages" / clean_archive_name
        )
    else:
        clean_stage_folder = base_directory / "Base Areas" / clean_archive_name

    working_stage_folder = (
        base_directory / "Stages To Randomise Enemies" / stage_data.archive
    )

    if not working_stage_folder.is_dir():
        working_stage_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

    for completion_set in stage_data.completion_sets:
        clean_set_file = clean_stage_folder / completion_set
        working_set_file = working_stage_folder / completion_set

        if not clean_set_file.is_file():
            raise FileNotFoundError(
                "Clean Dark Gaia completion SET file does not exist: "
                f"{clean_set_file}"
            )

        shutil.copy2(
            clean_set_file,
            working_set_file,
        )

        replace_goal_ring_with_return_collision(
            working_set_file,
            DARK_GAIA_RUN_3_RETURN_EVENT,
        )

        print(f"  Clean SET: {clean_set_file}")
        print(f"  Working SET: {working_set_file}")

    print()
    print("DARK GAIA RUN 3 READY")
    print(f"  Assigned stage: {stage_name}")
    print(f"  Return event: {DARK_GAIA_RUN_3_RETURN_EVENT}")
    print(f"  Dark Gaia archive: {dark_gaia_archive}")

    return dark_gaia_archive, working_stage_folder
