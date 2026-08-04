from pathlib import Path

from data import LevelState
from medal_validator import StageAssignment
from xml_writer import write_xml_assignments


level_state = LevelState()

assignments = [
    StageAssignment(
        entrance=level_state.WID2,
        stage=level_state.SCN1,
    ),
    StageAssignment(
        entrance=level_state.SCN1,
        stage=level_state.WID2,
    ),
]


write_xml_assignments(
    assignments=assignments,
    source_directory=Path("Stages"),
    output_directory=Path("#Application"),
    create_backup=True,
    print_progress=True,
)