from app.models import Contact
from datetime import datetime
from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session

class DBEngine:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        self.session = Session(self.engine)
    
    def get_contacts_by_email_phone(self, email: str, phone: str) -> list[Contact]:
        conditions = []

        if email:
            conditions.append(Contact.email == email)
        if phone:
            conditions.append(Contact.phoneNumber == phone)
        
        results = []
        if conditions:
            results = self.session.query(Contact).filter(or_(*conditions)).all()
        
        return results
    
    def get_connected_contacts(self, contacts: list[Contact]) -> list[Contact]:
        all_contacts: dict[int, Contact] = {}

        for contact in contacts:
            all_contacts[contact.id] = contact

            if contact.linkPrecedence == 'primary':
                related_contacts = self.get_secondary_contacts(contact)
            else:
                primary_contact = self.get_primary_contact(contact)
                related_contacts = self.get_secondary_contacts(primary_contact)
                related_contacts.append(primary_contact)
            
            for c in related_contacts:
                all_contacts[c.id] = c
        
        return list(all_contacts.values())
    
    def get_primary_contact(self, contact: Contact) -> Contact:
        contact = self.session.query(Contact).filter(Contact.id == contact.linkedId).first()
        return contact
    
    def get_secondary_contacts(self, contact: Contact) -> list[Contact]:
        contacts = self.session.query(Contact).filter(Contact.linkedId == contact.id).all()
        return contacts
    
    def resolve_multiple_primary_keys(self, contacts: list[Contact]) -> list[Contact]:
        if not contacts:
            return contacts
        
        oldest_contact = min(contacts, key=lambda c: c.createdAt)
        curr_datetime = datetime.now()

        for c in contacts:
            if c.id != oldest_contact.id and c.linkedId != oldest_contact.id:
                self.session.query(Contact).filter(Contact.id == c.id).update({
                    "linkPrecedence": "secondary",
                    "linkedId": oldest_contact.id,
                    "updatedAt": curr_datetime
                })

                c.linkPrecedence = "secondary"
                c.linkedId = oldest_contact.id
                c.updatedAt = curr_datetime
        self.session.commit()

        return contacts
    
    def resolve_new_data(self, contacts: list[Contact], email: str, phone: str) -> list[Contact]:
        if not contacts:
            new_contact = self.create_new_contact(email, phone)
            contacts.append(new_contact)
            return contacts
        
        if email and phone:
            is_email_new = True
            is_phone_new = True
            for c in contacts:
                if c.email == email:
                    is_email_new = False
                    break
            for c in contacts:
                if c.phoneNumber == phone:
                    is_phone_new = False
                    break
            
            if is_email_new or is_phone_new:
                primary_contact = [c for c in contacts if c.linkPrecedence == 'primary'][0]

                new_contact = self.create_new_contact(
                    email=email if is_email_new else primary_contact.email,
                    phone=phone if is_phone_new else primary_contact.phoneNumber,
                    linkedId=primary_contact.id,
                )
                contacts.append(new_contact)
        
        return contacts
    
    def create_new_contact(self, email: str, phone: str, linkedId: int = None) -> Contact:
        new_contact = Contact(
            email=email if email else None,
            phoneNumber=phone if phone else None,
            linkPrecedence="secondary" if linkedId else "primary",
            linkedId=linkedId if linkedId else None,
        )
        self.session.add(new_contact)
        self.session.commit()

        return new_contact
