First topic
===========

First section
-------------

.. prf:definition:: A definition
   :label: definition-a

   Definition text.

.. prf:theorem:: A theorem
   :label: theorem-a

   Theorem text.

.. prf:proof::

   Proof text.

.. prf:exercise:: An exercise
   :label: exercise-a

   Exercise text.

.. prf:lemma:: A lemma
   :label: lemma-a

   Lemma text.

.. prf:example:: An unlabeled example

   Example text.

.. prf:remark:: An unnumbered remark
   :label: unnumbered-remark
   :nonumber:

   Remark text.

.. ifconfig:: show_private

   .. prf:observation:: A private observation
      :label: private-observation

      Private text.

.. prf:quiz:: A quiz
   :label: quiz-a

   Quiz text.

.. ifconfig:: show_solutions

   .. prf:code:: Solution code
      :label: solution-code

      Solution text.

Deeper subsection
~~~~~~~~~~~~~~~~~

.. prf:theorem:: Another theorem
   :label: theorem-b

   Theorem text.

See :prf:ref:`definition-a`, :prf:ref:`theorem-a`,
:prf:ref:`exercise-a`, :prf:ref:`lemma-a`, :prf:ref:`quiz-a`,
:prf:ref:`theorem-b`, and :prf:ref:`unnumbered-remark`.
Also see :prf:ref:`custom theorem text <theorem-a>`.

Next section
------------

.. prf:lemma:: A new section
   :label: lemma-next

   Lemma text.
