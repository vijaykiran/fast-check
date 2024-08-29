from pydantic import UUID4
from dataclasses import dataclass

from litestar import Litestar, get, post

checks = []


@dataclass
class Check:
    id: UUID4
    type: str


@get("/checks/{check_id:uuid}")
async def get_check(check_id: UUID4) -> dict[str, int]:
    # find checks by id
    for check in checks:
        if check.id == check_id:
            return {"check_id": check.id, "check_type": check}
        else:
            return {"check_id": "not found"}


@post("/checks")
async def create_check(data: Check) -> dict[str, str]:
    checks.append(data)
    return {"check_id": data.id, "check_type": data.type}


app = Litestar([create_check, get_check])
