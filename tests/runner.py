class PytestTestRunner:
    """Runs pytest to discover and run tests."""

    def __init__(self, verbosity=0, failfast=False, keepdb=False, shuffle=True, timing=True, **kwargs):
        self.verbosity = verbosity
        self.failfast = failfast
        self.keepdb = keepdb
        self.shuffle = shuffle
        self.timing = timing
        self.extra_params = kwargs

    @classmethod
    def add_arguments(cls, parser):
        parser.add_argument("--keepdb", action="store_true", help="Preserves the test DB between runs.")
        parser.add_argument(
            "--cov",
            action="store_true",
            help="Generates a Code coverage Report",
        )
        parser.add_argument("--tag", action="append")

    def run_tests(self, test_labels):
        """Run pytest and return the exitcode.

        It translates some of Django's test command option to pytest's.
        """
        import pytest

        argv = []
        if self.verbosity == 0:
            argv.append("--quiet")
        if self.verbosity == 2:
            argv.append("--verbose")
        if self.verbosity == 3:
            argv.append("-vv")
        if self.failfast:
            argv.append("--exitfirst")
        if self.keepdb:
            argv.append("--reuse-db")
        if self.extra_params.get("cov"):
            argv.append("--cov")
            argv.append("--cov-report")
            argv.append("html")
        if self.extra_params.get("tag"):
            argv.append("-k")
            argv.extend(self.extra_params["tag"])

        argv.extend(test_labels)
        return pytest.main(argv)
