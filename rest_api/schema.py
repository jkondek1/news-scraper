import re

from pydantic import BaseModel, field_validator


class KeywordRequest(BaseModel):
    keywords: list

    @field_validator('keywords')
    def check_all_keywords(cls, kw_list):
        lowered = []
        for kw in kw_list:
            if not isinstance(kw, str):
                raise TypeError('keyword is not of type string')
            if re.search('[^a-z]+', kw):
                raise ValueError('keyword contains invalid characters')
            lowered.append(kw.lower())
        return lowered
