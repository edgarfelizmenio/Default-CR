from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
import config

Base = automap_base()

db_config = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
    config.db_user,
    config.db_password,
    config.db_host,
    config.db_port,
    config.db_name
)

engine = create_engine(db_config)
Base.prepare(engine, reflect=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                autoflush=False,
                                bind=engine))

Base.query = db_session.query_property()
