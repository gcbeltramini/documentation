#!/usr/bin/env bash

set -euo pipefail

#? My CLI command 0.1.0
#? Copyright (C) ...

##? Dummy command.
##?
##? Usage:
##?   my_command.sh action1 [--boolean-param]
##?                         [--named-param <v>]
##?                         [<in-value1> <in-value2>]
##?   my_command.sh action2 [--repeatable-param]...
##?                         [--param-array <v>]...
##?                         [<in-array1> <in-array2> <in-array3>]...
##?   my_command.sh         <argv>...
##?                         (--this_m | --that_m)
##?                         [--this_o | --that_o]
##?                         [-v -v -v]
##?   my_command.sh         --help | --version
##?
##? Arguments:
##?   <in-value>              Some inputs.
##?   <in-array>              Some inputs registered as array.
##?   <argv>                  Repeatable arguments.
##? 
##? Options:
##?   -h, --help              Show this help message and exit.
##?   --version               Show version and exit.
##?   --boolean-param         Boolean parameter.
##?   --named-param <v>       The value will be in "named_param", not in "v".
##?                           Without default, it will be "null". [default: 42]
##?   -r, --repeatable-param  The value will be the number of times this parameter
##?                           was passed.
##?   -a, --param-array <v>   The value will be in array "param_array", not in "v".
##?                           Without default, it will be "[]". [default: 37]
##?   --this_m                Mandatory option. Choose "this_m" or "that_m".
##?   --that_m                Mandatory option. Choose "this_m" or "that_m".
##?   --this_o                Optional parameter. Choose "this_o" or "that_o".
##?   --that_o                Optional parameter. Choose "this_o" or "that_o".
##?   -v                      Verbose (-v, -vv or -vvv).
##?
##? Examples:
##?   my_command.sh --help
##?   my_command.sh --version
##?   my_command.sh action1 --boolean-param --named-param foo in1
##?   my_command.sh action2 -r -r -a a1 -a a2 -a a3 in11 in21 in31 in12
##?   my_command.sh foo bar --that_m -vv

help=$(grep "^##?" "$0" | cut -c 5-)
version=$(grep "^#?"  "$0" | cut -c 4-)
eval "$(docopts -h "$help" -V "$version" : "$@")"

echo "help=${help}"
echo "version=${version}"

echo "action1=${action1}"
echo "action2=${action2}"
echo "boolean_param=${boolean_param}"
echo "named_param=${named_param}"
echo "in_value1=${in_value1}"
echo "in_value2=${in_value2}"

echo "repeatable_param=${repeatable_param}"
echo "param_array=${param_array[@]}"
echo "in_array1=${in_array1[@]}"
echo "in_array2=${in_array2[@]}"
echo "in_array3=${in_array3[@]}"

echo "argv=${argv[@]}"
echo "this_m=${this_m}"
echo "that_m=${that_m}"
echo "this_o=${this_o}"
echo "that_o=${that_o}"
echo "v=${v}"
