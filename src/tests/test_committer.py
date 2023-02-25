#!/usr/bin/env python3

from typing import Tuple
from unittest import IsolatedAsyncioTestCase, mock

from plants.committer import Committer
from plants.subprocess_utils import SubprocessError
from plants.unittest_utils import UnittestUtils


class TestCommitAndPush(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.mock_logger = UnittestUtils.patch(
            self,
            "plants.committer.logger",
            new_callable=mock.Mock,
        )
        self.mock_run = UnittestUtils.patch(
            self,
            "plants.subprocess_utils.SubprocessUtils._run",
            new_callable=mock.Mock,
        )
        self.mock_run.return_value.returncode = 0

    def _commit_and_push(self) -> None:
        Committer.commit_and_push(
            commit_message="commit_message",
            user_name="user_name",
            user_email="user_email",
        )

    def _raise_error_if_git_push(self, args: Tuple[str, ...]) -> mock.Mock:
        if args == ("git", "push"):
            return mock.Mock(
                returncode=1,
                stderr="stderr",
            )
        return mock.Mock(returncode=0)

    def test_success(self) -> None:
        self._commit_and_push()
        self.mock_run.assert_has_calls(
            [
                mock.call(("git", "status", "--short")),
                mock.call(("git", "add", "--all")),
                mock.call(
                    (
                        "git",
                        "-c",
                        "user.name=user_name",
                        "-c",
                        "user.email=user_email",
                        "commit",
                        "-m",
                        "commit_message",
                    ),
                ),
                mock.call(("git", "push")),
            ]
        )

    def test_push_failure(self) -> None:
        self.mock_run.side_effect = self._raise_error_if_git_push
        with self.assertRaises(SubprocessError):
            self._commit_and_push()
