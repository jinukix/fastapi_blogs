from fastapi import APIRouter

from app.routes import blog, product, user

router = APIRouter()

router.include_router(blog.router, tags=["blogs"], prefix="/blog")
router.include_router(product.router, tags=["products"], prefix="/product")
router.include_router(user.router, tags=["users"], prefix="/user")
