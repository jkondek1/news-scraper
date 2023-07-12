import re

from pydantic import BaseModel, field_validator


class KeywordRequest(BaseModel):
    """
    request class for api service
    """
    keywords: list

    @field_validator('keywords')
    def check_all_keywords(cls, kw_list):
        lowered = []
        for kw in kw_list:
            if not isinstance(kw, str):
                raise ValueError('keyword is not of type string')
            kw_decap = kw.lower()
            match = re.search(r'\W+', kw_decap)
            if match:
                raise ValueError(f'keyword contains invalid characters: {match.group()}')
            lowered.append(kw_decap)
        return lowered
