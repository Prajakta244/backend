import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from sqlalchemy.sql.expression import false

DatabaseUrl = 'sqlite:///./database.db'

engine = sql.create_engine(DatabaseUrl,connect_args={'check_same_thread':False})

sessionLocal = orm.sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative.declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()