from dataclasses import dataclass
from typing import Any

from data import Level, Stage, Shoe

@dataclass

class StageAssignment:
    entrance: Level
    stage: Level

def find_assignment_from_entrance(entrance: Level, assignments: list[StageAssignment]) -> StageAssignment | None:
    for assignment in assignments:
        if assignment.entrance == entrance: return assignment
    return None

@dataclass
class BlockedEntrance:
    entrance_name: str
    medal_type: str | None
    required_medals: int
    available_medals: int
    parent_name: str | None
    parent_completed: bool


@dataclass
class AccessibilityValidationResult:
    valid: bool
    final_sun_medals: int
    final_moon_medals: int
    completed_entrances: int
    total_entrances: int
    blocked_entrances: list[BlockedEntrance]

def get_required_medal_type(entrance: Level) -> str | None:
    return "moon" if entrance.type.value & 1 else "sun"


def validate_accessible_progression(
    assignments: list[StageAssignment],
    print_progress: bool = False,
) -> AccessibilityValidationResult:


    current_sun = 0
    current_moon = 0
    starting_entrance = None
    for assignment in assignments:
        if assignment.entrance.parent == None: starting_entrance = assignment

    blocked = []
    last_blocked = []
    queued = [starting_entrance]
    has_shoe = [Shoe.NONE]
    total_sun = 0
    total_moon = 0
    while True:
        complete = [starting_entrance]
        for queue in queued:
            for child in queue.entrance.children:
                child_assignment = find_assignment_from_entrance(child, assignments)
                if not child_assignment: continue
                if not child_assignment.entrance.recv_shoe in has_shoe:
                    has_shoe.append(child_assignment.entrance.recv_shoe)
                has_shoes = True
                for shoe in child_assignment.stage.req_shoe:
                    if not shoe in has_shoe:
                        has_shoes = False
                stage_blocked = False
                if not has_shoes:
                    stage_blocked = True
                if get_required_medal_type(child) == "moon" and total_moon < child_assignment.entrance.required_medal:
                    stage_blocked = True
                if get_required_medal_type(child) == "sun" and total_sun < child_assignment.entrance.required_medal:
                    stage_blocked = True
                if stage_blocked:
                    blocked.append(child_assignment)
                else:
                    complete.append(child_assignment)
                    queued.append(child_assignment)
        queued = [starting_entrance]
        total_sun = 0
        total_moon = 0
        for complete_stage in complete:
            total_sun += complete_stage.stage.sun
            total_moon += complete_stage.stage.moon
        is_stuck = False
        if len(blocked) == 0:
            break
        is_stuck = len(last_blocked) != 0
        for block in last_blocked:
            if not block in blocked:
                is_stuck = False
        if is_stuck:
            break
        last_blocked = blocked
        blocked = []

    blocked_entrances: list[BlockedEntrance] = []
    return AccessibilityValidationResult(
        valid=not is_stuck,
        final_sun_medals=total_sun,
        final_moon_medals=total_moon,
        completed_entrances=len(complete),
        total_entrances=len(assignments),
        blocked_entrances=blocked_entrances,
    )

    