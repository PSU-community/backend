from . import users, content, auth, file_storage, text, user_content, search

routers = [
    auth.router,
    users.router,
    content.router,
    file_storage.router,
    text.router,
    user_content.router,
    search.router
]
