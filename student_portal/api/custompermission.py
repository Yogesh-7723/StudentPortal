from rest_framework import permissions



class StudentReadOnlyPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'PUT' or request.method == 'POST' or request.method == 'PATCH' or request.method == 'DELETE':
            if request.user.is_admin or request.user.is_faculty:
                return True
            else:
                return False
        else:
            return False
        
class AdminFacultyPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_student:
            return False
        else:
            return True
        
class IsStudentPerm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_student:
            return True
        else:
            False
    

