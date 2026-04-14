from pydantic import BaseModel


class FilterOption(BaseModel):
    label: str
    value: str
    count: int


class FilterGroup(BaseModel):
    key: str
    label: str
    options: list[FilterOption]
