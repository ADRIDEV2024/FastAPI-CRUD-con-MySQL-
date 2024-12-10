from sqlalchemy import create_engine, MetaData


engine = create_engine("mysql+pymysql://adridev:633900@localhost:3300/db-employees")

conn = engine.connect()
metadata = MetaData()
