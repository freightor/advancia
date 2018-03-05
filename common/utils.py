import uuid

def make_employee_id(instance):
    Klass = instance.__class__
    new_code = uuid.uuid4().hex[:6].upper()
    if Klass.objects.filter(employee_no=new_code).exists():
        return make_employee_id(instance)
    return new_code
