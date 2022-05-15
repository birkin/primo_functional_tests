scratch-file...
===============

next...

- investigate multiprocessing.

- <https://linuxhint.com/python-multiprocessing-example/>

- at: <https://docs.python.org/3.8/library/multiprocessing.html#multiprocessing-programming> ...at ``An example showing how to use queues to feed tasks to a collection of worker processes and collect the results:``

---
---

2022-May-10

without output-write lock... (1000 elements, 100 at a time)
[10/May/2022 05:59:00] DEBUG [run_tests-check_bibs()::94] elapsed total, ``0:00:10.964812``

with lock...
[10/May/2022 06:18:50] DEBUG [run_tests-check_bibs()::94] elapsed total, ``0:00:10.966840``

---
---


may need: <https://github.com/rossrochford/selenium-trio>

---

title_classes = document.getElementsByClassName( "item-title" )
target_title_class = title_classes[0]
target_title_class.textContent

---
---

in console
title_classes_B = $x( "//*[@class='item-title']" )