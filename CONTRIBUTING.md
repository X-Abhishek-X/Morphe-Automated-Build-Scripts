# Contributing to ReVanced APK Patcher Scripts

Thank you for your interest in contributing! This project provides Windows wrapper scripts for the ReVanced CLI.

## 🎯 What You Can Contribute

### Script Improvements

- Bug fixes in batch/PowerShell scripts
- Better error handling
- Cross-platform compatibility (Linux/macOS scripts)
- Performance optimizations

### Documentation

- Clarifications in README
- Additional troubleshooting tips
- Translation to other languages
- Video tutorials or guides

### Features

- Auto-update checker for ReVanced components
- GUI wrapper for the scripts
- Additional patch presets
- Better logging and debugging

## 🚫 What NOT to Contribute Here

This repository is **ONLY** for wrapper scripts. Please do NOT submit:

- Patches for apps (contribute to [ReVanced Patches](https://github.com/ReVanced/revanced-patches))
- CLI improvements (contribute to [ReVanced CLI](https://github.com/ReVanced/revanced-cli))
- APK files or binaries
- Requests for specific app patches

## 📝 How to Contribute

### Reporting Issues

1. **Search existing issues** to avoid duplicates
2. **Use a clear title** describing the problem
3. **Provide details**:
   - Your Windows version
   - PowerShell version (`$PSVersionTable`)
   - Java version (`java -version`)
   - Complete error messages
   - Steps to reproduce

### Submitting Pull Requests

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**:
   - Follow existing code style
   - Test thoroughly on Windows
   - Update documentation if needed
4. **Commit with clear messages**:
   ```bash
   git commit -m "Add: feature description"
   ```
5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**:
   - Describe what you changed and why
   - Reference any related issues
   - Include testing details

## 💻 Code Style Guidelines

### Batch Scripts (.bat)

- Use `REM` for comments
- Include error checking with `if %ERRORLEVEL%`
- Use `@echo off` at the start
- Provide clear user feedback with `echo`

### PowerShell Scripts (.ps1)

- Use `Write-Host` with colors for user feedback
- Include parameter validation
- Use proper error handling with `try/catch`
- Follow PowerShell naming conventions (Verb-Noun)

### Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep line length reasonable (80-100 chars)
- Use proper Markdown formatting

## 🧪 Testing Requirements

Before submitting a PR, please test:

- ✅ Scripts run without errors on Windows 10/11
- ✅ Error messages are clear and helpful
- ✅ All file paths work correctly
- ✅ Documentation is accurate
- ✅ No hardcoded paths or credentials

## 📋 Pull Request Checklist

- [ ] Code follows the style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] Tested on Windows
- [ ] No breaking changes (or clearly documented)

## 🤝 Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on the issue, not the person
- Give credit where due

## 📞 Questions?

- Open a [Discussion](../../discussions) for general questions
- Open an [Issue](../../issues) for bugs or feature requests
- Check existing documentation first

## 🙏 Thank You!

Every contribution, no matter how small, helps make this project better for everyone!

---

**Note**: For contributions to the actual patching functionality, please contribute to the official [ReVanced repositories](https://github.com/ReVanced).
