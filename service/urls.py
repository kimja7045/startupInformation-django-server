from django.urls import path, include
from rest_framework import routers

from service.views import v1


router = routers.DefaultRouter()

# router.register('coupons', v1.CouponViewSet)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/me/profile/', v1.UserProfileView.as_view()),
    path('v1/users/sign-up/', v1.UserSignUpView.as_view()),
    path('v1/users/sign-in/', v1.UserSignInView.as_view()),
    path('v1/users/sign-out/', v1.logout_view),
    #
    # path('v1/users/reset-password/', v1.PasswordResetView.as_view()),
    # path('v1/users/sms-verify/', v1.SMSVerificationView.as_view()),
]
