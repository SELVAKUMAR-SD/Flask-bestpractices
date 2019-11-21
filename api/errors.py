""" Errors and Exceptions """


class APIError(Exception):
    """ API Error Base Class """

    def __init__(self, description, *args, **kwargs):
        super(APIError, self).__init__(*args, **kwargs)
        self.description = description


class PaymentError(APIError):
    """ Error in handling payment """


class ItemNotFoundError(APIError):
    """ `ItemNotFoundError` """


class OdooError(APIError):
    """ Odoo Error """


class NotFoundError(APIError):
    """ `NotFoundError` """
    code = 404


class OrderDateConflict(APIError):
    """ Conflict in order items dates """
    code = 409


class StudentPlanError(APIError):
    """ Error regarding the student plan """


class DataConflictError(APIError):
    """ Conflict in data """


class UnauthorizedError(APIError):
    """ Unauthorized access """
    code = 401


class UnsupportedMediaError(APIError):
    """ Unsupported file format """
    code = 415
