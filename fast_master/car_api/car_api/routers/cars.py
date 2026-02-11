from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func
from sqlalchemy.orm import selectinload

from car_api.core.database import get_session
from car_api.models.cars import Car, Brand
from car_api.models.users import User
from car_api.schemas.cars import (
    CarSchema,
    CarPublicSchema,
    CarListPublicSchema,
)

router = APIRouter()

@router.post(
    path='/',
    status_code=status.HTTP_201_CREATED,
    response_model=CarPublicSchema,
    summary='Criar novo carro',
)
async def create_car(
    car: CarSchema,
    db: AsyncSession = Depends(get_session),
):
    
    plate_exists = await db.scalar(
        select(exists().where(Car.plate == car.plate))
    )
    if plate_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Placa já está em uso',
        )
    
    brand_exists = await db.scalar(
        select(exists().where(Brand.id == car.brand_id))
    )
    if not brand_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Marca não encontrada',
        )
    
    owner_exists = await db.scalar(
        select(exists().where(User.id == car.owner_id))
    )
    if not owner_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Proprietario não encontrado',
        )
    db_car = Car(
        model=car.model,
        factory_year=car.factory_year,
        model_year=car.model_year,
        color=car.color,
        plate=car.plate,
        fuel_type=car.fuel_type,
        transmission=car.transmission,
        price=car.price,
        description=car.description,
        is_available=car.is_available,
        brand_id=car.brand_id,
        owner_id=car.owner_id,
    )

    db.add(db_car)
    await db.commit()
    await db.refresh(db_car)

    result = await db.execute(
        select(Car)
        .options(selectinload(Car.brand), selectinload(Car.owner))
        .where(Car.id == db_car.id)
    )
    car_with_relations = result.scalar_one()

    return car_with_relations

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=CarListPublicSchema,
    summary='Listar carros',
)
async def list_cars(
    offset: int = Query(0, ge=0, description='Número de registros para pular'),
    limit: int = Query(100, ge=1, le=100, description='Limite de registros'),
    db: AsyncSession = Depends(get_session),
):
    query = select(Car).options(selectinload(Car.brand), selectinload(Car.owner))

    query = query.offset(offset).limit(limit)

    result = await db.execute(query)
    cars = result.scalars().all()

    return {
        'cars': cars,
        'offset': offset,
        'limit': limit,
    }

@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=CarPublicSchema,
    summary='Buscar carro por ID',
)
async def get_car(
    car_id: int,
    db: AsyncSession = Depends(get_session),
):
    result = await db.execute(
        select(Car)
        .options(selectinload(Car.brand), selectinload(Car.owner))
        .where(Car.id == car_id)
    )
    car = result.scalar_one_or_none()

    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carro não encontrado'
        )
    
    return car

@router.delete(
    path='/{car_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar carro',
)
async def delete_car(
        car_id: int,
        db: AsyncSession = Depends(get_session),
):
    car = await db.get(Car, car_id)

    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carro não encontrado',
        )
    
    await db.delete(car)
    await db.commit()

    return 