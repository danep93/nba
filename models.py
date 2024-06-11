from typing import Union, List, Optional
from pydantic import BaseModel, field_validator, Field

from constants import COMPARE_METRICS


class PlayerGameOBT(BaseModel):
    GAME_ID: str
    TEAM_ID: str
    PLAYER_ID: str
    SEASON_ID: str
    GAME_ID: str
    GAME_DATE: str
    PLAYER_NAME: str
    START_POSITION: str
    MIN: int
    FGM: int
    FGA: int
    FG_PCT: float
    FG3M: int
    FG3A: int
    FG3_PCT: float
    FTM: int
    FTA: int
    FT_PCT: float
    OREB: int
    DREB: int
    REB: int
    AST: int
    STL: int
    BLK: int
    TURN: int
    PF: int
    PTS: int
    PLUS_MINUS: int
    SEASON_YEAR: int


    # by setting strict=False, Pydantic will try to coerce the data into the specified types before throwing an error
    def __init__(self, **data):
        super().__init__(**data, strict=False)

class PercentileFilter(BaseModel):
    field: str
    value: int
    agg: str

    @field_validator('field')
    def validate_field(cls, field_value):
        if field_value not in COMPARE_METRICS.values():
            raise ValueError(f"'{field_value}' is not a valid field in PlayerGameOBT")
        return field_value

    @field_validator('value')
    def validate_value(cls, value):
        if value < 0 or value > 100:
            raise ValueError(f"'percentile filter {value}' is out of range")
        return value

    @field_validator('agg')
    def validate_operator(cls, agg_value):
        if agg_value not in ['min','max','mean','sum']:
            raise ValueError(f"agg value '{agg_value}' must be min/max/mean")
        return agg_value




class PlayerFilter(BaseModel):
    field: str
    operator: str
    value: Union[int, float, str]

    @field_validator('field')
    def validate_field(cls, field_value):
        if field_value not in COMPARE_METRICS.values():
            raise ValueError(f"'{field_value}' is not a valid field in PlayerGameOBT")
        return field_value

    @field_validator('operator')
    def validate_operator(cls, operator_value):
        if operator_value not in ['==', '>', '>=', '<', '<=']:
            raise ValueError(f"'{operator_value}' is not a valid operator")
        return operator_value

    def pretty_print(self) -> str:
        return f"{self.field} {self.operator} {self.value}"


class PlayerComp(BaseModel):
    player_id: int = Field(strict=False)
    description: str
    filters: Optional[List[PlayerFilter]] = None
    playoffs_only: bool = False
    group_by_season: bool = False
    # group_by: Optional[str] = ""  # Validate this is by game, season, career
