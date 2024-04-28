from . import users, content, auth, file_storage

routers = [
    auth.router,
    users.router,
    content.router,
    file_storage.router,
]
