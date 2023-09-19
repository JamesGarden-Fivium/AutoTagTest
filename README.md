# Drone CI Plugin for Versioning

- [Drone CI Plugin for Versioning](#drone-ci-plugin-for-versioning)
  - [Overview](#overview)
  - [Usage](#usage)
  - [Settings](#settings)
  - [Environment Variables](#environment-variables)
---

## Overview

This plugin will tag the repository with a new version when build. If all commits since the last tag contain the minor commit string
then the minor version will be incremented. Otherwise the major version will be incremented.

## Usage

Before using this plugin tag your main branch with an initial version like `1.0`

```yaml
---
kind: pipeline
type: docker
name: semantic-version

steps:
  - name: generate-tag
    image: fivium-auto-tag
    settings:
      minor_commit_string_csv: "#autodeploy,#dependencyupdate"
      image_prefix: "main-"
```

## Settings

```yaml
settings:
  minor_commit_string_csv: "#autodeploy,#dependencyupdate"
  image_prefix: "main-"
```

All settings will be passed into the container using environment variables.
A complete overview of the available environment variables can be found in the table below.

## Environment Variables

The following table contains an overview of the available environment variables to configure
the application.

| Name                           | Description                                               | Default Value     |
| ------------------------------ | --------------------------------------------------------- | ----------------- |
| DRONE_BUILD_NUMBER             | Drone CI build number, injected by Drone CI               | `N/A`             |
| PLUGIN_MINOR_COMMIT_STRING_CSV | A csv of commit message prefixes to denote minor versions | `#autodeploy`     |
| PLUGIN_IMAGE_PREFIX            | A prefix to apply to all image tags                       | ``                |