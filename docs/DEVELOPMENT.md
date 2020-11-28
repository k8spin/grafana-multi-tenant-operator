# Development

## Setting up python local development environment

```bash
$ git clone git@github.com:k8spin/grafana-multi-tenant-operator.git
Cloning into 'grafana-multi-tenant-operator'...
remote: Enumerating objects: 85, done.
remote: Counting objects: 100% (85/85), done.
remote: Compressing objects: 100% (58/58), done.
remote: Total 85 (delta 21), reused 85 (delta 21), pack-reused 0
Receiving objects: 100% (85/85), 21.57 KiB | 3.59 MiB/s, done.
Resolving deltas: 100% (21/21), done.
$ cd grafana-multi-tenant-operator
```

Then

```bash
$ virtualenv -p python3.7 .venv
Running virtualenv with interpreter /usr/bin/python3.7
Using base prefix '/usr'
/usr/lib/python2.7/site-packages/virtualenv.py:1047: DeprecationWarning: the imp module is deprecated in favour of importlib; see the module's documentation for alternative uses
  import imp
New python executable in /home/angel/personal/grafana-user-operator/.venv/bin/python3.7
Also creating executable in /home/angel/personal/grafana-user-operator/.venv/bin/python
Installing setuptools, pip, wheel...done.
[angel@elitebook grafana-user-operator]$ source .venv/bin/activate
(.venv) $ pip install -r requirements-dev.txt
...
..
.
Installing collected packages: pyyaml, chardet, urllib3, certifi, idna, requests, grafana-api, async-timeout, multidict, yarl, attrs, aiohttp, typing-extensions, aiojobs, click, iso8601, pykube-ng, kopf, pycodestyle, autopep8, mccabe, six, lazy-object-proxy, typed-ast, wrapt, astroid, isort, pylint
Successfully installed aiohttp-3.6.2 aiojobs-0.2.2 astroid-2.3.3 async-timeout-3.0.1 attrs-19.3.0 autopep8-1.5 certifi-2019.11.28 chardet-3.0.4 click-7.0 grafana-api-0.9.3 idna-2.8 iso8601-0.1.12 isort-4.3.21 kopf-0.25 lazy-object-proxy-1.4.3 mccabe-0.6.1 multidict-4.7.4 pycodestyle-2.5.0 pykube-ng-20.1.0 pylint-2.4.4 pyyaml-5.3 requests-2.22.0 six-1.14.0 typed-ast-1.4.1 typing-extensions-3.7.4.1 urllib3-1.25.8 wrapt-1.11.2 yarl-1.4.2
```

## Building

Build the Grafana multi-tenant operator image and push it to a public registry such as `ghcr.io`:

```bash
$ pwd
grafana-multi-tenant-operator
$ export IMAGE=ghcr.io/k8spin/grafana-multi-tenant-operator:v1.1.0-rc3
$ docker build -t ${IMAGE} .
$ docker push ${IMAGE}
```
