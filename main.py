from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
import uvicorn
from fastapi import FastAPI, Security
import os
from typing import Dict

from settings import Settings

from pydantic import AnyHttpUrl,BaseModel

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi_azure_auth.user import User

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()
    yield


app = FastAPI(
    swagger_ui_oauth2_redirect_url='/oauth2-redirect',
    swagger_ui_init_oauth={
        'usePkceWithAuthorizationCodeGrant': True,
        'clientId': settings.OPENAPI_CLIENT_ID,
        'scopes': settings.SCOPE_NAME,
    },
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

azure_scheme = SingleTenantAzureAuthorizationCodeBearer(
    app_client_id=settings.APP_CLIENT_ID,
    tenant_id=settings.TENANT_ID,
    scopes=settings.SCOPES,
)

class User(BaseModel):
    name: str
    roles: list[str] = []


@app.get("/", dependencies=[Security(azure_scheme)])
async def root():
    print("Yo bro")
    return {"whoIsTheBest": "DNA Team is"}

@app.get("/test", dependencies=[Security(azure_scheme)])
async def root():
    print("Yo test")
    return {"whoIsTheBest": "DNA Team is!"}

@app.get("/me", dependencies=[Security(azure_scheme)])
async def me(request: Request):
    print("Me")
    return User(roles=request.state.user.roles,name=request.state.user.name)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True) 
