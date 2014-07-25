General list of things todo
---------------------------

* git grep 'TODO' and fix
* include what you use: lots of headers rely on ambient includes
* add more tests and have a run-under-valgrind target at least
* move more things over to the Request/Response way of doing things
* Double check it's ok to remove hixie, and do so.  Currently no way of testing it anyway
  (with reference to http://en.wikipedia.org/wiki/WebSocket#Browser_support it's been dead
  since before Chrome 14)

Further out things
------------------
* Generalise the request/response so that persistent connections can be phrased
  as them.
* Benchmark and add benchmarks to the tests.