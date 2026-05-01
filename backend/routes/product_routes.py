from flask import Blueprint
from controllers.product_controller import ProductController
from utils.auth_utils import token_required

product_bp = Blueprint('products', __name__)

product_bp.route('', methods=['GET'])(ProductController.get_products)
product_bp.route('', methods=['POST'])(token_required(ProductController.add_product))
product_bp.route('/<int:id>', methods=['DELETE'])(token_required(ProductController.delete_product))
