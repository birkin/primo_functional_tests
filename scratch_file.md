scratch-file...
===============

next...

- add elapsed-time for individual bib, vs elapsed time for set.

- replace the sleep with a simple selenium driver instantiation and access. this'll let us know if this concurrency is possible with selenium. I think it will be, given selenium's use of trio.

- research and try out writing out the result of each test to a json file. although if i were really updating a google-sheet, that could postentially, if not likely, be done concurrently.

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