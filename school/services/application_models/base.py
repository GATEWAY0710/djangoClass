from dataclasses import dataclass


@dataclass
class BaseResponse:
    status: bool
    message: str