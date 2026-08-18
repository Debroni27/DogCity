"""Базовая иерархия доменных ошибок."""

__all__ = (
    "DomainError",
    "IllegalStateTransitionError",
    "InvariantViolationError",
    "ValidationError",
)


class DomainError(Exception):
    """Общий предок ошибок домена. Точка перехвата на границе приложения."""


class ValidationError(DomainError):
    """Значение непригодно само по себе. Возбуждается в ``__post_init__`` VO."""

    def __init__(self, field: str, reason: str) -> None:
        super().__init__(field, reason)
        self.field = field
        self.reason = reason

    def __str__(self) -> str:
        return f"{self.field}: {self.reason}"


class InvariantViolationError(DomainError):
    """Сочетание корректных значений нарушает правило агрегата."""


class IllegalStateTransitionError(DomainError):
    """Переход недопустим в текущем состоянии сущности."""

    def __init__(self, entity: str, current_state: str, transition: str) -> None:
        super().__init__(entity, current_state, transition)
        self.entity = entity
        self.current_state = current_state
        self.transition = transition

    def __str__(self) -> str:
        return (
            f"{self.entity}: переход «{self.transition}» недопустим "
            f"из состояния «{self.current_state}»"
        )
