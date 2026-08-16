# accounts/validators.py
import re
from django.core.exceptions import ValidationError

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError("Şifrə minimum 8 simvol olmalıdır.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Şifrədə ən az 1 böyük hərf olmalıdır.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Şifrədə ən az 1 kiçik hərf olmalıdır.")
        if not re.search(r'\d', password):
            raise ValidationError("Şifrədə ən az 1 rəqəm olmalıdır.")

    def get_help_text(self):
        return "Minimum 8 simvol, 1 böyük hərf, 1 kiçik hərf və 1 rəqəm."