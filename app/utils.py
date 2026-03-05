from app.models import Contact
from app.schemas import Contact as ContactSchema

def log(msg: str, is_error: bool = False) -> None:
    if is_error:
        print(f"❌[ERROR] {msg}")
    else:
        print(f"🟢  [LOG] {msg}")

def create_contact_response_schema(contacts: list[Contact]) -> ContactSchema:
    primary_contact_id: int
    emails = set()
    phone_numbers = set()
    secondary_contact_ids = []

    for contact in contacts:
        if contact.linkPrecedence == "primary":
            primary_contact_id = contact.id
        else:
            secondary_contact_ids.append(contact.id)
        
        if contact.email:
            emails.add(contact.email)
        if contact.phoneNumber:
            phone_numbers.add(contact.phoneNumber)

    schema = ContactSchema(
        primaryContactId=primary_contact_id,
        emails=list(emails),
        phoneNumbers=list(phone_numbers),
        secondaryContactIds=secondary_contact_ids
    )

    return schema