class NoPutMixin:
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
