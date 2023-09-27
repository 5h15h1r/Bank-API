# views.py in the bank app
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Banks, Branch
from .serializers import BankSerializer, BranchSerializer
import re
import math


# Regex for finding valid IFSC code
regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
pattern = re.compile(regex)


class BankList(APIView):
    # List the name of all the banks

    def get(self, request):
        try:
            all_banks = Banks.objects.all()
            serializer = BankSerializer(all_banks, many=True)

            page = int(request.GET.get('page', 1))
            if page <= 0:
                return Response(
                    {"message": "Page number must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST)

            per_page = 10
            total = all_banks.count()
            last_page = math.ceil(total / per_page)

            if page > last_page:
                return Response(
                    {"message": "Enter a valid page number"},
                    status=status.HTTP_400_BAD_REQUEST)

            start = (page - 1) * per_page
            end = page * per_page

            return Response({
                "total": total,
                "page": page,
                "lastPage": last_page,
                "data": serializer.data[start:end]
            }, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": "Invalid page number format."},
                            status=status.HTTP_400_BAD_REQUEST)


class BranchDetail(APIView):
    # Returns branch details by taking either IFSC code or branch name
    # as a parameter

    def get(self, request, identifier):
        try:
            if pattern.match(identifier):
                branches = Branch.objects.filter(ifsc=identifier).first()
                if branches is not None:
                    serializer = BranchSerializer(branches)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({
                    "message": "IFSC code not found"},
                      status=status.HTTP_404_NOT_FOUND)

            branches = Branch.objects.filter(branch__istartswith=identifier).first()

            if branches is not None:
                serializer = BranchSerializer(branches)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(
                {"message": "Please enter a valid branch name "},
                status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"message": f"An error {e} occurred "},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
