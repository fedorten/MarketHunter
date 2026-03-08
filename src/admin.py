from sqladmin import Admin, ModelView
from src.db import engine
from src.tables import User, Chat, Advert, Message


def create_admin_page(app):
    admin = Admin(app, engine)

    class UserAdmin(ModelView, model=User):
        column_list = "__all__"

    class AdvertAdmin(ModelView, model=Advert):
        column_list = "__all__"

    class ChatAdmin(ModelView, model=Chat):
        column_list = "__all__"

    class MessageAdmin(ModelView, model=Message):
        column_list = "__all__"

    admin.add_view(UserAdmin)
    admin.add_view(AdvertAdmin)
    admin.add_view(ChatAdmin)
    admin.add_view(MessageAdmin)
