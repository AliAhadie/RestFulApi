from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from .serializers import PostSerializer
from blog.models import Post
from rest_framework import status

@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def postlist(request,):
    """ READ """
    if request.method=="GET":
        post=Post.objects.all()
        serializer=PostSerializer(post,many=True)
        return Response(serializer.data)
    """ CREATE """
    if request.method=="POST":
        serializer=PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

@api_view(['GET','PUT','DELETE']) 
@permission_classes([IsAuthenticatedOrReadOnly])       
def postdetail(request,pk):
    post=Post.objects.get(id=pk)
    if request.method=="GET":
        serailizer=PostSerializer(post)
        return Response (serailizer.data)
    """ UPDATE """
    if request.method=="PUT":
        serailizer=PostSerializer(post,data=request.data)
        if serailizer.is_valid():
            serailizer.save()
            return Response(serailizer.data,status=status.HTTP_200_OK)
        
        """ DELETE """
    if request.method=="DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    

