from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, String, func

Base = declarative_base()

class Contact(Base):
    __tablename__ = "Contact"

    def __repr__(self):
        return f"Contact(id={self.id}, phoneNumber={self.phoneNumber!r}, email={self.email!r}, linkedId={self.linkedId!r}, linkPrecedence={self.linkPrecedence})"

    id = Column(Integer, primary_key=True)
    phoneNumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedId = Column(Integer, ForeignKey("Contact.id"), nullable=True)
    linkPrecedence = Column(Enum("primary", "secondary", name="contact__link_precedence"), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now())
    deletedAt = Column(DateTime, nullable=True)
    