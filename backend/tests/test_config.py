from paragraf.config import Settings


def test_api_keys_are_not_leaked_in_repr(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "gsk_super_secret")
    settings = Settings()
    assert "gsk_super_secret" not in repr(settings)
    assert settings.groq_api_key.get_secret_value() == "gsk_super_secret"


def test_provider_is_validated(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "not-a-provider")
    try:
        Settings()
    except ValueError:
        return
    raise AssertionError("invalid LLM_PROVIDER was accepted")
