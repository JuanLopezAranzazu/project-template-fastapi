from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from .routes import test_route, auth_route, user_route

app = FastAPI()

# Crear la base de datos
# db_config.create_tables()

# uvicorn app.main:app --reload
# uvicorn app.main:app --reload --port 8080
# http://127.0.0.1:8000
# http://127.0.0.1:8000/docs

# Rutas de la aplicación
app.include_router(test_route.router)
app.include_router(auth_route.router)
app.include_router(user_route.router)

@app.get("/")
def read_root():
  return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
  return {"item_id": item_id}

# Manejador de excepciones
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
  return JSONResponse(
    status_code=exc.status_code,
    content={"message": exc.detail},
  )

# Iniciar el servidor
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)

       