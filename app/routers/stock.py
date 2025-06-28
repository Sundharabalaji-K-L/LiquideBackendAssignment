from fastapi import APIRouter, HTTPException, Depends
from pybreaker import CircuitBreaker, CircuitBreakerError
from starlette import status
from typing import List, Type

from app.dependencies import get_current_user, get_stock_service
from app.models.User import User
from app.models.stock import Holding, Position, Order
from app.schemas.stock import HoldingDTO, PositionDTO, OrderDTO
from app.services.stock import StockService


stockRouter = APIRouter(prefix="/stock", tags=["stock"])


@stockRouter.get("/holdings", status_code=status.HTTP_200_OK)
def get_holdings(
    user: User = Depends(get_current_user),
    stock_service: StockService = Depends(get_stock_service),
) -> List[HoldingDTO]:
   try:
       holdings: List[Type[Holding]] = stock_service.get_holdings(user.id)

   except CircuitBreakerError:
       raise HTTPException(status_code=503, detail="stock service temporarily unavailable")

   return [HoldingDTO.model_validate(holding) for holding in holdings]


@stockRouter.get('/positions', status_code=status.HTTP_200_OK)
def get_positions(
    user: User = Depends(get_current_user),
    stock_service: StockService = Depends(get_stock_service),
) -> List[PositionDTO]:
    try:
        positions = stock_service.get_positions(user.id)

    except CircuitBreakerError:
        raise HTTPException(status_code=503, detail="stock service temporarily unavailable")

    return [PositionDTO.model_validate(position) for position in positions]

@stockRouter.get('/orders', status_code=status.HTTP_200_OK)
def get_orders(
    user: User = Depends(get_current_user),
    stock_service: StockService = Depends(get_stock_service),
) -> List[OrderDTO]:
  try:
      orders = stock_service.get_orders(user.id)

  except CircuitBreakerError:
      raise HTTPException(status_code=503, detail="stock service temporarily unavailable")

  return [OrderDTO.model_validate(order) for order in orders]