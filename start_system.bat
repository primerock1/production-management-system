@echo off
echo ========================================
echo   Запуск системы управления производством
echo ========================================
echo.

echo Запуск Backend API...
start "Backend API" cmd /k "cd /d %~dp0backend && python run.py"

echo Ожидание запуска Backend...
timeout /t 3 /nobreak > nul

echo Запуск Frontend...
start "Frontend" cmd /k "cd /d %~dp0frontend && python -m http.server 3000"

echo.
echo ========================================
echo   Система запущена!
echo ========================================
echo   Backend API: http://localhost:8000
echo   Frontend:    http://localhost:3000
echo   Документация: http://localhost:8000/docs
echo ========================================
echo.
echo Нажмите любую клавишу для открытия браузера...
pause > nul

start http://localhost:3000

echo.
echo Для остановки системы закройте окна терминалов
pause