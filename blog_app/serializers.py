from rest_framework import serializers
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']

    # def create(self, validated_data):
    #     print(validated_data)
    #     blog = Blog.objects.create(user=validated_data['user'], title=validated_data['title'], blog_text = validated_data['blog_text'], main_image = validated_data['main_image'])
    #     blog.save() #required to save the password
    #     return validated_data