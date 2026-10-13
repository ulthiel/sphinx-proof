from bs4 import BeautifulSoup
import pytest
from sphinx.util.docutils import docutils_namespace

from sphinx_proof.proof_type import PROOF_TYPES

pytestmark = pytest.mark.sphinx(testroot="shared-counter", freshenv=True)


def build_app(make_app, app_params, builder="html", **config):
    app = make_app(**dict(app_params.kwargs, buildername=builder, confoverrides=config))
    app.build()
    return app


def read_html(app, docname):
    return BeautifulSoup(
        (app.outdir / (docname + ".html")).read_text(encoding="utf8"),
        "html.parser",
    )


def assert_block(soup, label, heading):
    block = soup.find(id=label)
    assert block is not None
    assert block.select_one(".admonition-title").get_text().startswith(heading)


@pytest.mark.parametrize("shared", [False, True])
def test_counter_modes(make_app, app_params, shared, warnings):
    app = build_app(make_app, app_params, proof_shared_counter=shared)
    assert warnings(app) == ""
    first = read_html(app, "first")
    second = read_html(app, "second")
    if shared:
        expected = {
            "definition-a": "Definition 1.1.1",
            "theorem-a": "Theorem 1.1.2",
            "exercise-a": "Exercise 1.1.3",
            "lemma-a": "Lemma 1.1.4",
            "private-observation": "Observation 1.1.6",
            "quiz-a": "Quiz 1.1.7",
            "solution-code": "Code 1.1.8",
            "theorem-b": "Theorem 1.1.9",
            "lemma-next": "Lemma 1.2.1",
        }
    else:
        expected = {
            "definition-a": "Definition 1.1.1",
            "theorem-a": "Theorem 1.1.1",
            "exercise-a": "Exercise 1.1.1",
            "lemma-a": "Lemma 1.1.1",
            "private-observation": "Observation 1.1.1",
            "quiz-a": "Quiz 1.1.1",
            "solution-code": "Code 1.1.1",
            "theorem-b": "Theorem 1.1.2",
            "lemma-next": "Lemma 1.2.1",
        }
    for label, heading in expected.items():
        assert_block(first, label, heading)
        for ref in first.select('a[href="#' + label + '"]'):
            assert ref.get_text() in {heading, "custom theorem text"}
    assert_block(first, "unnumbered-remark", "Remark")
    assert "1.1." not in first.find(id="unnumbered-remark").get_text()
    assert (
        first.select_one("div.example .admonition-title")
        .get_text()
        .startswith("Example 1.1.5" if shared else "Example 1.1.1")
    )
    for label, heading in [
        ("aufgabe-a", "Aufgabe 2.1.1"),
        ("beispiel-a", "Beispiel 2.1.2" if shared else "Beispiel 2.1.1"),
        ("algorithmus-a", "Algorithmus 2.1.3" if shared else "Algorithmus 2.1.1"),
        ("theorem-last", "Theorem 2.1.4" if shared else "Theorem 2.1.1"),
    ]:
        assert_block(second, label, heading)
        assert second.select_one('a[href="#' + label + '"]').get_text() == heading
    assert second.select_one('a[href="first.html#theorem-b"]').get_text() == (
        expected["theorem-b"]
    )
    assert second.select_one('a.reference[href="#independent-table"]').get_text() == (
        "Table 2.1.1"
    )


@pytest.mark.parametrize("depth", [0, 1])
def test_counter_scope(make_app, app_params, depth, warnings):
    app = build_app(
        make_app, app_params, proof_shared_counter=True, numfig_secnum_depth=depth
    )
    assert warnings(app) == ""
    first = read_html(app, "first")
    second = read_html(app, "second")
    assert_block(first, "theorem-b", "Theorem 1.9" if depth else "Theorem 9")
    assert_block(first, "lemma-next", "Lemma 1.10" if depth else "Lemma 10")
    assert_block(second, "aufgabe-a", "Aufgabe 2.1" if depth else "Aufgabe 11")
    assert_block(second, "theorem-last", "Theorem 2.4" if depth else "Theorem 14")


@pytest.mark.parametrize("builder", ["html", "singlehtml", "latex"])
def test_shared_counter_builders(make_app, app_params, builder, warnings):
    app = build_app(make_app, app_params, builder, proof_shared_counter=True)
    assert warnings(app) == ""
    if builder == "latex":
        output = (app.outdir / "sharedcountertests.tex").read_text(encoding="utf8")
        for heading in ["Theorem 1.1.2", "Lemma 1.1.4", "Beispiel 2.1.2"]:
            assert heading in output
    else:
        soup = read_html(app, "index" if builder == "singlehtml" else "first")
        assert_block(soup, "theorem-a", "Theorem 1.1.2")
        assert_block(soup, "theorem-b", "Theorem 1.1.9")


def test_parallel_build(make_app, app_params, warnings):
    app = make_app(
        **dict(
            app_params.kwargs,
            buildername="html",
            parallel=2,
            confoverrides={"proof_shared_counter": True},
        )
    )
    app.build()
    assert warnings(app) == ""
    assert_block(read_html(app, "first"), "theorem-b", "Theorem 1.1.9")
    assert_block(read_html(app, "second"), "theorem-last", "Theorem 2.1.4")


@pytest.mark.parametrize(
    "solutions,private", [(False, False), (True, False), (True, True)]
)
def test_conditional_numbers(make_app, app_params, solutions, private, warnings):
    app = build_app(
        make_app,
        app_params,
        proof_shared_counter=True,
        show_solutions=solutions,
        show_private=private,
    )
    assert warnings(app) == ""
    soup = read_html(app, "first")
    assert bool(soup.find(id="private-observation")) == private
    assert bool(soup.find(id="solution-code")) == solutions
    assert_block(soup, "quiz-a", "Quiz 1.1.7")
    assert_block(soup, "theorem-b", "Theorem 1.1.9")


@pytest.mark.parametrize("default_class", [None, "note"])
def test_all_environment_types(make_app, app_params, tmp_path, warnings, default_class):
    source_dir = tmp_path / "all-types"
    source_dir.mkdir()
    (source_dir / "conf.py").write_text(
        'extensions = ["sphinx_proof"]\nproof_shared_counter = True\n'
    )
    source = "All environments\n================\n\n"
    for typ in PROOF_TYPES:
        source += ".. prf:" + typ + "::\n   :label: " + typ + "-label\n\n   Text.\n\n"
    (source_dir / "index.rst").write_text(source)
    srcdir = type(app_params.kwargs["srcdir"])(str(source_dir))
    config = {} if default_class is None else {"proof_default_class": default_class}
    app = make_app(
        srcdir=srcdir, buildername="html", freshenv=True, confoverrides=config
    )
    app.build()
    assert warnings(app) == ""
    soup = read_html(app, "index")
    for number, typ in enumerate(PROOF_TYPES, 1):
        assert_block(soup, typ + "-label", typ.title() + " " + str(number) + " ")
        assert ("note" in soup.find(id=typ + "-label")["class"]) == (
            default_class == "note"
        )


def test_rebuild_after_switching_mode(make_app, app_params, warnings):
    srcdir = app_params.kwargs["srcdir"]
    for shared in [False, True, False]:
        with docutils_namespace():
            app = make_app(
                srcdir=srcdir,
                buildername="html",
                confoverrides={"proof_shared_counter": shared},
            )
            app.build()
            assert warnings(app) == ""
            assert_block(
                read_html(app, "first"),
                "theorem-a",
                "Theorem 1.1.2" if shared else "Theorem 1.1.1",
            )
            app.cleanup()


@pytest.mark.sphinx(srcdir="shared-counter-incremental")
def test_incremental_reference_numbers(make_app, app_params, warnings):
    with docutils_namespace():
        app = build_app(make_app, app_params, proof_shared_counter=True)
        app.cleanup()
    source = app_params.kwargs["srcdir"] / "first.rst"
    text = source.read_text(encoding="utf8")
    source.write_text(
        text.replace(
            ".. prf:theorem:: A theorem",
            ".. prf:example:: Inserted example\n"
            "   :label: inserted-example\n\n"
            "   Example text.\n\n"
            ".. prf:theorem:: A theorem",
        ),
        encoding="utf8",
    )
    with docutils_namespace():
        app = make_app(
            srcdir=app_params.kwargs["srcdir"],
            buildername="html",
            confoverrides={"proof_shared_counter": True},
        )
        app.build()
        assert warnings(app) == ""
        assert_block(read_html(app, "first"), "theorem-b", "Theorem 1.1.10")
        assert (
            read_html(app, "second")
            .select_one('a[href="first.html#theorem-b"]')
            .get_text()
            == "Theorem 1.1.10"
        )
        app.cleanup()


def test_default_class_overrides(make_app, app_params, tmp_path, warnings):
    source_dir = tmp_path / "default-class"
    source_dir.mkdir()
    (source_dir / "conf.py").write_text('extensions = ["sphinx_proof"]\n')
    (source_dir / "index.rst").write_text(
        "Default styles\n==============\n\n"
        ".. prf:definition::\n   :label: default-style\n\n   Text.\n\n"
        ".. prf:remark::\n   :label: unnumbered-style\n"
        "   :nonumber:\n\n   Text.\n\n"
        ".. prf:example::\n   :label: warning-style\n"
        "   :class: warning custom-style\n\n   Text.\n\n"
        ".. prf:lemma::\n   :label: custom-style\n"
        "   :class: custom-style\n\n   Text.\n\n"
        ".. prf:proof::\n\n   Proof text.\n\n"
        ".. prf:beweis::\n\n   Beweis text.\n"
    )
    srcdir = type(app_params.kwargs["srcdir"])(str(source_dir))
    app = make_app(
        srcdir=srcdir,
        buildername="html",
        freshenv=True,
        confoverrides={"proof_default_class": "note custom-default"},
    )
    app.build()
    assert warnings(app) == ""
    soup = read_html(app, "index")
    for label in ["default-style", "unnumbered-style"]:
        classes = soup.find(id=label)["class"]
        assert "note" in classes
        assert "custom-default" in classes
    for label in ["warning-style", "custom-style"]:
        classes = soup.find(id=label)["class"]
        assert "custom-style" in classes
        assert "note" not in classes
        assert "custom-default" not in classes
    assert "warning" in soup.find(id="warning-style")["class"]
    for typ in ["proof", "beweis"]:
        classes = soup.find(id=typ)["class"]
        assert "note" not in classes
        assert "custom-default" not in classes
    assert_block(soup, "unnumbered-style", "Remark")
    assert "1" not in soup.find(id="unnumbered-style").get_text()


@pytest.mark.sphinx(srcdir="default-class-incremental")
def test_rebuild_after_switching_default_class(make_app, app_params, warnings):
    srcdir = app_params.kwargs["srcdir"]
    for default_class in ["", "note", "warning", ""]:
        with docutils_namespace():
            app = make_app(
                srcdir=srcdir,
                buildername="html",
                confoverrides={"proof_default_class": default_class},
            )
            app.build()
            assert warnings(app) == ""
            first = read_html(app, "first")
            for label in ["definition-a", "unnumbered-remark"]:
                classes = first.find(id=label)["class"]
                for style in ["note", "warning"]:
                    assert (style in classes) == (style == default_class)
            assert_block(first, "theorem-a", "Theorem 1.1.1")
            assert "note" not in first.find(id="proof")["class"]
            assert "warning" not in first.find(id="proof")["class"]
            second = read_html(app, "second")
            assert "note" not in second.find(id="beweis")["class"]
            assert "warning" not in second.find(id="beweis")["class"]
            app.cleanup()
