# -*- coding: utf-8 -*-

from pydantic import BaseModel


class NewsArticleOutput(BaseModel):
    title: str
    authors: list[str]
    # publish_date: Union[datetime.date, str]
    text: str
