from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

from acctmarket.applications.users.models import (ContentManager,
                                            CustomerSupportRepresentative)


class ContentManagerRequiredMixin(LoginRequiredMixin):
    """
    A mixin that only allows access to content managers.
    """

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is authenticated first
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if the user is a content manager
        if not self.user_is_content_manager(request.user):
            return HttpResponseForbidden(
                "You don't have permission to access this page.",
            )
        return super().dispatch(request, *args, **kwargs)

    def user_is_content_manager(self, user):
        """
        Checks if the user is a content manager.
        """
        return ContentManager.objects.filter(user=user).exists()


class CustomerSupportRepresentativemixin(LoginRequiredMixin):
    """
    A mixin that only allows access to customer support representatives.
    """

    def dispatch(self, request, *args, **kwargs):
        # Ensure the user is authenticated first
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        # Check if the user is a customer support representative
        if not self.user_is_customer_support_representative(request.user):
            return HttpResponseForbidden(
                "You don't have permission to access this page.",
            )
        return super().dispatch(request, *args, **kwargs)

    def user_is_customer_support_representative(self, user):
        """
        Checks if the user is a customer support representative.
        """
        return CustomerSupportRepresentative.objects.filter(user=user).exists()
