from pathlib import Path

from attr import frozen


@frozen(slots=True)
class MetadataFlags:
    file_name: bool = False
    position: bool = False
    called_in: bool = False
    calls: bool = False
