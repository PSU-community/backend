from . import users, informational_content, auth

routers = [
    auth.router,
    users.router,
    informational_content.router
]
