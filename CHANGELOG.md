# Changelog

## [9.3.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.3.1...v9.3.2) (2024-10-06)


### Bug Fixes

* iteration over env vars ([#77](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/77)) ([07135e5](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/07135e5d712344c53b6f99b3824fb97ea03c801b))

## [9.3.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.3.0...v9.3.1) (2024-10-04)


### Bug Fixes

* use correct names when collecting builtin plugins ([#75](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/75)) ([359e8ed](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/359e8ed32990cbccbfeda7fe746ece19d12e75bf))

## [9.3.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.2.0...v9.3.0) (2024-10-04)


### Features

* load builtin snakemake executor plugins ([#73](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/73)) ([03ee96b](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/03ee96be5047d68f7d9de951ab75458e7c79d3e3))

## [9.2.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.1.1...v9.2.0) (2024-07-04)


### Features

* add a default for the `can_transfer_local_files` interface ([#67](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/67)) ([793df28](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/793df28ba733eb462fba7824f46729af65a58dc4))
* support for commas in wildcards ([#56](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/56)) ([0e8ed82](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/0e8ed82c2dc8338b402e646dde7ca48e02075922))

## [9.1.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.1.0...v9.1.1) (2024-04-12)


### Bug Fixes

* pass cores to remote jobs if they are set ([395af5e](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/395af5e05c8b09d107415159819d0e3cef58717f))

## [9.1.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.0.2...v9.1.0) (2024-03-26)


### Features

* add utils for encoding CLI args as base64 ([#64](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/64)) ([38a53ec](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/38a53ecec3af3fc45d2f962972460fa50258b2b1))

## [9.0.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.0.1...v9.0.2) (2024-03-22)


### Bug Fixes

* quote list of args ([#62](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/62)) ([656ba0a](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/656ba0afb867301ccb48b24837fda1793e3281dc))

## [9.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v9.0.0...v9.0.1) (2024-03-21)


### Bug Fixes

* fix quoting of string arguments that are passed to spawned jobs ([#60](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/60)) ([d3d55a3](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/d3d55a32dbd78be679727c3f95cd42308a9597ab))

## [9.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.2.0...v9.0.0) (2024-03-11)


### ⚠ BREAKING CHANGES

* pass common settings to SpawedJobArgsFactory; shell command arg quoting fixes ([#58](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/58))

### Features

* pass common settings to SpawedJobArgsFactory; shell command arg quoting fixes ([#58](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/58)) ([867a027](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/867a027e8abbfa8937900b648aeade91b01c2c38))

## [8.2.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.1.3...v8.2.0) (2024-01-16)


### Features

* add ability to pass group args to remote jobs ([bcfd819](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/bcfd81953b3feeaac6669a3487cc1eab3d5a2727))

## [8.1.3](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.1.2...v8.1.3) (2023-12-19)


### Bug Fixes

* break circular import ([aed33aa](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/aed33aa2aba20e229398deb5ad486d3b0ec7e213))

## [8.1.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.1.1...v8.1.2) (2023-12-12)


### Documentation

* CommonSettings ([#50](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/50)) ([85b995d](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/85b995d726cd941ea0f6e43b6217e95140a82327))

## [8.1.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.1.0...v8.1.1) (2023-12-08)


### Bug Fixes

* allow value of none for shared fs usage setting ([d334869](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/d33486933f41f2bccd099e2cab90b2d1a854def2))

## [8.1.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.0.2...v8.1.0) (2023-11-30)


### Features

* add method for checking whether there is a common workdir assumed in storage settings ([29dc8dd](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/29dc8dd43ba4bd8d33eeda14a3dff9272d3751f0))


### Bug Fixes

* adapt to API changes ([21cae32](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/21cae32a8a69b58b732b773a849abfb02b533575))

## [8.0.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.0.1...v8.0.2) (2023-11-20)


### Bug Fixes

* fix arg passing ([caee462](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/caee46241f4fc639ed585761421d335f7783399c))

## [8.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v8.0.0...v8.0.1) (2023-11-20)


### Bug Fixes

* cleanup ci ([061ff4c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/061ff4ce7a6ef699dfff58c149195425bef13e86))
* fix method name ([16138ad](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/16138ad9e085a289590b8308cc954662e8df0ffe))

## [8.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v7.0.3...v8.0.0) (2023-11-20)


### ⚠ BREAKING CHANGES

* added common setting for defining whether workflow sources shall be deployed.

### Features

* added common setting for defining whether workflow sources shall be deployed. ([04319bb](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/04319bbe410275eea28cbe47d2abfe9b0b50c3e5))

## [7.0.3](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v7.0.2...v7.0.3) (2023-10-26)


### Bug Fixes

* fix envvar declarations code ([fc31775](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/fc31775075f8b6ac6317b3762bcd385f31a8b746))
* improved precommand handling ([af1f010](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/af1f01006fd5e7a493659e0bcb80e570628e5176))

## [7.0.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v7.0.1...v7.0.2) (2023-10-20)


### Bug Fixes

* ignore errors when trying to delete tmpdir upon shutdown ([#39](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/39)) ([406422c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/406422c967ebd33227c34e257b0a1a5cdd0a3e4d))

## [7.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v7.0.0...v7.0.1) (2023-10-17)


### Miscellaneous Chores

* release 7.0.1 ([c51e47b](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/c51e47b5b3eed7a5d52e27dead1d51659563aa9d))

## [7.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v6.0.0...v7.0.0) (2023-10-17)


### ⚠ BREAKING CHANGES

* move behavior args into common settings and use __post_init__ method for additional initialization

### Features

* move behavior args into common settings and use __post_init__ method for additional initialization ([c6cb3c9](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/c6cb3c9c02de7e7aeba241558ba549a65abcfc2b))
* support precommand ([32da209](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/32da20943b1afe8854566356ed448015e4f67e6c))

## [6.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v5.0.2...v6.0.0) (2023-10-12)


### ⚠ BREAKING CHANGES

* adapt to API changes

### Features

* adapt to API changes ([f74151b](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/f74151b32a9b98a323bbbf88a818b7da5fe97427))


### Bug Fixes

* adapt to changes in snakemake ([e572f02](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/e572f02c7b5270fc02fc871ac6197575ce42ad5c))
* cleanup interfaces ([88c6554](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/88c65546db32fc5e48827173bb016d69691c41cb))
* udpate deps ([99b5b1e](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/99b5b1e61302d75fb6ca7a959fda18cceaf12703))

## [5.0.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v5.0.1...v5.0.2) (2023-09-22)


### Documentation

* mention poetry plugin ([733f2f9](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/733f2f93b0e1fedb9aeda21ea6987b7b7059be11))

## [5.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v5.0.0...v5.0.1) (2023-09-22)


### Bug Fixes

* adapt to changes in snakemake-interface-common ([faa05a4](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/faa05a40068e656e533671324c4a3928158e652e))
* adapt to fixes in snakemake-interface-common ([2a92560](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/2a92560fa602cab4b3085643324bdaaa36d1ea42))

## [5.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v4.0.1...v5.0.0) (2023-09-21)


### ⚠ BREAKING CHANGES

* maintain Python 3.7 compatibility by moving settings base classes to the settings module

### Bug Fixes

* maintain Python 3.7 compatibility by moving settings base classes to the settings module ([71c976e](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/71c976ea2a51afa418683effd3db9d80dca15150))
* use bugfix release of snakemake-interface-common ([2441fc3](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/2441fc36fc0cfc404aafeb0d8b86e7f107c7ebb6))

## [4.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v4.0.0...v4.0.1) (2023-09-20)


### Bug Fixes

* return correct value for next_seconds_between_status_checks ([0606922](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/06069228debfc55629f2eb6f2e88ac1b81ad90c8))

## [4.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v3.0.2...v4.0.0) (2023-09-19)


### ⚠ BREAKING CHANGES

* rename ExecutorJobInterface into JobExecutorInterface

### Code Refactoring

* rename ExecutorJobInterface into JobExecutorInterface ([9f61b6a](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/9f61b6a5f16ab39582429b813640fa08f3e0231c))

## [3.0.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v3.0.1...v3.0.2) (2023-09-12)


### Bug Fixes

* add error details in case of improper join_cli_args usage ([cb0245f](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/cb0245fe47adfc73e07600821b5813687025ad9c))

## [3.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v3.0.0...v3.0.1) (2023-09-11)


### Bug Fixes

* avoid dependeing on argparse_dataclass fork ([0a1f02d](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/0a1f02d5facf81a48ab687d8cb2809aebd6518d8))
* fix NoneType definition ([1654a41](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/1654a4140b7ee91c5e7f7370795fd67e5e70014b))

## [3.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v2.0.0...v3.0.0) (2023-09-11)


### ⚠ BREAKING CHANGES

* unify self.report_job_error and self.print_job_error.

### Features

* add further metadata to ExecutorSettings ([30f0977](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/30f0977a646f13bc86a649e3e76ddfbf417f3ace))
* add get_items_by_category method to ExecutorSettings ([7f62bb9](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/7f62bb9d15aa80f87964974d7a0bca504990e540))
* add support for env_var specification in ExecutorSettings ([a1e3123](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/a1e3123a80db7b96bdb3cca11fa3faa21ab90ab3))
* unify self.report_job_error and self.print_job_error. ([2f24fb9](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/2f24fb938cef05abf912e4a66a066fdce414f06b))


### Documentation

* update readme ([100bdc0](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/100bdc015ef2e8af4aa35fb2a027f46aeb73d244))
* update readme ([836b893](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/836b893287c8abed89dc738f9a3f48c335d9827a))

## [2.0.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v1.2.0...v2.0.0) (2023-09-08)


### ⚠ BREAKING CHANGES

* rename ExecutorPluginRegistry.get to get_plugin.
* naming
* improved API

### Features

* add touch_exec ([0ac8b16](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/0ac8b16e86419267e6cea49dee3451ed22fbde80))
* allow to set the next sleep time ([f8fde6c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/f8fde6c0cbdbaf7cf164db65aae3ead5f5db919a))
* allow to specify the initial amount of seconds to sleep before checking job status ([0e88e6f](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/0e88e6ff4d3547c2c0991bc9d172413c9ed0d70b))
* improved API ([0226c9d](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/0226c9d2e7ab330f8552827f9714a43ff7f805c5))
* naming ([978f74c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/978f74cab5ab1e829f1636993dd46b8b51589ce8))
* rename ExecutorPluginRegistry.get to get_plugin. ([c1b50d9](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/c1b50d9fb433d685749c10319827dea973caa8b2))
* simplify API ([3e4be2a](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/3e4be2af66fd6fdbd3b0b60562023a4bdc64f92e))


### Bug Fixes

* API typing ([c9180fa](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/c9180fa55897e1b974edb068531f4cd6edce8d15))

## [1.2.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v1.1.2...v1.2.0) (2023-09-05)


### Features

* simplify executor API ([7479c1c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/7479c1c98f0fdf04ee77cea11feae4da2421ff90))
* various API improvements ([a2808ad](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/a2808ad1ec480949e88efc442532952f42d8f450))

## [1.1.2](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v1.1.1...v1.1.2) (2023-09-01)


### Bug Fixes

* convert enum to cli choice ([a2f287c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/a2f287c9cd66d4b4ccb847434ee9294c4749b233))
* various adaptations to changes in Snakemake 8.0 ([58ff504](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/58ff50488b49b1a34e41c4fa9812297430cc9672))

## [1.1.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v1.1.0...v1.1.1) (2023-08-30)


### Bug Fixes

* practical improvements ([f91133a](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/f91133af160aef941e3663cfe3a50653589244f3))

## [1.1.0](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v1.0.1...v1.1.0) (2023-08-28)


### Features

* refactor and clean up interfaces ([#14](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/14)) ([fc28032](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/fc28032030204504e26c148e73ef8d85af9a5cf7))

## [1.0.1](https://github.com/snakemake/snakemake-interface-executor-plugins/compare/v1.0.0...v1.0.1) (2023-08-02)


### Bug Fixes

* release process fix ([b539c1b](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/b539c1b6795cfff9440bbd7e283e51c2df6518ba))

## 1.0.0 (2023-08-02)


### Features

* migrate interfaces from snakemake to this package ([#7](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/7)) ([cc3327c](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/cc3327c1e3020ff25f72f93f4c2711d7cadb11e6))
* migrate snakemake.common.Mode into this package ([b0aa928](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/b0aa928d30f4cf49d459b8fa6ed6904d269f9d27))
* object oriented plugin interface implementation ([a6923d2](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/a6923d2e5319124b5db2b72210280c43c5a47624))
* start of work to integrate functions ([#5](https://github.com/snakemake/snakemake-interface-executor-plugins/issues/5)) ([56f16d8](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/56f16d8f8ce9b0bf47d7d88be98548c6ed860970))


### Bug Fixes

* fix jobname checking logic ([1358f5f](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/1358f5fd3070cf1c4f0b08e65b9cd805dd8a1e90))
* jobname checking ([f7a67d4](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/f7a67d4d6dfee279fa1ff088e1d1f9241dfdcbe0))
* remove superfluous attribute ([7d283f8](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/7d283f8551f0d2c80dadf87717d804422b3b5c09))


### Performance Improvements

* improve plugin lookup ([514514f](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/514514f22fcd3387915a65969ffd1d6c14c56964))


### Miscellaneous Chores

* release 1.0 ([59415f4](https://github.com/snakemake/snakemake-interface-executor-plugins/commit/59415f461616ab69668ea06c4a34932de70ea4bc))
