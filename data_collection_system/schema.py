from sqlalchemy import Column, String
from sqlalchemy.types import Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import (
    ARRAY,
    BIGINT,
    BIT,
    BOOLEAN,
    BYTEA,
    CHAR,
    CIDR,
    DATE,
    DOUBLE_PRECISION,
    ENUM,
    FLOAT,
    HSTORE,
    INET,
    INTEGER,
    INTERVAL,
    JSON,
    JSONB,
    MACADDR,
    MONEY,
    NUMERIC,
    OID,
    REAL,
    SMALLINT,
    TEXT,
    TIME,
    TIMESTAMP,
    UUID,
    VARCHAR,
    INT4RANGE,
    INT8RANGE,
    NUMRANGE,
    DATERANGE,
    TSRANGE,
    TSTZRANGE,
    TSVECTOR,
)
from sqlalchemy.sql import func

Base = declarative_base()


class TestTable(Base):
    __tablename__ = "test_sm130"

    time = Column(Time, primary_key=True, default=func.now())
    sensor_1 = Column(DOUBLE_PRECISION)
    sensor_2 = Column(DOUBLE_PRECISION)
