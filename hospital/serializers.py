from rest_framework import serializers
from .models import Patient
from datetime import datetime
import re
import uuid


class PatientSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=200,
        error_messages={'required': 'Patient name required', 'blank': 'Patient name required'}
    )
    patient_id = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True
    )
    mobile = serializers.CharField(
        max_length=10,
        error_messages={'required': 'Mobile number needed', 'blank': 'Mobile number needed'}
    )
    gender = serializers.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        error_messages={'required': 'Please select gender'}
    )
    address = serializers.CharField(
        required=False,
        allow_blank=True
    )
    dob = serializers.DateField(
        error_messages={'required': 'Birth date required', 'invalid': 'Use valid format YYYY-MM-DD'}
    )
    doctor_name = serializers.CharField(
        max_length=200,
        error_messages={'required': 'Doctor name required', 'blank': 'Doctor name required'}
    )
    created_at = serializers.DateTimeField(read_only=True)

    def validate_mobile(self, value):
        pattern = r'^(98|97|96)\d{8}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Mobile must contain 10 digits and begin with 98, 97 or 96'
            )
        return value

    def validate_dob(self, value):
        if value > datetime.now().date():
            raise serializers.ValidationError(
                'Birth date cannot be a future date'
            )
        return value

    def create(self, validated_data):
        if not validated_data.get('patient_id'):
            validated_data['patient_id'] = 'PAT-' + str(uuid.uuid4())[:8].upper()
        return Patient.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, val in validated_data.items():
            setattr(instance, field, val)
        instance.save()
        return instance