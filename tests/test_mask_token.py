from main import TOKEN_RE


def test_mask_token_in_url():
    line = "POST https://api.telegram.org/bot1234567890:ABCDefGHIjklMNOpqrSTUvwxYZ-_12345/getMe"
    masked = TOKEN_RE.sub("bot<TOKEN>", line)
    assert "bot<TOKEN>" in masked
    assert "1234567890" not in masked
    assert "ABCDefGHI" not in masked


def test_mask_token_no_match():
    line = "Просто текст без токена"
    masked = TOKEN_RE.sub("bot<TOKEN>", line)
    assert masked == line


def test_mask_multiple_tokens():
    text = (
        "bot111:AAA/getMe и bot222:BBB/getUpdates "
        "и снова bot111:AAA/deleteWebhook"
    )
    masked = TOKEN_RE.sub("bot<TOKEN>", text)
    assert masked.count("bot<TOKEN>") == 3
    assert "111:AAA" not in masked
    assert "222:BBB" not in masked
