#!/usr/bin/env bash

set -euo pipefail


# Convenience functions
info () {
  printf "\r[ \033[00;34m..\033[0m ] $1\n"
}

success () {
  printf "\r\033[2K[ \033[00;32mOK\033[0m ] $1\n"	  
}

fail () {
  printf "\r\033[2K[\033[0;31mFAIL\033[0m] $1\n"
}

check_binary () {
  which $1 > /dev/null 2>&1
  status=$?
  if [ $status -eq 0 ]; then
    success "Found binary ${1} in PATH"
  else
    fail "No valid binary for ${1} found in PATH. Please correct your installation"
    exit 1
  fi
}


# Get user inputs

nodes=4
while getopts "n:" opt; do
  case ${opt} in
    n) nodes="${OPTARG}"
    ;;
    \?) info "Invalid option -${OPTARG}"
  esac
done


# Setup checks
set +e

info "Checking for Docker installation..."
check_binary "docker"

info "Checking for minikube installation..."
check_binary "minikube"

info "Checking for kubectl installation"
check_binary "kubectl"

set -e


# Minikube startup
minikube start --nodes ${nodes}
