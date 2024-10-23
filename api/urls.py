from django.urls import path
from . views import *

urlpatterns = [
    path("categories/", categories),
    path("tests/", tests),
    path("test/<str:slug>/", test),
    path("create-test/", create_test),
    path("test/<str:slug>/", test),
    path("get-test-and-questions/<str:slug>", get_test_and_questions),
    path("edit-test/", edit_test),
    path("delete-test/", delete_test),
    path("add-question/", add_question),
    path("edit-question/", edit_question),
    path("delete-question/", delete_question),
    path("attempt-test/", attempt_test),
    path("submit-test/", submit_test),
    path("tests-by-user/<str:pk>/", tests_by_user),
    path("upload-banner/", upload_banner),
    path("publish-test/", publish_test),
    path("attempt-answers/<str:pk>/", attempt_answers),
    path("attempted-tests/", attempted_tests),
    path("tests-by-category/<str:pk>/", tests_by_category),
    path("user-profile/<str:pk>/", user_profile),
    path("search/", search),
]
