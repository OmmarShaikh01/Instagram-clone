import argparse
import os
import time


def runtest(parsed_args: argparse.Namespace):
    print("")
    print("TEST ---------------------------------------------------------------------------")
    cmd = [r".\.venv\Scripts\python.exe", "-m", "manage", "test"]
    if parsed_args.tag is not None:
        cmd.append("--tag")
        cmd.extend(parsed_args.tag)
    os.system(r" ".join(cmd))


def runtest_cov(parsed_args: argparse.Namespace):
    print("")
    print("TEST ---------------------------------------------------------------------------")
    cmd = [r".\.venv\Scripts\coverage.exe", "run", "manage.py", "test", "--cov"]
    os.system(r" ".join(cmd))
    if parsed_args.tag is not None:
        cmd.append("--tag")
        cmd.extend(parsed_args.tag)
    os.system(r"explorer.exe .\tests\coverage\html\index.html")


def runserver(parsed_args: argparse.Namespace):
    print("")
    print("MAKEMIGRATIONS -----------------------------------------------------------------")
    os.system(r".\.venv\Scripts\python.exe -m manage makemigrations --force-color")

    print("")
    print("MIGRATE ------------------------------------------------------------------------")
    os.system(r".\.venv\Scripts\python.exe -m manage migrate --run-syncdb --force-color")

    if args.populate:
        print("")
        print("LOAD DATA SERVER ---------------------------------------------------------------")
        os.system(r".\.venv\Scripts\python.exe -m manage loaddata .\tests\user\load_data.json")
        os.system(r".\.venv\Scripts\python.exe -m manage loaddata .\tests\user_relationship\load_data.json")

    print("")
    print("RUNSERVER ----------------------------------------------------------------------")
    os.system(r".\.venv\Scripts\python.exe -m manage runserver --force-color")


def rundoc_gen(args):
    print("")
    print("DOC GEN ------------------------------------------------------------------------")
    os.system(r".\.venv\Scripts\sphinx-apidoc.exe -f -e -o .\docs\source .\instagram_clone")
    print("")
    os.system(r".\.venv\Scripts\sphinx-build.exe .\docs\source .\docs\build")


def reformat():
    print("")
    print("ISORT REFORMAT -----------------------------------------------------------------")
    os.system(r".\.venv\Scripts\isort.exe .")
    print("")
    print("BLACK REFORMAT -----------------------------------------------------------------")
    os.system(r".\.venv\Scripts\black.exe .")


def flush_server():
    print("")
    print("FLUSH SERVER -------------------------------------------------------------------")
    os.system(r".\.venv\Scripts\python.exe -m manage flush --no-input")
    print("FLUSHED")


if __name__ == "__main__":
    t1 = time.time()
    os.environ["ENV_FOR_DYNACONF"] = "TESTING"
    os.environ["DJANGO_SETTINGS_MODULE"] = "instagram_clone.settings"
    original_dir = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument("session_name", choices=["test", "dev", "test_cov", "doc_gen"])
    cli_parser.add_argument("--reformat", action="store_true")
    cli_parser.add_argument("--flush", action="store_true")
    cli_parser.add_argument("--populate", action="store_true")

    group_test = cli_parser.add_argument_group("test")
    group_test.add_argument("--tag", action="append")

    args = cli_parser.parse_args()
    os.system(r"cls")
    if args.reformat:
        reformat()
    if args.populate or args.flush:
        flush_server()

    if args.session_name == "doc_gen":
        rundoc_gen(args)
    elif args.session_name == "dev":
        runserver(args)
    elif args.session_name == "test":
        runtest(args)
    elif args.session_name == "test_cov":
        runtest_cov(args)

    print(f"Finished {round(time.time() - t1, 4)} sec")
    os.chdir(original_dir)
