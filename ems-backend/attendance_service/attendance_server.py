from sqlalchemy import create_engine, MetaData, Table, insert, select
from datetime import datetime
from random import choice
from uuid import uuid4

status_choices = ['present']*20
ab = ['absent']*3
leave = ['leave']*7
status_choices.extend(ab)
status_choices.extend(leave)
print(status_choices)
engine = create_engine("mysql+mysqlconnector://root@localhost:3306/employee_management_system")
with engine.connect() as conn:
    metadata = MetaData()
    attendance = Table("Attendance", metadata, autoload_with=engine)
    employee = Table("Employee", metadata, autoload_with=engine)
    emp_ids = conn.execute(select(employee.c.employee_id))
    emp_ids_list = [emp_id[0] for emp_id in emp_ids.fetchall()]
    print(emp_ids_list)
    attendance_list = []
    for i in range(1, 32):
        dt = datetime(2021, 1, i)
        for emp in emp_ids_list:
            attendance_dict = {
                "employee_id": emp, 
                "attendance_id": uuid4().int%(2147483647), 
                "date": dt, 
                "status": choice(status_choices)
            }
            attendance_list.append(attendance_dict)

    stmt = insert(attendance)
    print(stmt)
    conn.execute(stmt, attendance_list)
    print(attendance_list[:3])

