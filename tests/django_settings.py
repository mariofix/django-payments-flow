# import dj_database_url

# INSTALLED_APPS = [
#     "django.contrib.admin",
#     "django.contrib.auth",
#     "django.contrib.contenttypes",
#     "django.contrib.sessions",
#     "django.contrib.messages",
#     "django.contrib.staticfiles",
#     "payments",
#     "tests.test_app",
# ]

# SECRET_KEY = "django-insecure-secret-key"

# ROOT_URLCONF = "tests.django_urlconf"

# DATABASES = {"default": dj_database_url.config(default="sqlite:///:memory:")}

# USE_TZ = True

# PAYMENT_HOST = "example.com"
# PAYMENT_MODEL = "test_app.BaseTestPayment"
# PAYMENT_VARIANTS = {
#     "flow": (
#         "django_payments_flow.FlowProvider",
#         {
#             "endpoint": "https://sandbox.flow.cl/api",
#             "key": "key",
#             "secret": "secret",
#         },
#     )
# }
