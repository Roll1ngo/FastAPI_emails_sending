from fastapi import APIRouter, HTTPException, status, Depends, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.connect import get_db
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactResponse, BirthdaysResponse

router = APIRouter(prefix='/contacts', tags=['contacts'])


@router.get('/', response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                       db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.create_contact(body, db)
    return contact


@router.put('/{contact_id}', status_code=status.HTTP_201_CREATED)
async def update_contact(body: ContactSchema, contact_id: int = Path(qe=1), db: AsyncSession = Depends(get_db)):
    todo = await repositories_contacts.update_contact(contact_id, body, db)
    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return todo


@router.delete('/{contact_id}')
async def delete_contact(contact_id: int = Path(qe=1), db: AsyncSession = Depends(get_db), ):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return f"{contact.name} {contact.lastname} has been deleted"


@router.get('/birthdate/', response_model=list[ContactResponse])
async def get_birthdays(db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_birthdays(db)
    return contacts


@router.get('/search/{search_string}', response_model=list[ContactResponse])
async def search_contacts(search_string: str = Path(min_length=2, max_length=20), db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.search_contacts(search_string, db)
    return contacts
