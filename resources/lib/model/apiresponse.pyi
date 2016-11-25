from typing import Dict
from typing import List


class ApiResponse:
    name = ... # type: str
    year = ... # type: str
    genre = ... # type: List[str]
    plot = ... # type: str
    posters = ... # type: List[str]
    fanarts = ... # type: Dict[str]
    def __init__(self, name:str=None, year:str=None, genre:List[str]=None, plot:str=None, posters:List[str]=None, fanarts:Dict[str]=None): ...
    @classmethod
    def from_dict(cls, name=None, year=None, genre=None, plot=None, posters=None, fanarts=None, **kwargs): ...
