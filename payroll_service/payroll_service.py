from sqlalchemy import select, create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Float
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from models.root_db import Model
from sqlalchemy.sql import func, extract

from models.Employee import Employee
from models.Salary_structure import Salary_structure
from models.Attendance import Attendance, AStatusEnum
from models.Transaction import Transaction
from models.Payroll import Payroll

from datetime import datetime
from uuid import uuid4

engine = create_engine("mysql+mysqlconnector://root@localhost:3306/employee_management_system")


LEAVE_DEDUCTION_RATE = 500.0 # INR/day

def slab_rate(income: float):
    if income > 1500000.0:
        return 0.3
    elif 1500000.0 >= income > 1250000.0:
        return 0.25
    elif 1250000.0 >= income > 1000000.0:
        return 0.2
    elif 1000000.0 >= income > 750000.0:
        return 0.15
    elif 750000.0 >= income > 500000.0:
        return 0.1
    elif 500000.0 >= income > 250000.0:
        return 0.05
    else:
        return 0.0

# simplified payroll calc
# amount to be paid = monthly income - TDS monthly
# monthly income = fixed monthly income - leave_deduction
# taxable annual income = annual income - deductions
# tax to be paid = slab rate * taxable annual income
# average rate of TDS = tax to be paid/annual income(without deductions) * 100
# TDS monthly = average rate of TDS * monthly income

def calculate_payroll_amounts(fixed_monthly_income: float, unpaid_leaves: int, exemptions=0.0):
    leave_deduction = unpaid_leaves * LEAVE_DEDUCTION_RATE
    monthly_income = fixed_monthly_income - leave_deduction
    annual_income = 12*fixed_monthly_income
    taxable_annual_income = annual_income - exemptions
    tax_payable = slab_rate(annual_income) * taxable_annual_income
    average_TDS_rate = tax_payable/annual_income
    TDS_monthly = average_TDS_rate * monthly_income
    amount_payable = monthly_income - TDS_monthly
    return amount_payable, TDS_monthly

def get_fixed_monthly_income(_employee_id: int):
    session = Session(engine)
    emp: Employee = session.query(Employee).filter_by(employee_id=_employee_id).first()
    fixed_monthly_income = emp.position_info.value
    return fixed_monthly_income

def get_number_of_leaves(_employee_id: int, month: int):
    session = Session(engine)
    leave_attendance_records = session.query(Attendance).filter(Attendance.employee_id == _employee_id).\
        filter(extract('month', Attendance.date) == month).\
        filter(Attendance.status == AStatusEnum.LEAVE).all()
    num_leave_records = len(leave_attendance_records)
    return num_leave_records


# DUMMY FUNCTION - WISE API TO BE USED IF ACTUALLY IMPLEMENTING
def make_payment(transaction: Transaction, fail=False):
    if not fail:
        return
    from random import choice
    if not choice([True, True, True, True, True, False]):
        raise Exception("Payment failed")

def make_batch_transactions():
    session = Session(engine)
    emps = session.query(Employee).all()
    for emp in emps:
        unpaid_leaves = get_number_of_leaves(emp.employee_id, datetime.now().month)
        fixed_monthly_income = get_fixed_monthly_income(emp.employee_id)
        amount_payable, TDS_monthly = calculate_payroll_amounts(fixed_monthly_income, unpaid_leaves)
        newTransaction = Transaction()
        newTransaction.transaction_id = uuid4().int%(2147483647)
        newTransaction.net_amount = amount_payable
        newTransaction.TDS = TDS_monthly
        newTransaction.time_stamp = None
        newTransaction.recipient_id = emp.employee_id
        newTransaction.is_successful = False
        session.add(newTransaction)

    newPayroll = Payroll()
    newPayroll.date = datetime.now()
    newPayroll.run_id = uuid4().int%(2147483647)
    newPayroll.TDS_collected = 0.0
    session.add(newPayroll)
    
    session.commit()
    session.close()

def make_batch_payments():
    session = Session(engine)
    transactions = session.query(Transaction).filter_by(is_successful=False).all()
    print("Unsuccessful transactions-", len(transactions))  
    TDS_collection_amount = 0.0
    for transaction in transactions:
        try:
            make_payment(transaction)
            transaction.is_successful = True
            transaction.time_stamp = datetime.now()
            session.add(transaction)
            session.commit()
            TDS_collection_amount += transaction.TDS
        except:
            pass
    latest_payroll_date = session.query(func.max(Payroll.date)).first()[0]
    res = session.query(Payroll).filter(Payroll.date == latest_payroll_date).first()
    if TDS_collection_amount > 0.0:
        res.TDS_collected += TDS_collection_amount
        session.add(res)
    session.commit()
    session.close()

def run_payroll():
    session = Session(engine)
    latest_payroll_date = session.query(func.max(Payroll.date)).first()[0]
    res = session.query(Payroll).filter(Payroll.date == latest_payroll_date).first()
    if res is not None:
        if res.date.month < datetime.now().month:
            make_batch_transactions()
    
    else:
        make_batch_transactions()

    make_batch_payments()

    session.close()
    


run_payroll()
    
    













def run_payroll():
    pass