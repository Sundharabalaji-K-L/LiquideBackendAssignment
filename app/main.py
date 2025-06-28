from fastapi import FastAPI
from app.routers.auth import authRouter
from app.routers.stock import stockRouter
from contextlib import asynccontextmanager
from app.core.database import Base, engine
from app.seeds import seed_db


@asynccontextmanager
async def lifespan(app: FastAPI):

    Base.metadata.create_all(bind=engine)
    seed_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(authRouter)
app.include_router(stockRouter)

@app.get('/health')
def health():
    return {'status': 'ok'}

