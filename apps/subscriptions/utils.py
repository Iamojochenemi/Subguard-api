from rest_framework.response import Response

def api_response(data=None, message="success", status="success"):
    return Response({
        "status": status,
        "message": message,
        "data": data
    })