from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from random import randbytes, randint
from typing import Any, Dict, Tuple

import yaml
from bs4 import BeautifulSoup
from conftest import ShadcnProject

Options = Dict[str, Any]
Content = Tuple[str, Options | None, str | Path | None]


@dataclass
class OptionTesterCase:
    content: str
    options: dict[str, Any] | None = None
    path: str | Path = field(
        default_factory=lambda: randbytes(8).hex() + ".md"
    )
    id: int | str = field(default_factory=lambda: randint(0, 2**32 - 1))

    def __hash__(self) -> int:
        return hash(self.path)


class OptionTester(ABC):
    """Every page option tester must follow this interface

    cases() generates pages to build and test
    test() check every case

    Cases could be identified identified by either path or id
    """

    @abstractmethod
    def cases(self) -> OptionTesterCase | list[OptionTesterCase]: ...

    @abstractmethod
    def test(self, soup: BeautifulSoup, case: OptionTesterCase) -> None: ...


class HideSidebarOptionTester(OptionTester):
    def cases(self) -> list[OptionTesterCase]:
        return [
            OptionTesterCase(
                content="## Test hide_sidebar\n",
                options={"hide_sidebar": True},
                id="hide",
            ),
            OptionTesterCase(
                content="## Test hide_sidebar\n",
                options={"hide_sidebar": False},
                id="show",
            ),
        ]

    def test(self, soup: BeautifulSoup, case: OptionTesterCase):
        if case.id == "hide":
            sidebar = soup.find("div", {"view-transition-name": "sidebar"})
            assert sidebar is not None
            assert sidebar.find(True) is None, sidebar.contents
        elif case.id == "show":
            sidebar = soup.find("div", {"view-transition-name": "sidebar"})
            assert sidebar is not None
            assert sidebar.find(True) is not None


def test_page_options(shadcn_project: ShadcnProject):
    testers: dict[OptionTesterCase, OptionTester] = {}
    for tester in OptionTester.__subclasses__():
        instance = tester()
        cases = instance.cases()
        if not isinstance(cases, list):
            cases = [cases]

        for case in cases:
            # create the page
            if case.options is not None:
                page = f"---\n{yaml.dump(case.options)}---\n"

            page += f"\n{case.content}"

            shadcn_project.write_file(case.path, page)
            testers[case] = instance

    shadcn_project.build()

    for case, tester in testers.items():
        html_file = shadcn_project.get_built_file(case.path)
        print(case.path, os.listdir(shadcn_project.path / "site"))
        with open(html_file, "r") as html:
            soup = BeautifulSoup(html.read(), features="html.parser")
            tester.test(soup, case)
