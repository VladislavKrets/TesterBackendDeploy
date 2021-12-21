from rest_framework import serializers
from core import models


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = models.Answer
        fields = ['id', 'right', 'text']


class QuestionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        question = super().create(validated_data)
        for answer in answers:
            answer['question'] = question
            models.Answer.objects.create(**answer)
        return question

    def update(self, instance, validated_data):
        answers = validated_data.pop('answers')
        question = super().update(instance, validated_data)
        models.Answer.objects.filter(question=question).delete()
        for answer in answers:
            answer['question'] = question
            models.Answer.objects.create(**answer)
        return question

    class Meta:
        model = models.Question
        fields = ['id', 'text', 'type', 'topic', 'answers']
        read_only_fields = ['id']
