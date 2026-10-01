import argparse
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

from packer import get_hedgearcpack_path, pack_application
from seed_system import generate_seed_code, normalise_seed, seed_to_integer

SKILL_SEED_NAMESPACE = "WEREHOG_SKILLS"

SKILL_NAMES = {
    2: "Donkey Kick Combo",
    3: "Egg Scrambler",
    4: "Flying Double Punch Crush",
    5: "Aerial Claw Slash and Spin",
    6: "Double Axle Combo",
    7: "Wereclap",
    8: "Shooting Star Combo",
    9: "Typhoon Combo",
    10: "Wereclaw Charge",
    11: "Triple Wild Claw",
    12: "Spinning Needle Attack",
    13: "Were-Rush",
    14: "Missile Punch",
    15: "Were-Tornado",
    16: "Feral Were-Hammer",
    17: "Feral Wild Whirl",
    18: "Werewheel Rush",
    19: "Earthshaker",
    20: "Vertical Were-Hammer",
    21: "Wild Whirl Were-Hammer",
    22: "Crescent Moon Strike",
    23: "Hurricane Combo",
    24: "Tricky Tornado Uppercut",
    25: "Wild Werewhip",
    26: "Comet Punch",
    27: "Were-Cyclone",
    28: "Knuckle Sandwich Combo",
    29: "Ultimate Wild Combo",
    30: "Unleashed Knuckle Sandwich",
    31: "Unleashed Wild Combo",
}

# Dependencies use VANILLA levels as stable skill IDs.
DEPENDENCIES = {
    28: {2},
    30: {28},
    29: {3},
    31: {29},
    18: {16},
    20: {16},
}


def get_base_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = get_base_directory()
EDITED_ARCHIVES_DIR = BASE_DIR / "Edited Archives"
CLEAN_COMBO_DIR = BASE_DIR / "Clean Werehog Combos"
APPLICATION_DIR = BASE_DIR / "+#Application"
EVIL_ACTION_COMMON_DIR = EDITED_ARCHIVES_DIR / "+EvilActionCommon"

CLEAN_EVIL_ATTACK_ACTION = CLEAN_COMBO_DIR / "EvilAttackAction1.xml"
CLEAN_SKILL_PARAMETER = CLEAN_COMBO_DIR / "SkillParameter.xml"
CLEAN_SKILL_NAME_FCO = CLEAN_COMBO_DIR / "skill_name_list.fco"

WORKING_EVIL_ATTACK_ACTION = APPLICATION_DIR / "EvilAttackAction1.xml"
WORKING_SKILL_PARAMETER = APPLICATION_DIR / "SkillParameter.xml"
WORKING_SKILL_NAME_FCO = EVIL_ACTION_COMMON_DIR / "skill_name_list.fco"

DEFAULT_SKILL_LOG = BASE_DIR / "werehog_skill_spoiler_log.txt"


def validate_skill_files() -> None:
    required_files = (
        CLEAN_EVIL_ATTACK_ACTION,
        CLEAN_SKILL_PARAMETER,
        CLEAN_SKILL_NAME_FCO,
    )
    missing = [path for path in required_files if not path.is_file()]
    if missing:
        missing_text = "\n".join(f"  {path}" for path in missing)
        raise FileNotFoundError(
            "The following clean Werehog combo files are missing:\n" f"{missing_text}"
        )

    required_directories = (APPLICATION_DIR, EVIL_ACTION_COMMON_DIR)
    missing_directories = [path for path in required_directories if not path.is_dir()]
    if missing_directories:
        missing_text = "\n".join(f"  {path}" for path in missing_directories)
        raise FileNotFoundError(
            "The following working archive folders are missing:\n" f"{missing_text}"
        )


def restore_clean_werehog_skills(print_progress: bool = True) -> int:
    validate_skill_files()
    copies = (
        (CLEAN_EVIL_ATTACK_ACTION, WORKING_EVIL_ATTACK_ACTION),
        (CLEAN_SKILL_PARAMETER, WORKING_SKILL_PARAMETER),
        (CLEAN_SKILL_NAME_FCO, WORKING_SKILL_NAME_FCO),
    )
    for source, destination in copies:
        shutil.copy2(source, destination)
        if print_progress:
            print(f"Restored: {source.name} -> {destination.parent.name}")
    return len(copies)


def generate_skill_progression(rng: random.Random) -> dict[int, int]:
    remaining = set(range(2, 32))
    placed = set()
    order: list[int] = []

    while remaining:
        available = [
            skill
            for skill in remaining
            if DEPENDENCIES.get(skill, set()).issubset(placed)
        ]
        if not available:
            raise RuntimeError("Werehog skill dependency graph contains a cycle.")

        chosen = rng.choice(sorted(available))
        order.append(chosen)
        placed.add(chosen)
        remaining.remove(chosen)

    progression = {
        destination: source for destination, source in zip(range(2, 32), order)
    }
    validate_dependency_order(progression)
    return progression


def validate_dependency_order(progression: dict[int, int]) -> None:
    source_to_destination = {
        source: destination for destination, source in progression.items()
    }
    for skill, prerequisites in DEPENDENCIES.items():
        for prerequisite in prerequisites:
            if source_to_destination[prerequisite] >= source_to_destination[skill]:
                raise AssertionError(
                    f"{SKILL_NAMES[prerequisite]} must unlock before "
                    f"{SKILL_NAMES[skill]}."
                )


def _randomise_evil_attack_action(
    source_path: Path,
    output_path: Path,
    progression: dict[int, int],
) -> None:
    text = source_path.read_text(encoding="utf-8")
    source_to_destination = {
        source: destination for destination, source in progression.items()
    }
    feral_destination = source_to_destination[16]
    action_pattern = re.compile(r"<Action>.*?</Action>", re.DOTALL)
    changed_by_source = {level: 0 for level in range(2, 32)}
    feral_cutoff_changes = 0

    def edit_action(match: re.Match[str]) -> str:
        nonlocal feral_cutoff_changes
        block = match.group(0)
        min_match = re.search(r"<ValidLevel_Min>(\d+)</ValidLevel_Min>", block)
        if min_match is None:
            return block

        vanilla_min = int(min_match.group(1))
        action_name_match = re.search(
            r"<ActionName>(.*?)</ActionName>", block, re.DOTALL
        )
        action_name = action_name_match.group(1).strip() if action_name_match else ""

        if 2 <= vanilla_min <= 31:
            destination_level = source_to_destination[vanilla_min]
            block = re.sub(
                r"<ValidLevel_Min>\d+</ValidLevel_Min>",
                f"<ValidLevel_Min>{destination_level}</ValidLevel_Min>",
                block,
                count=1,
            )
            changed_by_source[vanilla_min] += 1

        # Feral Were-Hammer replaces the beginner Were-Hammer route.
        if vanilla_min == 1 and action_name in {"NSC", "NSD_2"}:
            max_match = re.search(r"<ValidLevel_Max>(\d+)</ValidLevel_Max>", block)
            if max_match is not None and int(max_match.group(1)) == 15:
                block = re.sub(
                    r"<ValidLevel_Max>15</ValidLevel_Max>",
                    f"<ValidLevel_Max>{feral_destination - 1}</ValidLevel_Max>",
                    block,
                    count=1,
                )
                feral_cutoff_changes += 1

        return block

    new_text = action_pattern.sub(edit_action, text)

    missing_levels = [level for level, count in changed_by_source.items() if count == 0]
    if missing_levels:
        raise ValueError(
            "No gameplay actions were found for vanilla skill level(s): "
            f"{missing_levels}"
        )

    if feral_cutoff_changes != 2:
        raise ValueError(
            "Expected to update exactly two beginner Were-Hammer cutoff "
            f"actions (NSC and NSD_2), but updated {feral_cutoff_changes}."
        )

    output_path.write_text(new_text, encoding="utf-8")


SKILL_BLOCK_PATTERN = re.compile(
    r"<Lv(?P<level>\d+)>\s*"
    r"<Id>Lv(?P=level)</Id>\s*"
    r"<Command>(?P<command>.*?)</Command>\s*"
    r"<Lv>(?P=level)</Lv>\s*"
    r"</Lv(?P=level)>",
    re.DOTALL,
)


def _randomise_skill_parameter(
    source_path: Path,
    output_path: Path,
    progression: dict[int, int],
) -> dict[int, str]:
    text = source_path.read_text(encoding="utf-8")
    commands: dict[int, str] = {}

    for match in SKILL_BLOCK_PATTERN.finditer(text):
        level = int(match.group("level"))
        if 2 <= level <= 31:
            commands[level] = match.group("command")

    expected_levels = set(range(2, 32))
    if set(commands) != expected_levels:
        missing = sorted(expected_levels - set(commands))
        extra = sorted(set(commands) - expected_levels)
        raise ValueError(
            "SkillParameter Lv2-Lv31 entries did not match expectations. "
            f"Missing={missing}, extra={extra}"
        )

    replaced = 0

    def edit_skill_block(match: re.Match[str]) -> str:
        nonlocal replaced
        destination_level = int(match.group("level"))
        if not 2 <= destination_level <= 31:
            return match.group(0)

        source_skill = progression[destination_level]
        source_command = commands[source_skill]
        block = match.group(0)
        block = re.sub(
            r"<Command>.*?</Command>",
            f"<Command>{source_command}</Command>",
            block,
            count=1,
            flags=re.DOTALL,
        )
        replaced += 1
        return block

    new_text = SKILL_BLOCK_PATTERN.sub(edit_skill_block, text)
    if replaced != 30:
        raise ValueError(
            f"Expected to update 30 SkillParameter entries, but updated {replaced}."
        )

    output_path.write_text(new_text, encoding="utf-8")
    return commands


def _scan_fco_string_records(data: bytes) -> list[tuple[int, str, int]]:
    records: list[tuple[int, str, int]] = []

    for offset in range(0, len(data) - 8):
        length = int.from_bytes(data[offset : offset + 4], "big")
        if not 1 <= length <= 64:
            continue

        string_start = offset + 4
        string_end = string_start + length
        if string_end > len(data):
            continue

        raw = data[string_start:string_end]
        if not all(32 <= byte < 127 for byte in raw):
            continue

        padded_length = (length + 3) & ~3
        padded_end = string_start + padded_length
        if padded_end > len(data):
            continue

        padding = data[string_end:padded_end]
        if any(byte != 0x40 for byte in padding):
            continue

        try:
            value = raw.decode("ascii")
        except UnicodeDecodeError:
            continue

        records.append((offset, value, padded_end))

    return records


def _randomise_skill_name_fco(
    source_path: Path,
    output_path: Path,
    progression: dict[int, int],
) -> None:
    data = source_path.read_bytes()
    records = _scan_fco_string_records(data)
    target_names = {f"Lv{level}" for level in range(2, 32)}
    found: dict[int, tuple[int, int, int]] = {}

    for index, (record_start, value, payload_start) in enumerate(records):
        if value not in target_names:
            continue

        level = int(value[2:])
        if level in found:
            raise ValueError(f"FCO contains more than one target cell named {value}.")
        if index + 1 >= len(records):
            raise ValueError(f"Could not determine the end of FCO cell {value}.")

        next_record_start = records[index + 1][0]
        found[level] = (record_start, payload_start, next_record_start)

    expected_levels = set(range(2, 32))
    if set(found) != expected_levels:
        missing = sorted(expected_levels - set(found))
        raise ValueError(f"Missing FCO Skill cell(s): {missing}")

    prefixes: dict[int, bytes] = {}
    payloads: dict[int, bytes] = {}
    for level, (cell_start, payload_start, cell_end) in found.items():
        prefixes[level] = data[cell_start:payload_start]
        payloads[level] = data[payload_start:cell_end]

    replacements: list[tuple[int, int, bytes]] = []
    for destination_level in range(2, 32):
        source_skill = progression[destination_level]
        cell_start, _, cell_end = found[destination_level]
        replacement = prefixes[destination_level] + payloads[source_skill]
        replacements.append((cell_start, cell_end, replacement))

    new_data = data
    for start, end, replacement in sorted(replacements, reverse=True):
        new_data = new_data[:start] + replacement + new_data[end:]

    if len(new_data) != len(data):
        raise ValueError(
            f"FCO size changed unexpectedly: {len(data)} -> {len(new_data)} bytes."
        )

    output_path.write_bytes(new_data)


def _write_skill_spoiler_log(
    output_path: Path,
    seed_code: str,
    numeric_seed: int,
    progression: dict[int, int],
    commands: dict[int, str],
) -> Path:
    lines = [
        "SONIC UNLEASHED - WEREHOG SKILL RANDOMISATION",
        "=" * 70,
        f"Seed Code: {seed_code}",
        f"Derived Skill Seed: {numeric_seed}",
        "",
        "COMBAT LEVEL PROGRESSION",
        "-" * 70,
    ]

    for destination_level in range(2, 32):
        source_skill = progression[destination_level]
        lines.append(
            f"Level {destination_level:>2} -> {SKILL_NAMES[source_skill]} "
            f"[vanilla Lv{source_skill}; {commands[source_skill]}]"
        )

    lines.extend(
        [
            "",
            "DEPENDENCY RULES",
            "-" * 70,
            "Donkey Kick Combo < Knuckle Sandwich Combo < Unleashed Knuckle Sandwich",
            "Egg Scrambler < Ultimate Wild Combo < Unleashed Wild Combo",
            "Feral Were-Hammer < Werewheel Rush",
            "Feral Were-Hammer < Vertical Were-Hammer",
            "",
        ]
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def pack_evil_action_common(
    hedgearcpack_path: Path,
    print_output: bool = True,
) -> None:
    command = [
        str(hedgearcpack_path),
        str(EVIL_ACTION_COMMON_DIR),
        "-P",
        "-T=hh",
    ]

    if print_output:
        print()
        print("Packing +EvilActionCommon...")

    completed_process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    if print_output:
        if completed_process.stdout.strip():
            print(completed_process.stdout.strip())
        if completed_process.stderr.strip():
            print(completed_process.stderr.strip())
        print()

    if completed_process.returncode != 0:
        raise RuntimeError(
            "+EvilActionCommon packing failed with exit code "
            f"{completed_process.returncode}."
        )

    if print_output:
        print("+EvilActionCommon packed successfully.")


def pack_werehog_skill_archives(print_output: bool = True) -> None:
    hedgearcpack_path = get_hedgearcpack_path(BASE_DIR)

    if print_output:
        print()
        print("Packing +#Application...")

    application_result = pack_application(
        hedgearcpack_path=hedgearcpack_path,
        application_directory=APPLICATION_DIR,
        print_output=print_output,
    )
    if not application_result.success:
        raise RuntimeError(
            "Werehog skill files were written, but +#Application packing failed."
        )

    pack_evil_action_common(
        hedgearcpack_path=hedgearcpack_path,
        print_output=print_output,
    )


def reset_werehog_skills(
    pack_archives: bool = True,
    print_progress: bool = True,
) -> dict[str, int | bool]:
    if print_progress:
        print()
        print("RESETTING WEREHOG SKILLS TO VANILLA")

    restored = restore_clean_werehog_skills(print_progress=print_progress)

    if pack_archives:
        pack_werehog_skill_archives(print_output=print_progress)

    if print_progress:
        print()
        print("WEREHOG SKILL RESET COMPLETE")

    return {"files_restored": restored, "packed": pack_archives}


def randomise_werehog_skills(
    seed_code: str,
    log_path: str | Path | None = None,
    pack_archives: bool = True,
    print_progress: bool = True,
) -> dict[str, object]:
    seed_code = normalise_seed(seed_code)
    derived_seed = seed_to_integer(f"{seed_code}:{SKILL_SEED_NAMESPACE}")
    rng = random.Random(derived_seed)

    if print_progress:
        print()
        print("RANDOMISING WEREHOG COMBO UNLOCKS")
        print(f"Seed Code: {seed_code}")

    # Always restore from clean originals before applying a seed.
    restore_clean_werehog_skills(print_progress=print_progress)
    progression = generate_skill_progression(rng)

    _randomise_evil_attack_action(
        source_path=CLEAN_EVIL_ATTACK_ACTION,
        output_path=WORKING_EVIL_ATTACK_ACTION,
        progression=progression,
    )
    commands = _randomise_skill_parameter(
        source_path=CLEAN_SKILL_PARAMETER,
        output_path=WORKING_SKILL_PARAMETER,
        progression=progression,
    )
    _randomise_skill_name_fco(
        source_path=CLEAN_SKILL_NAME_FCO,
        output_path=WORKING_SKILL_NAME_FCO,
        progression=progression,
    )

    if log_path is None:
        log_path = DEFAULT_SKILL_LOG
    else:
        log_path = Path(log_path)

    written_log_path = _write_skill_spoiler_log(
        output_path=Path(log_path),
        seed_code=seed_code,
        numeric_seed=derived_seed,
        progression=progression,
        commands=commands,
    )

    if print_progress:
        print()
        print("GENERATED WEREHOG SKILL PROGRESSION")
        print("-" * 70)
        for destination_level in range(2, 32):
            source_skill = progression[destination_level]
            print(
                f"Level {destination_level:>2} -> "
                f"{SKILL_NAMES[source_skill]:<34} {commands[source_skill]}"
            )
        print()
        print(f"Werehog skill spoiler log: {written_log_path}")

    if pack_archives:
        pack_werehog_skill_archives(print_output=print_progress)

    if print_progress:
        print()
        print("WEREHOG SKILL RANDOMISATION COMPLETE")

    return {
        "seed_code": seed_code,
        "derived_seed": derived_seed,
        "progression": progression,
        "commands": commands,
        "log_path": written_log_path,
        "packed": pack_archives,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Randomise Sonic Unleashed Werehog Combat skill unlock progression."
        )
    )
    parser.add_argument(
        "--seed",
        default=None,
        help="Shareable seed code. Omit to generate one.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Restore vanilla Werehog skill files.",
    )
    parser.add_argument(
        "--no-pack",
        action="store_true",
        help="Write/reset the files without running HedgeArcPack.",
    )
    parser.add_argument(
        "--log",
        default=None,
        help="Optional Werehog skill spoiler-log path.",
    )
    args = parser.parse_args()

    if args.reset:
        reset_werehog_skills(
            pack_archives=not args.no_pack,
            print_progress=True,
        )
        return

    seed_code = generate_seed_code() if args.seed is None else normalise_seed(args.seed)
    randomise_werehog_skills(
        seed_code=seed_code,
        log_path=args.log,
        pack_archives=not args.no_pack,
        print_progress=True,
    )


if __name__ == "__main__":
    main()
