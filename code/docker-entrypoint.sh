#!/bin/bash

#credits: KNR Web

ownership() {
    # Fixes ownership of output files
    # source: https://github.com/BD2KGenomics/cgl-docker-lib/blob/master/mutect/runtime/wrapper.sh#L5
    user_id=$(stat -c '%u:%g' /code)
    chown -R "${user_id}" /code
}

echo "Installing missing packets"
pip install -r ./requirements.txt
echo "Waiting for postgres"
chmod +x wait-for-it.sh
./wait-for-it.sh -t 80 "$POSTGRES_SERVICE":5432 || exit 1

echo '--------------------------'
echo 'Database migration'
echo '--------------------------'
python manage.py makemigrations || exit 1
python manage.py migrate || exit 1


echo '--------------------------'
echo 'Run test + coverage'
echo '--------------------------'
coverage run --source='.' manage.py test --noinput
coverage report

echo '--------------------------'
echo 'Fixing ownership of files'
echo '--------------------------'
ownership

echo '--------------------------'
echo 'Run command'
# shellcheck disable=SC2068
echo $@
echo '--------------------------'
# shellcheck disable=SC2068
python manage.py $@ || exit 1
