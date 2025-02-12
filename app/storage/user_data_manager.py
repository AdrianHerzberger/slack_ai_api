import asyncio
from ..instances.create_async_engine import AsyncSessionLocal
from ..models.user_model import User
from ..storage_manager.user_data_manager_interface import UserDataManagerInterface
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import datetime


class UserDataManager(UserDataManagerInterface):
    def __init__(self):
        self.db_session_factory = AsyncSessionLocal

    async def create_user(self, user_email, user_name, user_password):
        hashed_password = generate_password_hash(user_password)
        create_date = datetime.datetime.utcnow()
        password_expire_date = create_date + timedelta(days=90)
        is_locked = False
        status = "active"

        async with self.db_session_factory() as session:
            try:
                new_user = User(
                    user_email=user_email,
                    user_name=user_name,
                    user_password=hashed_password,
                    create_date=create_date,
                    password_expire_date=password_expire_date,
                    is_locked=is_locked,
                    status=status
                )
                session.add(new_user) 
                await session.commit() 
                await session.refresh(new_user) 
                return True     
            except Exception as e:
                print(f"Error creating user: {e}")
                await session.rollback() 
                return None

    async def get_all_users(self):
        async with self.db_session_factory() as session:
            try:
                all_users = await session.execute(select(User))
                return all_users.scalars().all()
            except Exception as e:
                print(f"Error fetching users: {e}")
                return None

    async def get_user_by_id(self, user_id):
        async with self.db_session_factory() as session:
            try:
                user_id_query = await session.execute(select(User).filter_by(id=user_id))
                return user_id_query.scalar_one_or_none()
            except Exception as e:
                print(f"Error fetching user by id: {e}")
                return None

    async def get_user_by_email(self, user_email):
        async with self.db_session_factory() as session:
            try:   
                user_email_query = await session.execute(select(User).filter_by(user_email=user_email))
                return user_email_query.scalar_one_or_none()
            except Exception as e:
                print(f"Error fetching user by email: {e}")
                return None

    async def delete_user(self, user_id: str) -> bool:
        async with self.db_session_factory() as session:
            try:
                user_id_to_delete = await session.execute(
                    delete(User)
                    .where(User.id == user_id)
                )

                if user_id_to_delete.rowcount == 0:
                    return False

                await session.commit()
                return True
            except Exception as e:
                print(f"Error deleting user by id: {e}")
                return None

    async def update_user(self, user_id: str, update_user_name: str) -> bool:
        async with self.db_session_factory() as session:
            try:
                user_id_to_update = await session.execute(
                    update(User)
                    .where(User.id == user_id)
                    .values(user_name=update_user_name)
                )

                if user_id_to_update.rowcount == 0:
                    return False

                await session.commit()
                return True
            except Exception as e:
                print(f"Error updating user by id: {e}")
                await session.rollback()
                return None

    def check_user_password(self, user_password, stored_hashed_password):
        return check_password_hash(stored_hashed_password, user_password)

    async def update_user_profile_picture(self, user_id, user_profile_picture_url):
        async with self.db_session_factory() as session:
            try:
                user_id_query = await session.execute(select(User).filter_by(id=user_id)).scalar_one_or_none()
                if user_id_query:
                    user_id_query.user_profile_picture_url = user_profile_picture_url
                    await session.commit()
            except Exception as e:
                print(f"Error updating user profile picture: {e}")
                await session.rollback()
                return None

    async def update_user_last_login_date(self, user_id, last_login_date):
        async with self.db_session_factory() as session:
            try:
                user_id_query = await session.execute(select(User).filter_by(id=user_id))
                user = user_id_query.scalar_one_or_none()
                if user:
                    user.last_login_date = last_login_date
                    await session.commit()
                    return True
            except Exception as e:
                print(f"Error updating users last login date: {e}")
                await session.rollback()
                return None
            
