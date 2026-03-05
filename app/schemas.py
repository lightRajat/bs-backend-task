from pydantic import BaseModel

class IdentifyRequest(BaseModel):
    email: str | None
    phoneNumber: str | None

class Contact(BaseModel):
    primaryContactId: int
    emails: list[str]
    phoneNumbers: list[str]
    secondaryContactIds: list[int]

class IdentifyResponse(BaseModel):
    contact: Contact