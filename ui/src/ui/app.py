from pydantic import UUID4
from dataclasses import dataclass

from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import get, Litestar, post

from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from pathlib import Path
from typing import Annotated
from litestar.enums import RequestEncodingType
from litestar.params import Body

checks = []


@dataclass
class Check:
    id: UUID4
    type: str


@get("/checks/{check_id:uuid}")
async def get_check(check_id: UUID4) -> dict[str, int]:
    for check in checks:
        if check.id == check_id:
            return {"check_id": check.id, "check_type": check}
        else:
            return {"check_id": "not found"}


@get("/checks")
async def get_checks() -> list[dict[str, str]]:
    return [{"check_id": check.id, "check_type": check.type} for check in checks]


@post("/checks")
async def create_check(
    data: Annotated[Check, Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> dict[str, str]:
    checks.append(data)
    return {"check_id": data.id, "check_type": data.type}


@get(path="/")
async def index(request: HTMXRequest) -> Template:
    htmx = request.htmx
    return HTMXTemplate(template_name="index.html")


app = Litestar(
    route_handlers=[index, get_checks, create_check, get_check],
    request_class=HTMXRequest,
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates", engine=JinjaTemplateEngine
    ),
)
