from rest_framework.authentication import get_authorization_header
from rest_framework.throttling import SimpleRateThrottle


class FriendRequestThrottle(SimpleRateThrottle):
    rate = '3/minute'

    def get_cache_key(self, request, view):
        auth_header = get_authorization_header(request).decode('utf-8').split()
        if not auth_header or auth_header[0].lower() != 'bearer':
            return None

        token = auth_header[1]
        return f'friend_request_{token}'
