#########
# BUILD #
#########
develop:  ## install dependencies and build library
	python -m pip install -e .[develop]

build:  ## build the python library
	python setup.py build build_ext --inplace

install:  ## install library
	python -m pip install .


#########
# LINTS #
#########
lint:  ## run static analysis with black, flake8, and pylint
	python -m black --check mctk setup.py
	python -m flake8 --max-line-length 120 mctk setup.py
	python -m pylint --disable=C0301,C0114,C0115,C0116,R1720 mctk setup.py

# Alias
lints: lint

format:  ## run autoformatting with black
	python -m black mctk/ setup.py

# alias
fix: format

check:  ## check assets for packaging
	check-manifest -v

# Alias
checks: check

annotate:  ## run type checking
	python -m mypy ./mctk


#########
# TESTS #
#########
test: ## clean and run unit tests
	python -m pytest -v mctk/tests

coverage:  ## clean and run unit tests with coverage
	python -m pytest -v mctk/tests --cov=mctk --cov-branch --cov-fail-under=75 --cov-report term-missing

# Alias
tests: test
cov: coverage


###########
# VERSION #
###########
show-version:
	bump2version --dry-run --allow-dirty setup.py --list | grep current | awk -F= '{print $2}'

patch:
	bump2version patch

minor:
	bump2version minor

major:
	bump2version major


########
# DIST #
########
dist-build:  # Build python dist
	python setup.py sdist bdist_wheel

dist-check:
	python -m twine check dist/*

dist: clean build dist-build dist-check  ## Build dists

publish:  # Upload python assets
	echo "would usually run python -m twine upload dist/* --skip-existing"


#########
# CLEAN #
#########
clean-deep: ## clean everything untracked from the repository
	git clean -fdx

clean-linux: ## clean the repository
	rm -rf .coverage coverage cover htmlcov logs build dist *.egg-info .pytest_cache


############################################################################################


# Thanks to Francoise at marmelab.com for this
.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

print-%:
	@echo '$*=$($*)'

.PHONY: develop build install lint lints format fix check checks annotate test cov coverage tests show-version patch minor major dist-build dist-check dist publish clean-deep clean-linux help
