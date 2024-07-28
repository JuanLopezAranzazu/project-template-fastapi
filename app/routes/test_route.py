from fastapi import APIRouter

# Ruta para pruebas

NAME_ROUTE = "test"

router = APIRouter(
  prefix=f"/{NAME_ROUTE}",
  tags=[NAME_ROUTE]
)

@router.get("/")
async def read_root():
  return {"Hello": "Test"}

