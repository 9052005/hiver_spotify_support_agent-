INTENTS = [
    "billing_payment",
    "refund",
    "subscription_cancel",
    "subscription_plan",
    "account_login",
    "account_security",
    "premium_not_working",
    "playback_problem",
    "app_technical_problem",
    "playlist_music_problem",
    "family_student_plan",
    "gift_code",
    "feature_request",
    "general_complaint",
    "other",
]

HIGH_RISK_INTENTS = {
    "billing_payment",
    "refund",
    "account_security",
}

AUTO_INTENTS = {
    "subscription_plan",
    "playback_problem",
    "app_technical_problem",
    "playlist_music_problem",
    "family_student_plan",
    "gift_code",
    "feature_request",
}
