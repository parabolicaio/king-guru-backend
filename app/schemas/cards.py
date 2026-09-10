from uuid import UUID

from pydantic import BaseModel


class AddCardResponse(BaseModel):
    redirect_url: str


class SavedCardResponse(BaseModel):
    token_id: str
    card_type: str
    masked_number: str
    expiry: str


class SavedCardsListResponse(BaseModel):
    cards: list[SavedCardResponse]


class CheckoutSavedCardRequest(BaseModel):
    token_id: str
    level_id: UUID
