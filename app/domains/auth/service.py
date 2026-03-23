import app.core.auth as auth
from app.infrastructure.repositories.user_repository import UserRepository
from app.domains.auth.schemas import UserSignup as SignSch, UserLogin as LoginSch

class AuthService:

    @staticmethod
    def get_current_user():
        pass

    @staticmethod
    def login(data: LoginSch):

        # 1. Get user
        user = UserRepository.get_user_by_email(data.email)

        if not user:
            raise InvalidCredentialsException("Invalid email or password")

        # 2. Check if it's an OAuth account (Google, etc.)
        if not user.password_hash:
            raise OAuthAccountException("This account uses Google login")

        # 3. Verify password
        if not verify_password(data.password, user.password_hash):
            raise InvalidCredentialsException("Invalid email or password")

        # 4. Generate token
        access_token = create_access_token({"sub": str(user.id)})

        # 5. Return structured response
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        }

    @staticmethod
    def signup():
        pass
