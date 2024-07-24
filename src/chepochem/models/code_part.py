from pathlib import Path

from attr import frozen

from chepochem.models.position import Position


@frozen(slots=True)
class CodePart:
    code: str
    file_name: Path
    position: Position
    called_in: list["CodePart"]
    calls: list["CodePart"]
