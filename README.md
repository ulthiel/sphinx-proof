# sphinx-proof

[![Documentation Status][rtd-badge]][rtd-link]
[![Github-CI][github-ci]][github-link]
[![Coverage Status][codecov-badge]][codecov-link]
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/executablebooks/sphinx-proof/master.svg)](https://results.pre-commit.ci/latest/github/executablebooks/sphinx-proof/master)


**A proof extension for Sphinx**.

This package contains a [Sphinx](http://www.sphinx-doc.org/) extension
for producing proof, theorem, axiom, lemma, definition, criterion, remark, conjecture,
corollary, algorithm, example, property, observation, proposition and assumption directives.

## Fork by UT

* Added environments "Quiz", "Code", "Question", "Conjecture" (in files nodes.py and proof_type.py)

* Added optional argument to proof so that one can use `{prf:proof} Idea of proof` (in directive.py).

* Added German environments "Aufgabe", "Code", "Question", "Frage", "Conjecture", "Vermutung" (in files nodes.py and proof_type.py). Even though there is internationalization, I have added the German versions as separate environments because I use both in the same project and the internationalization does not work on individual files, just globally.

* Added German environment Beweis `{prf:beweis}`.

To get nice icons you can add the following to your custom.css:

```css
/* Icons for sphinx-proof stuff 
   Suggested mostly by ChatGPT :-) */

/* fa-scroll: Classical mathematics vibe */
div.proof.theorem p.admonition-title::after {
  content: "\f70e";
}

/* fa-shapes: Suggests structure and building blocks. */
div.proof.proposition p.admonition-title::after {
  content: "\f61f";
}

/* fa-lightbulb: A lemma is a “smart little insight” that supports a theorem, so this reads well visually. */
div.proof.lemma p.admonition-title::after {
  content: "\f0eb";
}

/* fa-arrow-turn-down-right: Indicates a conclusion that follows straight from something else. */
div.proof.corollary p.admonition-title::after {
  content: "\f3be";
}

div.proof.korollar p.admonition-title::after {
  content: "\f058";
}

/* fa-book-open: “Opening the book” to define something. */
div.proof.definition p.admonition-title::after {
  content: "\f518";
}

div.admonition-question p.admonition-title::after {
  content: "\f059";
}

/* Brain */
div.proof.quiz p.admonition-title::after {
  content: "\f5dc";
}

/* Pencil */
div.proof.exercise p.admonition-title::after {
  content: "\f303";
}

div.proof.aufgabe p.admonition-title::after {
  content: "\f303";
}

/* fa-flask: Examples act like experiments or demonstrations */
div.proof.example p.admonition-title::after {
  content: "\f0c3";
}

div.proof.code p.admonition-title::after {
  content: "\f120";
}

/* Make all sphinx-proof proof admonitions look like #proof */
div.admonition.proof {
  padding: .4rem .6rem .4rem 2rem !important;
  border-color: var(--grey-border-color);
  background-color: none;
}
```


## Get started

To get started with `sphinx-proof`, first install it through `pip`:

```
pip install sphinx-proof
```

then, add `sphinx_proof` to your sphinx `extensions` in the `conf.py`

```python
...
extensions = ["sphinx_proof"]
...
```


## Documentation

See the [Sphinx Proof documentation](https://sphinx-proof.readthedocs.io/en/latest/) for more information.


## Contributing

We welcome all contributions! See the [EBP Contributing Guide](https://executablebooks.org/en/latest/contributing.html) for general details, and below for guidance specific to sphinx-proof.


[rtd-badge]: https://readthedocs.org/projects/sphinx-proof/badge/?version=latest
[rtd-link]: https://sphinx-proof.readthedocs.io/en/latest/?badge=latest
[github-ci]: https://github.com/executablebooks/sphinx-proof/workflows/ci.yml/badge.svg?branch=main
[github-link]: https://github.com/executablebooks/sphinx-proof
[codecov-badge]: https://codecov.io/gh/executablebooks/sphinx-proof/branch/main/graph/badge.svg
[codecov-link]: https://codecov.io/gh/executablebooks/sphinx-proof
