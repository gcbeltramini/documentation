#!/usr/bin/env bash

set -euo pipefail

eval "$(docopts -G ARGS -V - -h - : "$@" <<EOF
Dummy command.

Usage:
  my_command.sh action1 [--boolean-param]
                        [--named-param <v>]
                        [<in-value1> <in-value2>]
  my_command.sh action2 [--repeatable-param]...
                        [--param-array <v>]...
                        [<in-array1> <in-array2> <in-array3>]...
  my_command.sh         <argv>...
                        (--this_m | --that_m)
                        [--this_o | --that_o]
                        [-v -v -v]
  my_command.sh         --help | --version

Arguments:
  <in-value>              Some inputs.
  <in-array>              Some inputs registered as array.
  <argv>                  Repeatable arguments.

Options:
  -h, --help              Show this help message and exit.
  --version               Show version and exit.
  --boolean-param         Boolean parameter.
  --named-param <v>       The value will be in "named_param", not in "v".
                          Without default, it will be "null". [default: 42]
  -r, --repeatable-param  The value will be the number of times this parameter
                          was passed.
  -a, --param-array <v>   The value will be in array "param_array", not in "v".
                          Without default, it will be "[]". [default: 37]
  --this_m                Mandatory option. Choose "this_m" or "that_m".
  --that_m                Mandatory option. Choose "this_m" or "that_m".
  --this_o                Optional parameter. Choose "this_o" or "that_o".
  --that_o                Optional parameter. Choose "this_o" or "that_o".
  -v                      Verbose (-v, -vv or -vvv).

Examples:
  my_command.sh --help
  my_command.sh --version
  my_command.sh action1 --boolean-param --named-param foo in1
  my_command.sh action2 -r -r -a a1 -a a2 -a a3 in11 in21 in31 in12
  my_command.sh foo bar --that_m -vv

----
My CLI command 0.1.0
Copyright (C) ...
EOF
)"


# # Or:
# get_help() {
#   cat << EOH
# Dummy command.

# Usage:
#   my_command.sh action1 [--boolean-param]
# (...))
# EOH
# }

# get_version() {
#   cat << EOV
# My CLI command 0.1.0
# Copyright (C) ...
# EOV
# }
# eval "$(docopts -G ARGS -h "$(get_help)" -V "$(get_version)" : "$@")"


# Print arguments:
source docopts.sh
docopt_print_ARGS -G

# Access associative array:
echo "----"
echo "ARGS_param_array[0]=${ARGS_param_array[0]}"
