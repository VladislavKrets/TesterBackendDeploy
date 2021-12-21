from django.urls import path
from rest_framework.routers import SimpleRouter
from core import views

router = SimpleRouter()
router.register(r'topics', views.TopicViewSet, 'topics')
router.register(r'questions', views.QuestionViewSet, 'questions')
urlpatterns = router.urls
urlpatterns += [
    path('too_many_questions/', views.TooManyQuestions.as_view()),
    path('google_sheet/', views.GoogleSheetDataRequest.as_view())
]