from django.urls import path
from .views import StaffImageSingleView,StudentImageSingleView,StaffImageListView,StudentImageListView,train_model,rekognition_get

urlpatterns = [
    path("student/image/<int:pk>",StudentImageSingleView.as_view()),
    path("student/image",StudentImageListView.as_view()),
    
    path("staff/image/<int:pk>",StaffImageSingleView.as_view()),
    path("staff/image",StaffImageListView.as_view()),

    path("<str:entity>/train/", train_model),
    path("<str:entity>/predict/", rekognition_get),
]