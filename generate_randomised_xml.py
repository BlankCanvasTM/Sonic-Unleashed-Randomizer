from pathlib import Path
import secrets
import sys

from packer import pack_application
from spoiler_log import write_spoiler_log
from data import LevelState
from xml_writer import write_xml_assignments
from enemy_randomiser import randomise_all_night_stages

from assignment_generator import (
    generate_valid_randomiser_assignments,
    get_no_upgrade_levels,
    get_non_dlc_levels,
)

from seed_system import (
    generate_seed_code,
    normalise_seed,
    seed_to_integer,
)



def get_base_directory() -> Path:

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def main() -> None:

    base_directory = get_base_directory()

    source_directory = base_directory / "Stages"
    application_directory = base_directory / "+#Application"
    hedgearcpack_path = base_directory / "HedgeArcPack.exe"
    spoiler_log_path = base_directory / "randomiser_log.txt"
    enemy_spoiler_log_path = base_directory / "enemy_spoiler_log.txt"

    while True:
        dlc_input = input(
            "\nInclude DLC stages? [Y/N]: "
        ).strip().lower()

        if dlc_input in {"y", "yes"}:
            include_dlc = True
            break

        if dlc_input in {"n", "no"}:
            include_dlc = False
            break

        print("Please enter Y or N.")

    while True:
        enemy_input = input(
            "\nRandomise Night stage enemies? [Y/N]: "
        ).strip().lower()

        if enemy_input in {"y", "yes"}:
            randomise_enemies = True
            break

        if enemy_input in {"n", "no"}:
            randomise_enemies = False
            break

        print("Please enter Y or N.")

    enemy_seed = None

    if randomise_enemies:
        enemy_seed_input = input(
            "\nEnter an enemy seed "
            "(leave blank to generate one): "
        ).strip()

        if enemy_seed_input:
            try:
                enemy_seed = int(enemy_seed_input)
            except ValueError as exc:
                raise ValueError(
                    "Enemy seed must be a whole number."
                ) from exc
        else:
            enemy_seed = secrets.randbits(64)

    seed_input = input(
        "\nEnter a seed code "
        "(leave blank to generate one): "
    ).strip()


    if seed_input:
        seed_code = normalise_seed(seed_input)
    else:
        seed_code = generate_seed_code()

    numeric_seed = seed_to_integer(seed_code)

    print()
    print(f"Seed Code: {seed_code}")
    print(f"DLC Included: {'Yes' if include_dlc else 'No'}")
    print(
        f"Enemy Randomisation: "
        f"{'Yes' if randomise_enemies else 'No'}"
    )

    if randomise_enemies:
        print(f"Enemy Seed: {enemy_seed}")


    level_state = LevelState()

    if include_dlc:
        participating_levels = level_state.levels
    else:
        participating_levels = get_non_dlc_levels(
            level_state
        )

    first_stage_pool = get_no_upgrade_levels(
        participating_levels
    )

    #fixed_levels = {
    #level_state.BOSS_DARK_GUARDIAN,
    #level_state.BOSS_DARK_GAIA_PHEONIX,
    #level_state.BOSS_DARK_MORAY,
#}

    fixed_levels = set()

    if include_dlc:
        fixed_levels.update({
            level_state.WID2_2,
            level_state.WIN1_3,
            level_state.SCD3_2,
            level_state.RRD1_2,
            level_state.RRD2_2,
            level_state.RRD4,
            level_state.RRD5,
            level_state.RRN1_2,
            level_state.CED1_2,
            level_state.CED2_2,
            level_state.CED3,
            level_state.CED4,
            level_state.CEN2,
            level_state.CEN3,
            level_state.DRD1_2,
            level_state.DRD2_2,
            level_state.DRN1_2,
            level_state.ASD1_2,
            level_state.ASD3,
            level_state.ASN2,
            level_state.SSD1_2,
            level_state.SSN2,
            level_state.JJD1_2,
            level_state.JJN1_2,
            level_state.SCD1_2,
            level_state.SCD5,
            level_state.JJN3,
            level_state.SSN3,
            level_state.WID1_2,
        })

    assignments, validation_result = generate_valid_randomiser_assignments(
    entrances=participating_levels,
    randomisable_stages=participating_levels,
    first_entrance=level_state.WID1,
    first_stage_pool=first_stage_pool,
    seed=numeric_seed,
    fixed_levels=fixed_levels,
    max_attempts=10_000,
    print_attempts=True,
)

    print()
    print("VALID RANDOMISATION FOUND")
    print()

    for assignment in assignments:
        print(
            f"{assignment.entrance.name:<40} "
            f"-> {assignment.stage.name}"
        )


    if not validation_result.valid:
        raise RuntimeError(
            "The generated assignments failed final validation."
        )


    write_xml_assignments(
    assignments=assignments,
    source_directory=source_directory,
    output_directory=application_directory,
    print_progress=True,
)

    print()
    print("RANDOMISED XML FILES READY")
    print(
        f"Completed entrances: "
        f"{validation_result.completed_entrances}/"
        f"{validation_result.total_entrances}"
    )
    print(
        f"Maximum obtainable medals: "
        f"{validation_result.final_sun_medals} Sun, "
        f"{validation_result.final_moon_medals} Moon"
    )
    print()
    print("+#Application is ready to pack.")


    written_log_path = write_spoiler_log(
        seed_code=seed_code,
        assignments=assignments,
        validation_result=validation_result,
        output_path=spoiler_log_path,
        include_dlc=include_dlc,
        fixed_levels=fixed_levels,
    )

    print(f"Spoiler log written to: {written_log_path}")


    pack_result = pack_application(
        hedgearcpack_path=hedgearcpack_path,
        application_directory=application_directory,
        print_output=True,
    )

    if not pack_result.success:
        raise RuntimeError(
            "The randomised XML files were generated successfully, "
            "but HedgeArcPack failed to pack +#Application."
        )

    enemy_result = None

    if randomise_enemies:
        print()
        print("RANDOMISING NIGHT STAGE ENEMIES")

        enemy_result = randomise_all_night_stages(
            seed=enemy_seed,
            log_path=enemy_spoiler_log_path,
            pack_archives=True,
            print_progress=True,
        )

    print()
    print("RANDOMISATION COMPLETE")
    print(f"Seed Code: {seed_code}")
    print(
        f"Validated entrances: "
        f"{validation_result.completed_entrances}/"
        f"{validation_result.total_entrances}"
    )
    print(
        f"Maximum obtainable medals: "
        f"{validation_result.final_sun_medals} Sun, "
        f"{validation_result.final_moon_medals} Moon"
    )
    print(f"Spoiler log: {written_log_path}")

    if enemy_result is not None:
        print(f"Enemy seed: {enemy_seed}")
        print(
            f"Enemy spoiler log: "
            f"{enemy_result['log_path']}"
        )

    print("Application archive packed successfully.")
    print()
    print("Keep the seed code to reproduce this randomisation.")

    if randomise_enemies:
        print(
            "Keep the enemy seed to reproduce the same "
            "enemy randomisation."
        )

if __name__ == "__main__":
    main()