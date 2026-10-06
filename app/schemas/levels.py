from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, field_serializer


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

    # Pydantic v2 serializes Decimal to a JSON *string* by default (to avoid
    # float precision loss) — every non-Python client (mobile's Dart `as num`
    # cast included) expects a JSON number here, so serialize explicitly.
    @field_serializer("price_amount")
    def _serialize_price_amount(self, v: Decimal | None) -> float | None:
        return float(v) if v is not None else None


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

    @field_serializer("amount")
    def _serialize_amount(self, v: Decimal) -> float:
        return float(v)
