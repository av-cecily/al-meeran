from flask import Blueprint
from controllers.gallery_controller import GalleryController
from utils.auth_utils import token_required

gallery_bp = Blueprint('gallery', __name__)

gallery_bp.route('', methods=['GET'])(GalleryController.get_gallery)
gallery_bp.route('', methods=['POST'])(token_required(GalleryController.add_gallery_item))
gallery_bp.route('/<int:id>', methods=['DELETE'])(token_required(GalleryController.delete_gallery_item))
