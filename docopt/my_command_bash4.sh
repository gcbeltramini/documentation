#!/usr/bin/env bash

set -euo pipefail

# Dummy command.
#
# Usage:
#   my_command.sh action1 [--boolean-param]
#                         [--named-param <v>]
#                         [<in-value1> <in-value2>]
#   my_command.sh action2 [--repeatable-param]...
#                         [--param-array <v>]...
#                         [<in-array1> <in-array2> <in-array3>]...
#   my_command.sh         <argv>...
#                         (--this_m | --that_m)
#                         [--this_o | --that_o]
#                         [-v -v -v]
#   my_command.sh         --help | --version
#
# Arguments:
#   <in-value>              Some inputs.
#   <in-array>              Some inputs registered as array.
#   <argv>                  Repeatable arguments.
# 
# Options:
#   -h, --help              Show this help message and exit.
#   --version               Show version and exit.
#   --boolean-param         Boolean parameter.
#   --named-param <v>       The value will be in "named_param", not in "v".
#                           Without default, it will be "null". [default: 42]
#   -r, --repeatable-param  The value will be the number of times this parameter
#                           was passed.
#   -a, --param-array <v>   The value will be in array "param_array", not in "v".
#                           Without default, it will be "[]". [default: 37]
#   --this_m                Mandatory option. Choose "this_m" or "that_m".
#   --that_m                Mandatory option. Choose "this_m" or "that_m".
#   --this_o                Optional parameter. Choose "this_o" or "that_o".
#   --that_o                Optional parameter. Choose "this_o" or "that_o".
#   -v                      Verbose (-v, -vv or -vvv).
#
# Examples:
#   my_command.sh --help
#   my_command.sh --version
#   my_command.sh action1 --boolean-param --named-param foo in1
#   my_command.sh action2 -r -r -a a1 -a a2 -a a3 in11 in21 in31 in12
#   my_command.sh foo bar --that_m -vv
#
# ----
# My CLI command 0.1.0
# Copyright (C) ...


# Option 1.1
source docopts.sh
help=$(docopt_get_help_string "$0")
version=$(docopt_get_version_string "$0")
parsed=$(docopts -G ARGS -h "${help}" -V "${version}" : "$@")
eval "${parsed}"


# # Option 1.2
# source docopts.sh
# help=$(docopt_get_help_string "$0")
# version=$(docopt_get_version_string "$0")
# parsed=$(docopts -A ARGS -h "${help}" -V "${version}" : "$@")
# eval "${parsed}"
# for a in "${!ARGS[@]}"; do
#     echo "$a=${ARGS[$a]}"
# done

# # Construct array (only works when using 'docopts -A ...'):
# # myarray=( $(docopt_get_values ARGS "--param-array") )
# eval "$(docopt_get_eval_array ARGS "--param-array" myarray)" # same effect as the above
# echo "${myarray[@]}"


# # Option 2:
# # Problem: the example 'my_command.sh --version' does not show the version
# source docopts.sh --auto -G "$@"
# # This command uses 'docopt_auto_parse'


# Print arguments:

docopt_print_ARGS -G # only works when using 'docopts -G ...'

# Access associative array:
echo "----"
echo "ARGS_param_array[0]=${ARGS_param_array[0]}"
