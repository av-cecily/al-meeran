from flask import Blueprint
from controllers.analytics_controller import AnalyticsController
from utils.auth_utils import token_required

analytics_bp = Blueprint('analytics', __name__)

analytics_bp.route('/stats', methods=['GET'])(token_required(AnalyticsController.get_stats))
