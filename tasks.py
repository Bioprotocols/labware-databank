"""
Tasks for maintaining the project.

Execute 'invoke --list' for guidance on using Invoke
"""
import os
import sys
import platform
import shutil
import webbrowser
from pathlib import Path
from distutils.util import strtobool
import venv 

import pytest
from invoke import task, exceptions  # type: ignore

OS_PLATFORM = platform.system() 
HOME_DIR = str(Path.home())
ROOT_DIR = Path(__file__).parent
BIN_DIR = ROOT_DIR.joinpath("bin")
SETUP_FILE = ROOT_DIR.joinpath("setup.py")
TEST_DIR = ROOT_DIR.joinpath("tests")
SOURCE_DIR = ROOT_DIR.joinpath("labop_labware_ontology")
TOX_DIR = ROOT_DIR.joinpath(".tox")
JUNIT_XML_FILE = BIN_DIR.joinpath("report.xml")
COVERAGE_XML_FILE = BIN_DIR.joinpath("coverage.xml")
COVERAGE_HTML_DIR = BIN_DIR.joinpath("coverage_html")
COVERAGE_HTML_FILE = COVERAGE_HTML_DIR.joinpath("index.html")
DOCS_DIR = ROOT_DIR.joinpath("docs")
DOCS_SOURCE_DIR = DOCS_DIR.joinpath("source")
DOCS_BUILD_DIR = DOCS_DIR.joinpath("_build")
DOCS_INDEX = DOCS_BUILD_DIR.joinpath("index.html")
PYTHON_DIRS = [str(d) for d in [SOURCE_DIR, TEST_DIR]]
SAFETY_REQUIREMENTS_FILE = BIN_DIR.joinpath("safety_requirements.txt")
PYPI_URL = "https://pypi.python.org/api/pypi/pypi/simple"
PYTHON_VERSION = 3.9
CI_PROJECT_NAME = "labop-labware-ontology"
CI_REGISTRY_IMAGE = "registry.gitlab.com/opensourcelab/labop-labware-ontology"
DOCKERFILE = "Dockerfile"
DOCKER_BUILD_PLATFORM = "--platform linux/amd64"
VENV_MODULE_NAME = "venv"



def _delete_file(file):
    """
    If the file exists, delete it

    :param file: The file to delete
    """
    try:
        file.unlink(missing_ok=True)
    except TypeError:
        # missing_ok argument added in 3.8
        try:
            file.unlink()
        except FileNotFoundError:
            pass


def _run(_c, command):
    """
    It runs a command

    :param _c: The context object that is passed to invoke tasks
    :param command: The command to run
    """
    return _c.run(command, pty=platform.system() != 'Windows')


def _get_registry_path_str(python_version):
    """
    It takes a build tag and a Python version, and returns a string that is the path to the image in the registry

    :param python_version: The version of Python to use
    :return: The registry path for the image.
    """
    ci_commit_ref_name = os.popen("git symbolic-ref --short -q HEAD").read().strip()
    build_tag = ci_commit_ref_name if ci_commit_ref_name else "latest"
    image_name = f"{CI_PROJECT_NAME}:py{python_version}-{build_tag}"
    registry_path = f"{CI_REGISTRY_IMAGE}/{image_name}"
    return registry_path


@task(help={'check': "Checks if source is formatted without applying changes"})
def format(_c, check=False):
    """
    It runs the `black` and `isort` tools on the Python code in the `PYTHON_DIRS` directories

    :param _c: The context object that is passed to invoke tasks
    :param check: If True, the code will be checked for formatting, but not changed, defaults to False (optional)
    """
    python_dirs_string = " ".join(PYTHON_DIRS)
    # Run black
    black_options = "--check" if check else ""
    _run(_c, f"black {black_options} {python_dirs_string}")
    # Run isort
    isort_options = "--check-only --diff" if check else ""
    _run(_c, f"isort {isort_options} {python_dirs_string}")


@task
def lint_flake8(_c):
    """
    It runs the flake8 linter on all Python files in the project

    :param _c: The context object that is passed to invoke tasks
    """
    _run(_c, f"flake8 {' '.join(PYTHON_DIRS)}")


@task
def lint_mypy(_c):
    """
    It runs mypy on all Python files in the project

    :param _c: The context object that is passed to invoke tasks
    """
    _run(_c, "mypy {}".format(" ".join(PYTHON_DIRS)))


@task(lint_flake8, lint_mypy)
def lint(_):
    """
    It runs all linting tools on all Python files in the project
    """


@task
def security_bandit(_c):
    """
    It runs bandit security checks on the source directory

    :param _c: The command to run
    """
    _run(_c, f"bandit -c pyproject.toml -r {SOURCE_DIR}")


@task
def security_safety(_c):
    """
    It runs security checks on package dependencies

    :param _c: The context object that is passed to the task
    """
    Path(BIN_DIR).mkdir(parents=True, exist_ok=True)
    _run(_c, f"poetry export --dev --format=requirements.txt --without-hashes --output={SAFETY_REQUIREMENTS_FILE}")
    _run(_c, f"safety check --file={SAFETY_REQUIREMENTS_FILE} --full-report")


@task(security_bandit, security_safety)
def security(_):
    """
    It runs all security checks
    """


@task(
    optional=["coverage"],
    help={
        "coverage": 'Add coverage, ="html" for html output or ="xml" for xml output',
        "junit": "Output a junit xml report",
    },
)
def test(_, coverage=None, junit=False):
    """
    It runs the tests in the current directory

    :param _: The context object that is passed to invoke tasks
    :param coverage: Generates coverage report, "html" for html output or "xml" for xml output (optional)
    :param junit: If True, the test results will be written to a JUnit XML file, defaults to False (optional)
    """
    pytest_args = ["-v"]

    if junit:
        pytest_args.append(f"--junitxml={JUNIT_XML_FILE}")

    if coverage is not None:
        pytest_args.append(f"--cov={SOURCE_DIR}")

    if coverage == "html":
        pytest_args.append(f"--cov-report=html:{COVERAGE_HTML_DIR}")
    elif coverage == "xml":
        pytest_args.append(f"--cov-report=xml:{COVERAGE_XML_FILE}")

    pytest_args.append(str(TEST_DIR))
    return_code = pytest.main(pytest_args)

    if coverage == "html":
        webbrowser.open(COVERAGE_HTML_FILE.as_uri())

    if return_code:
        raise exceptions.Exit("Tests failed", code=return_code)


@task
def clean_docs(_c):
    """
    It takes a list of strings and returns a list of strings

    :param _c: The context object that is passed to invoke tasks
    """
    _run(_c, f"rm -fr {DOCS_BUILD_DIR}")
    _run(_c, f"rm -fr {DOCS_SOURCE_DIR}")


@task(pre=[clean_docs], help={"launch": "Launch documentation in the web browser"})
def docs(_c, launch=True):
    """
    It generates and opens the documentation for the project

    :param _c: The context object that is passed to invoke tasks
    :param launch: If True, the docs will be opened in a browser. defaults to True (optional)
    """
    # Generate autodoc stub files
    _run(_c, f"sphinx-apidoc -e -P -o {DOCS_SOURCE_DIR} {SOURCE_DIR}")
    # Generate docs
    _run(_c, f"sphinx-build -b html {DOCS_DIR} {DOCS_BUILD_DIR}")
    if launch:
        webbrowser.open(DOCS_INDEX.as_uri())


@task
def clean_build(_c):
    """
    It cleans all the Python build and distribution artifacts

    :param _c: The context object that is passed to invoke tasks
    """
    _run(_c, "rm -fr build/")
    _run(_c, "rm -fr dist/")
    _run(_c, "rm -fr .eggs/")
    _run(_c, "find . -name '*.egg-info' -exec rm -fr {} +")
    _run(_c, "find . -name '*.egg' -exec rm -f {} +")


@task
def clean_python(_c):
    """
    It removes all the Python artifacts

    :param _c: The context object that is passed to invoke tasks
    """
    _run(_c, "find . -name '*.pyc' -exec rm -f {} +")
    _run(_c, "find . -name '*.pyo' -exec rm -f {} +")
    _run(_c, "find . -name '*~' -exec rm -f {} +")
    _run(_c, "find . -name '__pycache__' -exec rm -fr {} +")


@task
def clean_tests(_):
    """
    It deletes all the test artifacts

    :param _: The context object that is passed to invoke tasks
    """
    _delete_file(JUNIT_XML_FILE)
    _delete_file(COVERAGE_XML_FILE)
    shutil.rmtree(COVERAGE_HTML_DIR, ignore_errors=True)
    shutil.rmtree(BIN_DIR, ignore_errors=True)
    shutil.rmtree(TOX_DIR, ignore_errors=True)


@task(pre=[clean_build, clean_python, clean_tests, clean_docs])
def clean(_):
    """
    It runs all clean sub-tasks

    :param _: The context object that is passed to invoke tasks
    """
    pass


@task(
    pre=[clean_python],
    optional=["python_version"],
    help={
        "python_version": 'Python version to use, e.g. "3.9"',
    },
)
def docker_build(_c, python_version=PYTHON_VERSION, target="test"):
    """
    It builds a Docker image with the given tag using the given Python version

    :param _c: The context object that is passed to invoke tasks
    :param python_version: The base python version to use
    :param target: The target to build ("test", "regression"), defaults to "test" (optional)
    """
    build_args = f"--build-arg PYTHON_BASE={python_version} --build-arg PYPI_URL={PYPI_URL}"
    registry_path = _get_registry_path_str(python_version)
    cache = f"--cache-from {registry_path}"
    target_tag = f"--target {target}"
    _run(
        _c,
        f"docker build {build_args} {DOCKER_BUILD_PLATFORM} {cache} -f {DOCKERFILE} -t {registry_path} {target_tag} .",
    )


@task
def docker_pull(_c, python_version=PYTHON_VERSION):
    """
    It pulls the image from the local registry, or if it doesn't exist, it prints a message

    :param _c: The context object that is passed to invoke tasks
    :param python_version: The base python version to use
    """
    registry_path = _get_registry_path_str(python_version)
    _run(_c, f'docker pull {registry_path} || echo "No pre-made image available"')


@task
def docker_push(_c, python_version=PYTHON_VERSION):
    """
    It pushes the image to the registry

    :param _c: The context object that is passed to invoke tasks
    :param python_version: The base python version to use
    """
    registry_path = _get_registry_path_str(python_version)
    _run(_c, f"docker push {registry_path}")


@task
def docker_test(_c, python_version=PYTHON_VERSION):
    """
    It runs the tests in a docker container

    :param _c: The context object that is passed to invoke tasks
    :param python_version: The base python version to use
    :param target: The target to test ("test", "regression"), defaults to "test" (optional)
    """
    volume_mount = (
        f"--volume {BIN_DIR}:/labop_labware_ontology/bin/ --volume {ROOT_DIR}:/labop_labware_ontology:rw"
    )
    registry_path = _get_registry_path_str(python_version)
    pytest_arg = f"pytest -v --cov-report xml:/labop_labware_ontology/bin/coverage.xml {TEST_DIR}"
    Path(BIN_DIR).mkdir(parents=True, exist_ok=True)
    _run(_c, f"docker run {DOCKER_BUILD_PLATFORM} {volume_mount} {registry_path} {pytest_arg}")


@task
def docker_shell(_c, python_version=PYTHON_VERSION):
    """
    It opens shell in the docker container

    :param _c: The context object that is passed to invoke tasks
    :param python_version: The base python version to use
    """
    volume_mount = (
        f"--volume {BIN_DIR}:/labop_labware_ontology/bin/ --volume {ROOT_DIR}:/labop_labware_ontology:rw"
    )
    registry_path = _get_registry_path_str(python_version)
    bash_path = "/bin/bash"
    _run(_c, f"docker run -it {DOCKER_BUILD_PLATFORM} {volume_mount} {registry_path} {bash_path}")


@task
def init_repo(_c):
    """Initialise the repository with git-LFS and git flow

    :param _c: The context object that is passed to invoke tasks
    :type _c: context object
    """
    # check, if it is already a git repo
    # otherwise run git init
    _run(_c, "git-lfs install")
    _run(_c, "git flow init")

@task(pre=[clean])
def release_twine(
    _c,
    tag_name,
    pypi_user,
    pypi_pass,
    pypi_publish_repository="https://artifactory.aws.gel.ac/artifactory/api/pypi/pypi_genomics_dev",
    pip_repository_index="https://artifactory.aws.gel.ac/artifactory/api/pypi/pypi/simple",
):
    """
    It makes a release of the Python package and publishes to the GEL PyPI Artifactory using setup.py and twine

    :param _c: The context object that is passed to invoke tasks
    :param tag_name: The name of the tag that triggered the workflow
    :param pypi_user: The username of the account that has access to the repository
    :param pypi_pass: The password for the pypi user
    :param pypi_publish_repository: The URL of the repository to publish to (optional)
    :param pip_repository_index: The URL of the pip repository to use for installing twine (optional)
    """
    version_str = tag_name.replace("v", "")
    _run(_c, f'echo "Build tag - {version_str}."')
    _run(_c, f"echo {version_str} > VERSION")
    pypirc_str = (
        "[distutils]\n"
        "index-servers = gel_pypi\n"
        "\n"
        "[gel_pypi]\n"
        f"repository: {pypi_publish_repository}\n"
        f"username: {pypi_user}\n"
        f"password: {pypi_pass}\n)"
    )
    _run(_c, f'printf "{pypirc_str}" > ~/.pypirc')
    _run(_c, f"pip install -i {pip_repository_index} twine")
    _run(_c, 'mkdir -p dist && rm -rf dist/* || echo "Nothing found in dist/"; python setup.py sdist;')
    _run(_c, f'twine upload --repository-url {pypi_publish_repository} -u "{pypi_user}" -p "{pypi_pass}" dist/*')


@task
def generate_reqs(_c):
    """
    It generates requirements.txt and requirements_dev.txt using poetry (dependencies from pyproject.toml).

    :param _c: The context object that is passed to invoke tasks
    """
    _run(_c, f"poetry export --without dev --without-hashes -f requirements.txt -o {ROOT_DIR}/requirements.txt")
    _run(_c, f"poetry export --only dev --without-hashes -f requirements.txt -o {ROOT_DIR}/requirements_dev.txt")
# --------------- installation helper functions, please do not modify -----------------------------

def query_yes_no(question, default_answer="yes", help=""):
    """Ask user at stdin a yes or no question

    :param question: question text to user
    :param default_answer: should be "yes" or "no"
    :param help: help text string
    :return:  :type: bool
    """
    if default_answer == "yes":
        prompt_txt = "{question} [Y/n] ".format(question=question)
    elif default_answer == "no":  # explicit no
        prompt_txt = "{question} [y/N] ".format(question=question)
    else:
        raise ValueError("default_answer must be 'yes' or 'no'!")

    while True:
        try:
            answer = input(prompt_txt)
            if answer:
                if answer == "?":
                    print(help)
                    continue
                else:
                    return strtobool(answer)
            else:
                return strtobool(default_answer)
        except ValueError:
            sys.stderr.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
        except KeyboardInterrupt:
            sys.stderr.write("Query interrupted by user, exiting now ...")
            exit(0)


def query(question, default_answer="", help=""):
    """Ask user a question

    :param question: question text to user
    :param default_answer: any default answering text string
    :param help:  help text string
    :return: stripped answer string
    """
    prompt_txt = "{question} [{default_answer}] ".format(question=question, default_answer=default_answer)

    while True:
        answer = input(prompt_txt).strip()

        if answer:
            if answer == "?":
                print(help)
                continue
            else:
                return answer
        else:
            return default_answer