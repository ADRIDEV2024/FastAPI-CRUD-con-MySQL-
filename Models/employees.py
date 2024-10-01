from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import metadata, engine

employees = Table("Employees", metadata,
            Column("Id", Integer, primary_key=True),
            Column("Name", String(200), nullable=False),
            Column("Password", String(200), nullable=False),
            Column("Age", Integer, nullable=False),
            Column("Department", String(200), nullable=False),
            Column("Position", String(200), nullable=False),
            Column("Years_worked", String(200), nullable=False),
            Column("Salary(Month)", Integer, nullable=False)
)