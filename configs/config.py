import os

from dynaconf import Dynaconf, Validator

_VALIDATORS = (Validator(*("DJANGO_SECRET_KEY", "DJANGO_DEBUG"), must_exist=True),)

# Main Region ----------------------------------------
ROOT = os.path.dirname(__file__)
SETTINGS = Dynaconf(
    load_dotenv=False,
    project_root=os.path.dirname(ROOT),
    settings_files=[
        os.path.join(ROOT, "settings.toml"),
        os.path.join(ROOT, "testing_settings.toml"),
        os.path.join(ROOT, ".secrets.toml"),
    ],
    envvar_prefix="DYNACONF",
    environments=True,
    env_switcher="ENV_FOR_DYNACONF",
    validate_only_current_env=True,
    validators=_VALIDATORS,
)
SETTINGS.validators.validate()
