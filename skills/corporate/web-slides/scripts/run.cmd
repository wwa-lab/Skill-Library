@echo off
setlocal
rem No PATH changes, installs, elevation, or shell-generated command strings.
if /I "%~1"=="--python" goto explicit
if defined CORPORATE_SLIDES_PYTHON goto configured
where py >nul 2>nul
if errorlevel 1 goto python3
py -3 -c "import sys; sys.exit(sys.version_info.major != 3)" >nul 2>nul
if errorlevel 1 goto python3
py -3 "%~dp0python-runtime.py" %*
exit /b %errorlevel%
:python3
where python3 >nul 2>nul
if errorlevel 1 goto python
python3 -c "import sys; sys.exit(sys.version_info.major != 3)" >nul 2>nul
if errorlevel 1 goto python
python3 "%~dp0python-runtime.py" %*
exit /b %errorlevel%
:python
where python >nul 2>nul
if errorlevel 1 goto missing
python -c "import sys; sys.exit(sys.version_info.major != 3)" >nul 2>nul
if errorlevel 1 goto missing
python "%~dp0python-runtime.py" %*
exit /b %errorlevel%
:explicit
if "%~2"=="" goto missing
"%~2" "%~dp0python-runtime.py" %*
exit /b %errorlevel%
:configured
"%CORPORATE_SLIDES_PYTHON%" "%~dp0python-runtime.py" %*
exit /b %errorlevel%
:missing
echo Python 3 was not found. Use --python with an existing python.exe path. 1>&2
exit /b 1
