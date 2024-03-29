from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import uvicorn

from src.database.connect import get_db
from src.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix="/rest_api")
app.include_router(contacts.router, prefix="/rest_api")


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "FastApi is here! Database configured correctly"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


if __name__ == '__main__':
    uvicorn.run('main:app', host="localhost", port=8000, reload=True)
