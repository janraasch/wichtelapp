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

### fly.io

```bash
# deploy
fly deploy

# start shell
fly ssh console

# then, to e.g. run python shell
export PATH="/app/.venv/bin:$PATH"
python manage.py shell

# stream logs
fly logs
```
