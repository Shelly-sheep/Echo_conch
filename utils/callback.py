from __future__ import annotations
import asyncio
from typing import Any,AsyncIterable,Dict,List,Literal,Union,cast
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult

class CustomAsyncIteratorCallbackHandler(AsyncCallbackHandler):
    """ Callback handler that returns an async iterator."""
    queue: asyncio.Queue[str]
    done: asyncio.Event

    @property
    def always_verbose(self) -> bool:
        return True
    def __init__(self) -> None:
        self.queue = asyncio.Queue()
        self.done = asyncio.Event()
        self.answer_prefix_tokens = ["Final","Answer",":"]
        self.answer_reached = False
        self.last_tokens = [""] * len(self.answer_prefix_tokens)

    async def on_llm_start(
            self, serialized:Dict[str,Any], prompts:List[str], **kwargs:Any
        ) -> None:
            self.done.clear()
            self.answer_reached = False

    async def on_llm_new_token(self, token:str,**kwargs:Any) -> None:
        if token is not None and token != "":
            self.last_tokens.append(token.strip())
            if len(self.last_tokens) > len(self.answer_prefix_tokens) + 1:
                self.last_tokens.pop(0)
            if self.last_tokens[:-1] == self.answer_prefix_tokens:
                self.answer_reached = True
            if self.answer_reached:
                 self.queue.put_nowait(token)

    async def on_llm_end(self, response:LLMResult,**kwargs:Any) -> None:
        if self.answer_reached:
            self.done.set()

    async def an_llm_error(self,error:BaseException,**kwargs:Any) -> None:
        self.done.set()

    async def aiter(self) -> AsyncIterable[str]:
        while not self.queue.empty() or not self.done.is_set():
            done,other = await asyncio.wait(
                [
                    asyncio.ensure_future(self.queue.get()),
                    asyncio.ensure_future(self.done.wait()),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )

            if other:
                other.pop().cancel()

            #提取完成的任务
            token_or_done = cast(Union[str,Literal[True]],done.pop().result())
            if token_or_done is True:
                break

            yield token_or_done