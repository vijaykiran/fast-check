from pydantic import UUID4
from dataclasses import dataclass

from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import get, Litestar, post

from litestar.response import Template
from litestar.template.config import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from pathlib import Path

checks = []


@dataclass
class Check:
    id: UUID4
    type: str


@get("/api/checks/{check_id:uuid}")
async def get_check(check_id: UUID4) -> dict[str, int]:
    for check in checks:
        if check.id == check_id:
            return {"check_id": check.id, "check_type": check}
        else:
            return {"check_id": "not found"}


@post("/api/checks")
async def create_check(data: Check) -> dict[str, str]:
    checks.append(data)
    return {"check_id": data.id, "check_type": data.type}


@get(path="/")
async def index(request: HTMXRequest) -> Template:
    htmx = request.htmx
    return HTMXTemplate(template_name="index.html")


app = Litestar(route_handlers=[index, create_check, get_check],
               request_class=HTMXRequest,
               template_config=TemplateConfig(
                   directory=Path(__file__).parent / "templates",
                   engine=JinjaTemplateEngine
               ))
