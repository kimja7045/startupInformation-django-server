from rest_framework.authentication import SessionAuthentication


class BaseSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        pass
