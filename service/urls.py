from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as p_routers

from service.views import v1

router = routers.DefaultRouter()
router.register('posts', v1.PostViewSet)
router.register('public-posts', v1.PublicPostViewSet)

post_router = p_routers.NestedSimpleRouter(router, 'posts', lookup='post')
post_router.register('reviews', v1.ReviewViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include(post_router.urls)),
    path('v1/open-posts/', v1.OpenPostView.as_view()),
    path('v1/me/profile/', v1.UserProfileView.as_view()),
    path('v1/users/sign-up/', v1.UserSignUpView.as_view()),
    path('v1/users/sign-in/', v1.UserSignInView.as_view()),
    path('v1/users/sign-out/', v1.logout_view),
]
