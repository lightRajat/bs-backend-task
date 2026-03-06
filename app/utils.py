from app.models import Contact
from app.schemas import Contact as ContactSchema

def log(msg: str, is_error: bool = False) -> None:
    if is_error:
        print(f"❌[ERROR] {msg}")
    else:
        print(f"🟢  [LOG] {msg}")

def create_contact_response_schema(contacts: list[Contact]) -> ContactSchema:
    for i in range(len(contacts)):
        if contacts[i].linkPrecedence == "primary":
            primary_contact = contacts[i]
            break
    
    primary_contact_id = primary_contact.id
    emails = set()
    phone_numbers = set()
    secondary_contact_ids = []

    for c in contacts:
        if c.email:
            emails.add(c.email)
        if c.phoneNumber:
            phone_numbers.add(c.phoneNumber)
        if c.linkPrecedence != 'primary':
            secondary_contact_ids.append(c.id)
    
    emails = list(emails)
    if primary_contact.email:
        emails.remove(primary_contact.email)
        emails.insert(0, primary_contact.email)

    phone_numbers = list(phone_numbers)
    if primary_contact.phoneNumber:
        phone_numbers.remove(primary_contact.phoneNumber)
        phone_numbers.insert(0, primary_contact.phoneNumber)

    schema = ContactSchema(
        primaryContactId=primary_contact_id,
        emails=emails,
        phoneNumbers=phone_numbers,
        secondaryContactIds=secondary_contact_ids
    )

    return schema