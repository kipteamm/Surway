from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Optional,
    Type,
    TypeVar,
    Union,
)


T = TypeVar("T", bound=Any)

class flag:
    def __init__(self, func: Callable[..., int]) -> None:
        self.func = func

    def __get__(self, instance: T, owner: Type[T]) -> Union[bool, int]:
        flag_value = self.func()

        if instance is None:
            return flag_value

        return flag_value in instance
    

class Flags:
    @flag
    def create_content():
        return 1 << 0

    @flag
    def manage_account():
        return 1 << 1

    @flag
    def developer_tools():
        return 1 << 2

    @flag
    def partner_tools():
        return 1 << 3

    @flag
    def verified_account():
        return 1 << 4

    @flag
    def feature_previews():
        return 1 << 5

    @flag
    def manage_reports():
        return 1 << 6

    @flag
    def manage_cases():
        return 1 << 7

    @flag
    def manage_permissions():
        return 1 << 8

    @flag
    def enhanced_content():
        return 1 << 9

    @flag
    def enhanced_profile():
        return 1 << 10

    @flag
    def default_upload_size():
        return 1 << 11

    @flag
    def small_upload_size():
        return 1 << 12

    @flag
    def medium_upload_size():
        return 1 << 13

    @flag
    def large_upload_size():
        return 1 << 14
    
    @flag 
    def manage_users():
        return 1 << 15


class Permissions(Flags):
    def __init__(
        self,
        *,
        permissions: Optional[int] = None,
        **permission_mapping: bool,
    ) -> None:
        self.value = permissions or self._get_enabled_perms_value(permission_mapping)

    def _get_enabled_perms_value(self, permission_mapping: Dict[str, bool]) -> int:
        permissions = 0
        for name, enabled in permission_mapping.items():
            if enabled:
                permissions |= getattr(Flags, name, 0)

        return permissions

    def add(self, permission: int):
        self.value |= permission

    def remove(self, permission: int):
        self.value &= ~permission
    
    def _contains(self, permission: int) -> bool:
        return (self.value & permission) == permission

    def __contains__(self, item: Any) -> bool:
        if isinstance(item, Permissions):
            return self._contains(item.value)

        elif isinstance(item, int):
            return self._contains(item)

        elif isinstance(item, list):
            return any(self._contains(value) for value in item)

        else:
            raise TypeError(
                f"Can't compare {self.__class__.__name__} with {item.__class__.__name__}"
            )

    def _list_enabled_perms(self) -> Generator[str, None, None]:
        for cls in type(self).mro():
            for flag_name, value in cls.__dict__.items():
                if (isinstance(value, flag)) and (getattr(cls, flag_name) in self):
                    yield f"{flag_name}=True"

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(self._list_enabled_perms())})"

    def __repr__(self) -> str:
        return self.__str__()


class Roles(Enum):
    BOT = 1 # CREATE_CONTENT
    VERIFIED_BOT = 17 # CREATE_CONTENT + VERIFIED_ACCOUNT
    USER = 3 # CREATE_CONTENT + MANAGE_ACCOUNT
    DEVELOPER = 7 # CREATE_CONTENT + MANAGE_ACCOUNT + DEVELOPER_TOOLS
    VERIFIED_USER = 19 # CREATE_CONTENT + MANAGE_ACCOUNT + VERIFIED_ACCOUNT
    VERIFIED_DEVELOPER = 20 # CREATE_CONTENT + MANAGE_ACCOUNT + DEVELOPER_TOOLS + VERIFIED_ACCOUNT
    PARTNER = 11 # CREATE_CONTENT + MANAGE_ACCOUNT + PARTNER_TOOLS
    TESTER = 32 # FEATURE_PREVIEWS
    MODERATOR = 64 # MANAGE_REPORST
    ADMINISTRATOR = 192 # MANAGE_REPORST + MANAGE_CASES
    TEAM = 448 # MANAGE_REPORTS + MANAGE_CASES + MANAGE_PERMISSIONS

    @staticmethod
    def get_by_name(name: str) -> Enum:
        for role in Roles:
            if role.name == name:
                return role
                
        return Roles.BOT