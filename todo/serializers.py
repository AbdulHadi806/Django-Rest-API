from rest_framework import serializers
from .models import Todo
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('name', 'description', 'created_at', 'id', 'user_id', 'completed')