#!/usr/bin/env python3

"""
Dummy command.

Usage:
  my_command.py action1 [--boolean-param]
                        [--named-param <v>]
                        [<in-value1> <in-value2>]
  my_command.py action2 [--repeatable-param]...
                        [--param-array <v>]...
                        [<in-array1> <in-array2> <in-array3>]...
  my_command.py         <argv>...
                        (--this_m | --that_m)
                        [--this_o | --that_o]
                        [-v -v -v]
  my_command.py         --help | --version

Arguments:
  <in-value>              Some inputs.
  <in-array>              Some inputs registered as array.
  <argv>                  Repeatable arguments.

Options:
  -h, --help              Show this help message and exit.
  --version               Show version and exit.
  --boolean-param         Boolean parameter.
  --named-param <v>       The value will be in "named-param", not in "v".
                          Without default, it will be "null". [default: 42]
  -r, --repeatable-param  The value will be the number of times this parameter
                          was passed.
  -a, --param-array <v>   The value will be in array "param-array", not in "v".
                          Without default, it will be "[]". [default: 37]
  --this_m                Mandatory option. Choose "this_m" or "that_m".
  --that_m                Mandatory option. Choose "this_m" or "that_m".
  --this_o                Optional parameter. Choose "this_o" or "that_o".
  --that_o                Optional parameter. Choose "this_o" or "that_o".
  -v                      Verbose (-v, -vv or -vvv).

Examples:
  my_command.py --help
  my_command.py --version
  my_command.py action1 --boolean-param --named-param foo in1
  my_command.py action2 -r -r -a a1 -a a2 -a a3 in11 in21 in31 in12
  my_command.py foo bar --that_m -vv
"""

from docopt import docopt
from schema import Schema, And, Or, Use, SchemaError


def list_with_str_content(li: list) -> bool:
  return isinstance(li, list) and all([isinstance(el, str) for el in li])


def non_negative_int(x: int) -> bool:
  return isinstance(x, int) and x >= 0


str_or_empty = Or(str, None)


if __name__ == '__main__':
    args = docopt(__doc__, version='My CLI command 0.1.0')

    schema = Schema({
      '--boolean-param': bool,
      '--help': bool,
      '--named-param': str_or_empty, 
      '--param-array': list_with_str_content,
      '--repeatable-param': non_negative_int,
      '--that_m': bool,
      '--that_o': bool,
      '--this_m': bool,
      '--this_o': bool,
      '--version': bool,
      '-v': non_negative_int,
      '<argv>': list_with_str_content,
      '<in-array1>': list_with_str_content,
      '<in-array2>': list_with_str_content,
      '<in-array3>': list_with_str_content,
      '<in-value1>': str_or_empty,
      '<in-value2>': str_or_empty,
      'action1': bool,
      'action2': bool})

    try:
      args = schema.validate(args)
    except SchemaError as e:
      exit(e)

    print(args)
