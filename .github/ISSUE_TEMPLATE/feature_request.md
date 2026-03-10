---
name: Feature Request
description: Suggest an idea for this project
labels: ["enhancement"]
body:
  - type: markdown
    attributes:
      value: |
        We would love to hear your ideas for improving NeuralKPI!
  - type: textarea
    id: feature-description
    attributes:
      label: Describe the feature
      description: A clear and concise description of what the feature is.
    validations:
      required: true
  - type: textarea
    id: problem-solved
    attributes:
      label: Problem Statement
      description: Is your feature request related to a problem? Please describe.
    validations:
      required: true
  - type: textarea
    id: proposed-solution
    attributes:
      label: Proposed Solution
      description: A clear and concise description of what you want to happen.
    validations:
      required: true
  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: A clear and concise description of any alternative solutions or features you've considered.
  - type: checkboxes
    id: checks
    attributes:
      label: Check-list
      options:
        - label: I have searched the existing issues
          required: true
