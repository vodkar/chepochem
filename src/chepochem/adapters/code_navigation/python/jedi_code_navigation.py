from functools import cache
from pathlib import Path
from typing import Any, Optional, Union

import jedi
import jedi.api.classes as jedi_classes
from attr import frozen

from chepochem.adapters.code_navigation.code_navigation import (
    CodeNavigation,
    Definition,
)
from chepochem.adapters.code_navigation.Position import Position
from chepochem.models.code_part import CodePart


class JediPosition(Position):
    @classmethod
    def from_jedi_position(cls, jedi_position: Optional[Any]):
        if not jedi_position:
            raise ValueError(f"Failed to construct position")
        if (
            isinstance(jedi_position, tuple)
            and isinstance(jedi_position[0], int)
            and isinstance(jedi_position[1], int)
        ):
            return JediPosition(int(jedi_position[0]), int(jedi_position[1]))
        raise ValueError(f"Invalid start position {jedi_position}")


@frozen(slots=True)
class JediDefinition(Definition):
    _name: jedi_classes.Name

    @property
    def start_position(self) -> Position:
        return JediPosition.from_jedi_position(
            self._name.get_definition_start_position()
        )

    @property
    def end_position(self) -> Position:
        return JediPosition.from_jedi_position(self._name.get_definition_end_position())


class JediCodeNavigation(CodeNavigation):
    @classmethod
    def load_project(cls, project: Path):
        return cls(project)

    def __init__(self, project: Path):
        self.project = project
        self.__revised: dict[tuple[str, int, int], CodePart] = {}

    def get_definitions(self, file: Path) -> list[Definition]:
        jedi_script = self._get_jedi_file(file)
        definitions: list[Definition] = []
        for definition in jedi_script.get_names():
            if definition.description.startswith("def "):
                definitions.append(
                    JediDefinition(
                        file,
                        JediPosition.from_jedi_position(
                            definition.get_definition_start_position()
                        ),
                        definition,
                    )
                )
        return definitions

    def get_references(self, file: Path, position: Position) -> list[Definition]:
        jedi_script = self._get_jedi_file(file)
        references: list[Definition] = []
        for reference in jedi_script.get_references(position.line, position.column):
            references.append(
                JediDefinition(
                    file,
                    JediPosition.from_jedi_position(
                        reference.get_definition_start_position()
                    ),
                    reference,
                )
            )
        return references

    @cache
    def _get_jedi_project(self):
        return jedi.Project(self.project)

    @cache
    def _get_jedi_file(self, py_file: Union[Path, str]):
        return jedi.Script(path=str(py_file), project=self._get_jedi_project())
