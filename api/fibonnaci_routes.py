from flask import Blueprint, jsonify, request
from api.utils.fibonnaci import fibonacci_sum

fibonnaci_bp = Blueprint('fibonnaci', __name__)

@fibonnaci_bp.route('/fibonnaci', methods=['GET'])
def sum_fibonnaci():
    
    try:
        first = int(request.args.get('first'),0)
        second = int(request.args.get('second'),0)
        print(f"First: {first}, Second: {second}")  # Debugging line

        result = fibonacci_sum(first, second)
    
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        pass
