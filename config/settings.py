import os
import environ
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LIBS = [
    'rest_framework',
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',
    'taggit',
    'phonenumber_field',
    'multiselectfield',
]

APPS = [
    'api.v1.accounts.apps.AccountsConfig',
    'api.v1.products.apps.ProductsConfig',
    'api.v1.orders.apps.OrdersConfig',
    'api.v1.wishlists.apps.WishlistsConfig',
    'api.v1.discounts.apps.DiscountsConfig',
    'api.v1.general.apps.MainConfig',
    'api.v1.delivery.apps.DeliveryConfig',
    'api.v1.advertisements.apps.AdvertisementsConfig',

    # integration apps
    # 'api.v1.integrations.mail',
    # 'api.v1.integrations.google',
    # 'api.v1.integrations.oneid',
    # 'api.v1.integrations.payments',
    # 'api.v1.integrations.sms'
]

INSTALLED_APPS = DEFAULT_APPS + LIBS + APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

BASE_USER_PHONE_NUMBER = '+998912345678'
BASE_USER_EMAIL = 'super@gmail.com'
BASE_USER_PASSWORD = 'pbkdf2_sha256$320000$Bm7c6Hdu9WXa3DAlV082fF$2j1D1ygwUfr2/m2zMF3g6YzYW3o6G7W/i5WW/TU0fhk='

AUTHENTICATION_BACKENDS = [

    'api.v1.accounts.backends.CustomModelBackend',
]

EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        # 'api.v1.accounts.authentication.CustomAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static/'
# STATICFILES_DIRS = [BASE_DIR / 'static/']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

DIRECTOR_GROUP_PERMISSIONS = {
    'wishlists': ['delete_wishlist', 'view_wishlist'],

    'accounts': [
        'add_client', 'change_client', 'delete_client', 'view_client',
        'change_director', 'delete_director', 'view_director',
        'add_manager', 'change_manager', 'delete_manager', 'view_manager',
        'add_userdetailondelete', 'change_userdetailondelete', 'delete_userdetailondelete',
        'view_userdetailondelete', 'add_vendor', 'change_vendor', 'delete_vendor', 'view_vendor'
    ],

    'delivery': ['add_delivery', 'change_delivery', 'delete_delivery', 'view_delivery'],
    'discounts': [
        'add_discount', 'change_discount', 'delete_discount', 'view_discount',
        'add_discountitem', 'change_discountitem', 'delete_discountitem', 'view_discountitem'
    ],
    'general': ['add_shopabout', 'change_shopabout', 'delete_shopabout', 'view_shopabout'],
    'orders': [
        'add_order', 'change_order', 'delete_order', 'view_order',
        'add_orderitem', 'change_orderitem', 'delete_orderitem', 'view_orderitem'
    ],
    'products': [
        'add_brand', 'change_brand', 'delete_brand', 'view_brand',
        'add_category', 'change_category', 'delete_category', 'view_category',
        'add_product', 'change_product', 'delete_product', 'view_product',
        'add_productcolor', 'change_productcolor', 'delete_productcolor', 'view_productcolor',
        'add_productcomment', 'delete_productcomment', 'view_productcomment',
        'add_productitem', 'change_productitem', 'delete_productitem', 'view_productitem',
        'add_productmanufacturer', 'change_productmanufacturer', 'delete_productmanufacturer',
        'add_productsize', 'change_productsize', 'delete_productsize', 'view_productsize',
        'delete_productstar', 'view_productstar'
    ],
    'taggit': [
        'add_tag', 'change_tag', 'delete_tag', 'view_tag',
        'add_taggeditem', 'change_taggeditem', 'delete_taggeditem', 'view_taggeditem'
    ],
    'token_blacklist': [
        'view_blacklistedtoken', 'add_blacklistedtoken',
        'change_blacklistedtoken', 'delete_blacklistedtoken',
    ]
}

MANAGER_GROUP_PERMISSIONS = {
    'accounts': [
        'add_client', 'change_client', 'delete_client', 'view_client',
        'delete_director', 'view_director', 'change_manager', 'view_manager',
        'add_userdetailondelete', 'change_userdetailondelete', 'delete_userdetailondelete',
        'view_userdetailondelete', 'add_vendor', 'change_vendor', 'delete_vendor', 'view_vendor'
    ],
    'products': [
        'view_productstar', 'view_brand',
        'add_brand', 'change_brand', 'delete_brand', 'view_productmanufacturer',
        'add_category', 'change_category', 'delete_category', 'view_category',
        'add_product', 'change_product', 'delete_product', 'view_product',
        'add_productcolor', 'change_productcolor', 'delete_productcolor', 'view_productcolor',
        'add_productcomment', 'delete_productcomment', 'view_productcomment',
        'add_productitem', 'change_productitem', 'delete_productitem', 'view_productitem',
        'add_productmanufacturer', 'change_productmanufacturer', 'delete_productmanufacturer',
        'add_productsize', 'change_productsize', 'delete_productsize', 'view_productsize'
    ],
    'discounts': [
        'add_discount', 'change_discount', 'delete_discount', 'view_discount',
        'add_discountitem', 'change_discountitem', 'delete_discountitem', 'view_discountitem'
    ],
    'delivery': ['add_delivery', 'change_delivery', 'delete_delivery', 'view_delivery'],
    'wishlists': ['delete_wishlist', 'view_wishlist'],
    'general': ['view_shopabout'],
    'orders': [
        'add_order', 'change_order', 'delete_order', 'view_order',
        'add_orderitem', 'change_orderitem', 'delete_orderitem', 'view_orderitem'
    ],
    'token_blacklist': [
        'view_blacklistedtoken', 'delete_blacklistedtoken',
        'add_blacklistedtoken', 'change_blacklistedtoken'
    ],
    'taggit': [
        'add_tag', 'change_tag', 'delete_tag', 'view_tag',
        'add_taggeditem', 'change_taggeditem', 'delete_taggeditem', 'view_taggeditem'
    ],
}

VENDOR_GROUP_PERMISSIONS = {
    'accounts': [
        'add_client', 'change_client', 'view_client', 'change_userdetailondelete',
        'delete_director', 'view_director', 'view_manager', 'add_userdetailondelete',
        'view_userdetailondelete', 'view_vendor'
    ],
    'products': [
        'view_productstar', 'view_product', 'add_brand', 'change_brand',
        'add_category', 'change_category', 'view_category', 'add_product', 'change_product',
        'add_productcolor', 'change_productcolor', 'delete_productcolor', 'view_productcolor',
        'add_productcomment', 'delete_productcomment', 'view_productcomment', 'view_brand',
        'add_productitem', 'change_productitem', 'view_productitem',
        'add_productmanufacturer', 'change_productmanufacturer', 'view_productmanufacturer',
        'add_productsize', 'change_productsize', 'delete_productsize', 'view_productsize'
    ],
    'discounts': ['view_discount', 'view_discountitem'],
    'delivery': ['add_delivery', 'change_delivery', 'view_delivery'],
    'wishlists': ['delete_wishlist', 'view_wishlist'],
    'general': ['view_shopabout'],
    'orders': [
        'add_order', 'change_order', 'view_order',
        'add_orderitem', 'change_orderitem', 'view_orderitem',
    ],
    'token_blacklist': ['view_blacklistedtoken'],
    'taggit': [
        'add_tag', 'change_tag', 'delete_tag', 'view_tag',
        'add_taggeditem', 'change_taggeditem', 'delete_taggeditem', 'view_taggeditem'
    ],
}

CLIENT_GROUP_PERMISSIONS = {
    'delivery': ['view_delivery'],
    'general': ['view_shopabout'],
    'taggit': ['view_tag', 'view_taggeditem'],
    'discounts': ['view_discount', 'view_discountitem'],
    'wishlists': ['add_wishlist', 'change_wishlist', 'delete_wishlist', 'view_wishlist'],
    'accounts': ['change_client', 'delete_client', 'view_client', 'view_director', 'view_manager', 'view_vendor'],

    'products': [
        'view_productcomment', 'view_productsize', 'delete_productstar',
        'view_brand', 'view_category', 'view_product',
        'add_productcomment', 'change_productcomment', 'delete_productcomment',
        'view_productcolor', 'view_productitem', 'view_productmanufacturer',
        'view_productstar', 'add_productstar', 'change_productstar'
    ],

    'orders': [
        'add_order', 'change_order', 'delete_order', 'view_order',
        'add_orderitem', 'change_orderitem', 'delete_orderitem', 'view_orderitem'
    ],
}

USER_GROUP_PERMISSIONS = {
    'directors': DIRECTOR_GROUP_PERMISSIONS,
    'managers': MANAGER_GROUP_PERMISSIONS,
    'vendors': VENDOR_GROUP_PERMISSIONS,
    'clients': CLIENT_GROUP_PERMISSIONS
}
