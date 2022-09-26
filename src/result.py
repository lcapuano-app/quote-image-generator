import functools
import logging
from typing import Any, Callable, Generic, NoReturn, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E", bound=BaseException)


class Err(Generic[T, E]):
    _err: E
    __match_args__ = ("_err",)

    def __init__(self, err: E):
        self._err = err

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Err):
            return self._err == other._err  # type: ignore
        return False

    def unwrap(self) -> NoReturn:
        raise self._err

    def unwrap_or(self, default: T) -> T:
        return default

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return op(self._err)

    def __repr__(self) -> str:
        return f"Err({repr(self._err)})"


class Ok(Generic[T, E]):

    _value: T
    __match_args__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value  # type: ignore
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self.unwrap()

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.unwrap()

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"

class Some(Generic[T, E]):

    _value: T
    __match_args__ = ("_value",)

    def __init__(self, value: T):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Ok):
            return self._value == other._value  # type: ignore
        return False

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, default: T) -> T:
        return self.unwrap()

    def unwrap_or_else(self, op: Callable[[E], T]) -> T:
        return self.unwrap()

    def __repr__(self) -> str:
        return f"Ok({repr(self._value)})"


Result = Union[Ok[T, E], Some[T, E], Err[T, E]]


def _log_exception( err_level: str, err: Exception ) -> None:

    match err_level:
        case 'error': 
            logging.error( err, exc_info=True )
        case 'info': 
            logging.info( err )
        case 'debug' | 'degug' | 'degub':
            logging.debug( err )
        case 'warn' | 'warning':
            logging.warn( err )
        case 'critical':
            logging.critical( err, exc_info=True )
        case _:
            logging.fatal( err, exc_info=True )


def result_ok_err( err_level = 'error' ):
    def wrapper( fn ):
        @functools.wraps(fn)
        def inner( *args, **kwargs ) -> Union[Ok[T, E], Err[T, E]]:
            try:
                fn_result = fn(*args, **kwargs)
                return Ok(fn_result)
            except Exception as err:
                _log_exception( err_level, err )
                return Err(err)

        return inner

    return wrapper