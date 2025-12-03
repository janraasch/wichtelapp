## Notes to self

### requirements.txt

```bash
# update requirements.txt for production deploy
uv export --no-dev --no-hashes > requirements.txt
```

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

### fly.io

```bash
# deploy
fly deploy

# start shell
fly ssh console

# stream logs
fly logs
```
