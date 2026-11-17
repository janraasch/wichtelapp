## Notes to self

### just

```bash
# install
brew install just

# run dev server
just dev

# format code
just fmt

# run tests
just test
```

### Coolify (production)

Deployed as a Docker Compose resource on a Hetzner VM, domain `wichtelapp.janraasch.com`.
The app itself is the `wichtelapp` service in `docker-compose.yml`; Coolify's Traefik
proxy handles TLS, and SQLite data lives in the `wichtel-db` volume.

Environment variables (Coolify UI):

```bash
SECRET_KEY=$(openssl rand -base64 48)   # required
```

`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS` and `DEBUG` come from `docker-compose.yml`.
Set `DATABASE_URL` to switch from SQLite to Postgres; no other change needed.

```bash
# create the admin user (Coolify terminal)
python manage.py createsuperuser
```

Users are created by hand in `/admin/`: add a User, then a Profile (code name,
address) and optionally a Wishlist. Signup is disabled.
