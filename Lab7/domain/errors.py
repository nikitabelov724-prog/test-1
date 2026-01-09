class DomainError(Exception):
    """Base domain exception."""


class EmptyOrderError(DomainError):
    pass


class OrderAlreadyPaidError(DomainError):
    pass


class OrderLockedError(DomainError):
    pass
