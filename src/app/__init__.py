from fastapi import APIRouter
from src.app.router import router as router_main
from src.app.router_authorization import router as router_auto
from src.app.router_for_files import router as router_files
from src.app.router_basic_autorization import router as router_basic
from src.app.router_header import router as router_header
from src.app.router_templates import router as router_t

global_router = APIRouter(

)

global_router.include_router(router_main)
global_router.include_router(router_auto)
global_router.include_router(router_files)
global_router.include_router(router_basic)
global_router.include_router(router_header)
global_router.include_router(router_t)