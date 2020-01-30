from rest_framework import serializers
from apps.person.models import Person
from apps.person.utils import image_to_array


class PersonListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, write_only=True)
    last_name = serializers.CharField(max_length=50, write_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Person
        fields = ['name', 'last_name', 'id']


class PersonDetailSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, read_only=True)
    last_name = serializers.CharField(max_length=50, read_only=True)
    has_vector = serializers.SerializerMethodField()
    vector = serializers.ImageField(write_only=True)

    def update(self, instance, validated_data):
        image = validated_data['vector']
        instance.vector = image_to_array(image)
        instance.save()
        return instance

    def get_has_vector(self, *args, **kwargs):
        return True if self.instance.vector else False

    class Meta:
        model = Person
        fields = ['name', 'last_name', 'has_vector', 'vector']


class HasVector:
    def __call__(self, serializer_field):
        if not serializer_field.vector:
            message = f'Vectors are required for compare.'
            raise serializers.ValidationError(message)


class PersonCompareSerializer(serializers.Serializer):
    person1 = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), validators=[HasVector()])
    person2 = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all(), validators=[HasVector()])
