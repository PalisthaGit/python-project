from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ContactIn(BaseModel):
    name: str
    phone: str

@app.post("/contacts")
def add_contact(contact: ContactIn):
    new_contact = {
        "id": len(contacts)+1,
        "name": contact.name,
        "phone": contact.phone

    }
    contacts.append(new_contact)
    return new_contact

@app.get("/")
def home():
    return {"message": "Welcome to the Contact API!"}

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int):
    for contact in contacts:
        if contact["id"] == contact_id:
            contacts.remove(contact)
            return {"message": "Contact deleted"}
    raise HTTPException(status_code=404, detail="Contact not found")

contacts = [
    {"id": 1, "name": "Ram", "phone": "9800000000"},
    {"id": 2, "name": "Sita", "phone": "9811111111"},
]


@app.get("/contacts")
def get_contacts():
    return contacts


@app.get("/contacts/{contact_id}")
def get_contact(contact_id: int):
    for contact in contacts:
        if contact["id"] == contact_id:
            return contact
    raise HTTPException(status_code=404, detail="Contact not found")

@app.put("/contacts/{contact_id}")
def update_contact(contact_id:int, new_contact: ContactIn):
    for existing_contact in contacts:
        if existing_contact["id"] == contact_id:
            existing_contact["name"] = new_contact.name
            existing_contact["phone"] = new_contact.phone
            return existing_contact
    raise HTTPException(status_code = 404, detail = "Contact not found")