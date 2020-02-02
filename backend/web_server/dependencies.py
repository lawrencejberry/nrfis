from . import Session as SessionLocal


def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
