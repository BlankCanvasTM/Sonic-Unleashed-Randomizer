from __future__ import annotations

import argparse
import random
import secrets
import shutil
import xml.etree.ElementTree as ET
import sys
from copy import deepcopy
from pathlib import Path

from enemy_data import (
    Enemy,
    EnemyState,
    HOLE_RANDOM_TARGETS,
    HOLE_FIRST_STATE_OVERRIDES,
    PROTECTED_HOLE_SOURCE_TYPES,
)

from dataclasses import dataclass
import subprocess

def get_base_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


BASE_DIR = get_base_directory()


STAGES_TO_RANDOMISE_DIR = BASE_DIR / "Stages To Randomise Enemies"
BASE_AREAS_DIR = BASE_DIR / "Base Areas"
ENEMY_RANDOMISER_DIR = BASE_DIR / "Enemy Randomiser"
HEDGEARCPACK_PATH = BASE_DIR / "HedgeArcPack.exe"


PRESERVED_FIELDS = ("Position", "Rotation", "SetObjectID")

RANDOMISE_DIRECT_ENEMIES = True
RANDOMISE_ENEMY_HOLES = True
LARGE_ENEMY_ROLL_SIZE = 33

def _append_parameter(parent: ET.Element, name: str, value: object) -> None:
	element = ET.SubElement(parent, name)

	if isinstance(value, dict):
		for child_name, child_value in value.items():
			_append_parameter(element, child_name, child_value)
	else:
		element.text = str(value)


def _is_revival_enemy(element: ET.Element) -> bool:

	#Protect any source object explicitly marked IsRevival=true.

	is_revival = element.find("IsRevival")
	if is_revival is None or is_revival.text is None:
		return False

	return is_revival.text.strip().lower() == "true"


def _get_set_object_id(element: ET.Element) -> str:
	set_object_id = element.find("SetObjectID")
	if set_object_id is None or set_object_id.text is None:
		return "unknown"

	return set_object_id.text.strip()


def _get_position(element: ET.Element) -> str:
	position = element.find("Position")
	if position is None:
		return "unknown"

	values = {}
	for axis in ("x", "y", "z"):
		child = position.find(axis)
		values[axis] = child.text.strip() if child is not None and child.text else "?"

	return f"X={values['x']} Y={values['y']} Z={values['z']}"


def _build_replacement_element(
	original: ET.Element,
	replacement: Enemy,
) -> ET.Element:
	"""
	Create the replacement object.

	The original Position, Rotation and SetObjectID are copied exactly.
	All other enemy-specific fields come from the replacement's metadata.
	"""
	preserved = {}

	for field_name in PRESERVED_FIELDS:
		field = original.find(field_name)
		if field is not None:
			preserved[field_name] = deepcopy(field)

	new_element = ET.Element(replacement.class_name)


	for name, value in replacement.parameters.items():
		_append_parameter(new_element, name, value)

	for field_name in ("Position", "Rotation", "SetObjectID"):
		if field_name in preserved:
			new_element.append(preserved[field_name])

	new_element.tail = original.tail

	return new_element

def _build_bonus_large_enemy(
    hole: ET.Element,
    enemy: Enemy,
) -> ET.Element:
    """
    Create a bonus Titan or Big Mother at an EnemyHole position.

    Position and Rotation are copied from the hole.
    SetObjectID is intentionally omitted because the bonus enemy
    is not part of the hole's event logic.
    """

    new_element = ET.Element(enemy.class_name)

    for name, value in enemy.parameters.items():
        _append_parameter(new_element, name, value)

    for field_name in ("Position", "Rotation"):
        field = hole.find(field_name)

        if field is not None:
            new_element.append(deepcopy(field))

    new_element.tail = hole.tail

    return new_element


def _choose_replacement(
	rng: random.Random,
	targets: list[Enemy],
) -> Enemy:
	return rng.choice(targets)


def _randomise_children(
	parent: ET.Element,
	enemy_state: EnemyState,
	targets: list[Enemy],
	rng: random.Random,
	file_name: str,
	log_entries: list[str],
	area_state: dict,
) -> tuple[int, int]:

	randomised_count = 0
	skipped_count = 0

	for index, child in enumerate(list(parent)):
		source = enemy_state.by_class.get(child.tag)

		if source is None:
			# The object itself is not a recognised direct enemy. It may still
			# contain nested XML, so continue walking it.
			child_randomised, child_skipped = _randomise_children(
				child,
				enemy_state,
				targets,
				rng,
				file_name,
				log_entries,
				area_state,
			)
			randomised_count += child_randomised
			skipped_count += child_skipped
			continue

		set_object_id = _get_set_object_id(child)
		position = _get_position(child)

		if not source.randomisable_source:
			log_entries.extend([
				"[SKIPPED]",
				f"File: {file_name}",
				f"SetObjectID: {set_object_id}",
				f"Position: {position}",
				f"Enemy: {source.name} ({source.class_name})",
				"Reason: Protected source enemy",
				"",
			])
			skipped_count += 1
			continue

		if _is_revival_enemy(child):
			log_entries.extend([
				"[SKIPPED]",
				f"File: {file_name}",
				f"SetObjectID: {set_object_id}",
				f"Position: {position}",
				f"Enemy: {source.name} ({source.class_name})",
				"Reason: IsRevival=true",
				"",
			])
			skipped_count += 1
			continue

		available_targets = targets
		if area_state["titan_spawned"]:
			available_targets = [
				enemy
				for enemy in targets
				if enemy.class_name != "EvilEnemyTitan"
			]

		replacement = _choose_replacement(rng, available_targets)


		if replacement.class_name == "EvilEnemyTitan":
			area_state["titan_spawned"] = True

		
		new_element = _build_replacement_element(child, replacement)
		parent[index] = new_element

		log_entries.extend([
			"[RANDOMISED]",
			f"File: {file_name}",
			f"SetObjectID: {set_object_id}",
			f"Position: {position}",
			f"Original: {source.name} ({source.class_name})",
			f"Replacement: {replacement.name} ({replacement.class_name})",
			"",
		])

		randomised_count += 1

	return randomised_count, skipped_count


def _write_xml(tree: ET.ElementTree, path: Path) -> None:
	#Write game XML using the declaration style already used by these files.

	xml_body = ET.tostring(
		tree.getroot(),
		encoding="unicode",
		short_empty_elements=True,
	)

	path.write_text(
		'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n'
		+ xml_body
		+ "\n",
		encoding="utf-8",
	)


def restore_clean_enemysets(
	base_stage_folder: str | Path,
	working_stage_folder: str | Path,
) -> int:

	base_stage_folder = Path(base_stage_folder)
	working_stage_folder = Path(working_stage_folder)

	if not base_stage_folder.is_dir():
		raise FileNotFoundError(
			f"Base stage folder does not exist: {base_stage_folder}"
		)

	if not working_stage_folder.is_dir():
		raise FileNotFoundError(
			f"Working stage folder does not exist: {working_stage_folder}"
		)

	base_files = sorted(
		base_stage_folder.glob("*.set.xml")
	)

	if not base_files:
		raise FileNotFoundError(
			f"No *.set.xml files found in base folder: "
			f"{base_stage_folder}"
		)

	enemy_state = EnemyState()

	restored_count = 0

	for base_file in base_files:

		tree = ET.parse(base_file)
		root = tree.getroot()

		is_relevant = False

		for element in root.iter():

			if element.tag in enemy_state.by_class:
				is_relevant = True
				break

			if element.tag == "EnemyObjEnemyHole":
				is_relevant = True
				break

		if not is_relevant:
			continue

		destination = (
			working_stage_folder
			/ base_file.name
		)

		shutil.copy2(
			base_file,
			destination,
		)

		restored_count += 1

	return restored_count

def find_stage_pairs() -> list[tuple[Path, Path]]:
	stage_pairs = []

	for working_stage in sorted(
		STAGES_TO_RANDOMISE_DIR.glob("+#ActN_*")
	):
		if not working_stage.is_dir():
			continue

		base_stage_name = working_stage.name.removeprefix("+#")
		base_stage = BASE_AREAS_DIR / base_stage_name

		if not base_stage.is_dir():
			print(
				f"Skipping {working_stage.name}: "
				f"matching base folder was not found."
			)
			continue

		stage_pairs.append(
			(
				working_stage,
				base_stage,
			)
		)

	return stage_pairs

def move_packed_archives_to_root(
	archive_directory: Path,
	output_directory: Path,
) -> None:

	archive_name = archive_directory.name
	source_directory = archive_directory.parent

	packed_files = list(
		source_directory.glob(
			f"{archive_name}.ar*"
		)
	)

	packed_files += list(
		source_directory.glob(
			f"{archive_name}.arl"
		)
	)

	for packed_file in packed_files:

		if not packed_file.is_file():
			continue

		destination = (
			output_directory
			/ packed_file.name
		)

		if destination.exists():
			destination.unlink()

		shutil.move(
			str(packed_file),
			str(destination),
		)


def randomise_direct_enemies(
	stage_folder: Path,
	base_stage_folder: Path,
	rng: random.Random,
	seed: int,
) -> tuple[dict[str, int], list[str]]:

	if not stage_folder.is_dir():
		raise FileNotFoundError(
			f"Stage folder does not exist: {stage_folder}"
		)

	restored_files = restore_clean_enemysets(
		base_stage_folder,
		stage_folder,
	)

	enemy_state = EnemyState()

	targets = enemy_state.direct_targets

	if not targets:
		raise RuntimeError(
			"enemy_data.py contains no valid direct enemy targets."
		)

	set_files = sorted(
		stage_folder.glob("*.set.xml")
	)

	if not set_files:
		raise FileNotFoundError(
			f"No *.set.xml files found in: {stage_folder}"
		)

	log_entries = [
		"",
		"=" * 60,
		stage_folder.name,
		"=" * 60,
		f"Stage folder: {stage_folder}",
		f"Base folder: {base_stage_folder}",
		f"SET files restored from base: {restored_files}",
		f"SET files scanned: {len(set_files)}",
		"",
	]

	total_randomised = 0
	total_skipped = 0
	total_holes_randomised = 0
	total_holes_skipped = 0
	total_large_enemies = 0
	files_changed = 0

	for set_file in set_files:

		# XMLParser instances cannot be reused after parsing,
		# so create one per file while preserving comments.
		parser = ET.XMLParser(
			target=ET.TreeBuilder(insert_comments=True)
		)

		tree = ET.parse(
			set_file,
			parser=parser,
		)

		root = tree.getroot()

		file_entries = []

		area_state = {
			"titan_spawned": False,
		}

		if RANDOMISE_DIRECT_ENEMIES:
			randomised_count, skipped_count = _randomise_children(
				root,
				enemy_state,
				targets,
				rng,
				set_file.name,
				file_entries,
				area_state,
			)
		else:
			randomised_count = 0
			skipped_count = 0

		if RANDOMISE_ENEMY_HOLES:
			(
				hole_randomised_count,
				hole_skipped_count,
				large_enemy_count,
			) = randomise_enemy_holes(
				root,
				enemy_state,
				rng,
				set_file.name,
				file_entries,
			)
		else:
			hole_randomised_count = 0
			hole_skipped_count = 0
			large_enemy_count = 0

		if (
			randomised_count
			or skipped_count
			or hole_randomised_count
			or hole_skipped_count
		):
			log_entries.extend([
				"-" * 60,
				set_file.name,
				"-" * 60,
				"",
			])

			log_entries.extend(
				file_entries
			)

		if randomised_count or hole_randomised_count:
			_write_xml(
				tree,
				set_file,
			)

			files_changed += 1

		total_randomised += randomised_count
		total_skipped += skipped_count
		total_holes_randomised += hole_randomised_count
		total_holes_skipped += hole_skipped_count
		total_large_enemies += large_enemy_count

	log_entries.extend([
		"=" * 60,
		f"{stage_folder.name} SUMMARY",
		"=" * 60,
		f"Seed: {seed}",
		f"Files changed: {files_changed}",
		f"Files restored from base: {restored_files}",
		f"Direct enemies randomised: {total_randomised}",
		f"Direct enemies skipped: {total_skipped}",
		f"Enemy holes randomised: {total_holes_randomised}",
		f"Enemy holes skipped: {total_holes_skipped}",
		f"Bonus large enemies spawned: {total_large_enemies}",
		"",
	])

	return (
		{
			"files_restored": restored_files,
			"files_scanned": len(set_files),
			"files_changed": files_changed,
			"randomised": total_randomised,
			"skipped": total_skipped,
			"holes_randomised": total_holes_randomised,
			"holes_skipped": total_holes_skipped,
			"large_enemies": total_large_enemies,
		},
		log_entries,
	)

def randomise_enemy_holes(
    root: ET.Element,
    enemy_state: EnemyState,
    rng: random.Random,
    file_name: str,
    log_entries: list[str],
) -> tuple[int, int, int]:

    randomised_count = 0
    skipped_count = 0
    large_enemy_count = 0

    parent_map = {
        child: parent
        for parent in root.iter()
        for child in parent
    }

    for element in list(root.iter("EnemyObjEnemyHole")):
        enemy_type_element = element.find("EnemyType")

        if enemy_type_element is None or enemy_type_element.text is None:
            continue

        original_type = int(enemy_type_element.text.strip())
        generate_max_element = element.find("GenerateMaxCount")

        generate_max_count = None

        if (
            generate_max_element is not None
            and generate_max_element.text is not None
        ):
            generate_max_count = int(
                generate_max_element.text.strip()
            )

        set_object_id = _get_set_object_id(element)
        position = _get_position(element)

        if original_type in PROTECTED_HOLE_SOURCE_TYPES:
            log_entries.extend([
                "[SKIPPED HOLE]",
                f"File: {file_name}",
                f"SetObjectID: {set_object_id}",
                f"Position: {position}",
                f"EnemyType: {original_type}",
                "Reason: Protected Float / progression enemy type",
                "",
            ])

            skipped_count += 1
            continue

        if generate_max_count == -1:
            log_entries.extend([
                "[SKIPPED HOLE]",
                f"File: {file_name}",
                f"SetObjectID: {set_object_id}",
                f"Position: {position}",
                f"EnemyType: {original_type}",
                f"GenerateMaxCount: {generate_max_count}",
                "Reason: Infinite/progression spawner",
                "",
            ])

            skipped_count += 1
            continue

        replacement_type = rng.choice(HOLE_RANDOM_TARGETS)

        enemy_type_element.text = str(replacement_type)

        if replacement_type in HOLE_FIRST_STATE_OVERRIDES:
            first_state_element = element.find("FirstState")

            if first_state_element is not None:
                first_state_element.text = str(
                    HOLE_FIRST_STATE_OVERRIDES[
                        replacement_type
                    ]
                )

        first_state_element = element.find("FirstState")

        first_state = (
            first_state_element.text.strip()
            if (
                first_state_element is not None
                and first_state_element.text is not None
            )
            else "Unknown"
        )

        log_entries.extend([
            "[RANDOMISED HOLE]",
            f"File: {file_name}",
            f"SetObjectID: {set_object_id}",
            f"Position: {position}",
            f"Original EnemyType: {original_type}",
            f"FirstState: {first_state}",
            f"Replacement EnemyType: {replacement_type}",
            "",
        ])

        randomised_count += 1

        large_enemy_roll = rng.randrange(
            LARGE_ENEMY_ROLL_SIZE
        )

        if large_enemy_roll == 31:
            large_enemy = enemy_state.TITAN

        elif large_enemy_roll == 32:
            large_enemy = enemy_state.BIG_MOTHER

        else:
            large_enemy = None

        if large_enemy is not None:
            parent = parent_map.get(element)

            if parent is not None:
                bonus_element = _build_bonus_large_enemy(
                    element,
                    large_enemy,
                )

                element_index = list(parent).index(element)

                parent.insert(
                    element_index + 1,
                    bonus_element,
                )

                log_entries.extend([
                    "[BONUS LARGE ENEMY]",
                    f"File: {file_name}",
                    f"Source Hole SetObjectID: {set_object_id}",
                    f"Position: {position}",
                    (
                        f"Enemy: {large_enemy.name} "
                        f"({large_enemy.class_name})"
                    ),
                    "SetObjectID: None",
                    (
                        f"Roll: {large_enemy_roll} / "
                        f"{LARGE_ENEMY_ROLL_SIZE - 1}"
                    ),
                    "",
                ])

                large_enemy_count += 1

    return (
        randomised_count,
        skipped_count,
        large_enemy_count,
    )

@dataclass
class PackResult:
	success: bool
	executable_path: Path
	archive_directory: Path
	return_code: int
	stdout: str
	stderr: str


def pack_archive(
	hedgearcpack_path: str | Path,
	archive_directory: str | Path,
	print_output: bool = True,
) -> PackResult:

	hedgearcpack_path = Path(hedgearcpack_path)
	archive_directory = Path(archive_directory)

	if not hedgearcpack_path.is_file():
		raise FileNotFoundError(
			f"HedgeArcPack executable was not found: "
			f"{hedgearcpack_path}"
		)

	if not archive_directory.is_dir():
		raise FileNotFoundError(
			f"Archive directory was not found: "
			f"{archive_directory}"
		)

	command = [
		str(hedgearcpack_path),
		str(archive_directory),
		"-P",
		"-T=hh",
	]

	if print_output:
		print()

	completed_process = subprocess.run(
		command,
		capture_output=True,
		text=True,
		encoding="utf-8",
		errors="replace",
		check=False,
	)

	result = PackResult(
		success=completed_process.returncode == 0,
		executable_path=hedgearcpack_path,
		archive_directory=archive_directory,
		return_code=completed_process.returncode,
		stdout=completed_process.stdout,
		stderr=completed_process.stderr,
	)

	if print_output:

		if result.stdout.strip():
			print(result.stdout.strip())

		if result.stderr.strip():
			print(result.stderr.strip())

		print()

		if result.success:
			print("Archive packed successfully.")
		else:
			print(
				f"HedgeArcPack failed with exit code "
				f"{result.return_code}."
			)

	if result.success:
		ENEMY_RANDOMISER_DIR.mkdir(
			parents=True,
			exist_ok=True,
		)

		move_packed_archives_to_root(
			archive_directory,
			ENEMY_RANDOMISER_DIR,
		)

	return result

def reset_all_night_stages(
    pack_archives: bool = True,
    print_progress: bool = True,
) -> dict[str, int]:

    stage_pairs = find_stage_pairs()

    if not stage_pairs:
        raise FileNotFoundError(
            "No matching Night-stage folders were found."
        )

    total_files_restored = 0

    if print_progress:
        print()
        print("RESETTING NIGHT STAGE ENEMIES")


    for stage_folder, base_stage_folder in stage_pairs:

        restored_count = restore_clean_enemysets(
            base_stage_folder=base_stage_folder,
            working_stage_folder=stage_folder,
        )

        total_files_restored += restored_count

        if print_progress:
            print(
                f"{stage_folder.name}: "
                f"{restored_count} SET files restored"
            )

        if pack_archives:
            pack_result = pack_archive(
                HEDGEARCPACK_PATH,
                stage_folder,
                print_output=print_progress,
            )

            if not pack_result.success:
                raise RuntimeError(
                    f"Enemy reset completed for "
                    f"{stage_folder.name}, but archive "
                    f"packing failed."
                )

    if print_progress:
        print()
        print("ENEMY RESET COMPLETE")
        print(
            f"Stages restored: {len(stage_pairs)}"
        )
        print(
            f"SET files restored: {total_files_restored}"
        )

    return {
        "stages_restored": len(stage_pairs),
        "files_restored": total_files_restored,
    }


def randomise_all_night_stages(
	seed: int,
	log_path: str | Path | None = None,
	pack_archives: bool = True,
	print_progress: bool = True,
) -> dict[str, int | Path]:
	"""
	Randomise enemies across every matching Night-stage folder.

	This is the public entry point intended for the main randomiser.

	The caller owns the enemy seed. A single random.Random instance is created
	from that seed and shared across every stage, so the enemy layout is fully
	reproducible without affecting the main stage-randomiser seed.

	A separate enemy spoiler log is always written.
	"""

	rng = random.Random(seed)

	stage_pairs = find_stage_pairs()

	if not stage_pairs:
		raise FileNotFoundError(
			"No matching Night-stage folders were found."
		)

	if log_path is None:
		log_path = BASE_DIR / "enemy_spoiler_log.txt"
	else:
		log_path = Path(log_path)

	log_entries = [
		"SONIC UNLEASHED ENEMY RANDOMISATION",
		"=" * 60,
		f"Enemy seed: {seed}",
		f"Stages found: {len(stage_pairs)}",
		"",
	]

	total_files_restored = 0
	total_files_scanned = 0
	total_files_changed = 0
	total_direct_randomised = 0
	total_direct_skipped = 0
	total_holes_randomised = 0
	total_holes_skipped = 0
	total_large_enemies = 0

	if print_progress:
		print(f"Enemy seed: {seed}")
		print(f"Stages found: {len(stage_pairs)}")

	for stage_folder, base_stage_folder in stage_pairs:

		if print_progress:
			print()
			print("=" * 60)
			print(f"Randomising {stage_folder.name}")
			print("=" * 60)

		result, stage_log_entries = randomise_direct_enemies(
			stage_folder=stage_folder,
			base_stage_folder=base_stage_folder,
			rng=rng,
			seed=seed,
		)

		log_entries.extend(stage_log_entries)

		total_files_restored += result["files_restored"]
		total_files_scanned += result["files_scanned"]
		total_files_changed += result["files_changed"]
		total_direct_randomised += result["randomised"]
		total_direct_skipped += result["skipped"]
		total_holes_randomised += result["holes_randomised"]
		total_holes_skipped += result["holes_skipped"]

		if print_progress:
			print(
				f"SET files restored: "
				f"{result['files_restored']}"
			)
			print(
				f"SET files scanned: "
				f"{result['files_scanned']}"
			)
			print(
				f"Files changed: "
				f"{result['files_changed']}"
			)
			print(
				f"Direct enemies randomised: "
				f"{result['randomised']}"
			)
			print(
				f"Direct enemies skipped: "
				f"{result['skipped']}"
			)
			print(
				f"Enemy holes randomised: "
				f"{result['holes_randomised']}"
			)
			print(
				f"Enemy holes skipped: "
				f"{result['holes_skipped']}"
			)

		if pack_archives:
			pack_result = pack_archive(
				HEDGEARCPACK_PATH,
				stage_folder,
				print_output=print_progress,
			)

			if not pack_result.success:
				raise RuntimeError(
					f"Enemy randomisation completed for "
					f"{stage_folder.name}, but archive "
					f"packing failed."
				)

	log_entries.extend([
		"",
		"=" * 60,
		"FULL RANDOMISATION SUMMARY",
		"=" * 60,
		f"Seed: {seed}",
		f"Stages randomised: {len(stage_pairs)}",
		f"SET files restored: {total_files_restored}",
		f"SET files scanned: {total_files_scanned}",
		f"Files changed: {total_files_changed}",
		f"Direct enemies randomised: {total_direct_randomised}",
		f"Direct enemies skipped: {total_direct_skipped}",
		f"Enemy holes randomised: {total_holes_randomised}",
		f"Enemy holes skipped: {total_holes_skipped}",
		"",
	])

	log_path.parent.mkdir(
		parents=True,
		exist_ok=True,
	)

	log_path.write_text(
		"\n".join(log_entries),
		encoding="utf-8",
	)

	if print_progress:
		print()
		print("=" * 60)
		print("FULL RANDOMISATION SUMMARY")
		print("=" * 60)
		print(
			f"Stages randomised: "
			f"{len(stage_pairs)}"
		)
		print(
			f"SET files restored: "
			f"{total_files_restored}"
		)
		print(
			f"SET files scanned: "
			f"{total_files_scanned}"
		)
		print(
			f"Files changed: "
			f"{total_files_changed}"
		)
		print(
			f"Direct enemies randomised: "
			f"{total_direct_randomised}"
		)
		print(
			f"Direct enemies skipped: "
			f"{total_direct_skipped}"
		)
		print(
			f"Enemy holes randomised: "
			f"{total_holes_randomised}"
		)
		print(
			f"Enemy holes skipped: "
			f"{total_holes_skipped}"
		)
		print()
		print(f"Spoiler log: {log_path}")

	return {
		"seed": seed,
		"stages_randomised": len(stage_pairs),
		"files_restored": total_files_restored,
		"files_scanned": total_files_scanned,
		"files_changed": total_files_changed,
		"direct_randomised": total_direct_randomised,
		"direct_skipped": total_direct_skipped,
		"holes_randomised": total_holes_randomised,
		"holes_skipped": total_holes_skipped,
		"log_path": log_path,
	}


def main() -> None:

	parser = argparse.ArgumentParser(
		description=(
			"Randomise enemies across all available "
			"Sonic Unleashed Night stages."
		)
	)

	parser.add_argument(
		"--seed",
		type=int,
		default=None,
		help=(
			"Optional enemy seed. "
			"Omit to generate a new random seed."
		),
	)

	parser.add_argument(
		"--log",
		default=None,
		help=(
			"Optional enemy spoiler-log output path."
		),
	)

	parser.add_argument(
		"--no-pack",
		action="store_true",
		help=(
			"Randomise the SET files without packing "
			"the Night-stage archives."
		),
	)

	args = parser.parse_args()

	if args.seed is None:
		seed = secrets.randbits(64)
	else:
		seed = args.seed

	randomise_all_night_stages(
		seed=seed,
		log_path=args.log,
		pack_archives=not args.no_pack,
		print_progress=True,
	)


if __name__ == "__main__":
	main()
