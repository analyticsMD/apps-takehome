from .models import Part
from .serializers import PartSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import nltk

@api_view(['GET'])
def list(request, format=None):
    if request.method == 'GET':
        parts = Part.objects.all()
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
   

@api_view(['POST'])
def create(request, format=None):
    serializer = PartSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get(request, part_id):
    try:
        part = Part.objects.get(pk=str(part_id))
    except Part.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = PartSerializer(part)
    return Response(serializer.data)


@api_view(['PUT'])
def update(request, part_id):
    try:
        part = Part.objects.get(pk=str(part_id))
    except Part.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = PartSerializer(part, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    else:
        return Response(serializer.data, status=status.HTTP_404_BAD_REQUEST)


@api_view(['DELETE'])
def delete(request, part_id):
    try:
        part = Part.objects.get(pk=str(part_id))
    except Part.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    part.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_common_words(request, most_common_quantity):
 
    nltk.download('punkt')
    nltk.download('stopwords')

    parts = Part.objects.all()
    serializer = PartSerializer(parts, many=True)

    all_descriptions = ' '.join([part.description for part in parts])

    words = nltk.tokenize.word_tokenize(all_descriptions)
    words_dist = nltk.FreqDist(w.lower() for w in words)
    most_common = words_dist.most_common(int(most_common_quantity))
    response =  [{item[0]: item[1]} for item in most_common]
    
    return Response(response)