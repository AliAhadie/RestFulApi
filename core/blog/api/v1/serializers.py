from rest_framework import serializers
from blog.models import Post

"""
class PostSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255) 
    author=serializers.CharField(max_length=255)
    id=serializers.IntegerField()
"""
class PostSerializer(serializers.ModelSerializer) :
    class Meta:
        model=Post
        fields=['id','title','status','author','published_date']  