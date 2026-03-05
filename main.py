from app.db import DBEngine
from app.schemas import IdentifyRequest, IdentifyResponse
from app.utils import create_contact_response_schema, log
from fastapi import FastAPI

app = FastAPI()
db = DBEngine()

@app.post("/identify", response_model=IdentifyResponse)
def identify(identity: IdentifyRequest):
    try:
        contacts = db.get_contacts_by_email_phone(identity.email, identity.phoneNumber)
        log(f"Contacts: {contacts}")
        contacts = db.get_connected_contacts(contacts)
        log(f"Connected Contacts: {contacts}")
        contacts = db.resolve_multiple_primary_keys(contacts)
        log(f"Resolved Multiple Primary Keys: {contacts}")
        contacts = db.resolve_new_data(contacts, identity.email, identity.phoneNumber)
        log(f"Resolved New Data: {contacts}")

        response = IdentifyResponse(
            contact=create_contact_response_schema(contacts)
        )
    except Exception as e:
        log(e, is_error=True)
        response = IdentifyResponse(
            contact = {
                "primaryContactId": -1,
                "emails": ["error occurred while processing the request"],
                "phoneNumbers": ["check backend logs for more details"],
                "secondaryContactIds": []
            }
        )

    return response

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
