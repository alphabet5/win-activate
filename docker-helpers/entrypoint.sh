#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status.

# allow arguments to be passed
if [[ ${1:0:1} = '-' ]]; then
  EXTRA_ARGS="$@"
  set --  #If no arguments follow this option, then the positional parameters are unset.
          #Otherwise, the positional parameters are set to the arguments,
          #even if some of them begin with a '-'.
elif [[ ${1} == win-activate || ${1} == $(which win-activate) ]]; then # if the first parameter is "win-activate" or "/some/dir/win-activate" then the extra args start later.
  EXTRA_ARGS="${@:2}"
  set --
fi

if [[ -z ${1} ]]; then # if the string (argument 1) is null
  echo "Starting win-activate..."
  exec $(which win-activate) ${EXTRA_ARGS}
else
  exec "$@"
fi