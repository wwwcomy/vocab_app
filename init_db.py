from app.models.user import Base
from app.database import engine

Base.metadata.create_all(bind=engine)
