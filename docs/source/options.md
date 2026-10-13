# Options

## Shared numbering

By default, each environment has its own numbering sequence: Theorem 1.1,
Exercise 1.1, Lemma 1.1, Theorem 1.2. Set `proof_shared_counter` to `True` to
number all proof environments in one sequence, in reading order:
Theorem 1.1, Exercise 1.2, Lemma 1.3, Theorem 1.4.

For a Sphinx project, add this to `conf.py`:

```python
proof_shared_counter = True
```

For a Jupyter Book v1 project, add this to `_config.yml`:

```yaml
sphinx:
  config:
    proof_shared_counter: true
```

The shared sequence includes definitions, examples, exercises, quizzes, remarks,
and all other numbered proof environments, including their German counterparts.
Environment names, labels, and `{prf:ref}` references retain their usual meaning.
Proofs and environments with `:nonumber:` do not consume a number. Equations,
figures, tables, and Sphinx's numbered code blocks keep their separate counters.
The `prf:code` environment participates in the shared sequence.

Section prefixes and counter resets still follow `numfig_secnum_depth`.
For example, with a numbered table of contents and `numfig_secnum_depth = 2`,
items in section 1.1 are numbered 1.1.1, 1.1.2, and so on. The sequence
continues through deeper subsections and restarts in section 1.2. With
`numfig_secnum_depth = 0`, there is one sequence across the book.

Sphinx assigns numbers before evaluating `sphinx.ext.ifconfig` conditions.
Consequently, conditional numbered environments reserve their numbers even
when hidden. Builds differing only in these conditions retain the same numbers
for their common items, with gaps where numbered content is hidden.

### Example

The following MyST source gives an example and a lemma sharing a counter when
the option is enabled:

````markdown
```{prf:example}
:label: shared-counter-example

An example.
```

```{prf:lemma}
:label: shared-counter-lemma

A lemma following the example.
```

See {prf:ref}`shared-counter-lemma`.
````

```{prf:example}
:label: shared-counter-example

An example.
```

```{prf:lemma}
:label: shared-counter-lemma

A lemma following the example.
```

See {prf:ref}`shared-counter-lemma`.

## Minimal color scheme

This package has the option to choose a more **minimal** color scheme.

The aim is to create admonitions that are clearly different to the core text with
colors that do not over emphasises the admonition such as

```{figure} _static/img/definition-minimal.png
```

compared to the current default

```{figure} _static/img/definition.png
```

To enable the `minimal` color scheme you can use the following.

### Jupyter Book Project

Add `proof_minimal_theme = True` to your `_config.yml`

```yaml
sphinx:
  config:
    proof_minimal_theme: true
```

### Sphinx Project

Add `proof_minimal_theme = True` to your `conf.py`
