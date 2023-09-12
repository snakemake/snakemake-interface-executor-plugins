# Changelog

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
