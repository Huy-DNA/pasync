# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://github.com/Huy-DNA/pasync/compare/39dcb9c42984191ff61a5b4ade4b5291c4c239c3...HEAD)</small>

### Fixed

- fix!: method name change ([9069a24](https://github.com/Huy-DNA/pasync/commit/9069a24f9d99cb651c04e29e301358d147cb79b5) by Huy-DNA).
- fix: handling of coroutine return ([054db3e](https://github.com/Huy-DNA/pasync/commit/054db3ebf8cdac5596f83b335f9fbc5131c65e13) by Huy-DNA).
- fix: forgot run queue task for blocking event loop ([96eeacc](https://github.com/Huy-DNA/pasync/commit/96eeacc312ab89bfc5352d1a3fcb07a410cbe715) by Huy-DNA).
- fix: incorrect call to __run_non_blocking in runner ([f9e22d3](https://github.com/Huy-DNA/pasync/commit/f9e22d35e0aabd84720f020f3d592cc7d452cc16) by Huy-DNA).
- fix: wrong type annotations ([5dbed53](https://github.com/Huy-DNA/pasync/commit/5dbed539adbe4e947b29f5cf63768b97e51938bd) by Huy-DNA).
- fix: remove unused parameters in Runner.__enter__ ([f6e642f](https://github.com/Huy-DNA/pasync/commit/f6e642fc6b9935958116f7dbe094e333fdb70037) by Huy-DNA).
- fix: prevent queueing when a blocking event loop is already running ([98671a6](https://github.com/Huy-DNA/pasync/commit/98671a620ca7e6b6ea476b82839d32a0702bef17) by Huy-DNA).
- fix: error message in event_loop.queue ([7977f65](https://github.com/Huy-DNA/pasync/commit/7977f658dba8b139f994793172e50a3f1dc1599d) by Huy-DNA).
- fix: acquire variable condition before notifying ([250d913](https://github.com/Huy-DNA/pasync/commit/250d913242415b4df84c05c8bb019412794b4b7e) by Huy-DNA).
- fix: acquire and release condition variable ([c70665a](https://github.com/Huy-DNA/pasync/commit/c70665a9e8068fd2179712ca07eb6b3dfd85bf2e) by Huy-DNA).
- fix: event_loop run_non_blocking check ([aefb04d](https://github.com/Huy-DNA/pasync/commit/aefb04d6718288e77cbec34a46805d8b6785efdd) by Huy-DNA).
- fix: catch StopIteration instead of StopAsyncIteration ([056aa7e](https://github.com/Huy-DNA/pasync/commit/056aa7e3d4c1799ad984b66bbada297a310d3e23) by Huy-DNA).
- fix: forget to start thread ([eee5877](https://github.com/Huy-DNA/pasync/commit/eee58774a0ecf31b44e9c2abee5451f26e100dcd) by Huy-DNA).
- fix: import paths ([5acffb0](https://github.com/Huy-DNA/pasync/commit/5acffb09238546267b178751dae53ae24488c6b6) by Huy-DNA).
- fix: __enter__ and __exit__ of runner ([0916105](https://github.com/Huy-DNA/pasync/commit/0916105bf621c39fb7beb8cc99efe00a9483993f) by Huy-DNA).
- fix: remove unused imports ([c73fedf](https://github.com/Huy-DNA/pasync/commit/c73fedf420fe081f94b6b7d1b3480a8dc47797fc) by Huy-DNA).
- fix: hide Task ([dac8a72](https://github.com/Huy-DNA/pasync/commit/dac8a72ac8140d790ee4702cbbbe69abce39265e) by Huy-DNA).
- fix: import path ([63fe318](https://github.com/Huy-DNA/pasync/commit/63fe318d4ee7cbc7a39ead131cea77e221745042) by Huy-DNA).

<!-- insertion marker -->
