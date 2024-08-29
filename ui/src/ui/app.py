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
    id: str
    type: str
    dataset: str
    column: str


@get("/checks")
async def list_checks() -> HTMXTemplate:
    return HTMXTemplate(template_name="checks.html", context={"checks": checks})

@post("/checks")
async def create_check(
    data: Annotated[Check, Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> HTMXTemplate:
    checks.append(data)
    return HTMXTemplate(template_name="alert.html", context={"message": "Check created"})


@get(path="/")
async def index(request: HTMXRequest) -> Template:
    htmx = request.htmx
    return HTMXTemplate(template_name="index.html")


app = Litestar(
    route_handlers=[index, create_check, list_checks],
    request_class=HTMXRequest,
    template_config=TemplateConfig(
        directory=Path(__file__).parent / "templates", engine=JinjaTemplateEngine
    ),
)
