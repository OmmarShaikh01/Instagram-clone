"""
App Urls
"""
from rest_framework import routers

from instagram_clone.user_relationship.views import UserRelationshipView

router = routers.SimpleRouter()
router.register(r"user/relationship", UserRelationshipView, basename="user")
url_path = router.urls
