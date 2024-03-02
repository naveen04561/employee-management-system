from models.root_db import db
from models.Transaction import Transaction
from flask import Blueprint, session, request

from datetime import datetime
from uuid import uuid4
import json

from controllers.AccountantController import *

accountant = AccountantController()


accountant_bp = Blueprint('accountant_bp', __name__)

accountant_bp.route('/view_expenditure', methods=['GET'])(accountant.viewExpenditure)