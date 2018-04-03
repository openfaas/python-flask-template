# python-flask-template

Python OpenFaaS template with Flask

To try this out with either Python 2.7 or Python 3.6:

```bash
faas template pull https://github.com/openfaas-incubator/python-flask-template
faas new --list
Languages available as templates:
- python27-flask
- python3-flask
```

Generate a function with one of the languages:

```bash
faas new --lang python3-flask myfunction
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
