from django.contrib.auth.mixins import UserPassesTestMixin


class SuperUserRequiredMixin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_superuser
    

class TherapistRequiredMixin(UserPassesTestMixin):
    
    def test_func(self):
        return not self.request.user.is_superuser and self.request.user.is_staff