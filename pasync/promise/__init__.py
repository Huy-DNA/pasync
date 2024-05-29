from __future__ import annotations

from enum import Enum
import inspect

from typing import Any, Callable, Awaitable, Generic, Optional, TypeVar, Union

from pasync.task import Task as _Task

T1 = TypeVar("T1")
E1 = TypeVar("E1")
T2 = TypeVar("T2")
E2 = TypeVar("E2")
T3 = TypeVar("T3")
E3 = TypeVar("E3")

class PromiseState(Enum):
    Uninitiated = 0
    Pending = 1
    Fulfilled = 2
    Error = 3

class Promise(Generic[T1, E1, T2, E2]):
    def __init__(
        self,
        callback: Union[
            Callable[[Callable[[T1], None], Callable[[Union[E1, Exception]], None]], Any],
            Callable[[Callable[[T1], None], Callable[[Union[E1, Exception]], None]], Awaitable[T1]]]
    ):
        self.__state = PromiseState.Uninitiated
        self.__result: Optional[T1] = None
        self.__error: Optional[Union[E1, Exception]] = None
        disable_error = False

        def resolve(value: T1):
            if inspect.isawaitable(value):
                self.__task = _Task(value)
                return
            nonlocal disable_error
            self.__result = value
            disable_error = True
            self.__state = PromiseState.Fulfilled

        def reject(error: Union[E1, Exception]):
            nonlocal disable_error
            self.__error = error
            disable_error = True
            self.__state = PromiseState.Error

        async def asyncified():
            try:
                self.__state = PromiseState.Pending
                result = callback(resolve, reject)
                if inspect.isawaitable(result):
                    await result
            except Exception as e:
                if not disable_error:
                    reject(e)
        
        self.__awaitable = asyncified()
        self.__task = _Task(self.__awaitable)

    @property
    def state(self):
        return self.__state

    @property
    def task(self):
        return self.__task

    def then(
        self,
        next: Union[
            Callable[[T1], T2],
            Callable[[T1], Awaitable[T2]]],
        handle: Optional[Union[
            Callable[[E1], T2],
            Callable[[E1], Awaitable[T2]]]],
    ) -> Promise[T2, E2, T3, E3]:
        async def thenify(
            resolve: Callable[[T2], None],
            reject: Callable[[Union[E2, Exception]], None],
        ) -> Any:
            await self.__awaitable
            try:
                match self.__state:
                    case PromiseState.Fulfilled:
                        any_result: Any = self.__result
                        resolve_result = next(any_result)
                        while inspect.isawaitable(resolve_result):
                            resolve_result = await resolve_result
                        resolve_result: Any = resolve_result
                        resolve(resolve_result)
                    case PromiseState.Error:
                        any_error: Any = self.__error
                        if not handle:
                            reject(any_error)
                            return
                        handle_result = handle(any_error)
                        while inspect.isawaitable(handle_result):
                            handle_result = await handle_result 
                        handle_result: Any = handle_result
                        resolve(handle_result)
            except Exception as e:
                reject(e)

        return Promise(thenify)
    
    def catch(
        self,
        handle: Union[
            Callable[[E1], T2],
            Callable[[E1], Awaitable[T2]]],
    ) -> Promise[T2, E2, T3, E3]:
        async def catchify(
            resolve: Callable[[T2], None],
            reject: Callable[[Union[E2, Exception]], None],
        ) -> Any:
            await self.__awaitable
            try:
                if self.__state == PromiseState.Error:
                    any_error: Any = self.__error
                    handle_result = handle(any_error)
                    while inspect.isawaitable(handle_result):
                        handle_result = await handle_result 
                    handle_result: Any = handle_result
                    resolve(handle_result)
            except Exception as e:
                reject(e)

        return Promise(catchify)
