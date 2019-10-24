Quickstart
----------

.. code:: ipython3

    from jelm import Jelm

.. code:: ipython3

    el = Jelm()

.. code:: ipython3

    el.add_node(id='n1')
    el.add_node(id='n2')
    el.add_edge(source='n1',
                target='n2')

.. code:: ipython3

    el




.. parsed-literal::

    ::jelm Graph with 2 nodes and 1 edge::



.. code:: ipython3

    n1 = el.nodes['n1']

.. code:: ipython3

    n1




.. parsed-literal::

    ::jelm Node (n1) with 1 neighbor::



.. code:: ipython3

    n1.neighbors




.. parsed-literal::

    {'n2': [::jelm Edge connecting n1 to n2::]}


