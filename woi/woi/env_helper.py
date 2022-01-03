import os

from pathlib import Path
from typing import Any, Callable, Union
from warnings import warn


_PATH = Path(__file__).resolve()
_default = os.urandom(40)


class ConfigurationError(Exception):
    pass


def _bool(value: str) -> bool:
    return value.lower() in ('true', 'on', 'yes', '1')


class Configuration:

    def __init__(
        self,
        paths: Union[list, str, Path] = None,
        env_override: bool = False,
        guess_type: bool = True,
        list_item_separator: str = ' ',
        **additional_config
    ) -> None:
        if paths is None:
            paths = [_PATH / '.env']
        elif isinstance(paths, (str, Path)):
            paths = [paths]
        self.paths = [Path(x).resolve() for x in paths]
        self.env_override = env_override
        self.guess_type = guess_type
        self.list_item_separator = list_item_separator
        self._config = {}
        self.load()
        self._config.update(additional_config)
        self._cache = {}

    def load_file(self, path: Path) -> None:
        with path.open() as fp:
            for line in fp:
                if line.strip() and not line.startswith('#'):
                    name, value = line.split('=', 1)
                    name = name.strip()
                    if name in os.environ and self.env_override:
                        value = os.environ.get(name)
                    self._config[name] = value.strip()

    def load(self) -> None:
        for path in self.paths:
            if not path.exists():
                warn(f'File {path} does not exist, skipping...')
            else:
                self.load_file(path)

    def get(
        self,
        key: str,
        default: Any = _default,
        convert: Callable = str
    ) -> Any:
        if key not in self._cache:
            self._cache[key] = self._get(key, default, convert)
        return self._cache[key]

    def _get(self, key, default, convert):
        if (
            default != _default
            and default is not None
            and self.guess_type
            and convert == str
        ):
            convert = type(default)
        if convert == bool:
            convert = _bool
        if key in self._config:
            value = self._config[key].strip()
            if value:
                if convert == list:
                    if self.list_item_separator == ' ':
                        value = value.strip('()')
                    return [x.strip() for x in
                            value.split(self.list_item_separator) if x.strip()]
                return convert(value)
            return ''
        if default != _default:
            print(f'Key {key} not found, using default: {default}')
            return default
        else:
            raise ConfigurationError(
                f'Key {key} not found and no default given!'
            )

    def dump(self) -> None:
        for key in sorted(self._config.keys()):
            print(f'{key}={self._config[key]}')
