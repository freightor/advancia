import string
import random

def make_employee_id(instance):
    Klass = instance.__class__
    new_code = "".join(random.sample(string.ascii_uppercase,3)+random.sample(string.digits,3))
    if Klass.objects.filter(employee_no=new_code).exists():
        return make_employee_id(instance)
    return new_code