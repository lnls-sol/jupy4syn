# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.3] - 2019-11-26
### Fixed
- Configuration display-number default value

## [0.2.2] - 2019-11-01
### Added
- SpecPlot command. It plots a SPEC file with matplotlib.

### Fixed
- move Command parsing
- connect_display KeyboardInterruption
- Configuration user display check

## [0.2.1] - 2019-09-25
### Added
- CommandButton can operate with every command (it calls UserCommand if the command specified is not defined in the CommandDict)

### Fixed
- ScanGuiCommand parses its arguments correctly
- CommandButton handling for SystemExit
- MoveCommand string parsing

## [0.2.0] - 2019-09-19
### Added
- Documentation for all Commands
- Text box verification for edition/visualization

### Fixed
- Motors and Slits string parsing

### Changed
- commandButton class is now CommandButton (following PEP8)

### Removed
- Button classes

## [0.1.4] - 2019-08-13
### Added
- exec_ssh script for Windows

### Fixed
- commandButton for commands slits and motors now parses arguments correctly.
- connect_display script loop performance

## [0.1.3] - 2019-08-05
### Added
- Generic command for commandButton.

## [0.1.2] - 2019-08-05
### Added
- "lock/test" system for users_displays.yml file.
- Error handling for file editing. (File existence and permission checks)

## [0.1.1] - 2019-08-02
### Added
- SSH Connection scripts for local and remote machines.

### Changed
- Updated commandButton calls to use new display system.

## [0.1.0] - 2019-08-01
### Added
- Initial Release.
