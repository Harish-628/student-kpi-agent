---
name: Bug Report
description: Create a report to help us improve
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  - type: textarea
    id: bug-description
    attributes:
      label: Describe the bug
      description: A clear and concise description of what the bug is.
      placeholder: Bug description...
    validations:
      required: true
  - type: textarea
    id: steps-to-reproduce
    attributes:
      label: Steps to Reproduce
      description: How can we see the bug for ourselves?
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true
  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
  - type: textarea
    id: environment
    attributes:
      label: Environment Info
      description: OS, Browser, Python version, etc.
      placeholder: |
        - OS: Windows 11
        - Python: 3.10.12
        - FastAPI: 0.100.0
    validations:
      required: true
  - type: checkboxes
    id: checks
    attributes:
      label: Check-list
      options:
        - label: I have searched the existing issues
          required: true
        - label: I am using the latest version of the code
          required: true
