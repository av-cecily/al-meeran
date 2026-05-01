from flask import Blueprint
from controllers.order_controller import OrderController
from utils.auth_utils import token_required

order_bp = Blueprint('orders', __name__)

order_bp.route('', methods=['GET'])(token_required(OrderController.get_orders))
order_bp.route('', methods=['POST'])(OrderController.create_order)
