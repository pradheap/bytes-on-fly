from django.forms import widgets
from rest_framework import serializers
from onlineide.models import Snippet, Filestats
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets')

class SnippetSerializer(serializers.Serializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    language = serializers.CharField(required=False,
                                  max_length=100)
    snippet = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000)
    creator = serializers.Field(source='creator.username')

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            instance.snippet = attrs.get('snippet', instance.title)
            instance.language = attrs.get('language', instance.style)
            return instance.pk

        # Create new instance
        return Snippet(**attrs)

class FilestatsSerializer(serializers.Serializer):
    error = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000)
    result = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000)
    stats = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000)
