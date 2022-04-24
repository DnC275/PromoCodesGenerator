# PromoCodesGenerator
## Set up
```bash 
python -m venv venv
```

```bash
pip install -r requirements.txt
```

## Usage
Generates codes:
```bash
./manage.py generate_codes {group_name} {amount} -f file_name
```
Option -f not required and allows to specify the name of JSON file where  generated promo codes will be stored.
By default, "promo_codes.json" will be used. This file will be stored in the root of project.
```bash
./manage.py check_promocode {promo_code}
```
## Testing
```bash
./manage.py test
```