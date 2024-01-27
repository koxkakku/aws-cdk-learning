# from sqlalchemy.orm import sessionmaker
# from .session import SessionHandler
# from .models import Report
# from .db import DB

# def createReport(report):

#     db = DB.getInstance()
#     print('db')
#     engine = db.engine
#     print('engine %s', engine)
#     Session = sessionmaker(bind=engine)
#     print(session)
#     session = Session()

#     try:
#         print(report)
#         report_session = SessionHandler.create(session, Report)
#         print(1)
#         # add a new record
#         report_session.add(report)

#         session.commit()
#     except Exception as e:
#         session.rollback()
#         raise e
#     finally:
#         session.close()