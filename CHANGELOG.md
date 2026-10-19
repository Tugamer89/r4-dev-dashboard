# Changelog

## [0.2.0](https://github.com/Tugamer89/r4-dev-dashboard/compare/v0.1.1...v0.2.0) (2026-10-19)


### Features

* add monitor and upload-monitor targets to Makefile for improved firmware management ([084a4b9](https://github.com/Tugamer89/r4-dev-dashboard/commit/084a4b95f5135626b2bbcd022083da801a7506b2))
* add run-daemon-win target to Makefile for Windows daemon execution ([c7933e3](https://github.com/Tugamer89/r4-dev-dashboard/commit/c7933e3e8b7acb5bc15fa4b684ffcbfe74654bf9))
* add workflow to sync uv.lock on pull request events ([d7f44a0](https://github.com/Tugamer89/r4-dev-dashboard/commit/d7f44a072c02aadd869ac6322ffe9ff7f1d8999f))
* enhance Arduino attachment script with improved device search and error handling ([36b995c](https://github.com/Tugamer89/r4-dev-dashboard/commit/36b995c5c4289c4c8a9af46bf2e729ce707f9b79))
* enhance dynamic repository detection and CI/CD monitoring integration ([f7c2137](https://github.com/Tugamer89/r4-dev-dashboard/commit/f7c213705f2ddef9dad745f49ce527f5fcbb991b))
* enhance system monitoring with build process detection and mode reporting ([bbadf71](https://github.com/Tugamer89/r4-dev-dashboard/commit/bbadf71ac00967a715bb103fc6c4bd4a871a2028))
* enhance telemetry monitoring and WebSocket communication in daemon ([fd95649](https://github.com/Tugamer89/r4-dev-dashboard/commit/fd95649dfe0f4afd4078ea28ad95da7c0cf06d43))
* enhance WSL integration to extract git repositories from UNC paths and improve command line detection ([1e55ac4](https://github.com/Tugamer89/r4-dev-dashboard/commit/1e55ac496783bc96497ec4c366e1d96dc702b549))
* implement configuration management and CI/CD monitoring for R4 Dev Dashboard ([70239de](https://github.com/Tugamer89/r4-dev-dashboard/commit/70239de31532fd946fb0b0011459c68cb64e8576))
* refactor NetworkManager to use UDP instead of WebSockets for communication ([ba86990](https://github.com/Tugamer89/r4-dev-dashboard/commit/ba8699002393adaf53bae63f0aa536d789d2dfc0))
* refactor system monitoring to use dedicated functions for CPU, RAM, and GPU metrics ([83069a6](https://github.com/Tugamer89/r4-dev-dashboard/commit/83069a6c795579a02fe315a68c90d6dd60a583cc))


### Bug Fixes

* add auto-attach option for usbipd to improve device connection during flashing ([7f97dd4](https://github.com/Tugamer89/r4-dev-dashboard/commit/7f97dd4397903b853d6322fa27735b43a1ba77e1))
* add defensive fallback for GitHub token and polling interval in monitor_github ([89efc13](https://github.com/Tugamer89/r4-dev-dashboard/commit/89efc1348d24624a34d33983dddf35a35d42595a))
* add permissions for write access in sync-lock job ([82a8fb9](https://github.com/Tugamer89/r4-dev-dashboard/commit/82a8fb9b29f6165153935e9f7b35664f05d12670))
* correct coverage and CPD exclusions in sonar-project.properties ([d091596](https://github.com/Tugamer89/r4-dev-dashboard/commit/d0915966222195a4830df803e7b86ec068d97d01))
* enhance build rendering with state transition handling and animation reset ([44f8b75](https://github.com/Tugamer89/r4-dev-dashboard/commit/44f8b759f498d5de69ab83c2e9e775bc4494afcc))
* improve metrics extraction by ensuring all required fields are floats ([419303b](https://github.com/Tugamer89/r4-dev-dashboard/commit/419303b7fc1cb5047f1fc5cbc2accb6b61f03e11))
* improve readability of Makefile setup commands in sync workflow ([60303d2](https://github.com/Tugamer89/r4-dev-dashboard/commit/60303d230ce87c5cd53fcde49daea06cd8e8bbf4))
* increase WiFi retry interval to 10 seconds for improved connection stability ([2d49369](https://github.com/Tugamer89/r4-dev-dashboard/commit/2d49369445e8dbd8e1106879a5b0951f8367f2c1))
* refine client registration logic in UDPProtocol to ensure only valid PING packets are registered ([bc1bd52](https://github.com/Tugamer89/r4-dev-dashboard/commit/bc1bd528ae95a4bbe1227227ccd95dd90ac1230c))
* remove auto-attach option from usbipd attach command in attach_arduino.ps1 ([089a5d1](https://github.com/Tugamer89/r4-dev-dashboard/commit/089a5d153537c6077aedd601957f02fabd66e7c9))
* streamline uv.lock update process by removing unnecessary setup commands ([aee5444](https://github.com/Tugamer89/r4-dev-dashboard/commit/aee5444c0f60e742a7c3d4c04dc032497dcddaf0))
* trigger release please ([9b95cd2](https://github.com/Tugamer89/r4-dev-dashboard/commit/9b95cd207542cf8510705499b0dac3de1a46d758))
* update checkout token to use PAT_TOKEN for improved access ([577807b](https://github.com/Tugamer89/r4-dev-dashboard/commit/577807be4876bf8ae9ac7cb692a64cd207c5ce30))
* update Makefile setup command to ensure proper environment setup for uv ([8c7afb9](https://github.com/Tugamer89/r4-dev-dashboard/commit/8c7afb98135296a114f1ba664b0f063c17caf6f9))
* update r4-daemon version to 0.1.1 in uv.lock ([c990d6f](https://github.com/Tugamer89/r4-dev-dashboard/commit/c990d6f543a9d74515cdfb4fa6e524804cf72f8d))
* update run-daemon-win to open a new Windows terminal for the daemon ([0e48f3b](https://github.com/Tugamer89/r4-dev-dashboard/commit/0e48f3b8475d5d7fcb3500d9c929ac625c261eeb))
* update version to 0.1.1 in pyproject.toml ([449fc05](https://github.com/Tugamer89/r4-dev-dashboard/commit/449fc05f389cb3694ec9d2c641b9d2779e9da0dd))

## [0.1.1](https://github.com/Tugamer89/r4-dev-dashboard/compare/v0.1.0...v0.1.1) (2026-10-18)


### Features

* add get_daemon_version function to retrieve package version dynamically ([c542050](https://github.com/Tugamer89/r4-dev-dashboard/commit/c542050f7234863754be11d4f5e71ab7ad0d1b07))
* initial project setup and architecture ([a6a1682](https://github.com/Tugamer89/r4-dev-dashboard/commit/a6a1682968e49dc07566573de88bd13df356662f))


### Bug Fixes

* correct command for formatting check in Python linter workflow ([890a7e2](https://github.com/Tugamer89/r4-dev-dashboard/commit/890a7e2e514a63dc692e1c06fca370b51c21ba12))
