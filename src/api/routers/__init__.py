from . import users, informational_content, auth, file_storage

routers = [
    auth.router,
    users.router,
    informational_content.router,
    filestorage.router,
]
