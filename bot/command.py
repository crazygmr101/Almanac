from typing import Tuple, Dict, List, Union, Literal

from discord.ext import commands
from discord.ext.commands import Greedy

from bot.converters import MapLayerType

FRIENDLY_TYPE_NAMES = {
    int: "integer",
    float: "decimal",
    MapLayerType: "map layer name",
    str: "text"
}


class AlmanacCommand(commands.Command):
    def __init__(self, func, name, **attrs):
        self.arg_list: Dict[str, Tuple[bool, type, str]] = attrs.pop("arg_list")
        super(AlmanacCommand, self).__init__(func, name=name, **attrs)

    @property
    def argument_doc(self) -> List[str]:
        return [
            f"`{name}` ({'Optional ' if arg[0] else ''} "
            f"{FRIENDLY_TYPE_NAMES.get(arg[1], arg[1].__name__)}) - {arg[2]}"
            for name, arg in self.arg_list.items()
        ]

    @property
    def signature(self):
        # exactly the same as d.py's except usage doesn't override it
        params = self.clean_params
        if not params:
            return ''

        result = []
        for name, param in params.items():
            greedy = isinstance(param.annotation, Greedy)
            optional = False  # postpone evaluation of if it's an optional argument

            # for typing.Literal[...], typing.Optional[typing.Literal[...]], and Greedy[typing.Literal[...]], the
            # parameter signature is a literal list of it's values
            annotation = param.annotation.converter if greedy else param.annotation
            origin = getattr(annotation, '__origin__', None)
            if not greedy and origin is Union:
                none_cls = type(None)
                union_args = annotation.__args__
                optional = union_args[-1] is none_cls
                if len(union_args) == 2 and optional:
                    annotation = union_args[0]
                    origin = getattr(annotation, '__origin__', None)

            if origin is Literal:
                name = '|'.join(f'"{v}"' if isinstance(v, str) else str(v) for v in annotation.__args__)
            if param.default is not param.empty:
                # We don't want None or '' to trigger the [name=value] case and instead it should
                # do [name] since [name=None] or [name=] are not exactly useful for the user.
                should_print = param.default if isinstance(param.default, str) else param.default is not None
                if should_print:
                    result.append(f'[{name}={param.default}]' if not greedy else
                                  f'[{name}={param.default}]...')
                    continue
                else:
                    result.append(f'[{name}]')

            elif param.kind == param.VAR_POSITIONAL:
                if self.require_var_positional:
                    result.append(f'<{name}...>')
                else:
                    result.append(f'[{name}...]')
            elif greedy:
                result.append(f'[{name}]...')
            elif optional:
                result.append(f'[{name}]')
            else:
                result.append(f'<{name}>')

        return ' '.join(result)