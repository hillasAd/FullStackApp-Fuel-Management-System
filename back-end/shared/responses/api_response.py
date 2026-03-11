from rest_framework.response import Response

def success(data, status=200):
    return Response({
        "success": True,
        "data": data,
        "error": None
    }, status=status)

def error(message, code="ERROR", status=400):
    return Response({
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }, status=status)
