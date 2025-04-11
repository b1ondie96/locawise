import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
async def expected_dict_for_default_java_properties() -> dict[str, str]:
    return {
        "app.name": "TestApplication",
        "db.url": "jdbc:mysql://localhost:3306/testdb",
        "user.timeout": "3600",
        "logging.level": "INFO",
        "max.connections": "100",
        "app.version": "1.0.0",
        "server.port": "8080",
        "debug.enabled": "false",
        "upload.path": "/tmp/uploads",
        "mail.smtp.host": "smtp.example.com"
    }


@pytest_asyncio.fixture(scope="module")
async def expected_dict_for_special_characters_java_properties() -> dict[str, str]:
    return {
        "app.name": "TestApplication_Æøå",
        "db.url": "jdbc:mysql://localhost:3306/testdb",
        "user.timeout": "3600",
        "logging.level": "INFO",
        "max.connections": "100",
        "app.version": "1.0.0",
        "server.port": "8080",
        "debug.enabled": "false",
        "upload.path": "/tmp/uploads_şğıöçİ",
        "location.name": "Trondheim, Norveç",
        "welcome.message": "Hoş geldiniz!",
        "description": "Dette er en test med norske tegn (æøå)",
        "company.name": "Şirket Örneği",
        "error.message": "Hata oluştu! Lütfen tekrar deneyin."
    }


@pytest_asyncio.fixture(scope="module")
async def expected_dict_for_multiline_java_properties() -> dict[str, str]:
    return {
        "app.name": "MultilineTestApp",
        "app.version": "2.1.0",
        "description": "This is a long description that spans multiple lines using backslash continuation. This "
                       "approach keeps the property on multiple lines in the file while being treated as a single "
                       "line value.",
        "email.template": "<!DOCTYPE html><html><head><title>Welcome Email</title></head><body><h1>Welcome to our "
                          "service!</h1><p>Thank you for signing up.</p></body></html>",
        "app.config": "{\"debug\": true,\"max_connections\": 100,\"timeout\": 30,\"features\": {\"dark_mode\": true,"
                      "\"notifications\": true}}",
        "error.message": "Error occurred!• Check network connection• Verify credentials• Restart application",
        "unix.path": "/var/log/app/data",
        "windows.path": "C:\\Program Files\\MyApp\\data",
        "temp.directory": "",
        "welcome.message": "Hello World",
        "special.chars": "This has = equals and : colons and # hash symbols"
    }
