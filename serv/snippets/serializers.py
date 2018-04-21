from django.contrib.auth.models import User
from rest_framework import serializers

from snippets.models import Snippet
from django.contrib.auth import get_user_model


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # highlight = serializers.HyperlinkedIdentityField(
    #     view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('title','owner', 'code', 'created')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets', 'password')
