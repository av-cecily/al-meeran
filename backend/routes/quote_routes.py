from flask import Blueprint
from controllers.quote_controller import QuoteController
from utils.auth_utils import token_required

quote_bp = Blueprint('quotes', __name__)

quote_bp.route('', methods=['GET'])(token_required(QuoteController.get_quotes))
quote_bp.route('', methods=['POST'])(QuoteController.submit_quote)
