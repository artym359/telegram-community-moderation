from community_moderation import config


def test_csv_env_normalizes_usernames(monkeypatch):
    monkeypatch.setenv(
        "TEST_MODERATION_USERNAMES",
        " @Alice, bob, , @ALICE ",
    )

    assert config._csv_env("TEST_MODERATION_USERNAMES") == {"alice", "bob"}
