from rest_framework import serializers
from .models import ScrapedData, User, ScraperTask, ScraperScript, ScraperLog, ScraperScript
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model=User
        fields = {'id', 'username', 'password', 'email', 'role'}

    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ScraperScriptSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ScraperScript
        fields = ['id', 'name', 'description', 'script_path']

class ScraperTaskSerializer(serializers.ModelSerializer):
    script = serializers.PrimaryKeyRelatedField(queryset=ScraperScript.objects.all())
    run_type = serializers.ChoiceField(choices=ScraperTask.RUN_TYPE_CHOICES)
    run_once_time = serializers.DateTimeField(required=False)

    class Meta:
        model=ScraperTask
        fields = '__all__'
        read_only_fields = ['status', 'created_by', 'created_at', 'updated_at']

    def validate(self, data):
        run_type = data.get('run_type')
        if run_type == 'recurring' and not data.get('schedule_time'):
            raise serializers.ValidationError("Schedule time is required for recurring tasks.")
        
        if run_type == 'once' and not data.get('run_once_time'):
            raise serializers.ValidationError("Run once time is required for one-time tasks.")
        return data
    
class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'

class ScraperLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScraperLog
        fields = '__all__'