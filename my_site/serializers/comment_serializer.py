from my_site import models
from rest_framework import serializers


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comments
        fields = "__all__"
