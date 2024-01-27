# from dataclasses import dataclass
# from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint, func
# from sqlalchemy.ext.declarative import declarative_base
# from .db import DB
    
# Base = declarative_base()
# @dataclass
# class Report(Base):
#     __tablename__ = 'report'
#     id = Column(Integer, primary_key=True)
#     customer_id = Column(String)
#     customer_name = Column(String)
#     account_number = Column(String)
#     account_balance = Column(String)

# # create table if it does not exist, if you change the model,
# #  you have to drop the table first for this code to alter it in the db
# db = DB.getInstance()
# if db is not None:
#     engine = db.engine
#     if engine is not None:
#         Base.metadata.create_all(engine)