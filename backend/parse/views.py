from celery.result import AsyncResult
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_202_ACCEPTED,
                                   HTTP_400_BAD_REQUEST,
                                   HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView

from .tasks import parse_corpus


class CeleryTaskView(APIView):
    '''Implements Celery task status view'''
    status_code_mapping = {
        "PENDING": HTTP_202_ACCEPTED,
        "STARTED": HTTP_202_ACCEPTED,
        "RETRY": HTTP_202_ACCEPTED,
        "FAILURE": HTTP_500_INTERNAL_SERVER_ERROR,
        "SUCCESS": HTTP_200_OK,
    }

    def get(self, request, *args, **kwargs):
        '''Returns task status'''
        task_id = kwargs.get("task_id", None)
        if task_id is None:
            return Response("No task ID specified.", HTTP_400_BAD_REQUEST)

        task = AsyncResult(str(task_id))

        response = Response()
        response.data = {
            "id": task.id,
            "status": task.status,
            "result": task.result
        }
        response.status_code = self.status_code_mapping.get(task.status, HTTP_500_INTERNAL_SERVER_ERROR)

        return response


class ParseTaskView(CeleryTaskView):
    '''View for starting Alpino parse tasks'''

    def post(self, request, *args, **kwargs):
        '''Starts a parse task and returns task id'''
        corpus_id = request.data.get('corpus_id')
        res = parse_corpus.delay(corpus_id)

        return Response({
            "transcript_id": corpus_id,
            "task_id": res.id},
            HTTP_202_ACCEPTED)
