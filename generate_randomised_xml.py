from pathlib import Path
import sys

from packer import pack_application
from spoiler_log import write_spoiler_log
from data import LevelState
from xml_writer import write_xml_assignments

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
    application_directory = base_directory / "#Application"
    hedgearcpack_path = base_directory / "HedgeArcPack.exe"
    spoiler_log_path = base_directory / "randomiser_log.txt"

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


    level_state = LevelState()

    participating_levels = get_non_dlc_levels(
        level_state
    )

    first_stage_pool = get_no_upgrade_levels(
        participating_levels
    )

    assignments, validation_result = generate_valid_randomiser_assignments(
    entrances=participating_levels,
    randomisable_stages=participating_levels,
    first_entrance=level_state.WID1,
    first_stage_pool=first_stage_pool,
    seed=numeric_seed,
    fixed_levels=set(),
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
    print("#Application is ready to pack.")


    written_log_path = write_spoiler_log(
        seed_code=seed_code,
        assignments=assignments,
        validation_result=validation_result,
        output_path=spoiler_log_path,
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
            "but HedgeArcPack failed to pack #Application."
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
    print("Application archive packed successfully.")
    print()
    print("Keep the seed code to reproduce this randomisation.")

if __name__ == "__main__":
    main()