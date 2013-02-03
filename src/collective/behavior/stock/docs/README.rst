=========================
collective.behavior.stock
=========================

collective.behavior.stock provides stock related behavior to dexterity content types.

Currently tested with
---------------------

* Plone-4.2.4 [taito]

Behavior
--------

The behavior can be added through the web or directly through the file system to the dexterity content type xml file like::

  <property name="behaviors">
    ...
    <element value="collective.behavior.stock.interfaces.IStock" />
    ...
  </property>
