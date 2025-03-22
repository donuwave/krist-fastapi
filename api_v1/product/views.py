from fastapi import APIRouter, Depends, status
from typing import List
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .dependencies import product_by_id
from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial

http_bearer = HTTPBearer()
router = APIRouter(tags=["Product"], dependencies=[Depends(http_bearer)])


@router.get("/", response_model=List[Product])
async def get_products(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_products(session)


@router.get("/{product_id}", response_model=Product)
async def get_item_products(product: Product = Depends(product_by_id)):
    return product


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_product(session=session, product_in=product_in)


@router.put("/{product_id}", response_model=Product)
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update
    )


@router.patch("/{product_id}", response_model=Product)
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Product:
    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_product(session=session, product=product)
