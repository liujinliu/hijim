# -*- coding: utf-8 -*-
import pytest

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)
    create_date = Column(DateTime, server_default=func.now())

    # required in order to access columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    __mapper_args__ = {"eager_defaults": True}


async def async_test_main():
    engine = create_async_engine(
        "sqlite+aiosqlite:///unitestdb",
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # expire_on_commit=False will prevent attributes from being expired
    # after commit.
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    A(data="a1"),
                    A(data="a2"),
                    A(data="a3"),
                ]
            )

        stmt = select(A)

        result = await session.execute(stmt)

        for a1 in result.scalars():
            print(a1)
            print(f"created at: {a1.create_date}")

        result = await session.execute(select(A).order_by(A.id))

        a1 = result.scalars().first()

        a1.data = "new data"

        # should commit here, otherwise a1.data won't change!
        await session.commit()

        # access attribute subsequent to commit; this is what
        # expire_on_commit=False allows
        print(a1.data)

    # for AsyncEngine created in function scope, close and
    # clean-up pooled connections
    await engine.dispose()


@pytest.mark.asyncio
async def test_0():
    await async_test_main()
