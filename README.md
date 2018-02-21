# python27-flask-template
Python 2.7 OpenFaaS template with Flask

To try this out:

```bash
faas template pull https://github.com/alexellis/python27-flask-template
faas new --lang python27-flask myfunction
mv myfunction.yml stack.yml

```

Followed by the usual flow:

```
faas build \
  && faas deploy
  && faas list --verbose

# Wait a couple of seconds then:

echo -n content | faas invoke myfunction
```
