from flask import Blueprint, jsonify, request
from api.models import TransactionHeader
from api.models import TransactionDetail
from api.db import SessionLocal

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route('/transactions', methods=['GET'])
def get_transactions():
    session = SessionLocal()
    try:
        # Pagination params
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        code = request.args.get('code')
        category_id = request.args.get('category_id')

        query = session.query(TransactionHeader)
        if code:
            query = query.filter(TransactionHeader.code.like(f"%{code}%"))
        if category_id:
            query = query.join(TransactionHeader.details).filter(TransactionDetail.transaction_category_id == category_id)

        total = query.count()
        transactions = query.offset((page-1)*per_page).limit(per_page).all()
        result = []
        for trx in transactions:
            trx_details = []
            for detail in trx.details:
                trx_details.append({
                    'id': detail.id,
                    'transaction_category_id': detail.transaction_category_id,
                    'name': detail.name,
                    'value_idr': detail.value_idr,
                    'category':{
                      'id':detail.category.id,
                      'name': detail.category.name,
                    }
                })
            result.append({
                'id': trx.id,
                'description': trx.description,
                'code': trx.code,
                'rate_euro': trx.rate_euro,
                'date_paid': str(trx.date_paid),
                'details': trx_details
            })
        return jsonify({
            'page': page,
            'per_page': per_page,
            'total': total,
            'transactions': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
        
@transaction_bp.route('/transactions', methods=['POST'])
def create_transaction():
    session = SessionLocal()
    try:
        from datetime import datetime
        data = request.get_json()

        # Validate required fields
        required_fields = ['id', 'description', 'code', 'rate_euro', 'details']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # Parse date_paid or use now
        date_paid = datetime.now()

        trx = TransactionHeader(
            id=data['id'],
            description=data['description'],
            code=data['code'],
            rate_euro=data['rate_euro'],
            date_paid=date_paid
        )

        details_data = data['details']
        for detail in details_data:
            trx_detail = TransactionDetail(
                id=detail.get('id'),
                transaction_category_id=detail.get('transaction_category_id'),
                name=detail.get('name'),
                value_idr=detail.get('value_idr')
            )
            trx.details.append(trx_detail)
        session.add(trx)
        session.commit()
        # Return created transaction data
        return jsonify({
            'id': trx.id,
            'description': trx.description,
            'code': trx.code,
            'rate_euro': trx.rate_euro,
            'date_paid': trx.date_paid.isoformat() if trx.date_paid else None,
            'details': [
                {
                    'id': d.id,
                    'transaction_category_id': d.transaction_category_id,
                    'name': d.name,
                    'value_idr': d.value_idr
                } for d in trx.details
            ]
        }), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@transaction_bp.route('/transaction/<code>', methods=['PUT'])
def update_transaction(code):
    session = SessionLocal()
    try:
        data = request.get_json()

        trx = session.query(TransactionHeader).filter_by(code=code).first()
        if not trx:
            return jsonify({'error': 'Transaction not found'}), 404
        # Update header fields
        if 'description' in data:
            trx.description = data['description']
        if 'rate_euro' in data:
            trx.rate_euro = data['rate_euro']

        # Update details if present
        if 'details' in data:
            # Remove all old details
            for detail in list(trx.details):
                session.delete(detail)
            trx.details = []
            # Add new details
            for detail in data['details']:
                trx_detail = TransactionDetail(
                    id=detail.get('id'),
                    transaction_category_id=detail.get('transaction_category_id'),
                    name=detail.get('name'),
                    value_idr=detail.get('value_idr')
                )
                trx.details.append(trx_detail)
        session.commit()
        # Return updated transaction with details
        return jsonify({
            'id': trx.id,
            'description': trx.description,
            'code': trx.code,
            'rate_euro': trx.rate_euro,
            'date_paid': trx.date_paid.isoformat() if trx.date_paid else None,
            'details': [
                {
                    'id': d.id,
                    'transaction_category_id': d.transaction_category_id,
                    'name': d.name,
                    'value_idr': d.value_idr
                } for d in trx.details
            ]
        }), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@transaction_bp.route('/transaction/<code>', methods=['DELETE'])
def delete_transaction(code):
    session = SessionLocal()
    try:
        trx = session.query(TransactionHeader).filter_by(code=code).first()
        if not trx:
            return jsonify({'error': 'Transaction not found'}), 404
        # Explicitly delete details (if not using cascade)
        for detail in trx.details:
            session.delete(detail)
        session.delete(trx)
        session.commit()
        return jsonify({'message': 'Transaction deleted successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()

@transaction_bp.route('/transaction/<code>', methods=['GET'])
def get_transaction_details(code):
    session = SessionLocal()
    try:
        trx = session.query(TransactionHeader).filter_by(code=code).first()
        if not trx:
            return jsonify({'error': 'Transaction not found'}), 404
        trx_details = [
            {
                'id': detail.id,
                'transaction_category_id': detail.transaction_category_id,
                'name': detail.name,
                'value_idr': detail.value_idr,
                'category':{
                  'id':detail.category.id,
                  'name': detail.category.name,
                }
            }
            for detail in trx.details
        ]
        result = {
            'id': trx.id,
            'description': trx.description,
            'code': trx.code,
            'rate_euro': trx.rate_euro,
            'date_paid': str(trx.date_paid),
            'details': trx_details
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
