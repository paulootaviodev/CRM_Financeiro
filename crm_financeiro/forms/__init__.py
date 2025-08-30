from .blog import BlogPostFilterForm
from .client import UpdateClientForm, ClientFilterForm
from .editable_fields import EditableFieldsMixin
from .installment import InstallmentFilterForm
from .loan_proposal import LoanProposalFilterForm
from .login import CustomLoginForm
from .simulation import SimulationFilterForm
from .users import (
    UserRegisterForm,
    UserFilterForm,
    UserUpdateForm,
    ChangePasswordForm
)

__all__ = [
    BlogPostFilterForm,
    UpdateClientForm,
    ClientFilterForm,
    EditableFieldsMixin,
    InstallmentFilterForm,
    LoanProposalFilterForm,
    CustomLoginForm,
    SimulationFilterForm,
    UserRegisterForm,
    UserFilterForm,
    UserUpdateForm,
    ChangePasswordForm
]
