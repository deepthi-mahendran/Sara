from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
import hmac
import hashlib
import os
from ..database import get_db
from .. import models
from ..limiter import limiter

router = APIRouter()

from typing import Optional
from .auth import SECRET_KEY

def generate_receipt_signature(order: models.Order) -> str:
    raw = f"{order.id}:{order.created_at.isoformat() if order.created_at else ''}:{order.total_amount}:{order.email}"
    return hmac.new(SECRET_KEY.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()

@router.get("/{order_id}/receipt")
@limiter.limit("20/minute")
def get_digital_receipt(request: Request, order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items = db.query(models.OrderItem).filter(models.OrderItem.order_id == order.id).all()
    signature = generate_receipt_signature(order)

    return {
        "order_id": order.id,
        "full_name": order.full_name,
        "email": order.email,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "signature": signature,
        "verification_url": f"/api/receipts/verify-receipt/{signature}?order_id={order.id}",
        "items": [
            {
                "product_name": item.product_name,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item in items
        ],
    }

@router.get("/verify-receipt/{signature}")
@limiter.limit("20/minute")
def verify_digital_receipt(
    request: Request,
    signature: str,
    order_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db)
):
    if order_id:
        order = db.query(models.Order).filter(models.Order.id == order_id).first()
        if order:
            expected = generate_receipt_signature(order)
            if hmac.compare_digest(expected, signature):
                return {
                    "valid": True,
                    "order_id": order.id,
                    "customer_name": order.full_name,
                    "email": order.email,
                    "total_amount": order.total_amount,
                    "status": order.status,
                    "issued_at": order.created_at.isoformat() if order.created_at else None,
                }
        return {"valid": False, "message": "Invalid or tampered receipt signature."}

    orders = db.query(models.Order).order_by(models.Order.id.desc()).limit(100).all()
    for order in orders:
        expected = generate_receipt_signature(order)
        if hmac.compare_digest(expected, signature):
            return {
                "valid": True,
                "order_id": order.id,
                "customer_name": order.full_name,
                "email": order.email,
                "total_amount": order.total_amount,
                "status": order.status,
                "issued_at": order.created_at.isoformat() if order.created_at else None,
            }

    return {"valid": False, "message": "Invalid or tampered receipt signature."}

