"""Regression tests using local Git repositories only."""

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "bin" / "git-vendor"
INSTALL = ROOT / "install.sh"


class GitVendorTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="git-vendor-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.env = os.environ.copy()
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        self.env["GIT_CONFIG_GLOBAL"] = os.devnull
        self.work = self.repo("work")

    def run_cmd(self, cwd, *args, env=None):
        return subprocess.run(
            args,
            cwd=cwd,
            env=env or self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def repo(self, name):
        path = self.root / name
        path.mkdir()
        self.assertEqual(self.run_cmd(path, "git", "init", "-q", "-b", "master").returncode, 0)
        self.run_cmd(path, "git", "config", "user.name", "Review Test")
        self.run_cmd(path, "git", "config", "user.email", "review@example.test")
        (path / "file.txt").write_text(name + "\n")
        self.run_cmd(path, "git", "add", ".")
        self.assertEqual(self.run_cmd(path, "git", "commit", "-qm", "initial").returncode, 0)
        return path

    def remote(self, alias):
        source = self.repo("source-" + alias)
        self.assertEqual(self.run_cmd(self.work, "git", "remote", "add", alias, str(source)).returncode, 0)
        return source

    def vendor(self, *args):
        return self.run_cmd(self.work, str(VENDOR), *args)

    def test_unknown_dependency_is_an_error(self):
        for command in ("update", "remove", "upstream"):
            with self.subTest(command=command):
                result = self.vendor(command, "missing")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Unknown dependency", result.stderr)

    def test_duplicate_name_is_rejected(self):
        self.remote("first")
        self.remote("second")
        self.assertEqual(self.vendor("add", "same", "first").returncode, 0)
        result = self.vendor("add", "same", "second")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)
        self.assertFalse((self.work / "vendor" / "second").exists())

    def test_unreadable_names_are_rejected(self):
        self.remote("source")
        for name in ("", "two words", "foo\tbar", r"foo\bar"):
            with self.subTest(name=name):
                result = self.vendor("add", name, "source")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Dependency name", result.stderr)

    def test_names_with_regex_metacharacters_resolve_exactly(self):
        self.remote("first.repo")
        self.remote("firstXrepo")
        self.assertEqual(self.vendor("add", "foo.bar", "first.repo").returncode, 0)
        self.assertEqual(self.vendor("add", "fooXbar", "firstXrepo").returncode, 0)

        listed = self.vendor("list", "foo.bar")
        self.assertEqual(listed.returncode, 0)
        self.assertIn("foo.bar@master:", listed.stdout)
        self.assertNotIn("fooXbar@master:", listed.stdout)

        updated = self.vendor("update", "foo.bar", "master")
        self.assertEqual(updated.returncode, 0, updated.stderr)
        self.assertTrue((self.work / "vendor" / "first.repo" / "file.txt").exists())

    def test_distinct_directories_both_appear_in_list(self):
        for name in ("foo-bar", "foo_bar"):
            self.remote(name)
            self.assertEqual(self.vendor("add", name, name).returncode, 0)
        listed = self.vendor("list")
        self.assertEqual(listed.returncode, 0)
        self.assertIn("foo-bar@master:", listed.stdout)
        self.assertIn("foo_bar@master:", listed.stdout)

    def test_readded_directory_uses_its_newest_name(self):
        self.remote("source")
        self.assertEqual(self.vendor("add", "old", "source").returncode, 0)
        self.assertEqual(self.vendor("remove", "old").returncode, 0)
        self.assertEqual(self.vendor("add", "new", "source").returncode, 0)
        listed = self.vendor("list")
        self.assertEqual(listed.returncode, 0)
        self.assertIn("new@master:", listed.stdout)
        self.assertNotIn("old@master:", listed.stdout)

    def test_git_failures_are_reported(self):
        self.remote("source")
        self.assertEqual(self.vendor("add", "dep", "source").returncode, 0)

        update = self.vendor("update", "dep", "missing-ref")
        self.assertNotEqual(update.returncode, 0)

        upstream = self.vendor("upstream", "dep", "master", "--repo", str(self.root / "absent"))
        self.assertNotEqual(upstream.returncode, 0)

        hook = self.work / ".git" / "hooks" / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        remove = self.vendor("remove", "dep")
        self.assertNotEqual(remove.returncode, 0)
        self.assertTrue((self.work / ".git" / "hooks" / "pre-commit").exists())
        self.assertIn("D  vendor/source/file.txt", self.run_cmd(self.work, "git", "status", "--short").stdout)

    def test_missing_repository_metadata_is_an_error(self):
        directory = self.work / "vendor" / "source"
        directory.mkdir(parents=True)
        (directory / "file.txt").write_text("source\n")
        self.run_cmd(self.work, "git", "add", ".")
        message = "Add dep\n\ngit-vendor-name: dep\ngit-vendor-dir: vendor/source\n"
        self.assertEqual(self.run_cmd(self.work, "git", "commit", "-qm", message).returncode, 0)
        for command in ("update", "upstream"):
            with self.subTest(command=command):
                result = self.vendor(command, "dep")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("has no repository", result.stderr)

    def test_installer_preserves_existing_tmp_directory(self):
        temp_root = self.root / "temporary space"
        temp_root.mkdir()
        existing = temp_root / "git-vendor"
        existing.mkdir()
        (existing / "sentinel").write_text("keep")

        fake_bin = self.root / "fake-bin"
        fake_bin.mkdir()
        fake_git = fake_bin / "git"
        fake_git.write_text('#!/bin/sh\ntest "$1" = clone && test -d "$3"\n')
        fake_git.chmod(0o755)
        fake_make = fake_bin / "make"
        fake_make.write_text("#!/bin/sh\nexit 0\n")
        fake_make.chmod(0o755)
        env = self.env.copy()
        env["PATH"] = str(fake_bin) + os.pathsep + env["PATH"]
        env["TMPDIR"] = str(temp_root)

        installed = self.run_cmd(self.root, "bash", str(INSTALL), env=env)
        self.assertEqual(installed.returncode, 0, installed.stderr)
        self.assertEqual((existing / "sentinel").read_text(), "keep")
        self.assertEqual(list(temp_root.glob("git-vendor.*")), [])


if __name__ == "__main__":
    unittest.main()
