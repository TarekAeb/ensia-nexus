from http.client import HTTPException

import app.core.auth as auth
from app.core.security import verify_password, token_generator, hash_password
from app.infrastructure.repositories.user_repository import UserRepository
from app.domains.auth.schemas import UserSignup as SignSch, UserLogin as LoginSch

whitelisted_email_domains = ["@ensia.edu.dz"]
whitelist_active = True


class AuthService:

    @staticmethod
    def get_current_user():
        pass

    @staticmethod
    def login(data: LoginSch):

        # 1. Get user
        user = UserRepository.get_user_by_email(data.email)

        if not user:
            raise ValueError("Invalid email or password")

        # 2. Check if it's an OAuth account (Google, etc.)
        if not user.password_hash:
            raise ValueError("This account uses Google login")

        # 3. Verify password
        if not verify_password(data.password, user.password_hash):
            raise ValueError("Invalid email or password")

        return user

    @staticmethod
    def signup(data: SignSch):

        # 1. Check if user already exists
        existing_user = UserRepository.get_user_by_email(data.email)
        if existing_user:
            raise ValueError("Email already registered")

        # 2. Validate email domain if whitelist is active
        if whitelist_active and not any(data.email.endswith(domain) for domain in whitelisted_email_domains):
            raise ValueError("Email domain not allowed")

        # 3. hash password
        password_hash = hash_password(data.password)

        # 3. Create user
        user = UserRepository.create_user(
            {
                'email': data.email,
                'full_name': data.full_name,
                'password_hash': password_hash,
                'role': "STUDENT",  # force role to student for now, we can add an admin panel later to change roles
            }
        )

        return user

    @staticmethod
    def generate_token(user_id: int):
        return token_generator(user_id)
