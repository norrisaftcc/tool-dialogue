# Changelog

All notable changes to the Retro Terminal Dialogue System project will be documented in this file.

## [Unreleased]
- Variable system implementation
- Visual dialogue tree editor
- Enhanced import/export capabilities

## [0.5.0] - 2025-05-08
### Added
- Complete architecture redesign with three-layer structure:
  - Data layer for file operations
  - Logic layer for game state and dialogue navigation
  - GUI layer for Streamlit presentation
- Enhanced dialogue navigation with more robust state management
- Better condition evaluation and script handling
- Support for completed quests display

### Changed
- Terminal simulator completely reimplemented with layered architecture
- Improved file loading from conversations directory
- Enhanced error handling and recovery
- More robust dialogue state management

### Fixed
- Fixed issues with blank UI rendering
- Fixed image display for character portraits
- Added better handling for missing dialogues or files

## [0.4.0] - 2025-05-08
### Added
- Comprehensive dialogue validator with reference checking and naming validation
- Organized file structure with conversations/ and templates/ directories
- Template system for creating new dialogue files
- Dialogue testing framework with sample files
- Image support for character portraits
- Dropdown menu in simulator for selecting dialogue files

### Changed
- Updated terminal simulator to work with new directory structure
- Improved file loading and error handling
- Enhanced documentation with validation and organization guides

### Fixed
- Removed broken image URL from terminal simulator
- Fixed duplicate element IDs in Streamlit interface
- Fixed validation for quest stage references

## [0.3.0] - 2025-05-07
### Added
- Interactive tutorial dialogue with character "Pixel"
- CLI parser for command-line dialogue interaction
- JSON schema for dialogue format standardization
- Schema validator for checking and fixing dialogue files
- "About" dialogue discussing the system development
- Presentation materials (outline, examples, talking points)

### Changed
- Standardized JSON format with backward compatibility
- Updated README with comprehensive documentation
- Improved dialogue file organization

### Fixed
- Issues with inconsistent dialogue file formats
- Fixed references in dialogue files

## [0.2.0] - 2025-05-01
### Added
- Dialogue editor with tabbed interface
- Quest system implementation
- Multiple dialogue examples
- Documentation for dialogue format

### Changed
- Enhanced terminal simulator with improved styling
- Better dialogue navigation
- Support for different dialogue files

## [0.1.0] - 2025-04-15
### Added
- Initial implementation of terminal dialogue simulator
- Basic green-on-black terminal aesthetic
- Simple dialogue tree navigation
- Streamlit web interface
- Basic dialogue format in JSON
- Default example dialogue

## Project Origins
The Retro Terminal Dialogue System began as a simple project to create a Twine alternative that didn't require external tools. The core concept was to build a JSON-based dialogue system with an 80s terminal aesthetic that evoked nostalgic text adventures while providing modern functionality.

The project evolved from a basic text display to include:
- Interactive dialogue choices
- Quest tracking system
- Typewriter text effects
- Dialogue editing capabilities
- Standardized dialogue format

The system maintains its focus on the retro terminal experience while continuously improving its capabilities for narrative designers and developers.