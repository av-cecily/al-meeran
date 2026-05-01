from flask import Blueprint
from controllers.visualizer_controller import VisualizerController

visualizer_bp = Blueprint('visualizer', __name__)

visualizer_bp.route('/process', methods=['POST'])(VisualizerController.process)
