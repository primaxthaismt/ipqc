@echo off
if "%VERCEL_TOKEN%"=="" (
    echo Error: VERCEL_TOKEN environment variable is not set.
    exit /b 1
)
call npx vercel --prod --yes --token=%VERCEL_TOKEN%
