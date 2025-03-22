from fastapi import APIRouter

from .product.views import router as products_router
from .post.views import router as post_router
from .auth.views import router as auth_router
from .profile.views import router as profile_router
from .order.views import router as order_router

router = APIRouter()

router.include_router(router=auth_router, prefix="/auth")
router.include_router(router=products_router, prefix="/product")
router.include_router(router=post_router, prefix="/post")
router.include_router(router=profile_router, prefix="/profile")
router.include_router(router=order_router, prefix="/order")
