from pathlib import Path
import secrets
import sys
import shutil

from packer import pack_application, get_hedgearcpack_path
from spoiler_log import write_spoiler_log
from data import LevelState
from xml_writer import write_xml_assignments


from enemy_randomiser import (
    randomise_all_night_stages,
    reset_all_night_stages,
)

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

from werehog_skill_randomiser import (
    pack_evil_action_common,
    randomise_werehog_skills,
    reset_werehog_skills,
)



def get_base_directory() -> Path:

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent

def reset_stages_to_vanilla(
    source_directory: Path,
    application_directory: Path,
) -> int:

    if not source_directory.is_dir():
        raise FileNotFoundError(
            f"Stages folder was not found: {source_directory}"
        )

    if not application_directory.is_dir():
        raise FileNotFoundError(
            f"+#Application folder was not found: {application_directory}"
        )

    restored_count = 0

    for source_file in sorted(source_directory.glob("*.seq.xml")):
        destination_file = application_directory / source_file.name

        shutil.copy2(
            source_file,
            destination_file,
        )

        restored_count += 1

    return restored_count


def ask_yes_no(prompt: str) -> bool:
    while True:
        answer = input(prompt).strip().lower()

        if answer in {"y", "yes"}:
            return True

        if answer in {"n", "no"}:
            return False

        print("Please enter Y or N.")


def main() -> None:

    base_directory = get_base_directory()

    source_directory = base_directory / "Stages"
    application_directory = base_directory / "+#Application"
    hedgearcpack_path = get_hedgearcpack_path(base_directory)
    spoiler_log_path = base_directory / "randomiser_log.txt"
    enemy_spoiler_log_path = base_directory / "enemy_spoiler_log.txt"
    skill_spoiler_log_path = base_directory / "werehog_skill_spoiler_log.txt"

    reset_stages = False
    reset_enemies = False
    reset_skills = False

    reset_files = ask_yes_no(
    "\nReset files to vanilla? [Y/N]: "
    )

    if reset_files:
        while True:
            print()
            print("What would you like to reset?")
            print("1. Stages only")
            print("2. Enemies only")
            print("3. Werehog skills only")
            print("4. Everything")
            print()

            reset_choice = input(
                "\nSelect an option [1/2/3/4]: "
            ).strip()

            if reset_choice in {"1", "2", "3", "4"}:
                break

            print("Please enter 1, 2, 3 or 4.")

        reset_stages = reset_choice in {"1", "4"}
        reset_enemies = reset_choice in {"2", "4"}
        reset_skills = reset_choice in {"3", "4"}

        application_needs_pack = False

        if reset_stages:
            print()
            print("RESETTING STAGES TO VANILLA")

            restored_stage_files = reset_stages_to_vanilla(
                source_directory=source_directory,
                application_directory=application_directory,
            )

            print(
                f"Stage sequence files restored: "
                f"{restored_stage_files}"
            )

            application_needs_pack = True

        if reset_skills:
            print()

            reset_werehog_skills(
                pack_archives=False,
                print_progress=True,
            )

            application_needs_pack = True

        if application_needs_pack:
            pack_result = pack_application(
                hedgearcpack_path=hedgearcpack_path,
                application_directory=application_directory,
                print_output=True,
            )

            if not pack_result.success:
                raise RuntimeError(
                    "Files were restored, but "
                    "+#Application packing failed."
                )

        if reset_skills:
            pack_evil_action_common(
                hedgearcpack_path=hedgearcpack_path,
                print_output=True,
            )

        if reset_enemies:
            reset_all_night_stages(
                pack_archives=True,
                print_progress=True,
            )

    randomise_stages = ask_yes_no(
        "\nRandomise stages? [Y/N]: "
    )
                    
    include_dlc = False

    if randomise_stages:
        include_dlc = ask_yes_no(
            "\nInclude DLC stages? [Y/N]: "
        )

    randomise_enemies = ask_yes_no(
        "\nRandomise Night stage enemies? [Y/N]: "
    )

    randomise_skills = ask_yes_no(
        "\nRandomise Werehog combo unlocks? [Y/N]: "
    )

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

    seed_code = None
    numeric_seed = None

    if randomise_stages or randomise_skills:
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

        if randomise_stages:
            print(f"DLC Included: {'Yes' if include_dlc else 'No'}")

    print(
        f"Enemy Randomisation: "
        f"{'Yes' if randomise_enemies else 'No'}"
    )

    if randomise_enemies:
        print(f"Enemy Seed: {enemy_seed}")



    if randomise_stages:

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


    skill_result = None

    if randomise_skills:
        print()
        print("RANDOMISING WEREHOG SKILLS")

        skill_result = randomise_werehog_skills(
            seed_code=seed_code,
            log_path=skill_spoiler_log_path,
            pack_archives=False,
            print_progress=True,
        )

    if randomise_stages or randomise_skills:
        pack_result = pack_application(
            hedgearcpack_path=hedgearcpack_path,
            application_directory=application_directory,
            print_output=True,
        )

        if not pack_result.success:
            raise RuntimeError(
                "Randomisation completed, but "
                "HedgeArcPack failed to pack +#Application."
            )

    if randomise_skills:
        pack_evil_action_common(
            hedgearcpack_path=hedgearcpack_path,
            print_output=True,
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

    if randomise_stages or randomise_skills:
        print(f"Seed Code: {seed_code}")

    if randomise_stages:
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

    else:
        print()
        print("Stage Randomisation: No")

    if randomise_skills:
        print()
        print("Werehog Skill Randomisation: Yes")
        print(f"Werehog skill spoiler log: {skill_spoiler_log_path}")

    else:
        print()
        print("Werehog Skill Randomisation: No")

    if randomise_enemies:
        print()
        print("Enemy Randomisation: Yes")
        print(f"Enemy Seed: {enemy_seed}")
        print(f"Enemy spoiler log: {enemy_spoiler_log_path}")

    else:
        print()
        print("Enemy Randomisation: No")


    if randomise_stages or randomise_skills:
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