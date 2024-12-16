from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi_azure_auth import SingleTenantAzureAuthorizationCodeBearer
<<<<<<< HEAD
import uvicorn
from fastapi import FastAPI, Security
import os
from typing import Dict
=======
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
>>>>>>> 20927639742a2f4a6a6fda42dfc6906f9db4916e

from settings import Settings

<<<<<<< HEAD
from pydantic import AnyHttpUrl,BaseModel

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi_azure_auth.user import User

=======
class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: list[str | AnyHttpUrl] = ['http://localhost:8000']
    OPENAPI_CLIENT_ID: str = "7a6732b1-565d-46e9-a080-e4003dfdc965"
    APP_CLIENT_ID: str = "272f31f4-76fb-4641-816b-ce43703522ce"
    TENANT_ID: str = "758eba73-8a49-40b5-915d-0085acccfcca"
    SCOPE_DESCRIPTION: str = "user_impersonation"

    
    @property
    def SCOPE_NAME(self) -> str:
        return f'api://{self.APP_CLIENT_ID}/{self.SCOPE_DESCRIPTION}'

    
    @property
    def SCOPES(self) -> dict:
        return {
            self.SCOPE_NAME: self.SCOPE_DESCRIPTION,
        }

    
    @property
    def OPENAPI_AUTHORIZATION_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/authorize"

    
    @property
    def OPENAPI_TOKEN_URL(self) -> str:
        return f"https://login.microsoftonline.com/{self.TENANT_ID}/oauth2/v2.0/token"

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

>>>>>>> 20927639742a2f4a6a6fda42dfc6906f9db4916e
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

<<<<<<< HEAD
class User(BaseModel):
    name: str
    roles: list[str] = []
=======
@app.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()
>>>>>>> 20927639742a2f4a6a6fda42dfc6906f9db4916e

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