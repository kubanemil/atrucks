from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PhoneInfo
from .serializers import PhoneInfoSerializer


class PhoneInfoView(APIView):
    """
    Provides phone operator and region information based on a phone number.
    """

    serializer_class = PhoneInfoSerializer

    @extend_schema(parameters=[OpenApiParameter("phone_number", OpenApiTypes.STR)])
    def get(self, request: Request):
        phone_number = request.query_params.get("phone_number")
        if not phone_number:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not phone_number.isdigit():
            return Response(
                {"error": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST
            )

        abc_code = int(phone_number[1:4])
        region_code = int(phone_number[4:])

        info = PhoneInfo.objects.filter(
            abc_code=abc_code, min_code__lte=region_code, max_code__gte=region_code
        ).first()

        if not info:
            return Response(
                {"error": "Not any info found"}, status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "phone_number": phone_number,
            "operator": info.operator,
            "region": info.region,
        }
        return Response(data, status=status.HTTP_200_OK)
