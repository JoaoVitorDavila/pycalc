#!/bin/sh
set -e

if [ -f /ansible/ansible/pycalc-key.pem ]; then
    cp /ansible/ansible/pycalc-key.pem /tmp/pycalc-key.pem
    chmod 600 /tmp/pycalc-key.pem
fi

exec ansible-playbook "$@"