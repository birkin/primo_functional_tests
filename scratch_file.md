scratch-file...
===============

next...

- refactor output into bib-data, and item-data.
- grab more data.
- begin logic for tests, given logged-in status and available item-data.

---
---

# ## old! verify.
# def _log_into_shib( self, driver ):
#     """ Helper function for tests.
#         Takes driver; logs in user; returns driver.
#         Called by module test functions. """
#     driver.find_element_by_id("username").clear()
#     driver.find_element_by_id("username").send_keys( self.USERNAME )
#     driver.find_element_by_id("password").clear()
#     driver.find_element_by_id("password").send_keys( self.PASSWORD )
#     driver.find_element_by_css_selector("button[type=\"submit\"]").click()
#     return driver

---
---

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