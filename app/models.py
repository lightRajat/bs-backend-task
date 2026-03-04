from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime, String, func

Base = declarative_base()

class Contact(Base):
    __tablename__ = "Contact"

    id = Column(Integer, primary_key=True)
    phoneNumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    linkedId = Column(Integer, ForeignKey("Contact.id"), nullable=True)
    linkPrecedence = Column(Enum("primary", "secondary"), nullable=False)
    createdAt = Column(DateTime, nullable=False, server_default=func.now())
    updatedAt = Column(DateTime, nullable=False, server_default=func.now())
    deletedAt = Column(DateTime, nullable=True)
    