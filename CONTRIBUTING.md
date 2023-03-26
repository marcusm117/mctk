# Contributing to MCTK

Hi! Thanks for your interest in contributing to [MCTK](https://github.com/marcusm117/mctk). You can contribute in many ways, including:

1. **Report Bugs**: please follow [Reporting Bugs](#reporting-bugs).
2. **Suggest Enhancements**: please follow [Suggesting Enhancements](#suggesting-enhancements).
3. **Contribute Code**: please follow [Contributing Code](#contributing-code).
4. **Contribute Documentation**: please follow [Contributing Documentation](#contributing-documentation).
5. **Contribute Tests**: please follow [Contributing Tests](#contributing-tests).
6. **Contribute Examples**: please follow [Contributing Examples](#contributing-examples).
7. **Contribute Artwork**: please follow [Contributing Artwork](#contributing-artwork).
8. **Contribute Translations**: please follow [Contributing Translations](#contributing-translations)
9. **Share Ideas**: If you have any other ideas or feedback, please follow [Sharing Ideas](#sharing-ideas).

## Reporting Bugs

This section guides you through submitting a bug report for MCTK. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

### Before Submitting a Bug Report

Please check the following list:

1. **Check [MCTK Documentation](https://marcusm117.github.io/mctk/)**: you might be able to find the cause of the problem and fix things yourself. Most importantly, check the [FAQ](https://marcusm117.github.io/mctk/faq.html) and the [Troubleshooting](https://marcusm117.github.io/mctk/troubleshooting.html) sections.
2. **Check [MCTK Issues](https://github.com/marcusm117/mctk/issues)**: you might be able to find the same or similar report. If you find a report that seems related to yours, please add a comment to the existing report instead of opening a new one.
  
### Submitting a Bug Report

Please follow these steps:

1. **Open a New Issue**: open a new issue on [MCTK Issues](https://github.com/marcusm117/mctk/issues). Please use the **Bug Report** template.
2. **Label the Issue**: label the issue with the `bug` label.
3. **Write a Meaningful Title**: write a concise, descriptive title. Try to use the same words you would use searching for an existing bug report. Please do not write titles like "Help!" or "Urgent!".

## Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for MCTK, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion and find related suggestions.

### Before Submitting an Enhancement Suggestion

Please check the following list:

1. **Check [MCTK Documentation](https://marcusm117.github.io/mctk/)**: you might be able to find the cause of the problem and fix things yourself. Most importantly, check the [FAQ](https://marcusm117.github.io/mctk/faq.html) and the [Troubleshooting](https://marcusm117.github.io/mctk/troubleshooting.html) sections.
2. **Check [MCTK Issues](https://github.com/marcusm117/mctk/issues):** you might be able to find the same or similar suggestion. If you find a suggestion that seems related to yours, please add a comment to the existing suggestion instead of opening a new one.

### Submitting an Enhancement Suggestion

Please follow these steps:

1. **Open a New Issue**: open a new issue on [MCTK Issues](https://github.com/marcusm117/mctk/issues). Please use the **Enhancement Suggestion** template.
2. **Label the Issue**: label the issue with the `enhancement` label.
3. **Write a Meaningful Title**: write a concise, descriptive title. Try to use the same words you would use searching for an existing enhancement suggestion. Please do not write titles like "Help!" or "Urgent!".

## Contributing Code

This section guides you through contributing code to MCTK. Following these guidelines helps maintainers and the community understand your contribution and find related contributions.

### Before Opening a Pull Request

Please follow these steps:

1. **Open a New Issue**: open a new issue on [MCTK Issues](https://github.com/marcusm117/mctk/issue) if there is not already an open issue for the code you want to contribute. Please follow the guidelines in [Reporting Bugs](#reporting-bugs) or [Suggesting Enhancements](#suggesting-enhancements) depending on the type of contribution you want to make.
2. **Fork the Repository**: fork [MCTK Repository](https://github.com/marcusm117/mctk) to your Github.
3. **Clone your Fork**: clone your Fork to your Local Environment.

   ```bash
   git clone https://github.com/[YOUR_USERNAME]/mctk.git
   ```

4. **Create a New Branch**: create a new branch for the issue you are working on. Please check out [MCTK Pull Requests](https://github.com/marcusm117/mctk/pulls?q=is%3Apr+is%3Aclosed) to see the latest available branch number. For example, if `MCTK-100` is the last branch that was merged, you should use `MCTK-101`. It's okay if there exist an open pull request using the same branch number, since the first pull request being merged will own the branch number.

   ```bash
   git checkout -b MCTK-[YOUR_BRANCH_NUMBER]
   ```

5. **Check Prerequisites**: make sure that you have the following prerequisites:

   - [Python 3.8+](https://www.python.org/downloads/)

6. **Install Dependencies**: install the all development dependencies for MCTK.

   ```bash
   make develop
   ```

7. **Write Code**: write code for your changes. You can autoformat your code using the following command:

   ```bash
   make format
   ```

8. **Lint Code**: lint your code and make sure that there are no errors. You can lint your code using the following command:

   ```bash
   make lint
   ```

9. **Write Tests**: write tests for your changes. Make sure that all tests pass and the coverage is at least 100%. You can see the coverage using the following command:

   ```bash
   make coverage
   ```

10. **Commit your Changes**: commit your changes to your local repository. It's okay if you have multiple commits for a single pull request, since they will be squashed when merged, but please write meaningful commit messages. Please do not write commit messages like "fix" or "update".

    ```bash
    git commit -m "[YOUR_COMMIT_MESSAGE]"
    ```

11. **Push your Changes**: push your changes to your fork.

    ```bash
    git push origin MCTK-[YOUR_BRANCH_NUMBER]
    ```

### Opening a Pull Request

Please follow these steps:

1. **Open a New Pull Request**: open a new pull request on [MCTK Pull Requests](https://github.com/marcusm117/mctk/pulls) from your fork. Please use the **Code Contribution** template.
2. **Link Pull Request to the related Issue**: link the pull request to the issue you opened in [Before Opening a Pull Request](#before-opening-a-pull-request).
3. **Label the Pull Request**: label the pull request with the labels depending on the type of contribution you made.
4. **Write a Meaningful Title**: write a title starting with your Branch Name followed by a colon, a short description, and the Issue Number. You don't need to worry about the Branch Number, since it will be changed when the pull request is merged. For the short description, please follow examples below:

   ``` text
   MCTK-[YOUR_BRANCH_NUMBER]: added feature A for module B, issue #X
   MCTK-[YOUR_BRANCH_NUMBER]: fixed bug C for funciton D, issue #Y
   MCTK-[YOUR_BRANCH_NUMBER]: updated section E for documentation F, issue #Z
   ```

5. **Make sure that all the checks pass**: make sure that all the checks pass. If there are any errors, please fix them and push your changes to your fork. The checks will automatically run again.
6. **Congratulations!**: you have successfully contributed code to MCTK. We will review your pull request as soon as possible! Please feel free to add comments or ask questions in your pull request.
