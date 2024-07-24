from attr import frozen


@frozen(slots=True)
class Position:
    line: int
    column: int
