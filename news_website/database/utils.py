import asyncio
import importlib
import pkgutil
import traceback



from pydantic import BaseModel, root_validator

from typing import Any, Callable, Optional, Tuple


from datetime import datetime, date

import orjson


def import_routers(package_name):
    package = importlib.import_module(package_name)
    prefix = package.__name__ + "."

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, prefix):
        # if not module_name.startswith(prefix + "router_"):
        #     continue

        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"Failed to import {module_name}, error: {e}")
            traceback.print_exc()


class AppModel(BaseModel):
    class Config:
        print('config')
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        # json_encoders = {datetime: convert_to_gmt, date: convert_to_gmt, ObjectId: str}

    @root_validator(skip_on_failure=True)
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}




