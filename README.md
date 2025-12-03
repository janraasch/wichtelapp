## Notes to self

### requirements.txt

```bash
# update requirements.txt for production deploy
uv export --no-dev --no-hashes > requirements.txt
```

### fly.io

```bash
# deploy
fly deploy

# start shell
fly ssh console

# stream logs
fly logs
```
