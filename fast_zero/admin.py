from sqladmin import Admin, ModelView
from fast_zero.models import User


class UserAdmin(ModelView, model=User):
    """Interface administrativa simples para o modelo User"""

    # Configurações básicas
    name = "Usuário"
    name_plural = "Usuários"

    # Colunas que aparecem na listagem
    column_list = [User.id, User.username, User.email]

    # Colunas que podem ser editadas
    column_editable_list = [User.username, User.email]

    # Colunas que podem ser pesquisadas
    column_searchable_list = [User.username, User.email]

    # Configurações de paginação
    page_size = 20

    # Configurações de formulário
    form_excluded_columns = ["password", "created_at", "updated_at"]

    # Configurações básicas
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
