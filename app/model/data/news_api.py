# -*- coding: utf-8 -*-

from pydantic import BaseModel


class NewsArticleOutput(BaseModel):
    title: str
    authors: list[str]
    text: str
