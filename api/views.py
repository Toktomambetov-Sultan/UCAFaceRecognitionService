from django.shortcuts import render
from .serializers import StudentImageSerializer,StaffImageSerializer
from .models import StudentImage,StaffImage
from rest_framework import generics
from rest_framework.decorators import api_view
from .recognition import train, predict
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class StudentImageSingleView(generics.RetrieveDestroyAPIView):
    serializer_class = StudentImageSerializer
    queryset = StudentImage.objects.all()

class StudentImageListView(generics.ListCreateAPIView):
    serializer_class = StudentImageSerializer 
    queryset = StudentImage.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_fields = ['trained','person_id']

class StaffImageSingleView(generics.RetrieveDestroyAPIView):
    serializer_class = StaffImageSerializer
    queryset = StaffImage.objects.all()

class StaffImageListView(generics.ListCreateAPIView):
    serializer_class = StaffImageSerializer 
    queryset = StaffImage.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    filterset_fields = ['trained','person_id']





@api_view(['GET'])
def train_model(request,entity):
    if entity == "student":
        Image = StudentImage
    elif entity == "staff": 
        Image = StaffImage
    else:
        return Response({"error": "Entity shoudl be student or staff"},status=status.HTTP_400_BAD_REQUEST)
    print("Training1 KNN classifier...")
    classifier = train(model_save_path="media/static/model/"+entity+".clf", model=Image, n_neighbors=2)
    for i in Image.objects.filter(trained=False):
        i.trained = True
        i.save()
    print("Training complete!")
    return Response({"message": "trained successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def rekognition_get(request,entity):
    if request.method == 'POST':
        if entity == "student" or entity == "staff":
            pass
        else:
            return Response({"error": "Entity shoudl be student or staff"},status=status.HTTP_400_BAD_REQUEST)
        res = predict(request.data["file"], model_path="media/static/model/"+entity+".clf",distance_threshold=0.5)
        if len(res) == 0:
            return Response({'error': "Person not found"}, status=status.HTTP_404_NOT_FOUND)
        res = res[0][0]
        try:
            int(res) 
        except:
            return Response({'error': res}, status=status.HTTP_404_NOT_FOUND)
        return Response(res, status=status.HTTP_200_OK)





