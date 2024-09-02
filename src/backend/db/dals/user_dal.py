from typing import Union, Dict, List
from sqlalchemy.future import select
from decimal import Decimal, ROUND_HALF_UP

from src.backend.config import config
from src.backend.common import custom_exc
from src.backend.schemas import user_schema
from src.backend.db.models.user import User
from src.backend.db.session import get_db


class UserOtherDAL:
    """
    avoid operation of database out of Database Abstraction Layer (DAL)
    """
    @classmethod
    def get(cls, user_id: str, ) -> User:
        session = next(get_db())
        try:
            q = session.execute(select(User).where(User.UserId == int(user_id)))
            user = q.scalar()
            return user

        except Exception as e:
            msg = f"Database error: user not exist, error: {e}"
            print(msg)
            raise Exception(msg)
        finally:
            session.close()


class UserDAL:
    def __init__(self, db_session):
        self.session = db_session

    def get_by(self, *, email: str = None, user_id: int = None, role: int = None) -> User:
        if email:
            stmt = select(User).where(User.Email == email)
        elif user_id:
            stmt = select(User).where(User.UserId == user_id)
        elif role:
            stmt = select(User).where(User.RoleId == role)
        else:
            raise custom_exc.EnumException()
        q = self.session.execute(stmt)
        return q.scalar()

    def get_all_user(self) -> List[User]:
        stmt = select(User)
        q = self.session.execute(stmt)
        return q.scalars().all()

    def create_new_user(self, user: Union[user_schema.User, Dict]):
        obj = User(**user) if isinstance(user, dict) else User(**user.dict())
        self.session.add(obj)
        self.session.commit()
        return obj

    def delete_user(self, user_id: int):
        self.session.query(User).filter(User.UserId == user_id).delete()
        self.session.commit()

    def update_user_role(self, user_id: int, role: int):
        self.session.query(User).filter(User.UserId == user_id).update({"RoleId": role})
        self.session.commit()
        updated_user = self.get_by(user_id=user_id)
        return updated_user

    def update_profile(self, user: Union[user_schema.Update, Dict], user_id: int):
        update_info = User(**user) if isinstance(user, dict) else User(**user.dict())
        self.session.query(User).filter(User.UserId == user_id).update({"Gender": update_info.gender, "Birthday": update_info.birthday, "Avatar": update_info.avatar, "UpdateTime": update_info.update_time})
        self.session.commit()
        updated_user = self.get_by(user_id=user_id)
        return updated_user

    def update_password(self, password: str, user_id: int):
        self.session.query(User).filter(User.UserId == user_id).update({"Password": User.get_password_hash(password)})
        self.session.commit()
        updated_user = self.get_by(user_id=user_id)
        return updated_user

    def set_admin(self, user_id: int):
        self.session.query(User).filter(User.UserId == user_id).update({"role": config.ADMIN})
        self.session.commit()
        updated_user = self.get_by(user_id=user_id)
        return updated_user
    
    def lock_user(self, user_id: int):
        self.session.query(User).filter(User.UserId == user_id).update({"is_locked": True})
        self.session.commit()
        updated_user = self.get_by(user_id=user_id)
        return updated_user

