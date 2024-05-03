from . import users, content, auth, file_storage, text

routers = [
    auth.router,
    users.router,
    content.router,
    file_storage.router,
    text.router
]
