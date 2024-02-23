import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

Base = dec.declarative_base()

__factory = None


def global_init(*,
                database: str,
                password: str,
                user: str,
                host: str) -> None:

    global __factory

    if __factory:
        return

    if not database or not database.strip():
        raise Exception("Необходимо указать название базы данных.")

    # conn_str = os.environ.get('DATABASE_URL') or f'sqlite:///{db_file.strip()}?check_same_thread=False'
    # conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    # print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}/{database}",
        # isolation_level="REPEATABLE READ",
        echo=False
    )
    __factory = orm.sessionmaker(bind=engine)

    Base.metadata.create_all(engine)


def get_session() -> Session:
    global __factory
    return __factory()
