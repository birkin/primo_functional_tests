scratch-file...
===============

next...

√ replace working Lock() with Semaphore( 0 ) and test.

- while I have the existing error, improve error-handling so the process is closed. (continue)

- handle dict correctly.


---
---

timing semaphore vs lock
- 1000 jobs w/100 workers, 
- each job randomly takes between .4 and .6 seconds
- initial uncounted run (setting cache?)
- running 5 times, 
- dropping the high and low
- averaging 3
- rounding down to hundredth

Lock()
x6.70
x6.78

6.71
6.71
6.76
score: 6.726

Semaphore(1)
x6.67
x6.84

6.70
6.73
6.75
score: 6.726

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