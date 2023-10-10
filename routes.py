from fastapi import APIRouter ,HTTPException
from models.user import User , validate_email,validate_password
from config.db import conn 
from schemas.user import userEntity , usersEntity
from bson import ObjectId
user = APIRouter() 


@user.get('/')
async def find_all_users():
    return usersEntity(conn.Testify.Organisation.find())

@user.get('/{id}')
async def find_one_user(id):
    document = conn.Testify.Organisation.find_one({"_id":ObjectId(id)})
    if document is None: # Adding the http exception to check the errors 
        raise HTTPException(status_code=404, detail="User not found")
    return userEntity(document)

@user.post('/')
async def create_user(user: User):
    try:
        # Validate email and password
        validated_email = validate_email(user.email)
        validated_password = validate_password(user.password)

        # Create a new user document with validated data
        user_data = dict(user)
        user_data['email'] = validated_email
        user_data['password'] = validated_password

        # Insert the user data into the database
        _id = conn.Testify.Organisation.insert_one(user_data)

        # Return a success response
        document = userEntity(conn.Testify.Organisation.find_one({"_id": _id.inserted_id}))
        return {"status": "ok", "data": document}
    except ValueError as e:
        # Handle validation errors and return an appropriate response
        return {"status": "error", "message": str(e)}


@user.put('/{id}')
async def update_user(id,user: User):
    try:
        # Validate email and password
        if user.email:
            user.email = validate_email(user.email)
        if user.password:
            user.password = validate_password(user.password)

        # Update the user data in the database
        conn.Testify.Organisation.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})

        # Return a success response
        document = userEntity(conn.Testify.Organisation.find_one({"_id": ObjectId(id)}))
        return {"status": "ok", "data": document}
    except ValueError as e:
        # Handle validation errors and return an appropriate response
        return {"status": "error", "message": str(e)}

@user.delete('/{id}')
async def delete_user(id):
    try:
        # Delete the user data from the database
        document = userEntity(conn.Testify.Organisation.find_one_and_delete({"_id": ObjectId(id)}))
        return {"status": "ok", "data": document}
    except Exception as e:
        # Handle any exceptions that may occur during deletion
        return {"status": "error", "message": str(e)}