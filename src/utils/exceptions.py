TABLE_ALREADY_EXISTS = "Table with this name already exists."
TABLE_NOT_FOUND = "Table with this id does not exist."

RESERVATION_CONFLICT = "Table is already reserved for this time."
RESERVATION_NOT_FOUND =  "Reservation with this id does not exist."


class UniqueConstraintError(ValueError):
    def __init__(self):
        super().__init__(TABLE_ALREADY_EXISTS)


class ForeignKeyError(ValueError):
    def __init__(self):
        super().__init__(TABLE_NOT_FOUND)


class ReservationConflictError(ValueError):
    def __init__(self):
        super().__init__(RESERVATION_CONFLICT)
