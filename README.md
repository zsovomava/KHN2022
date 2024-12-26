# Helló, Világ!

## Előfeltételek
A szerver működtetéséhez **Python 3.8** (vagy újabb) szükséges.

## Telepítés
### Python
```sh
pip install -r requirements.txt

cd mysite/

python manage.py migrate main accounts groups

python manage.py createsuperuser
```

## Környezeti változók

Az e-mailezés működéséhez szükséges beállítani az EMAIL_HOST_USER-t és az EMAIL_HOST_PASSWORD-öt egy-egy környezeti változóként.

## Futtatás
```sh
cd mysite/

python manage.py runsever 0.0.0.0:6969
```

## Dokumentáció

A gyökérmappában található meg _Dokumentáció.pdf_ néven.
