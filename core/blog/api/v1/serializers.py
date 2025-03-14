from rest_framework import serializers
from blog.models import Post, Category

"""
class PostSerializer(serializers.Serializer):
    title=serializers.CharField(max_length=255) 
    author=serializers.CharField(max_length=255)
    id=serializers.IntegerField()
"""


class PostSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField(method_name="get_absolute_url")
    category = serializers.SlugRelatedField(
        many=False, queryset=Category.objects.all(), slug_field="name"
    )

    author = serializers.CharField(source="author.user.email", read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "status",
            "author",
            "published_date",
            "category",
            "absolute_url",
        ]
        read_only_fields = [
            "author",
        ]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.pk)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
        ]
