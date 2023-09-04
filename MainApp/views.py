import csv
import json
import os
from asgiref.sync import async_to_sync
from io import TextIOWrapper

from django.http import StreamingHttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db import transaction
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .models import Candle
from .serializers import CandleSerializer
from .utils import async_process_candles

@api_view(['POST'])
@parser_classes([FileUploadParser, JSONParser])
async def upload_csv(request):
# try:
    if 'timeframe' not in request.data:
        return Response({'error': 'Please provide a timeframe.'}, status=status.HTTP_400_BAD_REQUEST)
    
    timeframe = int(request.data.get('timeframe'))
    print("Request success fully accepted")
    candles = await process_csv(request.data['file'], timeframe)

    await store_candles(candles)
    json_file_path = await store_as_json(candles)
    return Response({'message': 'File uploaded and processed successfully.', 'json_file_path': json_file_path})
# except Exception as e:
#     return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

async def process_csv(csv_file, timeframe):
    candles = []
    csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
    reader = csv.DictReader(csv_data)
    for row in reader:
        serializer = CandleSerializer(data=row)
        if serializer.is_valid():
            candle = serializer.save()
            candles.append(candle)
    converted_candles = await async_process_candles(candles, timeframe)
    return converted_candles

@async_to_sync
async def store_candles(candles):
    with transaction.atomic():
        for candle in candles:
            candle.save()

async def store_as_json(candles):
    json_data = []
    for candle in candles:
        serializer = CandleSerializer(candle)
        json_data.append(serializer.data)

    json_file_path = 'converted_candles.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, cls=DjangoJSONEncoder)

    return json_file_path

@api_view(['GET'])
def download_json(request):
    json_file_path = request.GET.get('json_file_path')
    
    if not json_file_path or not os.path.exists(json_file_path):
        return Response({'error': 'JSON file not found.'}, status=status.HTTP_404_NOT_FOUND)

    def file_iterator(file_path, chunk_size=8192):
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk

    # This is used as the function was returning a coroutine instead of a json response
    response = StreamingHttpResponse(file_iterator(json_file_path), content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(json_file_path)}"'
    
    return response
