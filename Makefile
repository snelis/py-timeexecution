DE_PYPI_HOST=`docker-machine ip default`
DE_PYPI="http://${DE_PYPI_HOST}:8333/simple/"
VENVBIN= "venv/bin"
VENVACTIVATE = "${VENVBIN}/activate"
PYTHON=`. ${VENVACTIVATE}; which python`
PIP=`. ${VENVACTIVATE}; which pip`
FLAKE8=`. ${VENVACTIVATE}; which flake8`
TOX=`which tox || echo ${VENVBIN}/tox`
TOX_PY_LIST=`$$TOX -l | grep ^py | xargs | sed -e 's/ /,/g'`

.PHONY: clean virtualenv test

docsclean:
	@rm -fr docs/_build/

clean: docsclean
	@find . -name *.pyc -delete
	@rm -rf de_core.egg-info build

virtualenv: clean
	test -d venv || virtualenv-2.7 -p python2.7 venv
	$(PIP) install -U "pip>=7.0"
	$(PIP) install -i $(DE_PYPI) --trusted-host $(DE_PYPI_HOST) py-pkgversion -q
	$(PIP) install -i $(DE_PYPI) --trusted-host $(DE_PYPI_HOST) -r requirements.txt -q

build: clean
	$(TOX)

test: clean
	TOX=${TOX}; $$TOX -e ${TOX_PY_LIST}

test/%: clean
	$(TOX) -e $(TOX_PY_LIST) -- $*

lint: virtualenv
	$(FLAKE8) base.py

docs/%: virtualenv
	@make -C docs $*

docker:
	docker-compose run --rm app bash

docker/%:
	docker-compose run --rm app make $*

publish:
	$(PYTHON) setup_gen.py
	$(PYTHON) setup.py sdist upload -r de
