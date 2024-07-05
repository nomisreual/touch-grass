from ninja import NinjaAPI, Router
from ninja.security import APIKeyHeader
from client.models import Client
from main.models import Post
from main.schema import PostOutSchema
from typing import List

api = NinjaAPI()


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        user_id = request.headers.get("USER-ID")
        if user_id is None:
            return None
        try:
            client = Client.objects.get(user__id=user_id)
        except Client.DoesNotExist:
            return None
        api_key = client.key
        if key == api_key:
            return True


# Instantiate an ApiKey object:
api_key = ApiKey()

# Instantiate a NinjaAPI object:
api = NinjaAPI(
    title="Blog Posts API",
    version="0.1.0",
)

# Instantiate a router object:
router = Router()


@router.get("/post", response={200: List[PostOutSchema]}, auth=api_key)
def get_users(request):
    return Post.objects.all()


api.add_router("", router)
