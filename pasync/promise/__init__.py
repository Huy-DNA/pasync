from __future__ import annotations

from enum import Enum
import inspect

from typing import Any, Callable, Awaitable, Generic, Optional, TypeVar, Union

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

class Promise(Generic[T1, E1, T2, E2], Awaitable):
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
                async def wrapper():
                    try:
                        resolve(await value)
                    except Exception as e:
                        reject(e)

                self.__awaitable = wrapper()

                return

            self.__awaitable = None

            nonlocal disable_error
            self.__result = value
            disable_error = True
            self.__state = PromiseState.Fulfilled

        def reject(error: Union[E1, Exception]):
            if inspect.isawaitable(error):
                async def wrapper():
                    try:
                        reject(await error)
                    except Exception as e:
                        reject(e)

                self.__awaitable = wrapper()

                return
            self.__awaitable = None
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
                
                if inspect.isawaitable(self.__result):
                    self.__result = await self.__result

                return self.__result
            except Exception as e:
                if not disable_error:
                    reject(e)
                else:
                    raise e
        
        self.__awaitable = asyncified()

    @property
    def state(self):
        return self.__state

    def __await__(self):
        result = None

        if not self.__awaitable:
            async def identity():
                return self.__result
            result = yield from identity().__await__()
        while self.__awaitable:
            result = yield from self.__awaitable.__await__()

        self.__result = result

        return result

    def then(
        self,
        next: Union[
            Callable[[T1], T2],
            Callable[[T1], Awaitable[T2]]],
        handle: Optional[Union[
            Callable[[E1], T2],
            Callable[[E1], Awaitable[T2]]]] = None,
    ) -> Promise[T2, E2, T3, E3]:
        async def thenify(
            resolve: Callable[[T2], None],
            reject: Callable[[Union[E2, Exception]], None],
        ) -> Any:
            await self
            try:
                match self.__state:
                    case PromiseState.Fulfilled:
                        any_result: Any = self.__result
                        resolve_result = next(any_result)
                        while inspect.isawaitable(resolve_result):
                            resolve_result = await resolve_result
                        resolve_result: Any = resolve_result
                        resolve(resolve_result)
                        return resolve_result
                    case PromiseState.Error:
                        any_error: Any = self.__error
                        if not handle:
                            reject(any_error)
                            return
                        handle_result: Any = handle(any_error)
                        while inspect.isawaitable(handle_result):
                            handle_result = await handle_result 
                        resolve(handle_result)
                        return handle_result
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
            await self
            try:
                if self.__state == PromiseState.Error:
                    any_error: Any = self.__error
                    handle_result = handle(any_error)
                    while inspect.isawaitable(handle_result):
                        handle_result = await handle_result 
                    handle_result: Any = handle_result
                    resolve(handle_result)
                elif self.__state == PromiseState.Fulfilled:
                    any_result: Any = self.__result
                    resolve(any_result)
            except Exception as e:
                reject(e)

        return Promise(catchify)
