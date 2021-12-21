from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from core import models
from core import serializers
from core import request as sheet


class TopicViewSet(ModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer


class QuestionViewSet(ModelViewSet):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer

    def get_queryset(self):
        topic = models.Topic.objects.get(pk=self.request.META.get('HTTP_TOPIC'))
        return models.Question.objects.filter(topic=topic)


class TooManyQuestions(APIView):
    def post(self, request):
        question_serializer = serializers.QuestionSerializer(data=request.data, many=True)
        if (question_serializer.is_valid()):
            question_serializer.save()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)


class GoogleSheetDataRequest(APIView):
    def post(self, request):
        topic = models.Topic.objects.get(pk=self.request.META.get('HTTP_TOPIC'))
        sheet_id = request.data['sheet_id']
        range = request.data['range']
        questions = sheet.main(sheet_id, range)
        for question in questions:
            curr_question = models.Question.objects.create(topic=topic, text=question.text, type=question.question_type)
            for answer in question.answers:
                models.Answer.objects.create(question=curr_question, text=answer.text, right=answer.is_right)
        return Response(status=status.HTTP_201_CREATED)
