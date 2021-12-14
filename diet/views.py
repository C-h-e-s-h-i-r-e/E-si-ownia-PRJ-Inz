from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.settings import JITSI_SECRET
from diet.models import Diet, DietGroupParticipant, DietType, DietFile
from diet.serializers import DietGroupSerializerCreate, DietGroupSerializerGet, DietGroupSerializerGetAll, \
    participantsSerializerGet, DietGroupTypesSerializer, DietGroupFileSerializer
from payment.utilis import user1_give_money_user2_training
from training.utilis import get_price_and_days_to_add, participant_extend_subscription, jitsi_payload_create, \
    jitsi_token_encode
from users.utilis import put_owner_in_request_data

MAX_PING_ACTIVE_SECONDS = 30


@api_view(['POST'])
def diet_group_create(request):
    request = put_owner_in_request_data(request)
    serializer = DietGroupSerializerCreate(data=request.data)

    if serializer.is_valid():
        if serializer.save():
            return Response({'id': serializer.instance.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def diet_group_edit(request):
    request = put_owner_in_request_data(request)
    instance = Diet.objects.get(id=request.data['id'])
    serializer = DietGroupSerializerCreate(instance=instance, data=request.data)

    if serializer.is_valid():
        if serializer.save():
            return Response({'id': serializer.instance.id}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def diet_group_get(request):
    diet_group = Diet.objects.get(id=request.data['id'])
    serializer = DietGroupSerializerGet(diet_group)
    result = serializer.data
    result['files'] = []
    result['participants'] = []

    for diet_group_file in diet_group.dietfile_set.all():
        try:
            result['files'].append({'id': diet_group_file.id, 'url': diet_group_file.file.url})
        except Exception as e:
            print(e)

    for participant in diet_group.dietgroupparticipant_set.all():
        result['participants'].append(participantsSerializerGet(participant))

    return JsonResponse(result, safe=False)


@api_view(['POST'])
def diet_group_join(request):
    user = request.user
    diet_group = Diet.objects.get(id=request.data['diet_group'])
    print('A')
    owner = diet_group.owner
    price, days_to_add = get_price_and_days_to_add(request.data['payment_type'], diet_group)

    if price is None and days_to_add is None:
        return Response({'Payment type is invalid'}, status=status.HTTP_400_BAD_REQUEST)

    if user.money < price:
        return Response({'User does not have enough money'}, status=status.HTTP_400_BAD_REQUEST)

    diet_group_participant, _ = DietGroupParticipant.objects.get_or_create(user=user, diet_group=diet_group)

    participant_extend_subscription(diet_group_participant, days_to_add)
    user1_give_money_user2_training(user, owner, price)

    return Response({'OK'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def diet_group_participant_remove(request):
    diet_group = Diet.objects.get(id=request.data['diet_group'])
    DietGroupParticipant.objects.get(user=request.data['user'], diet_group=diet_group).delete()
    return Response({'OK'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def diet_group_remove(request):
    diet_group = Diet.objects.get(id=request.data['id'])
    diet_group.delete()

    return Response({'OK'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def diet_group_all(request):
    result = []
    diet_groups = Diet.objects.all()
    for diet_group in diet_groups:
        serializer = DietGroupSerializerGetAll(diet_group)
        result.append(serializer.data)
    return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def diet_group_type_get(request):
    diet_group_type = DietType.objects.get(id=request.data['id'])
    serializer = DietGroupTypesSerializer(diet_group_type)
    return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def diet_group_type_all(request):
    diet_group_types = DietType.objects.all()
    response = []
    for diet_group_type in diet_group_types:
        serializer = DietGroupTypesSerializer(diet_group_type)
        response.append(serializer.data)
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})


@api_view(['POST'])
def diet_group_file_add(request):
    request = put_owner_in_request_data(request)
    serializer = DietGroupFileSerializer(data=request.data)

    if serializer.is_valid():
        if serializer.save():
            return Response({'id': serializer.instance.id}, status=status.HTTP_200_OK)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def diet_group_file_remove(request):
    file_id = request.data['id']
    print(file_id)
    if DietFile.objects.filter(id=file_id).exists():
        DietFile.objects.get(id=file_id).delete()
        return Response({'OK'}, status=status.HTTP_200_OK)
    return Response({'error': 'File doesnt exist or problems when deleting'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def diet_jitsi_join(request):
    user = request.user
    diet = Diet.objects.get(id=request.data['id'])
    diet.participants.add(user)
    payload = jitsi_payload_create(user, diet)
    token = jitsi_token_encode(JITSI_SECRET, payload)
    return Response({'token': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def diet_jitsi_leave(request):
    user = request.user
    diet = Diet.objects.get(id=request.data['id'])
    diet.participants.remove(user)

    return Response({'OK'}, status=status.HTTP_200_OK)
