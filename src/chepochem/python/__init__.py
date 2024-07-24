from pathlib import Path

from attr import field, frozen

from chepochem.adapters.code_navigation.code_navigation import (
    CodeNavigation,
    Definition,
)
from chepochem.models.code_part import CodePart
from chepochem.models.position import Position


@frozen(slots=True)
class PythonProjectLoader:
    code_navigation: CodeNavigation
    __revised: dict[tuple[str, Position], CodePart] = field(factory=dict)

    def _build_code_part(self, file: Path, definition: Definition) -> CodePart:
        _start_position = definition.start_position
        if not _start_position:
            raise ValueError(f"Failed to get start position for {definition}")

        definition_key: tuple[str, Position] = (str(file), _start_position)
        if definition_key in self.__revised:
            code_part = self.__revised[definition_key]
        else:
            called_in: list[CodePart] = []
            for reference in self.code_navigation.get_references(file, _start_position):
                called_in.append(
                    self._build_code_part(
                        reference.file,
                        reference,
                    )
                )

            file_code = file.read_text()
            code_part = CodePart(
                self.__get_code(
                    file_code,
                    _start_position,
                    definition.end_position,
                ),
                file,
                _start_position,
                called_in,
                [],
            )
            self.__revised[definition_key] = code_part

        for called_in_code_part in code_part.called_in:
            called_in_code_part.calls.append(code_part)

        return code_part

    def __get_code(
        self, code: str, start_position: Position, end_position: Position
    ) -> str:
        splitted_code = code.split("\n")
        return "\n".join(splitted_code[start_position.line : end_position.line])
