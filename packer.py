from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class PackResult:
    success: bool
    executable_path: Path
    application_directory: Path
    return_code: int
    stdout: str
    stderr: str


def pack_application(
    hedgearcpack_path: str | Path,
    application_directory: str | Path,
    print_output: bool = True,
) -> PackResult:

    hedgearcpack_path = Path(hedgearcpack_path)
    application_directory = Path(application_directory)

    if not hedgearcpack_path.is_file():
        raise FileNotFoundError(
            f"HedgeArcPack executable was not found: "
            f"{hedgearcpack_path}"
        )

    if not application_directory.is_dir():
        raise FileNotFoundError(
            f"#Application directory was not found: "
            f"{application_directory}"
        )

    command = [
        str(hedgearcpack_path),
        str(application_directory),
        "-P",
        "-T=hh",
    ]

    if print_output:
        print("Packing command:")
        print(" ".join(f'"{part}"' for part in command))
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
        application_directory=application_directory,
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

    return result