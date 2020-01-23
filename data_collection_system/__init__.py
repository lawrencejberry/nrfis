from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine(
    "postgresql+psycopg2://postgres:@localhost/timescaletest", echo=False
)
Session = sessionmaker(db)
