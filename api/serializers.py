# from api.views import categories
# from os import write
# from django.core.validators import slug_re
from rest_framework import serializers
from blog.models import Category, Comment, Post, Tag
from datetime import datetime


class TagSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    accept_by_admin = serializers.BooleanField(default=False, read_only=True)

    def create(self, validated_data):
        return Tag.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        fields = ('id', 'name', 'supercategory')
        read_only_fields = ['id']


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(max_length=500)
    accept_by_admin = serializers.BooleanField(default=False, read_only=True)
    comment_send_time = serializers.DateTimeField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    comment_likes = serializers.StringRelatedField(many=True, read_only=True)

    def save(self, user):
        self.validated_data['comment_send_time'] = datetime.now()
        self.validated_data['user'] = user
        super().save()

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.validate(self.validated_data)
        instance.text = validated_data.get('text', instance.text)
        instance.post = validated_data.get('post', instance.post)
        # self.validate_user(validated_data.get('user'))
        instance.save()
        return instance

    def validate_user(self, new_user):
        if self.instance:
            print(getattr(self.instance, 'user'))
            if getattr(self.instance, 'user') != new_user:
                raise serializers.ValidationError("شما نمی توانید نظر فرد دیگری را تغییر دهید.")
        return new_user


class PostSerializer(serializers.ModelSerializer): 
    categories = serializers.StringRelatedField()
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'safe_text', 'image', 'show_post', 'post_send_time', 
                    'accept_by_admin', 'tags', 'categories', 'post_likes', 'user')
        read_only_fields = ['id', 'safe_text', 'show_post', 'post_send_time', 'accept_by_admin', 'post_likes', 'user', 'tags']
        extra_kwargs = {'text': {'write_only': True}}
