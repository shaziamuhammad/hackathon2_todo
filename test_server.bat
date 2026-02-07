@echo off
echo Testing FastAPI Server CORS Configuration...
echo.
echo Testing root endpoint:
curl -X GET http://localhost:8000/
echo.
echo.
echo Testing OPTIONS preflight for auth/register:
curl -X OPTIONS http://localhost:8000/api/v1/auth/register ^
-H "Origin: http://localhost:3000" ^
-H "Access-Control-Request-Method: POST" ^
-H "Access-Control-Request-Headers: Content-Type"
echo.
echo.
echo Testing GET on auth/register:
curl -X GET http://localhost:8000/api/v1/auth/register
echo.
echo.
echo Test completed!
pause