# class OpLoginError(Exception):
#     def __init__(self, err_desc: str = ""):
#         self.err_desc = err_desc
#
#
# class CheckLoginError(Exception):
#     def __init__(self, err_desc: str = "CheckLogin failed"):
#         self.err_desc = err_desc
#
#
class TokenAuthError(Exception):
    def __init__(self, err_desc: str = "User Authentication Failed"):
        self.err_desc = err_desc


class TokenExpired(Exception):
    def __init__(self, err_desc: str = "token expired, Please log in again"):
        self.err_desc = err_desc
#
#
# class AuthenticationError(Exception):
#     def __init__(self, err_desc: str = "Permission denied"):
#         self.err_desc = err_desc
#
#
class EnumException(Exception):
    def __init__(self, err_desc: str = "enum wrong"):
        self.err_desc = err_desc
#
#

