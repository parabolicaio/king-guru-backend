from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class LevelResponse(BaseModel):
    id: UUID
    code: str
    name: str
    description: str | None
    display_order: int
    daily_essay_enabled: bool
    translations: dict = {}
    icon_url: str | None = None
    topics: list = []
    guest_enabled: bool = False
    payment_required: bool = False
    price_amount: Decimal | None = None
    price_currency: str = "LKR"


class LevelsListResponse(BaseModel):
    levels: list[LevelResponse]


class CreateCheckoutRequest(BaseModel):
    level_id: UUID


class CreateCheckoutResponse(BaseModel):
    reference: str
    redirect_url: str


class PaymentStatusResponse(BaseModel):
    reference: str
    status: str  # 'pending' | 'success' | 'failed' | 'cancelled'
    level_id: UUID
    level_name: str
    amount: Decimal
    currency: str
