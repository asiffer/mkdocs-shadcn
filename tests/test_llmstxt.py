from typing import TypedDict

import pytest
from llms_txt import parse_llms_file

from tests.conftest import ShadcnProject


class _Options(TypedDict):
    title: str
    summary: str


class _File(TypedDict):
    relpath: str
    content: str
    options: _Options


def test_llmstxt(shadcn_project: ShadcnProject):
    llms_txt = shadcn_project.site_dir / "llms.txt"
    assert not llms_txt.exists()

    shadcn_project.update_config(
        {
            "theme": {
                "name": "shadcn",
                "llmstxt": True,
                "hide_source_files": False,
            }
        }
    )

    files: list[_File] = [
        {
            "relpath": "index.md",
            "content": "index",
            "options": {"title": "Index", "summary": "main page"},
        },
        {
            "relpath": "a/b/c.md",
            "content": "c",
            "options": {"title": "Page C", "summary": "summary of c"},
        },
        {
            "relpath": "a/b/d.md",
            "content": "d",
            "options": {"title": "Page D", "summary": "summary of d"},
        },
        {
            "relpath": "a/f/x.md",
            "content": "x",
            "options": {"title": "Page X", "summary": "summary of x"},
        },
        {
            "relpath": "a/w.md",
            "content": "w",
            "options": {"title": "Page W", "summary": "summary of w"},
        },
        {
            "relpath": "g/h.md",
            "content": "h",
            "options": {"title": "Page H", "summary": "summary of h"},
        },
        {
            "relpath": "g/u.md",
            "content": "h",
            "options": {"title": "Page U :)", "summary": "summary of u"},
        },
    ]

    for file in files:
        shadcn_project.write_file(**file)  # type: ignore

    shadcn_project.build()

    parsed_content: dict = parse_llms_file(llms_txt.read_text())
    assert parsed_content["title"] == shadcn_project.site_name, parsed_content
    assert parsed_content["summary"] == shadcn_project.site_description, (
        parsed_content
    )
    assert len(parsed_content["sections"]) == 2, parsed_content
    sections = {
        file["relpath"][0].upper()
        for file in files
        if not file["relpath"].startswith("index")
    }

    for section in sections:
        pages = parsed_content["sections"][section]
        assert len(pages) == len(
            [
                file
                for file in files
                if file["relpath"].startswith(f"{section.lower()}/")
            ]
        ), parsed_content

        for page in pages:
            assert isinstance(page, dict), type(page)
            url = page.get("url", "")
            file = next(
                file for file in files if ("/" + file["relpath"]) == url
            )
            assert file.get("options", {}).get("title") == page["title"]
            assert file.get("options", {}).get("summary") == page["desc"]

    print(parsed_content)


def test_llmstxt_requires_source_files(shadcn_project: ShadcnProject):
    shadcn_project.update_config(
        {
            "theme": {
                "name": "shadcn",
                "llmstxt": True,
                "hide_source_files": True,
            }
        }
    )
    with pytest.raises(RuntimeError):
        shadcn_project.build()
