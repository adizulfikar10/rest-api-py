from flask import Blueprint, jsonify
from api.db import SessionLocal
from api.models import MsCategory

category_bp = Blueprint('category', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    session = SessionLocal()
    try:
        categories = session.query(MsCategory).all()
        result = [
            {'id': cat.id, 'name': cat.name}
            for cat in categories
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
