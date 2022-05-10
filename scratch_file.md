scratch-file...
===============

next...

- √ add elapsed-time for individual bib, vs elapsed time for set.

- replace the sleep with a simple selenium driver instantiation and access. this'll let us know if this concurrency is possible with selenium. I think it will be, given selenium's use of trio.

- research and try out writing out the result of each test to a json file. although if i were really updating a google-sheet, that could postentially, if not likely, be done concurrently.

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